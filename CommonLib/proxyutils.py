# -*- coding: utf-8 -*-
"""
代理工具模块
"""
__author__ = 'xww'
import os
import sys
import random
import webutil
import xpathutil
import time
import socket
import urlparse

reload(sys)
sys.path.append('../')
sys.setdefaultencoding("UTF-8")

from lxml import etree
import exceputil
from proxy import ProxyServer
from ssdb_proxy import ssdb_proxy

proxy_shot_time = {} #(最近一次使用时间，使用次数)
proxy_shot_time_elapse = 120.0
new_proxy_list=[]
i=0
update_count=100
get_proxy_page_num=3

def get_host_name():
    sys = os.name
    if sys == 'nt':
        hostname = os.getenv('computername')
        return hostname
    elif sys == 'posix':
        host = os.popen('echo $HOSTNAME')
        try:
            hostname = host.read()
            return hostname
        finally:
            host.close()
    else:
        return 'Unkwon hostname'
    pass

def valid(proxy_str):
    """
    使用代理访问百度，测试代理是否有效
    :param proxy_str: （str) 代理ip地址或域名，可能会带有端口号  -> 218.23.145.67:8888
    :return:  (bool) 是否有效 -> True：有效  False: 无效
    """
    try:
        html_src=webutil.request("http://www.baidu.com",proxy=proxy_str,timeout=5)
        if  webutil.not_illegal_html(html_src):
            return False
        else:
            return True
    except Exception as e:
        return False

def kuaidaili(page):
    """
    去快代理抓取前page页的代理，返货通过验证的代理
    快代理网址：http://www.kuaidaili.com/free/inha/1/
    :param page: (int) 页数 ->5: 抓取前5页的代理
    :return: (list) 返回代理集合
    """
    kuaidaili_proxy_list=list()
    for i in range(1,page+1):
        url="http://www.kuaidaili.com/free/inha/%d/"%i
        html_src=webutil.request(url,encoding="utf-8")
        tree=etree.HTML(html_src)
        trs=tree.xpath(".//*[@id='list']/table/tbody/tr")
        for tr in trs:
            ip=xpathutil.gettext(tr,".//td[1]")
            port=xpathutil.gettext(tr,".//td[2]")
            proxy_str="%s:%s"%(ip,port)
            #验证代理是否有效
            if valid(proxy_str):
                kuaidaili_proxy_list.append(proxy_str)

    return kuaidaili_proxy_list


def get_crawler_proxy():
    """
    返回使用间隔超过proxy_shot_time_elapse秒的代理
    1、判断new_proxy_list集合是否有代理，如果没有则去快代理抓取前get_proxy_page_num页的内容
    2、如果最多update_count次没有请求代理则去快代理更新前get_proxy_page_num页的内容
    3、从new_proxy_list集合中找到使用间隔超过proxy_shot_time_elapse的代理并返回
    :return: (str) 代理 ->228.21.11.78:8064
    """
    global i,new_proxy_list,proxy_shot_time
    if len(new_proxy_list)<1:
        new_proxy_list=kuaidaili(get_proxy_page_num)
    i+=1
    if i%update_count==0:
        try:
            proxy_list=kuaidaili(get_proxy_page_num)
            if len(proxy_list)>=1:
                new_proxy_list=proxy_list
                proxy_shot_time.clear()

        except Exception as e:
            print u"更新代理队列出错,error:%s"%str(e)

    proxy = random.choice(new_proxy_list)
    while True:
        now_time = time.time()
        if proxy not in proxy_shot_time:
            proxy_shot_time[proxy] = (0.0, 1)
        elif now_time - proxy_shot_time[proxy][0] < proxy_shot_time_elapse:
            print u"随机选取的代理 %s 访问间隔小于%f秒 last:%f now:%f diff:%f" % (
                proxy, proxy_shot_time_elapse, proxy_shot_time[proxy][0], now_time,
                now_time - proxy_shot_time[proxy][0])
            time.sleep(0.1)
            proxy = random.choice(new_proxy_list)
            continue;
        else:
            proxy_shot_time[proxy] = (now_time, int(proxy_shot_time[proxy][1] + 1))
            break;
    return proxy

proxy_ssdb = None

def get_proxy_ssdb(crawler_name):
    """获取链接"""
    global proxy_ssdb
    while True:
        try:
            if proxy_ssdb is None:
                proxy_ssdb = ssdb_proxy(u"%s_%s" % (u"proxy", crawler_name), "spider8", 58433, 1, 300)
                pass
            else:
                proxy_ssdb.size()
                return proxy_ssdb
        except Exception as e:
            print u"ssdb连接异常:spider8-proxy"
            continue
        pass
    pass

