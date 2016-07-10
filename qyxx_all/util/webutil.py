# -*- coding: utf-8 -*-
# Created on 2014/10/28 16:56.
"""
网络请求基础模块
Test: test.webutiltest.py
"""
__author__ = 'xww'

import urllib
import urllib2
import urlparse
import os
import sys
import gzip
import chardet
import time
from StringIO import StringIO
from urllib2 import Request
from cookielib import Cookie
import re
import random
import platform
import pycurl
from common.retrying import retry

#spynner只支持windows系统
if platform.system() != "Linux":
    import spynner

#默认的编码
encoding_default='UTF-8'
#默认的超时时间
timeout_default=60
#默认的连接超时时间，目前只支持curl库
conn_timeout_default=20
#http Post方法
POST="post"
#http Get方法
GET="get"
#模拟浏览器方式分析页面编码
auto_encoding="auto"
#从http相应头的content-type中获取编码
head_encoding="head"
#从html的meta标签获取charset编码
content_encoding="content"
#自动识别编码
detect_encoding="detect"
#debug模式
debug_mode=True
#user-agent集合
USER_AGENT_LIST=[
    u"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 2.0.50727)",
    u"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET4.0E; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET4.0C)",
    u"Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.2; Trident/4.0; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET4.0E; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET4.0C)",
    u"Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
    u"Mozilla/5.0 (Windows NT 5.1; rv:5.0) Gecko/20100101 Firefox/5.0",
    u"Mozilla/5.0 (Windows NT 5.2) AppleWebKit/534.30 (KHTML, like Gecko) Chrome/12.0.742.122 Safari/534.300",
    u"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1)",
    u"Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.04506.648; .NET CLR 3.5.21022; .NET4.0E; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET4.0C)",
    u"Opera/9.80 (Windows NT 5.1; U; zh-cn) Presto/2.9.168 Version/11.50",
    u"Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/533.21.1 (KHTML, like Gecko) Version/5.0.5 Safari/533.21.1",
    u"Mozilla/5.0 (Windows; U; Windows NT 5.1; ) AppleWebKit/534.12 (KHTML, like Gecko) Maxthon/3.0 Safari/534.12",
    u"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)",
    u"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)"
]
#mobile user-agent集合
MOBILE_USER_AGENT_LIST=[
    u"Mozilla/5.0 (Linux; U; Android 0.5; en-us) AppleWebKit/522+ (KHTML, like Gecko) Safari/419.3",
    u"Mozilla/5.0 (Linux; U; Android 2.2; en-us; Nexus One Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    u"Mozilla/5.0 (Linux; U; Android 2.1; en-us; Nexus One Build/ERD62) AppleWebKit/530.17 (KHTML, like Gecko) Version/4.0 Mobile Safari/530.17"
    u"Mozilla/5.0 (Linux; U; Android 1.6; en-gb; Dell Streak Build/Donut AppleWebKit/528.5+ (KHTML, like Gecko) Version/3.1.2 Mobile Safari/ 525.20.1",
    u"Mozilla/5.0 (Linux; U; Android 2.1-update1; en-us; ADR6300 Build/ERE27) AppleWebKit/530.17 (KHTML, like Gecko) Version/4.0 Mobile Safari/530.17",
    u"Mozilla/5.0 (Linux; U; Android 1.6; en-us; WOWMobile myTouch 3G Build/unknown) AppleWebKit/528.5+ (KHTML, like Gecko) Version/3.1.2 Mobile Safari/525.20.1",
    u"Mozilla/5.0 (Linux; U; Android 2.2; nl-nl; Desire_A8181 Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    u"HTC_Dream Mozilla/5.0 (Linux; U; Android 1.5; en-ca; Build/CUPCAKE) AppleWebKit/528.5+ (KHTML, like Gecko) Version/3.1.2 Mobile Safari/525.20.1"
    u"Mozilla/5.0 (Linux; U; Android 2.2; en-gb; GT-P1000 Build/FROYO) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    u"Mozilla/5.0 (Linux; U; Android 2.2; en-ca; SGH-T959D Build/FROYO) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1"
    u"Mozilla/5.0 (Linux; U; Android 2.2; en-gb; GT-P1000 Build/FROYO) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    u"Mozilla/5.0 (Linux; U; Android 2.0.1; en-us; Droid Build/ESD56) AppleWebKit/530.17 (KHTML, like Gecko) Version/4.0 Mobile Safari/530.17",
    u"Mozilla/5.0 (iPhone; U; CPU iPhone OS 5_0 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Mobile/9A334 Safari/7534.48.3",
    u"Mozilla/5.0 (iPhone; CPU iPhone OS 5_0_1 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Mobile/9A405 Safari/7534.48.3",
    u"Mozilla/5.0 (iPhone; CPU iPhone OS 5_1_1 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9B206 Safari/7534.48.3"
]
def get_user_agent():
    """
    在USER_AGENT_LIST列表随机选取一个Uset-Agent
    :return: (unicode) User_Agent
    """
    return random.choice(USER_AGENT_LIST).strip()

