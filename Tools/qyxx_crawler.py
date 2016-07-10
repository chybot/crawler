# -*- coding: utf-8 -*-
"""
企业信息网父类模块
"""
from __future__ import division
__author__ = 'xww'

import sys
reload(sys)
sys.setdefaultencoding("UTF-8")
sys.path.append("../")
import urlparse
import time
import socket
import os
import re
import chardet
import uuid
import json
import hashlib

from abc import abstractmethod
from json import JSONEncoder
from common import mongoutil
from common import webutil
from common import timeutil
from common import charutils
from common import fileutil
from common import exceputil
from common.recchar import RecChar
from common.functions import use_dns_cache, remove_all_space_char
import config

from requests import post
l
from common import loggingutil
from common.functions import get_logger
from requests import get
import random
import logging
from common.SpiderMonitor import SpiderMonitor
webutil.debug_mode = config.debug
# 可选队列list
queue_list_1 = ['_bug', '_static', '_manyan', '_nonstatic', '_error']
queue_list_2 = ['_bug', '_manyan', '_static', '_nonstatic', '_error']

class qyxx_crawler(object):
    """
    企业信息网抓取模块父类
    """
    use_dns_cache() # dns缓存
    urlopen_timeout = 60.0

    class ValidException(Exception):
        """
        自定义异常，用于处理联系多次验证码失败时抛出
        """
        def __init__(self, *args, **kwargs):
            Exception.__init__(self, *args, **kwargs)

    class ValidYzmException(Exception):
        """
        自定义异常，用于处理验证码打码返回错误时抛出
        """
        def __init__(self, *args, **kwargs):
            Exception.__init__(self, *args, **kwargs)

    # 设置全局的socket超时
    socket.setdefaulttimeout(urlopen_timeout)
    #企业信用信息网地域中文名
    chinese = None
    #企业信用信息网地域拼音
    pinyin = None
    #验证码打码总次数
    yzm_count = 0
    #验证码打码失败次数
    yzm_error = 0
    #验证码打码成功次数
    yzm_success = 0
    #邮件列表
    mail_list = ["lvsijun@brandbigdata.com", "hehongjing@brandbigdata.com", "wangyao@brandbigdata.com", "fumenglin@brandbigdata.com", "wudewen@brandbigdata.com", "shuaiguangying@brandbigdata.com", "hubing@brandbigdata.com", "guomao@brandbigdata.com"]
    #公司队列
    company_name_queue = None
    #无效关键字集合
    notvalid_key_set = None
    #有效关键字集合
    valid_key_set = None
    #公司名前缀过滤集合
    filter_start_key = None
    #公司名后缀过滤集合
    filter_start_end = None
    #最后一次处理的公司名
    last_company_key_file = None

    #验证码识别次数，查询一个关键字验证码输入失败制定次数后，放弃
    exit_count = 10
    #日志
    logging = None
    #分词器
    fun_analyzer = None
    #mongo数据库操作句柄
    db_qyxx=None
    #每次查询最多返回条数
    max_num_perpage=None
    manyan_pro_list=[u'sichuan']
    def __init__(self, chinese, pinyin,  fun_analyzer=None,max_num_perpage=5,ext_table_name = None):
        """
        构造器
        :param chinese:(unicode)　地域中文名　->　上海
        :param pinyin:(unicode) 地域拼音 -> shanghai
        :param fun_analyzer:  function 分词函数
        :param max_num_perpage: (int) 每次查询最多返回条数
        :return: qyxx_crawler
        """
        self.max_num_perpage=max_num_perpage
        self.pinyin = pinyin

        loggingutil.DEFAULT_CONF['filename_prefix'] = 'qyxx_%s' % pinyin
        # 是否进入调试模式
        if config.debug == 0:
            loggingutil.DEFAULT_CONF['is_queue'] = True
            loggingutil.DEFAULT_CONF['level_queue'] = loggingutil.INFO
            loggingutil.DEFAULT_CONF['level_file'] = loggingutil.ERROR
            #TODO
            #self.kafka_mail = mailutil.mail(not config.debug)
        elif config.debug == 1:
            loggingutil.DEFAULT_CONF['level_file'] = loggingutil.DEBUG
        #TODO
        #self.logging = loggingutil.get_logger('qyxx_%s' % pinyin)
        self.logging=get_logger('qyxx_%s' % pinyin,level=logging.INFO)
        # 获取种子队列对象
        self.queue = storageutil.getdb_factory('', type=config.type0, host=config.host0, port=config.port0)

        # 获取内容队列对象
        
        if ext_table_name:
            self.db = storageutil.getdb_factory(ext_table_name, type=config.type1, host=config.host1, port=config.port1)
        else:
            self.db = storageutil.getdb_factory(pinyin, type=config.type1, host=config.host1, port=config.port1,max_connections=5000)
        self.initProxySSDB()

        # 邮件报警，kafka对象
        self.proxy_num=0
        self.proxy_error=0
        self.proxy_series_error=0
        self.proxy_typess=proxy_type_configure.get(self.pinyin,'all')
        if fun_analyzer is None:
            self.fun_analyzer = charutils.analyzer
        else:
            self.fun_analyzer = fun_analyzer
        self.chinese = chinese
        self.filter_start_key = {chinese, u"中国", u"中国%s" % chinese}
        self.filter_start_end = {u"有限公司", u"公司", u"股份有限公司"}
        self.last_company_key_file = u"./%s_last_company_key_file.txt.tmp" % chinese
        self.recChar = None
        # 代理
        self.proxy = None
        # 保存搜索关键词
        self.keyword = ''
        # 爬虫监控实例
        self.monitor = SpiderMonitor(u'企业信息', seconds=300)
        if not config.debug:
            self.monitor.start()
    def initProxySSDB(self):
        """
        init ssdb queue and set to restore proxy white and black list
        :return:

        """
        set_name = self.pinyin + "_black_proxy"
        queue_name=self.pinyin + "_white_proxy"
        # use to restore proxy ip black&white list
        type="ssdb"
        ssdb_server = "web29"
        ssdb_server_port = "9091"
        self.proxy_white_list_db = storageutil.getdb_factory(queue_name, type=type, host=ssdb_server, port=ssdb_server_port)
        #####NOTE black list is a set!!!!##################################################
        self.proxy_black_list_db = storageutil.getdb_factory(set_name, type=type, host=ssdb_server, port=ssdb_server_port)


    @abstractmethod
    def crawler(self, company_key, company_name):
        """
        抽象的爬虫核心函数,由每个子类重写
        :param company_key: (unicode) 待抓取公司分词   -> 钢铁
        :param company_name: (unicode) 待抓取公司名 -> 北京市钢铁公司
        :return: (int,bool) (公司数量，公司列表中是否包含company_name) ->（5,True）
        """
        pass
    @abstractmethod
    def crawler_url(self,company_url,company_name):
        """
        抽象的通过url抓取爬虫核心函数,由每个子类重写
        :param company_url: 单个公司的url,eg:http:
        :param company_name: (unicode) 该url抓取的公司名
        :return:(int,bool) (公司数量，公司列表中是否包含company_name) ->（5,True）
        """
    #获取代理服务器代理
    def get_proxy_qyxx(self,need_check=False, is_debug=False, area=u"电信"):
        try:
            if config.debug:
                return None
            else:
                # if self.proxy_white_list_db.size() > 0:
                #     return self.proxy_white_list_db.get()
                # else:
                return get("http://spider7:9876/qyxx?area=%s&type=%s" % (self.pinyin,self.proxy_typess)).text.strip()
        except Exception as e:
            exceputil.traceinfo(e)
            return proxyutils.choice_proxy(is_debug=False,area=u"电信",host=config.proxy_host,port=config.proxy_port)
    def put_proxy_into_queue_or_set(self,type='queue'):
        try:
            if type == "queue":
                return self.proxy_white_list_db.put_data_back(self.proxy)
            else:
                return  self.proxy_black_list_db.ssdb_put_zset(self.proxy,score=int(time.time()))
        except Exception as e:
            exceputil.traceinfo(e)
    # 获取优质代理
    def init(self):
        self.proxy_num=0
        self.proxy_error=0
        self.proxy_series_error=0

    def get_useful_proxy(self, need_check=False, is_debug=False, area=u"电信"):

        if self.proxy_series_error>=2:
            self.logging.info(u'%s代理连续访问次数大于3，放入黑名单:%s'%(self.proxy,self.put_proxy_into_queue_or_set('set')))
            self.init()
            return self.get_proxy_qyxx(need_check=False, is_debug=False, area=u"电信")
        if self.pinyin in proxy_series_configure:
            # 如果为连续访问IP设置时，则当非连续错误次数除以可以永许总访问的比大于等1%时候，
            # 或者当前IP使用的总次数大于等于最大永许访问次数时候，更换代理IP
            if self.proxy_num>= proxy_series_configure[self.pinyin] or (self.proxy_error>=10 and self.proxy_error/proxy_series_configure.get(self.pinyin,1000)>=0.01):
                self.init()
                return self.get_proxy_qyxx(need_check=False, is_debug=False, area=u"电信")
            else:
                if self.proxy_num==0:
                    #初次访问代理的设置
                    self.proxy_num+=1
                    return self.get_proxy_qyxx(need_check=False, is_debug=False, area=u"电信")
                self.proxy_num+=1
                self.proxy_error+=1
                self.proxy_series_error+=1
                return self.proxy
        else:
            self.init()
            return self.get_proxy_qyxx(need_check=False, is_debug=False, area=u"电信")


    # 放回优质代理，返回队列剩余代理数量
    def put_useful_proxy(self):
        pass


    def set_black_keyword(self, company_dic):
        """
        设置关键字黑名单
        :param key: 关键字
        :return:
        """
        save_data = dict()
        now = timeutil.format('%Y-%m-%d', time.time())
        save_data['do_time'] = now
        save_data.update(company_dic)
        self.queue.select_queue(self.pinyin + '_noncompany')

        key=filter(lambda x:x in company_dic,['name','zch','xydm'])
        key= company_dic[key[0]] if key else json.dumps(company_dic)
        key= key if len(key)<100 else key[:100]
        if  self.queue.ssdb_put_zset(key):
            self.queue.save(save_data)
            self.logging.info(u'成功写入%s_nonCompany队列一条数据：%s' % (self.pinyin,key))

    def set_white_key(self, key):
        """
        设置关键字白名单
        :param key:  (unicode) 关键字 -> 钢铁
        :return: （None)
        """
        pass



    def in_black_set(self,key):
        """
        判断关键字是否在黑名单里
        :param key: (unicode) 关键字 -> 钢铁
        :return: (bool) 关键字是否在黑名单里 -> True:在 False:不在
        """
        pass


    def in_white_set(self,key):
        """
        判断关键字是否在白名单里
        :param key: (unicode) 关键字 -> 钢铁
        :return: (bool) 关键字是否在白名单里 -> True:在 False:不在
        """
        pass


    def in_set(self, key):
        """
        判断关键字是否在黑名单或白名单里
        :param key: (unicode) 关键字 -> 钢铁
        :return: (bool) 关键字是否在黑名单或白名单里 -> True:在 False:不在
        """
        pass


    def append_bottom(self, company_name):
        """
        把上次处理失败的公司名放到redis队列末尾
        :param company_name: （str) 公司名
        :return: (None)
        """
        company_name_temp = company_name.encode("UTF-8", "ignore")
        self.queue.select_queue(self.pinyin + '_error')
        self.queue.save(company_name_temp)


    def process_last_error(self):
        """
        读取last_company_key_file文件内容，并放到redis队列末尾
        :return: (None)
        """
        if os.path.isfile(self.last_company_key_file):
            tmp_key = open(self.last_company_key_file, "r").read().decode("UTF-8", "ignore").strip()
            print tmp_key
            if len(tmp_key) > 1:
                self.append_bottom(tmp_key)
                fileutil.clear(self.last_company_key_file)


    def pop_company(self):
        """
        从redis队列中获取公司名
        :return: (str) 公司名 -> 北京钢铁公司
        """
        company_name = None
        if self.pinyin in self.manyan_pro_list:
            for name in queue_list_2:
                self.queue.select_queue(self.pinyin + name)
                company_name = self.queue.get()
                if not company_name:
                    self.logging.error(u'%s 队列为空！' % (self.pinyin + name))
                    continue
                break
        else:
            p = random.random()
            if p < 0.5:
                for name in queue_list_1:
                    self.queue.select_queue(self.pinyin + name)
                    company_name = self.queue.get()
                    if not company_name:
                        self.logging.error(u'%s 队列为空！' % (self.pinyin + name))
                        continue
                    else:
                        break
            else:
                for name in queue_list_2:
                    self.queue.select_queue(self.pinyin + name)
                    company_name = self.queue.get()
                    if not company_name:
                        self.logging.error(u'%s 队列为空！' % (self.pinyin + name))
                        continue
                    else:
                        break
        if company_name is None:
            time.sleep(10)
            raise Exception(u"公司队列没有内容返回，更换队列")
        company_name = company_name.strip()
        return company_name


    def process(self):
        """
        主程序
        1、获取上一次退出前最后下载失败的公司名并放到队列末尾
        2、从队列中读取公司名，写到本地文件中
        3、调用抓取调度模块，对公司名进行分词处理
        4、若抓取失败，公司名会放到队列末尾并清理本地文件
        5. 回到第2步
        :return: (None)
        """
        self.logging.info(u"开始%s站内容抓取" % self.chinese)
        #获取上一次退出前最后下载失败的公司名并放到队列末尾
        self.process_last_error()
        #失败次数，连续n个公司失败后会休眠1小时并发邮件
        fail_count = 10
        while True:
            try:
                #从队列中读取公司名进行处理
                company_name = self.pop_company().decode("UTF-8", "ignore")
                if len(company_name) < 1 or len(company_name) > 2000:
                    raise Exception(u"公司长度不合理")
                self.keyword = company_name
            except Exception as e:
                self.logging.error(u"队列取值错误.error:%s" % exceputil.traceinfo(e))
                time.sleep(1)
                continue
            #把redis队列中取到的内容写到本地文件中
            fileutil.write(self.last_company_key_file, company_name.encode("UTF-8", "ignore"))
            #当前时间
            #this_time = time.strftime(u"%Y-%m-%d %H:%M:%S",time.localtime())
            try:
                #若当前的代理为自建代理，则更换代理，非自建代理则继续使用
                self.logging.info(u"代理《%s》使用次数：%s"%(self.proxy,self.proxy_num))
                try:
                    if self.proxy:
                        if self.pinyin not in proxy_series_configure :
                            if str(self.proxy.split(":")[-1]) in  ["42271","42272"]:
                                self.proxy = self.get_useful_proxy()
                                self.logging.error(u"使用优化代理：%s开始抓取,公司名：%s" % (self.proxy, company_name))
                            elif self.proxy_num>=proxy_none_series_configure.get(self.pinyin,50):
                                self.proxy = self.get_useful_proxy()
                                self.logging.error(u"使用优化代理：%s开始抓取,公司名：%s" % (self.proxy, company_name))
                            else:
                                self.proxy_series_error=0
                                self.proxy_num+=1
                        elif self.proxy_num>=proxy_series_configure.get(self.pinyin,2000):
                            self.proxy = self.get_useful_proxy()
                        else:
                            self.proxy_series_error=0
                            self.proxy_num+=1
                    else:
                        self.proxy = self.get_useful_proxy()
                except Exception as e:
                    self.logging.error(e)
                #调用抓取调度模块，对公司名进行分词处理
                ret = self.crawler_scheduler(company_name)

                fileutil.clear(self.last_company_key_file)
                #成功，重置为初始值
                fail_count = 10
            except self.ValidException as e1:
                #连续失败计数
                fail_count -= 1
                #失败的公司名放到redis队列末尾
                self.append_bottom(company_name)
                #清理存有上次处理公司名的文件
                fileutil.clear(self.last_company_key_file)
                #如果连续失败10个公司验证码每个都失败10次则休眠1小时
                if (fail_count < 0):
                    #TODO
                    #if hasattr(self,"kafka_mail"):
                    #    self.kafka_mail.send_mail(self.mail_list, u'%s站验证码识别异常报告' % self.chinese, u'公司爬取失败数超过10个')
                    self.logging.error(u"公司爬取失败数超过10个")
                    time.sleep(60 * 30) # 这里休眠时间缩短，机器打码不需要休眠太久
                    #睡醒了，重置为初始值
                    fail_count = 10
                continue
            except Exception as e:
                self.logging.error(u"公司抓取异常。公司名:%s error:%s" % (company_name, exceputil.traceinfo(e)))
                #失败公司放到redis队列末尾
                self.append_bottom(company_name)
                #清理存有上次处理公司名的文件
                fileutil.clear(self.last_company_key_file)

        self.logging.info(u"%s站内容抓取完成" % self.chinese)

    def record_success(self,yzm,img_path,count=10000):
        """
        打码成功后记录，文件名使用yzm
        :param yzm:  验证码
        :param count: 保存验证码文件个数，默认10000个
        :return: (None)
        """
        try:
            dir_path=os.path.abspath('../')
            yzm_dir=os.path.join(dir_path,"yzm_success",self.pinyin)
            if not fileutil.isdir(yzm_dir):
                #建立目录
                fileutil.mkdirs(yzm_dir)
            pics = sum([len(files) for root,dirs,files in os.walk(yzm_dir)])
            self.logging.info(u"已存放%d张验证码图片"%(pics-1))
            if pics > count:
                self.logging.warn(u"已存放超%d张验证码图片"%count)
                return
            # 唯一的验证码图片文件名
            img = "%s.jpg"%str(uuid.uuid1())
            # 记录图片与验证码对应关系
            text_file_name=os.path.join(yzm_dir,"ans.txt")
            file=open(text_file_name,"a")
            file.write(img + ' ' + yzm + '\n')
            file.close()
            # 保存验证码图片
            img_name=os.path.join(yzm_dir,img)
            fileutil.copyfile(img_path,img_name)
        except Exception as e:
            self.logging.error(u"记录发生异常.错误信息:%s" % exceputil.traceinfo(e))


    def back_money(self,recChar,code_id,yzm,img_path):
        """
        打码失败后请求退钱，并且验证码内容存储到文本文件和图片一起存储到self.pinyin目录，文件名使用code_id。
        退钱正常的图片和验证码文本文件前缀为1,退钱失败前缀为0
        :param recChar:
        :param code_id:  打码系统id
        :param yzm:  验证码
        :param img_path:  图像地址
        :return: (None)
        """
        if code_id=="0":
            self.logging.warning(u"手工打码，无需退钱")
            return

        if recChar==None:
            self.logging.err(u"退钱发生异常。recChar==None")
            return
        #失败次数计数器加1
        self.yzm_error+=1
        today=timeutil.format("%Y-%m-%d",time.time())
        dir_path=os.path.abspath('.')
        yzm_dir=os.path.join(dir_path,self.pinyin,today)
        if not fileutil.isdir(yzm_dir):
            #建立目录
            fileutil.mkdirs(yzm_dir)
        try:
            #使用coide_id号退钱
            recChar.reportErrorID(code_id)
            #退钱正常文件名前缀为1
            img_name=os.path.join(yzm_dir,str(1),"%s.png"%code_id)
            text_file_name=os.path.join(yzm_dir,str(1),"%s.txt"%code_id)
            #把验证码文字写入到文本文件中，放到退钱目录
            fileutil.write(text_file_name,yzm.encode("UTF-8","ignore"))
            #把图片文件复制到退钱的目录
            fileutil.copyfile(img_path,img_name)
            self.logging.error(u"验证码没识别出来,退钱正常")
        except Exception as ee:
            #退钱失败文件名前缀为0
            img_name="%s\\%d_%s.png" %(yzm_dir,0,code_id)
            text_file_name="%s\\%d_%s.txt"%(yzm_dir,0,code_id)
            #把验证码文字写入到文本文件中，放到退钱目录
            fileutil.write(text_file_name,yzm.encode("UTF-8","ignore"))
            #把图片文件复制到退钱的目录
            fileutil.copyfile(img_path,img_name)
            self.logging.error(u"验证码没识别出来,errorType=5 。退钱发生异常.error:%s" % exceputil.traceinfo(ee))

    #验证码失败率，超过次失败率会发邮件并休眠1小时
    fail_per=50


    def valid_yzm(self):
        """
        处理验证码失败率过高异常
        :return: (None)
        """
        if  self.yzm_count>=100 and int(1.0*self.yzm_error/self.yzm_count*100)>self.fail_per:
            self.logging.error(u"验证码失败率高于%d"%self.fail_per + "%")
            content=u"验证码失败率高于%d"%(self.fail_per)
            content+="%"
            #发送验证码失败率过高的邮件
            #TODO
            #title=u"%s站验证码识别异常报告"%(self.chinese)
            #if hasattr(self,"kafka_mail"):
            #    self.kafka_mail.send_mail(self.mail_list, title, content)
            time.sleep(60*5)
            self.yzm_count=0
            self.yzm_error=0

    def bbd_yzm(self,img_src):
        try:
            yzm_html=post('http://spider7:5678/form',files={'files':img_src},data={'type':self.pinyin})
            yzm_html.encoding='utf-8'
            yzm_html=yzm_html.content
            assert len (yzm_html.split())==2
            yzm,img_name=yzm_html.split()
            print yzm,img_name
            return yzm, img_name, "no erro",img_name
        except Exception as e:
            self.logging.error(e)
            raise Exception(u"获取验证码错误：%s"%e)
    def parse_yzm(self,img_url,img_src,typecode,yzm_max_len=4,type=None):
        """
        对验证码进行人工打码验证
        :param img_url:  验证码图片地址
        :param img_src:  验证码图片内容
        :param typecode:
        :param yzm_max_len:  验证码最大长度
        :return: （unicode,unicode,bool,RecChar,unicode）(验证码内容, 打码系统id, 是否正常,打码对象,验证码图片地址)
        """
        try:
            dir_path=os.path.abspath('.')
            urlpret = urlparse.urlparse(img_url)
            img_path = os.path.join(dir_path,"%s_%s.png"%(urlpret.hostname,self.pinyin))
            print "img_path:", img_path, "type:", type
            fileutil.write(img_path,img_src)
            self.logging.info(u"请求验证码")
            #发送给打码公司打码 或 机器打码
            if type!=None and len(type)>0:
                if self.recChar == None:
                    self.recChar=RecChar(type)
                ret=self.recChar.rec(img_path)
                if ret!=None and len(ret)>0:
                    yzm= str(ret[0])
                    print "yzm:",yzm
                    if chardet.detect(yzm)['encoding'] == "utf-8":
                        yzm = yzm.decode("utf-8")
                    if yzm!=None and yzm.lower()=="none":
                        yzm=None
                    return yzm,"0",False,self.recChar,img_path
                else:
                    raise Exception(u"机器打码返回值为None或长度为0.")

            else:
                if self.recChar == None:
                    self.recChar = RecChar()
                self.yzm_count+=1
                (yzm, code_id, is_report_error,img_path)=self.bbd_yzm(img_src)
                #(yzm, code_id, is_report_error) = self.recChar.rec(img_path, typecode=typecode);
                # 手工打码，用于测试
                # recChar=""
                # yzm=raw_input()
                # yzm= yzm.decode("UTF-8",'ignore')
                # code_id="asdfasdfasdf"
                # is_report_error=False
                # print "yzm:",yzm
                self.logging.info(u"验证码返回结果,yzm:%s,code_id:%s,is_report_error:%s"%(yzm, str(code_id), str(is_report_error)))
                #退钱需要用coid_id,如果coid为空则证明没有打码失败没有收费，所以不需要退钱
                # if len(str(code_id))<4:
                #     self.logging.error(u"验证码识别错误。errorType=1,coid_id为空")
                #     self.yzm_error+=1
                #     raise self.ValidYzmException(u"验证码识别错误")
                # #验证码内容为空
                # if len(yzm)<1 or len(yzm)>yzm_max_len:
                #     self.logging.error(u"验证码识别错误。errorType=2,验证码长度不在正确范围")
                #     if len(code_id)>=4:
                #         self.back_money(self.recChar,code_id,yzm,img_path)
                #     else:
                #         self.yzm_error+=1
                #     time.sleep(0.1)
                #     raise self.ValidYzmException(u"验证码识别错误")

                return (yzm, code_id, is_report_error,self.recChar,img_path)




        except self.ValidYzmException as e1:
            self.logging.error(u"验证码处理异常,error:%s"%exceputil.traceinfo(e1))
            raise
        except Exception as  yzmerror:
            self.logging.error(u"验证码处理异常,errorType=4,error:%s"%exceputil.traceinfo(yzmerror))
            # self.back_money(self.recChar,code_id,yzm,img_path)
            raise

    def parse_people(self,ss):
        """
        去掉所有的不可见字符，包括空格，换行等等
        :param ss:
        :return:
        """
        return re.sub(r'[\x00-\x20]+',' ',ss).strip()


    def is_num(self, s):
        try:
            int(s)
            return True
        except:
            return False


    def save(self,company_name,save_data1):
        """
        通过公司名和日期生成唯一id，并把公司内容存入mongodb数据库。
        :param company_name:  (unicode) 公司名
        :param save_data:  (dict)  公司信息
        :return:  (bool) 是否成功存储 -> true / false
        """
        #清理数据
        save_data=dict()
        for key in save_data1:
            value=save_data1[key]
            new_key=remove_all_space_char(key)
            if len(new_key)>0:
                save_data[new_key]=value
        company_name = remove_all_space_char(company_name)
        fields=[u"成员出资总额",u'名称',u'注册号',u'登记机关',u'类型',u'经营状态',u'登记状态',u'营业场所',u'住所',u'营业期限自',u'营业期限至',u'成立日期',u'核准日期',u'吊销日期',u'注册资本',u"经营期限至",u"经营期限自"]
        people=[u"名称",u"经营者",u"法定代表",u"法定代表人",u"经营者姓名",u'负责人',u"法人",u"首席代表",u"投资人",u"执行事务合伙人",u"执行事务合伙人（委派代表）",u"股东"]

        for p in people:
            if save_data.has_key(p):
                value=self.parse_people(save_data[p])
                save_data[p]=value
                if len(value)<1:
                    self.logging.error(u"字段内容长度为0,公司名:%s,字段名:%s"%(company_name,p))
        for field in fields:
            if save_data.has_key(field):
                value=remove_all_space_char(save_data[field])
                save_data[field]=value
                if len(value)<1:
                    self.logging.error(u"字段内容长度为0,公司名:%s,字段名:%s"%(company_name,field))

        if len(save_data)<15:
            raise Exception(u"字段缺失:%s"%company_name)
        self.logging.info(u"存储数据,公司名:%s"%company_name)
        now=timeutil.format("%Y-%m-%d",time.time())
        id=mongoutil.get_id_key(company_name,now)
        # prefix="^"+company_name
        # ret=self.db_qyxx.table.find({"_id":{'$regex':prefix}}).sort("uptime",-1)
        #处理version,如果未指定则默认为1
        if not save_data.has_key("version"):
            save_data["version"]=3
        #处理没有type，如果未指定则默认为chinese
        if not save_data.has_key("type"):
            save_data["type"]=self.chinese

        save_data["company_name"] = company_name  #设置公司名字
        save_data["do_time"]=now
        save_data["uptime"]=time.time()
        save_data["down_type"]=0
        #处理键值为None
        if save_data.has_key(None):
            del save_data[None]

        #处理股东信息
        gdxx_list=list()
        if  save_data.has_key("gdxx"):
            gdxx_list=save_data["gdxx"]
            if not isinstance(gdxx_list,list):
                gdxx_list=list()
        save_data["gdxx"]=JSONEncoder().encode(gdxx_list)

        #处理备案信息
        baxx_list=list()
        if save_data.has_key("baxx"):
            baxx_list=save_data["baxx"]
            if not  isinstance(baxx_list,list):
                baxx_list=list()
        save_data["baxx"]=JSONEncoder().encode(baxx_list)

        #处理变更信息
        bgxx_list=list()
        if save_data.has_key("bgxx"):
            bgxx_list=save_data["bgxx"]
            if not  isinstance(bgxx_list,list):
                bgxx_list=list()
        save_data["bgxx"]=JSONEncoder().encode(bgxx_list)

        #处理分支机构
        fzjg_list=list()
        if save_data.has_key("fzjg"):
            fzjg_list=save_data["fzjg"]
            if not  isinstance(fzjg_list,list):
                fzjg_list=list()
        save_data["fzjg"]=JSONEncoder().encode(fzjg_list)

        #处理行政处罚
        xzcf_list=list()
        if  save_data.has_key("xzcf") and  isinstance(save_data["xzcf"],list):
            xzcf_list=save_data["xzcf"]
        save_data["xzcf"]=JSONEncoder().encode(xzcf_list)

        # 注册号策略
        save_data['keyword'] = self.keyword
        key_list =save_data.keys()
        res_list = filter(lambda x: u"注册号" in x , key_list)

        if not res_list:
            self.logging.error(u'没有注册号！')
            if self.is_num(self.keyword) and len(self.keyword) == 15:
                self.logging.info(u'写入注册号：%s' % self.keyword)
                save_data[u'注册号'] = self.keyword

        save_data['_id'] = id
        save_data['has_company'] = 1
        self.db.save(save_data)

        self.logging.info(u'成功写入%s一条数据：%s' % (config.type1, id))
        self.proxy_series_error=0
        if self.proxy and self.proxy.split(":")[-1]not in ['42271','42272']:
            self.logging.info(u"优质非自建代理插入队列尾部，当前非自建代理列表长度为：%s"% self.put_proxy_into_queue_or_set(type='queue'))
        if not config.debug:
            self.monitor.add()
        return True

    def notvalid_keyword(self,word):
        """
        判断关键字
        :param word:  关键字
        :return: (bool) 是否是无效
        """
        return False


    def get_gdxx_detail(self,company_url,detail_url):
        """
        根据公司详情url和公司股东详情相对url计算出绝对的url地址，访问并返回内容
        :param company_url: (str) 公司详情url
        :param detail_url:  (str) 公司股东详情相对url
        :return: (str) 公司股东详情详情html内容
        """
        detail_ab_url=urlparse.urljoin(company_url,detail_url)
        urlpret = urlparse.urlparse(detail_ab_url)
        head={
            "Referer":company_url,
            "Host":urlpret.netloc
        }
        return  webutil.request(detail_ab_url,headers=head,encoding=webutil.detect_encoding)



    def crawler_scheduler(self, company_name):
        """
         抓取调度器。
         1.公司名进行分词，然后用分词后的关键字去查询。
         2.如果有返回内容并且包含指定公司则停止抓取，返回True。。
         3.如果有返回内容达到max_num_perpage条但不包含指定公司则继续抓取，并设置关键字白名单和公司白名单。
        4.如果没有返回内容则结束抓取。
        :param company_name:  （str）  公司名 -> 北京钢铁公司
        :return: True/unicode  -> True                  :抓取到内容并且包含指定公司
                                 "没有指定公司"          :抓取到数据，没有指定公司
                                 "没有查询到企业信息"    :没有抓取到任何内容
        """
        has_data = False
        try:
            self.logging.info(u"分词:%s"%company_name)
            company_dic = {}
            is_dic = False
            try:
                #转换抓取的种子，目前种子可能是一个字典：例如：
                pattern_str = r"^\d{%d}" % len(company_name)
                if re.match(pattern_str, company_name):
                    company_dic[u"zch"] = company_name
                else:
                    if company_name.startswith('{') and company_name.endswith('}'):
                        company_name=json.loads(company_name)
                        company_dic.update(company_name)
                    else:
                        if not isinstance(company_name,unicode):
                            encoding= chardet.detect(company_name).get("encoding")
                            if encoding:
                                if encoding=='ascii':
                                    self.logging.error(u"关键字编码错误")
                                    return 0,False
                                else:
                                    company_name=company_name.decode(encoding,'ignore')
                        company_dic['name']=company_name
                    if 'keyword' in company_dic and ('zch' in company_dic.get('keyword') or 'name' in company_dic.get('keyword')):
                        company_dic.update(company_dic.get('keyword'))
                    is_dic = True
            except Exception as e:
                self.logging.error(u"种子队列转换出错：%s" % e)
                company_dic[u"name"] = company_name
                pass
            #抓取优先级为：注册号--》公司名----》信用代码
            company_count = 0
            inner_company = False
            is_Exception = []
            #使用注册号抓取
            if company_dic.get(u"zch"):
                try:
                    temp_key = company_dic.get(u"zch")
                    self.logging.info(u"抓取（1）:%s" % temp_key)
                    company_count, inner_company = self.crawler(temp_key, temp_key)
                except Exception as e:
                    is_Exception.append(e)
            #使用公司url抓取
            if company_count <1 and company_dic.get(u"name") and company_dic.get(u"url"):
                try:
                    company_name=company_dic.get(u"name")
                    self.logging.info(u"抓取（2）:%s" % company_name)
                    company_url=company_dic.get(u"url")
                    company_count,inner_company=self.crawler_url(company_url,company_name)
                except Exception as e:
                    is_Exception.append(e)
            #使用url抓取，能抓到公司，但是没有抓到该公司
            if company_count>=1 and inner_company==False and company_dic.get(u"name"):
                try:
                    temp_key = company_dic.get(u"name")
                    self.logging.info(u"抓取（3）:%s" % temp_key)
                    company_count, inner_company = self.crawler(temp_key, temp_key)
                except Exception as e:
                    is_Exception.append(e)
            #若使用注册号没有抓取到，则使用公司名抓取
            if company_count < 1 and company_dic.has_key(u"name") and company_dic.get(u"name", u""):
                try:
                    temp_key = company_dic.get(u"name", u"")
                    self.logging.info(u"抓取（4）:%s" % temp_key)
                    company_count, inner_company = self.crawler(temp_key, temp_key)
                except Exception as e:
                    is_Exception.append(e)
            #若使用公司名没有抓取到，则使用抓取信用代码抓取
            if company_count < 1 and company_dic.has_key(u"xydm") and company_dic.get(u"xydm", u""):
                try:
                    temp_key = company_dic.get(u"xydm", u"")
                    self.logging.info(u"抓取（5）:%s" % temp_key)
                    company_count, inner_company = self.crawler(temp_key, temp_key)
                except Exception as e:
                    is_Exception.append(e)

            #判断书否为元祖队列，且没有抓取的，记录数据，用于排查
            if company_count < 1 and is_dic:
                try:
                    if is_Exception:
                        company_dic[u"exception"] = u"no"
                    else:
                        company_dic[u"exception"] = u"yes"
                    self.queue.select_queue(self.pinyin + '_noncompany_dic')
                    self.queue.save(company_dic)
                except:
                    self.logging.error(u"保存为抓取的元祖队列失败:%s" % company_name)

            #程序抛错
            if is_Exception:
                raise json.dumps(is_Exception)
                #raise Exception('\n'.join(map(lambda x:x.decode(chardet.detect(x).get("encoding","UTF-8"),'ignore') if not isinstance(x,object) else str(x),is_Exception)))

            if company_count < 1:
                #没有抓取内容'''
                self.set_black_keyword(company_dic)
                # break
            else:
                #有抓取内容'''
                self.set_white_key(company_name)
                if inner_company == True:
                    return True
                else:
                    has_data = True
                    # if company_count < self.max_num_perpage:
                    #     break
        except self.ValidException as e1:
            self.logging.error(u"验证码异常,关键字:%s,错误信息:%s" % (company_name, exceputil.traceinfo(e1)))
            raise
        except Exception as e:
            self.logging.error(u"关键字:%s,错误信息:%s" % (company_name, exceputil.traceinfo(e)))
            raise


        if has_data:
            return u"没有指定公司"
        else:
            return u"没有查询到企业信息"


    def parse_baseinfo(self,tree,xpath,index=0):
        """

        :param tree: 目录数
        :param xpath: （str） table标签的xpath表达式
        :return: (dict) 数据内容
        """
        result=dict()

        #找到存在的table标签
        table=tree.xpath(xpath)

        #找不到table
        if table==None or len(table)<1:
            raise Exception(u"找不到table标签")

        #处理tbody
        tbody=table[index].xpath("./tbody")
        if tbody!=None and len(tbody)>0:
            trs=tbody[0].xpath("./tr")
        else:
            trs=table[index].xpath("./tr")

        if trs==None or  len(trs)==0:
            raise Exception(u"找不到tr")


        for tr in trs:
            tds=tr.xpath("./td")
            ths=tr.xpath("./th")

            if  len(tds)+len(ths)<2:
                continue
            elif len(ths)>0 and len(tds)>0:
                i=0
                for th in ths:
                    if len(tds)<=i:
                        break
                    td=tds[i]
                    if th.text!=None and  len(th.text)>0:
                        th_text=th.text.strip().replace(":","").replace(u"：","")
                        try:
                            td_text=td.text.strip().replace(":","").replace(u"：","")
                        except:
                            td_text = ''
                        if len(th_text)>0:
                            result[th_text] = td_text
                    i+=1

            elif len(ths)==0 and len(tds)>2:
                for i in range(len(tds)/2):
                    if tds[i*2].text!=None and len(tds[i*2].text)>0:
                        key_text=tds[i*2].text.strip().replace(":","").replace(u"：","")
                        try:
                            value_text=tds[i*2+1].text.strip().replace(":","").replace(u"：","")
                        except:
                            value_text = ''
                        if len(key_text)>0:
                            result[key_text] = value_text
            else:
                print len(ths),len(tds)
                raise Exception(u"格式不匹配")

        if len(result)>0:
            return result
        else:
            raise Exception(u"没有数据")


    # 提取基本信息
    def jbxx_xpath(self, jbxx_tree, path):
        dict_ = {}
        try:
            jbxxs = jbxx_tree.xpath(path)[0].xpath('.//tr')
        except:
            self.logging.error(u'xpath基本信息异常，网站结构可能发生改变！')
            return dict_
        try:
            jbxx_str = jbxxs[0].xpath('.//th/text()')[0].strip()
            if jbxx_str != u'基本信息':
                self.logging.error(u'此表格不是基本信息表格！')
                return dict_
        except:
            self.logging.error(u'xpath基本信息异常，网站结构可能发生改变！')
            return dict_
        try:
            for tr in jbxxs[1:]:
                f = lambda x: ''.join(x.xpath('./text()')).strip()
                headline = map(f, tr.xpath(".//th"))
                values = map(f, tr.xpath(".//td"))
                dict_.update(dict(zip(headline, values)))
        except:
            self.logging.error(u'xpath基本信息异常')
            return {}
        return dict_

    def get_md5(self, dic_):
        """获取md5值"""
        try:
            md5 = hashlib.md5()
            md5.update(json.dumps(dic_))
            return md5.hexdigest()
        except Exception as e:
            return None

    def get_request_html_inof(self, req_url, rsp_body, req_method=u"get", encoding=u"UTF-8", req_params={}, req_header={}):
        """保存网页原文信息"""
        if req_method == post:
            req_method = "post"
        elif req_method == get:
            req_method = "get"
        item = dict()
        item[u"req_method"] = req_method
        item[u"req_url"] = req_url
        item[u"req_params"] = req_params
        item[u"req_header"] = req_header
        item[u"rsp_body"] = rsp_body
        item[u"encoding"] = encoding
        item[u"md5"] = self.get_md5(item)
        return item