def choice_only_proxy(crawler_name, old_proxy, need_check=False, is_debug=False, area=u"中国", host=u"master", port=8880):
    """
    crawler_name:爬虫名称
    old_proxy：上次使用的代理
    need_check：是否需要校验当前代理的有效性
    is_debug：is_debug
    area：area
    host：host
    port：port
    """
    #获取ssdb连接
    proxy_ssdb = get_proxy_ssdb(crawler_name)
    temp_proxy = None
    while True:
        #获取一个代理
        temp_proxy = choice_proxy(is_debug=is_debug, host=host, area=area, port=port)
        #验证是否占用
        if proxy_ssdb.hexists(temp_proxy):
            continue
        else:
            if need_check:
                try:
                    html = webutil.request("http://site.baidu.com/", proxy=temp_proxy, retry=0, timeout=8)
                    if not webutil.not_illegal_html(html):
                        print "get a good proxy:", temp_proxy
                        break
                    else:
                        continue
                except Exception as e:
                    continue
            else:
                break
        pass
    #删除老的代理
    if old_proxy is not None:
        proxy_ssdb.hdel(old_proxy)
        pass
    #添加新的代理
    proxy_ssdb.hset(temp_proxy, u"%s_%d" % (get_host_name(), os.getpid()))
    #返回代理
    return temp_proxy

def choice_proxy(is_debug=True,url="",area=u"中国",host=u"master",port=8880):
    """
    获取代理地址,请求指定区域的代理,默认是全国范围。
    :param is_debug:  (bool) 是否不使用收费的代理 -> True:不使用收费代理  False:使用收费代理
    :param url: (unicode) 网页地址，目前只支持收费的代理。是为了代理访问网站的负载均衡
    :param area: (unicode) 代理地址所在的区域和类型，目前只支持收费的代理。->
                 中国,电信,联通，浙江 ,深圳，广东，上海
                 北京，福建,重庆,四川,新疆,湖北,山东,黑龙江
    :return: (str) 代理 ->228.21.11.78:8064
    """
    if is_debug:
        proxy=get_crawler_proxy()
    else:
        proxy=None
        while proxy is None or len(proxy) < 1:
            if len(url)>0:
                urlpret = urlparse.urlparse(url)
                host=urlpret.hostname
            try:
                proxy=get_server_proxy(host,area.encode("UTF-8","ignore"),port=port)
            except BaseException as e:
                print exceputil.traceinfo(e)
                time.sleep(10)
                continue
    proxy= proxy.strip()
    print "choice_proxy ret:", proxy
    return proxy


proxyServerClient = None

def init_proxy_client(host="master",port=8880):
    """
    初始化收费代理的处理对象
    :return:  收费代理的处理对象
    """
    reload(ProxyServer)
    #hostname = socket.gethostbyname(socket.gethostname())
    return  ProxyServer.ProxyServerClient(host=host,port=port)


def  get_server_proxy(host,area,port=8880):
    """
    获取收费代理地址
    :param host: （str) 域名
    :param area:  (str） 区域 ->全国
    :return: (unicode) 代理 -> 231.29.67.145:8585
    """
    global proxyServerClient
    if proxyServerClient==None:
        #初始化
        while True:
            try:
                proxyServerClient=init_proxy_client(host=host,port=port)
                break
            except Exception as e:
                print exceputil.traceinfo(e)
                time.sleep(10)
    proxy=""
    while True:
        try:
            proxy= proxyServerClient.getPorxy(host, area)
            if proxy!=None and len(proxy.strip())>0:
                break
            else:
                #代理是None或空字符串则重试
                time.sleep(10)
                while True:
                    try:
                        proxyServerClient=init_proxy_client(host=host,port=port)
                        break
                    except Exception as  e1:
                        print exceputil.traceinfo(e1)
                        time.sleep(10)
                continue
        except Exception as e:
            print exceputil.traceinfo(e)
            time.sleep(10)
            while True:
                try:
                    proxyServerClient=init_proxy_client(host=host,port=port)
                    break
                except Exception as  e1:
                    print exceputil.traceinfo(e1)
                    time.sleep(10)

    return proxy.strip()

if __name__=="__main__":
    # while True:
    #     try:
    #         proxy= choice_proxy(is_debug=False,host="192.168.2.71")
    #         print webutil.request("http://www.baidu.com",proxy=proxy,timeout=30)
    #         time.sleep(10)
    #     except Exception as e:
    #         print str(e)
    old_proxy = None
    while True:
        temp_proxy = choice_only_proxy("qyxx_sichuan", old_proxy, need_check=True, is_debug=False, host="master1", area=u"中国", port=8880)
        print temp_proxy
        old_proxy = temp_proxy