def  get_mobile_user_agent():
    """
    在MOBILE_USER_AGENT_LIST列表中随机选取一个User-Agent
    :return: (unicode) Mobile User_Agent
    """
    return random.choice(MOBILE_USER_AGENT_LIST).strip()

def build_header(url):
    urlpret = urlparse.urlparse(url)
    return   {
    "Host": urlpret.netloc,
    "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Encoding":"gzip, deflate",
    "Accept-Language"	:"zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3"
    }


@retry(stop_max_attempt_number=3, wait_fixed=1*1500)
def  request_urllib2(url,timeout=timeout_default,headers=None,data=None,encoding=None,proxy=None,cookie=None,method=GET,ua="",retry=0,data_union='&',savefile="./last_response.html",urllib2_debuglevel=None):
    """
    使用urllib2库。发起http请求，返回相应信息，如果相应信息是压缩的则解压缩，如果设置encoding参数，则会相应原文转换为unicode编码,
    :param url: 网页地址 --> http://www.baidu.com
    :param timeout: 请求超时时间,默认60 -->60
    :param headers: http请求头,字典形式，默认为空字典-->{‘Reference':'http://www.baidu.com'}
    :param data:http请求参数,字典形式--》{'user':'xww'}
    :param encoding:html编码，如果设置编码则会转换为unicode，如果没有指定编码则发挥原生态字符串
    :param proxy:代理地址，默认不使用--》238.23.12.54
    :param cookie:cookieJar对象
    :param method:http请求方法，目前只支持get和post--->get
    :param ua:user-agent-->	Mozilla/5.0 (Windows NT 5.1; rv:34.0) Gecko/20100101 Firefox/34.0
    :param retry:重试次数
    :param data_union:请求参数分隔符，默认为&
    :param savefile:保存到本地文件位置
    :return: 如果指定编码则返回unicode编码，否则返回网页原文str
    """
    #设置Header
    if not isinstance(headers,dict) or len(headers)<1:
        headers=build_header(url)
    #设置User-Agent
    if ua!=None and len(ua)>0:
        headers["User-Agent"]=ua
    if method==GET:
        #如果请求方法是Get并且有请求数据，则自动进行拼接
        if data is not None:
            param=urllib.urlencode(data)
            if url.find('?')>0:
                url=url+'&'+param
            else:
                url=urlparse.urljoin(url,'?'+param)
        req=Request(url,headers=headers)
    else:
        #POST方法拼接data字符串，没有使用urllib.urlencode是因为有些特殊网站使用\n来分割
        if isinstance(data,dict):
            index=0
            date_url=""
            for  d in data:
                if index>0:
                    date_url+=data_union
                va=data[d]
                if isinstance(va,list):
                    vlist=""
                    i2=0
                    for v in va:
                         if i2>0:
                            vlist+=data_union
                         vlist+=d+"="+v
                         i2+=1
                    date_url+=vlist
                else:
                    date_url+=d+"="+str(va)

                index+=1

            req=Request(url,data=date_url,headers=headers)
        elif isinstance(data,basestring):
            req=Request(url,data=data,headers=headers)
        else:
            req=Request(url,data="",headers=headers)

    handlers=[]
    #如果代理有效而且不是本地服务器则设置代理
    if isinstance(proxy,basestring) and len(proxy.strip())>0 and proxy!= "localhost" and  proxy !="127.0.0.1":
        if url.startswith("https"):
            handlers.append(urllib2.ProxyHandler({"https":'http://%s/'%proxy.strip()}))
        else:
            handlers.append(urllib2.ProxyHandler({"http":'http://%s/'%proxy.strip()}))
    #如果cookie有效则设置cookie
    if cookie is not None:
        handlers.append(urllib2.HTTPCookieProcessor(cookie))
    #count是请求次数，重试次数加上第一次请求
    count=retry+1;
    opener = None
    response = None

    if urllib2_debuglevel != None:
        print "headers:", headers
        #httpHandler = urllib2.HTTPHandler(debuglevel=1)
        #httpsHandler = urllib2.HTTPSHandler(debuglevel=1)
        httpHandler = urllib2.HTTPHandler(debuglevel=urllib2_debuglevel)
        httpsHandler = urllib2.HTTPSHandler(debuglevel=urllib2_debuglevel)
        handlers.append(httpHandler)
        handlers.append(httpsHandler)

    while(count>0):
        try:
            opener=urllib2.build_opener(*handlers)
            #发起http请求并获取响应数据
            response = opener.open(req, timeout=timeout)
            #获取http响应代码
            code=response.code
            if code!=200:
                raise Exception("error code,code=%d"%code)
            if response.info().get('Content-Encoding') == 'gzip':
                buf = StringIO( response.read())
                f = gzip.GzipFile(fileobj=buf)
                html_src = f.read()
            else:
                html_src = response.read()

            if  encoding is not None:
                enc=""
                if encoding == head_encoding:
                    enc=get_head_charset(response.info().get('Content-Type'))
                elif encoding==content_encoding:
                    enc=get_html_charset(html_src)
                elif encoding==detect_encoding:
                    enc=get_html_detect(html_src)
                elif encoding==auto_encoding:
                    enc=get_html_charset(html_src)
                    if len(enc)<1:
                        enc=get_head_charset(response.info().get('Content-Type'))
                    if len(enc)<1:
                        enc=get_html_detect(html_src)
                else:
                    enc=encoding
                if len(enc)>0:
                    result= html_src.decode(enc,"ignore")
                    if debug_mode:
                       save(savefile,html_src)
                    return result
                else:
                    if debug_mode:
                        save(savefile,html_src)
                    return html_src
            else:
                if debug_mode:
                    save(savefile,html_src)
                return html_src
        except Exception as e:
            print traceinfo(e)
            if count>1:
                count-=1
                time.sleep(2)
                continue
            else:
                raise
        finally:
            try:
                if opener != None:
                    opener.close()
            except Exception as e:
                print traceinfo(e)
            try:
                if response != None:
                    response.close()
            except Exception as e:
                print traceinfo(e)

