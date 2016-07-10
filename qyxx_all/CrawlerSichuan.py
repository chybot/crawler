# -*- coding: utf-8 -*-
#Created by wuyong on 2016/6

import sys
import time
import chardet
import random
import re
import PyV8
from CrawlerBase import CrawlerBase
from ModuleManager import Module,Event,Iterator,Sleep,ModuleInput,InputType, Bypass,OutputParameterShowUpType
# from ModuleManager import Module,Event,Iterator,Sleep,Bypass
from util.crawler_util import CrawlerRunMode, OutputType, EventType
from CommonLib.WebContent import WebAccessType, SeedAccessType
from CommonLib.md5util import getMd5WithString
from CommonLib import dataretrieve
reload(sys)

#TODO:行政处罚 和 年报 除 修改记录 股东出资信息 股权变更信息外的年报其它信息占时没看到有翻页信息
class CrawlerSichuan(CrawlerBase):
    def __init__(self, pinyin, callbackFromOuterControl):
        config_dict = dict()
        config_dict[CrawlerRunMode.COMPANY_KEY] = [self.initConfigValidateCode, self.checkCompanyName, self.initConfigSearchList,self.saveYzmSrc ,self.initConfigCompanyInfo]#, self.get_search_list]#, self.initConfigValidateCode, self.initConfigSearchList, self.initConfigCompanyInfo]
        check_dict = dict()
        check_dict['html_check_dict'] = {'过于频繁': WebAccessType.TOO_OFTEN, '非正常访问': WebAccessType.ACCESS_VIOLATION, '当前操作出现错误,请与管理员联系':WebAccessType.NO_CONTENT, '未经授权的访问':WebAccessType.NO_CONTENT, '数据查询中':WebAccessType.NO_CONTENT}
        CrawlerBase.__init__(self, pinyin, config_dict, check_dict, callbackFromOuterControl)
        # 关闭股东信息的解析
        self.setNonCompanyConfig({'您搜索的条件无查询结果'})
        self.parse_gdxx_on = False

    #下载识别保存验证码
    def initConfigValidateCode(self):
        module = Module(self.visitValidateCode, u'获取验证码图片')
        module.module_id = "check_validatecode"
        module.appendUrl("http://gsxt.scaic.gov.cn/ztxy.do?method=createYzm&dt=" + str(int(time.time())) + "&random=" + str(int(time.time())))
        module.appendHeaders(lambda ua:{
            "Host": "gsxt.scaic.gov.cn",
            "User-Agent": ua,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.8",
            "Accept-Encoding": "gzip, deflate, sdch",
            "Connection": "keep-alive",
            'Cache-Control':'max-age=0',
            'Upgrade-Insecure-Requests':1
        })
        #对验证码进行简单的断言
        def assertYzm(yzm=None):
            print 'Yzm  , ', yzm
            if isinstance(yzm, int):
               return True
            return True if yzm else False
        module.addEvent(Event(EventType.ASSERT_FAILED, retry_times=100, assert_function=assertYzm, redo_module="check_validatecode"))
        module.addEvent(Event(EventType.EXCEPTION_OCCURED, retry_times=100))
        module.addSleep(Sleep(2))
        self.module_manager.appendSubModule(module, True)


    #验证公司名字，response 一个 1,标示验证成功， 0验证错误
    def checkCompanyName(self):
        module = Module(self.getWebHtml, u'验证公司名称')
        module.appendUrl("http://gsxt.scaic.gov.cn/keyword.do?method=keywordFilter&random=" + str(int(time.time())))
        module.appendHeaders(lambda ua:{
            "User-Agent": ua,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3",
            "Accept-Encoding": "gzip, deflate",
            "Host": "gsxt.scaic.gov.cn",
            "Origin": "http://gsxt.scaic.gov.cn",
            "Referer": "http://gsxt.scaic.gov.cn/ztxy.do?method=index",
            "Connection": "keep-alive"
        })
        module.appendPostData(lambda company_key:{'qymc':company_key})
        module.appendWebMethod('post')
        def assertRecode(html):
            if self.report.access_type == SeedAccessType.NON_COMPANY:
                self.report.access_type = SeedAccessType.ERROR
            return True if html and html.strip() == '1' else False
        module.addEvent(Event(EventType.ASSERT_FAILED, retry_times=100, assert_function=assertRecode, redo_module="check_validatecode"))
        module.addEvent(Event(EventType.EXCEPTION_OCCURED, retry_times=100))
        module.addSleep(Sleep(3))
        self.module_manager.appendSubModule(module, True)

    #TODO: 之前没看到搜索列表翻页，待新增
    #获取搜索列表页面
    def initConfigSearchList(self):
        module = Module(self.visitSearchList, u"搜索列表")
        module.module_id = "get_search_list"
        module.appendUrl("http://gsxt.scaic.gov.cn/ztxy.do?method=list&djjg=&random=" + str(int(time.time()) * 1000))
        module.appendWebMethod("post")
        module.appendHeaders(lambda ua:{
            "User-Agent": ua,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3",
            "Accept-Encoding": "gzip, deflate",
            "Host": "gsxt.scaic.gov.cn",
            "Origin": "http://gsxt.scaic.gov.cn",
            "Referer": "http://gsxt.scaic.gov.cn/ztxy.do?method=index",
            "Connection": "keep-alive"
        })
        def getPostData(yzm, company_key):
            if isinstance(company_key, unicode):
                company_key = company_key.encode('gb2312')
            else:
                charcode = chardet.detect(company_key).get('encoding')
                if charcode:
                    company_key = company_key.decode(charcode).encode('gb2312')
            rs_dict =  {'currentPageNo': '1', 'yzm': yzm, 'maent.entname': company_key, "pName":u'请输入营业执照注册号或统一社会信用代码'.encode('gb2312')}
            return rs_dict
        module.appendPostData(getPostData)
        module.appendOutput(name="yzm_flag" ,type=OutputType.FUNCTION, function=self.getYzmFlag, show_up=OutputParameterShowUpType.OPTIONAL)
        def assertYzmFlag(yzm_flag=None):
            return True if yzm_flag == 'yes' else False
        module.addEvent(Event(EventType.ASSERT_FAILED, retry_times=100, assert_function=assertYzmFlag, redo_module='check_validatecode'))
        def assertNoCompany(yzm_flag=None):
            return False if  yzm_flag=='yes' and self.report.access_type == SeedAccessType.NON_COMPANY else True
        module.addEvent(Event(EventType.ASSERT_FAILED, retry_times=6 ,assert_function=assertNoCompany, redo_module="check_validatecode"))  #获取公司搜索列表(公司名和onclick事件参数)
        module.appendOutput("search_list_xpath", './/ul/li[@class="font16"]/a', OutputType.LIST)#,show_up=OutputParameterShowUpType.OPTIONAL)
        module.appendOutput(name="tag_alist", type=OutputType.FUNCTION, function=self.getSearchList, show_up=OutputParameterShowUpType.OPTIONAL)
        module.addEvent(Event(EventType.OUTPUT_NOT_SATISFIED, retry_times=100, redo_module="check_validatecode"))
        module.addEvent(Event(EventType.EXCEPTION_OCCURED, retry_times=100, redo_module='check_validatecode'))
        module.addSleep(Sleep(3))
        self.module_manager.appendSubModule(module, True)

    def saveYzmSrc(self):
        module = Module(None, u"保存验证码")
        module.appendExtraFunction(self.yzmSave)
        self.module_manager.appendSubModule(module, True)

    #遍历每家公司
    def initConfigCompanyInfo(self):
        iterator = Iterator("tag_alist", "tag_a")
        module = Module(None, u"获取公司信息", iterator)
        self.module_manager.appendSubModule(module, True)
        self.initConfigCompanyInfoPre(module)
        self.initConfigBaseInfo(module)
        self.initArchiveInfo(module)
        self.initPenaltyInfo(module)
        self.initShareHolderDetail(module)
        self.initAnnualReportPre(module)
        self.initAnnualReport(module)
        self.initResultCollect(module)

    #获取公司信息前的预处理,提取参数
    def initConfigCompanyInfoPre(self, module_super):
        module = Module(None, u"抓取公司前的预处理")
        module.module_id = "fetch_company_info"
        def setComParms(tag_a):
            query_ = {'company_name':tag_a[0], 'entbigtype': tag_a[1], 'pripid':tag_a[2]}
            return query_
        module.appendOutput(type=OutputType.FUNCTION, function=setComParms, show_up=OutputParameterShowUpType.OPTIONAL)
        module.addEvent(Event(EventType.EXCEPTION_OCCURED, retry_times=100))
        module_super.appendSubModule(module, True)

    #访问基本信息页面(包含基本信息，股东信息，变更信息)
    def  initConfigBaseInfo(self, module_super):
        module = Module(self.visitJbxx, u"基本信息")
        module.appendPostData(lambda pripid, entbigtype: {'djjg':'', 'maent.entbigtype':entbigtype, 'maent.pripid':pripid, 'method':'qyInfo', 'random':str(int(time.time()*1000))})
        module.appendWebMethod("post")
        module.appendUrl("http://gsxt.scaic.gov.cn/ztxy.do")
        module.appendHeaders(lambda ua :{"User-Agent": ua,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3",
            "Accept-Encoding": "gzip, deflate",
            "Host": "gsxt.scaic.gov.cn",
            "Origin": "http://gsxt.scaic.gov.cn",
            "Referer": "http://gsxt.scaic.gov.cn/ztxy.do?method=index",
            "Connection": "keep-alive"})
        module.appendOutput("company_zch_list", '//table[1]/tr[2]/td[1]/text()', OutputType.LIST)
        module.addEvent(Event(EventType.OUTPUT_NOT_SATISFIED, retry_times=5))
        def setCompanyZch(company_zch_list=None):
            self.value_dict['company_zch'] = company_zch_list[0] if company_zch_list else None
        module.appendOutput(type=OutputType.FUNCTION, function=setCompanyZch)
        #对公司名字和注册号码断言
        def assertNameZch(company_name=None, company_zch=None):
            if company_name and company_zch and (0<len(company_name)<100) and (0<len(company_zch)<100):
                #self.report.access_type = SeedAccessType.OK
                return True
            return False
        module.addEvent(Event(EventType.ASSERT_FAILED, retry_times=5, assert_function=assertNameZch))

        #从基本信息页面中提取股东详情的参数，组成访问股东详情的post参数
        def getXhPripid(html):
            return  re.findall(r'\s+onclick="showRyxx\(\'(.+?)\'\,\'(.+?)\'\)"', html, re.S)
        module.appendOutput(name='xh_pripid', type=OutputType.FUNCTION, function=getXhPripid, show_up=OutputParameterShowUpType.OPTIONAL)
        module.addEvent(Event(EventType.EXCEPTION_OCCURED, retry_times=5))
        module.addSleep(Sleep(2))
        module_super.appendSubModule(module, True)

    #获取股东详情
    def initShareHolderDetail(self, module_super):
        iterator = Iterator("xh_pripid", "xh_prid")
        module = Module(None, "进入股东详情", iterator)
        module.module_id = "fetch_gdxq_info"
        module_super.appendSubModule(module, True)
        sub_module = Module(self.visitGdxq, u"获取股东翻页信息")
        sub_module.appendUrl('http://gsxt.scaic.gov.cn/ztxy.do')
        sub_module.appendHeaders(lambda ua:{
            "User-Agent": ua,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3",
            "Accept-Encoding": "gzip, deflate",
            "Host": "gsxt.scaic.gov.cn",
            "Origin": "http://gsxt.scaic.gov.cn",
            "Referer": "http://gsxt.scaic.gov.cn/ztxy.do",
            "Connection": "keep-alive"})
        sub_module.appendWebMethod("post")
        sub_module.appendPostData(lambda xh_prid : {'maent.pripid': xh_prid[1], 'maent.entbigtype': xh_prid[0], 'random': str(int(time.time()*1000)), 'method': 'tzrCzxxDetial', 'random': str(int(time.time() * 1000))})
        module.addEvent(Event(EventType.EXCEPTION_OCCURED, retry_times=5))
        module.addSleep(Sleep(2))
        module.appendSubModule(sub_module, True)

    #获取备案信息
    def initArchiveInfo(self, module_super):
        module = Module(self.visitBaxx, u"获取备案信息")
        module.module_id = "fetch_baxx_info"
        module.appendUrl("http://gsxt.scaic.gov.cn/ztxy.do")
        module.appendHeaders(lambda ua : {"User-Agent": ua,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3",
            "Accept-Encoding": "gzip, deflate",
            "Host": "gsxt.scaic.gov.cn",
            "Origin": "http://gsxt.scaic.gov.cn",
            "Referer": "http://gsxt.scaic.gov.cn/ztxy.do?method=index",
            "Connection": "keep-alive"})
        module.appendWebMethod("post")
        module.appendPostData(lambda pripid,entbigtype :{'czmk':'czmk2', 'maent.entbigtype':entbigtype, 'maent.pripid':pripid, 'method':'baInfo', 'random':str(int(time.time()*1000))})
        module.addEvent(Event(EventType.EXCEPTION_OCCURED, retry_times=5))
        module.addSleep(Sleep(2))
        module_super.appendSubModule(module, True)

    #获取行政处罚信息
    def initPenaltyInfo(self, module_super):
        module = Module(self.visitXzcf, u"获取行政处罚信息")
        module.appendUrl("http://gsxt.scaic.gov.cn/ztxy.do")
        module.appendHeaders(lambda ua : {"User-Agent": ua,
                              "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                              "Accept-Language": "zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3",
                              "Accept-Encoding": "gzip, deflate",
                              "Host": "gsxt.scaic.gov.cn",
                              "Origin": "http://gsxt.scaic.gov.cn",
                              "Referer": "http://gsxt.scaic.gov.cn/ztxy.do?method=index",
                              "Connection": "keep-alive"})
        module.appendWebMethod("post")
        module.appendPostData(lambda pripid, entbigtype: {'czmk': 'czmk3', 'maent.entbigtype': entbigtype, 'maent.pripid': pripid, 'method': 'cfInfo', 'random': str(int(time.time() * 1000))})
        module.addEvent(Event(EventType.EXCEPTION_OCCURED, retry_times=5))
        module.addSleep(Sleep(2))
        module_super.appendSubModule(module, True)

    #遍历企业年报列表
    def initAnnualReportPre(self, module_super):
        module = Module(self.getWebHtml, u"获取年报年份列表")
        module.module_id = "fetch_qynb_list"
        module.appendUrl("http://gsxt.scaic.gov.cn/ztxy.do")
        module.appendHeaders(lambda ua: {"User-Agent": ua,
                              "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                              "Accept-Language": "zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3",
                              "Accept-Encoding": "gzip, deflate",
                              "Host": "gsxt.scaic.gov.cn",
                              "Origin": "http://gsxt.scaic.gov.cn",
                              "Referer": "http://gsxt.scaic.gov.cn/ztxy.do",
                              "Connection": "keep-alive"})
        module.appendWebMethod("post")
        def getQynbParamList(html):
            if html:
                rs = re.findall(r'\s+onclick="doNdbg\(\'(\d{4})\'\);"', html, re.S)
                return list(set(rs))
            return []
        module.appendPostData(lambda pripid: {'czmk':'czmk8', 'maent.pripid': pripid, 'method':'qygsInfo', 'random': str(int(time.time() * 1000))})
        module.appendOutput(name="qinb_param_list", type=OutputType.FUNCTION, function=getQynbParamList, show_up=OutputParameterShowUpType.OPTIONAL)
        module.addSleep(Sleep(2))
        module_super.appendSubModule(module, True)

    def initAnnualReport(self, module_super):
        iterator = Iterator("qinb_param_list", "qynb_year")
        module = Module(None, u"遍历年报信息", iterator)
        module_super.appendSubModule(module, True)
        self.initQynbInfo(module)

    #获取年报
    def initQynbInfo(self, module_super):
        module = Module(None, u"设置年份")
        def saveNbyear(qynb_year):
            if qynb_year and qynb_year.strip():
                self.value_dict['nb_name'] = qynb_year.strip()
        module.appendOutput(type=OutputType.FUNCTION, function=saveNbyear)
        module_super.appendSubModule(module, True)

        module = Module(self.visitQynb, u"获取企业年报")
        module.appendUrl("http://gsxt.scaic.gov.cn/ztxy.do")
        module.appendHeaders(lambda ua:{"User-Agent": ua,
                              "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                              "Accept-Language": "zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3",
                              "Accept-Encoding": "gzip, deflate",
                              "Host": "gsxt.scaic.gov.cn",
                               "Referer": "http://gsxt.scaic.gov.cn/ztxy.do",
                              "Connection": "keep-alive"})
        module.appendWebMethod("post")
        module.appendPostData(lambda pripid, qynb_year: {'maent.nd': qynb_year.strip(), 'maent.pripid': pripid, 'method': 'ndbgDetail', 'random': str(int(time.time() * 1000))})
        module.appendOutput("nb_zch", '//div[@id="qufenkuang"]/table[1]/tr[3]/td[1]/text()', OutputType.LIST)#, show_up=OutputParameterShowUpType.OPTIONAL)
        module.appendOutput("nb_qym", '//div[@id="qufenkuang"]/table[1]/tr[3]/td[2]/text()', OutputType.LIST)#, show_up=OutputParameterShowUpType.OPTIONAL)
        module.addEvent(Event(EventType.OUTPUT_NOT_SATISFIED, retry_times=5))   #粗略检测年报信息有没有注册号和企业名(没有可能会因为访问太快，没数据回来)
        module.addEvent(Event(EventType.EXCEPTION_OCCURED, retry_times=5))
        module.addSleep(Sleep(2))
        module_super.appendSubModule(module, True)

    #结果收集
    def initResultCollect(self, module_super):
        module = Module(self.resultCollect, u"结果收集")
        module_super.appendSubModule(module, True)


    def getSearchList(self, search_list_xpath=None):
        ret_args = []
        if not search_list_xpath:
            return []
        for xpath_a in search_list_xpath:
            com_list = xpath_a.xpath('./text()')
            ock_list = xpath_a.xpath('./@onclick')
            if com_list and ock_list and com_list[0].strip() and ock_list[0].strip():
                match_data = re.findall(r"\'(.*?)\'", ock_list[0].strip(), re.S)
                if len(match_data) >= 2:
                    entbigtype = match_data[1].strip()
                    pripid = match_data[0].strip()
                    if entbigtype and pripid:
                        ret_args.append((com_list[0].strip(), entbigtype, pripid))
        return ret_args

    def getYzmFlag(self, html):
        if not html:
            return 'no'
        zdm_index = html.rfind('/body')
        if -1 == zdm_index:
            return 'no'
        s = html[zdm_index:]
        rs = re.findall(r'var\s+flag\s*=\s*\'(.*?)\';\s+if', s, re.S)  # 从js函数中截取验证码返回的值，''为验证识别正确，其它的值为验证码识别失败或验证码过期
        if rs:
            return 'yes' if rs[0].strip() == '' else 'no'
        return 'no'