def  save(savefile,html_src):
    """
    保存文件
    :param savefile:  (unicode)  文件名
    :param html_src: (unicode) html源码
    :return:(None)
    """
    try:
        if savefile is not None and len(savefile)>0:
            f=open(savefile, "wb")
            f.write(html_src)
            try:
                f.close()
            except Exception as e1:
                pass
    except Exception as e:
        pass

def get_html_detect(html_src):
    """
     自动检测html编码
    :param html_src: html 源码
    :return:  (unicode)编码
    """

    info = chardet.detect(html_src)
    enc= info['encoding']
    if len(enc)>0:
     return enc
    return ""


def get_head_charset(response):
    """

    :param response:  (str) 响应体
    :return:
    """
    contentType=response.info().get('Content-Type')
    if contentType is not None:
        if len(contentType)>0:
            enc=re.search('"text/html;\\s*charset=([a-z0-9-]+)',contentType)
            if enc is not None:
                enc=enc.group(1)
                if len(enc)>0:
                    return "ignore"
    return ""


def get_html_charset(html_src):
    enc=re.search('"text/html;\\s*charset=([a-z0-9-]+)"',html_src)
    if enc is not None:
        enc=enc.group(1)
        if len(enc)>0:
            return enc
    return ""


headers_info = {}

def header_function(header_line):
    """
    回调函数，处理http相应头的一行数据, 存入headers_info字典里面。
    :param header_line: (str) http响应头的一行数据
    :return: None
    """

    # HTTP standard specifies that headers are encoded in iso-8859-1.
    # On Python 2, decoding step can be skipped.
    # On Python 3, decoding step is required.
    header_line = header_line.decode('iso-8859-1')

    # Header lines include the first status line (HTTP/1.x ...).
    # We are going to ignore all lines that don't have a colon in them.
    # This will botch headers that are split on multiple lines...
    if ':' not in header_line:
        return

    # Break the header line into header name and value.
    name, value = header_line.split(':', 1)

    # Remove whitespace that may be present.
    # Header lines include the trailing newline, and there may be whitespace
    # around the colon.
    name = name.strip()
    value = value.strip()

    # Header names are case insensitive.
    # Lowercase name here.
    name = name.lower()

    # Now we can actually record the header name and value.
    global headers_info
    if headers_info.has_key(name):
        headers_info[name]=headers_info[name]+"\r\n"+value
        return

    headers_info[name] = value


def  request_curl(url,timeout=timeout_default,conn_timeout=conn_timeout_default,headers={},data=None,encoding=None,proxy=None,cookie=None,method=GET,ua="",retry=0,data_union='&',savefile="./last_response.html",verbose=False):
    """
    使用curl库
    参考url：http://blog.sina.com.cn/s/blog_40e4b5660100sxa3.html
    发起http请求，返回相应信息，如果相应信息是压缩的则解压缩，如果设置encoding参数，则会相应原文转换为unicode编码
    :param url: 网页地址 --> http://www.baidu.com
    :param timeout: http请求的传输超时时间,默认60
    :param conn_timeout http请求的连接超时时间，默认20
    :param verbose 是否打印详细信息，默认False
    :param headers: http请求头,字典形式，默认为空字典-->{‘Reference':'http://www.baidu.com'}
    :param data:http请求参数,字典形式--》{'user':'xww'}
    :param encoding:html编码，如果设置编码则会转换为unicode，如果没有指定编码则发挥原生态字符串
    :param proxy:代理地址，默认不使用--》238.23.12.54
    :param cookie:cookieJar对象
    :param method:http请求方法，目前只支持get和post--->get
    :param ua:user-agent-->	Mozilla/5.0 (Windows NT 5.1; rv:34.0) Gecko/20100101 Firefox/34.0
    :param retry:重试次数
    :param data_union:请求参数分隔符，默认为&
    :param savefile:保存到本地文件位置
    :return: 如果指定编码则返回unicode编码，否则返回网页原文str

    """
    # http请求成功标志
    #success_flag=False
    # post data 字符串
    post_data=""
    crl=None
    fp=None
    #如果不设置User-Agent 则随机选择一个
    if not isinstance(ua,basestring) or len(ua)<5:
        ua=random.choice(USER_AGENT_LIST)

    if method==GET:
        if data is not None:
            param=urllib.urlencode(data)
            if url.find('?')>0:
                url=url+'&'+param
            else:
                url=urlparse.urljoin(url,'?'+param)
    else:
        if isinstance(data,dict):
            index=0
            data_url=""
            for  d in data:
                if index>0:
                    data_url+=data_union
                va=data[d]
                if isinstance(va,list):
                    vlist=""
                    i2=0
                    for v in va:
                         if i2>0:
                            vlist+=data_union
                         vlist+=d+"="+v
                         i2+=1
                    data_url+=vlist
                else:
                    data_url+=d+"="+str(va)

                index+=1
            post_data=data_url
        elif isinstance(data,basestring):
            post_data=data
        else:
            post_data=""
    count=retry+1;
    while(count>0):
        try:
            #创建一个同libcurl中的CURL处理器相对应的Curl对象
            crl = pycurl.Curl()
            #不打印详细日志
            crl.setopt(pycurl.VERBOSE,verbose)
            #不支持重定向
            crl.setopt(pycurl.FOLLOWLOCATION, True)
            #设置最大重定向次数
            crl.setopt(pycurl.MAXREDIRS, 2)
            fp = StringIO()
            #设置url地址
            crl.setopt(pycurl.URL, url)
            #设置回调函数
            crl.setopt(crl.WRITEFUNCTION, fp.write)
            #链接超时
            crl.setopt(pycurl.CONNECTTIMEOUT, conn_timeout)
             #下载超时
            crl.setopt(pycurl.TIMEOUT, timeout)
            if url.startswith("https"):
                #跳过SSL验证
                crl.setopt(pycurl.SSL_VERIFYPEER, 0)
                crl.setopt(pycurl.SSL_VERIFYHOST, 0)

            #设置http请求方法
            if method==POST:
                crl.setopt(pycurl.POST, 1)
                crl.setopt(pycurl.POSTFIELDS, post_data)

            #设置解析相应head内容的回调方法
            crl.setopt(crl.HEADERFUNCTION, header_function)
            if isinstance(proxy,basestring) and len(proxy.strip())>0 and proxy!= "localhost" and  proxy !="127.0.0.1":
                #设置代理
                proxy=proxy.strip()
                if not proxy.startswith("http"):
                    proxy="http://%s"%proxy
                crl.setopt(pycurl.PROXY,proxy)

            if cookie != None:
                thecookie=""
                for item in cookie:
                    if len(thecookie)>0:
                        thecookie+=";"
                    thecookie += item.name+"="+item.value
                if thecookie!=None and len(thecookie)>0:
                    crl.setopt(pycurl.COOKIE,thecookie)
                # cookie.save("./cookie.txt",True,True)
                # crl.setopt(pycurl.COOKIEFILE, "./cookie.txt")
                #crl.setopt(pycurl.COOKIEJAR, "./cookie1.txt")


            #设置UA
            crl.setopt(pycurl.USERAGENT, ua)
            #设置请求头
            if len(headers)>0:
                head_list=list()
                for h in headers:
                    if h !="User-Agent":
                        head_str="%s:%s"%(h,headers[h])
                        head_list.append(head_str)
                crl.setopt(crl.HTTPHEADER,head_list)
            #执行请求
            crl.perform()

            content_type=crl.getinfo(crl.CONTENT_TYPE)
            #解析content_encoding
            global headers_info
            content_encoding=""
            if headers_info !=None and headers_info.has_key("content-encoding"):
                content_encoding=headers_info["content-encoding"]

            code=crl.getinfo(crl.HTTP_CODE)
            #判断相应状态码是否是200
            if code!=200:
                raise Exception("error code,code=%d"%code)

            #解析setcookie，把内容存在cookie对象中
            if headers_info.has_key("set-cookie") and cookie!=None:
                #从响应头中拿到set-cookie内容
                set_cookies=headers_info["set-cookie"]
                #相应头中可能有多个set-cookie,用\r\n分割
                set_cookiess=set_cookies.split("\r\n")
                for set_cookie in set_cookiess:
                    #ASP.NET_SessionId=khov1sveqo5juo30gv301u1y; path=/; HttpOnly
                    # cookie分割符是分号，通过分号分割多个键值对.BAIDUPSID=5E7D7AE2681AD393F829553FCDE031CB
                    cookie_strs=set_cookie.split(";")
                    cookie_dict=dict()
                    for cookie_str in cookie_strs:
                        if len(cookie_str.strip())<1:
                            continue
                        #键值对通过等号分割
                        #path默认为根目录
                        path="/"
                        #domain默认为当前域名
                        urlpret = urlparse.urlparse(url)
                        domain=urlpret.netloc
                        #过期时间默认为两星期内
                        expire=time.time()+3600*24*14
                        if cookie_str.find("=")>0:
                            cookie_key_value=cookie_str.split("=")
                            #cookie键和值
                            key=cookie_key_value[0].strip()
                            value=cookie_key_value[1].strip()
                            #解析path
                            key=key.lower()
                            if key =="path":
                                path=value
                                continue
                            #解析域名
                            if key=="domain":
                                domain=value
                                continue
                            if key=="expire":
                                continue
                            cookie_dict[key]=value
                        for key in cookie_dict:
                            value=cookie_dict[key]
                            #构造一个cookie对象
                            c=Cookie(None,key,value,"","",domain,"","",path,"","",expire,"","","","")
                            #把cookie对象放到cookiejar里
                            cookie.set_cookie(c)


            #判断相应内容是否为压缩类型
            if content_encoding == 'gzip':
                #StringIO指针开头
                temp_si=StringIO(fp.getvalue())
                #解压缩
                f = gzip.GzipFile(fileobj=temp_si)
                html_src = f.read()
            else:
                html_src = fp.getvalue()

            result=html_src
            if  encoding !=None and len(encoding)>0:
                #使用相应头中的Content-Type
                if encoding == head_encoding:
                    enc=get_head_charset(content_type)
                #使用正文内容中的meta中的Content-Type
                elif encoding==content_encoding:
                    enc=get_html_charset(html_src)
                #自动检测内容编码
                elif encoding==detect_encoding:
                    enc=get_html_detect(html_src)
                #浏览器模式，先检查html的meta标签的Content-Type,如果没有在使用相应头的Content-Type,如果没有则自动检测编码
                elif encoding==auto_encoding:
                    enc=get_html_charset(html_src)
                    if len(enc)<1:
                        enc=get_head_charset(content_type)
                    if len(enc)<1:
                        enc=get_html_detect(html_src)
                else:
                    #调用时指定编码
                    enc=encoding
                #如果编码有效则转码，否则使用自动检测的编码
                if len(enc)>0:
                    result= html_src.decode(enc,"ignore")
                else:
                    enc=get_html_detect(html_src)
                    result=html_src.decode(enc,"ignore")
            #如果采用debug模式则保存内容
            if debug_mode:
                save(savefile,html_src)
            #设置请求成功标志
            #success_flag=True
            return result

        except Exception as e:
            print traceinfo(e)
            #如果小于重试次数则重试，否则抛出异常
            if count>1:
                count-=1
                time.sleep(2)
                continue
            else:
                raise
        finally:
            try:
                if crl != None:
                    #关闭curl对象
                    crl.close()
                #把response中的set-cookie存到COOKIEJAR中，curl对象关闭时会把cookie内容写入文件中
                # if cookie!=None and success_flag and os.path.exists("./cookie1.txt"):
                #     cookie.load(filename="./cookie1.txt",ignore_discard=True, ignore_expires=True)
            except Exception as e:
                 print traceinfo(e)
            try:
                if fp != None:
                    fp.close()
            except Exception as e:
                print traceinfo(e)



def  save(savefile,html_src):
    """
    资源内容存入文件中
    :param savefile:  文件名
    :param html_src:  资源内容
    :return:  成功返回True，失败返回False
    """
    if debug_mode:
        f=None
        try:
            if savefile is not None and len(savefile)>0:
                f=open(savefile, "wb")
                f.write(html_src)
                return True
        except Exception as e:
             print traceinfo(e)
             return False
        finally:
            if f!=None:
                try:
                    f.close()
                except Exception as e1:
                    print traceinfo(e1)
    else:
        return True

def get_html_detect(html_src):
    """
    返回检测的html编码类型
    :param html_src:  html内容
    :return:   自动检测出来的编码
    """
    info = chardet.detect(html_src)
    if info.has_key("encoding"):
        enc= info['encoding']
        if len(enc)>0:
            return enc
    return ""

def get_head_charset(contentType):
    """
    解析http响应头中的Conteyt-Type编码类型并返回
    :param contentType:  响应头的contentType内容
    :return:  (str) 编码 -> utf-8
    """
    if contentType is not None:
        if len(contentType)>0:
            enc=re.search('"text/html;\\s*charset=([a-z0-9-]+)',contentType)
            if enc is not None:
                enc=enc.group(1)
                if len(enc)>0:
                    return enc
    return ""


def get_html_charset(html_src):
    """
    在html源码里找meta标签的charset信息
    :param html_src: (str) html源文件
    :return: (str) 字符编码
    """
    enc=re.search('"text/html;\\s*charset=([a-z0-9-]+)"',html_src)
    if enc is not None:
        enc=enc.group(1)
        if len(enc)>0:
            return enc
    return ""

def  traceinfo(e):
    """
    获取异常堆栈信息
    :param e:  异常
    :return:  异常堆栈信息
    """
    exceptionType, exceptionValue, exceptionTraceback = sys.exc_info()
    result=u""
    import traceback
    excep_list=traceback.format_exception(exceptionType, exceptionValue, exceptionTraceback)
    print excep_list

    for ex in  excep_list:
        info = chardet.detect(ex)
        enc= info['encoding']
        result+=ex.decode(enc,"ignore")
    return result

def browse(url,spynner_browser_timeout,proxy=None):
    """
    模拟浏览器访问url地址，返回html源文
    :param url:  url地址
    :param spynner_browser_timeout:  超时时间
    :param proxy:  代理地址
    :return: html源文
    """

    urlpret = urlparse.urlparse(url)

    browser = spynner.Browser(
                    user_agent="Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9.1) Gecko/20090624 Firefox/3.5",
                    headers=[("Referer", '%s://%s' % (urlpret.scheme, urlpret.netloc))])
    if proxy !=None:
        browser.set_proxy(proxy)

    browser.load(url=url, load_timeout=spynner_browser_timeout)
    html=browser.html


    browser.close()
    return html



def not_illegal_html(html):
    """
    :param html:  html代码
    :return:    是否是无效长度的html
    """
    return len(html)<100  or len(html)>1024*1024*10

def illegal_html(html):
    """
    判断html内容长度
    :param html:  html代码
    :return: 是否有效的html代码
    """
    return len(html)>=100  and len(html)<=1024*1024*10

def not_illegal_json(html):
    """
    判断json是否是合法的json代码
    :param html:  json代码
    :return:   是否是不合法的json字符串
    """
    return len(html)<20

def  jsessionid(cookieJar,domain,path="/"):
    """
    从cookie 中抓取jsession数据并返回，不存在则返回空字符串
    :param cookieJar:  (cookieJar) cookie对象
    :param domain:  (str) 域名
    :param path: (str)路径
    :return: jsession内容，不存在返回空字符串
    """
    try:
        jsession=str(cookieJar._cookies[domain][path]['JSESSIONID'])
        import re
        return   re.search(r"JSESSIONID=(.+?)\s",jsession).group(1)
    except Exception as e:
        return ""

#默认request请求，使用request_urllib2.
request=request_urllib2

