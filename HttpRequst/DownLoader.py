# -*- coding: utf-8 -*-
"""
企业信息网下载模块
"""
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import os
import socket
import urlparse
import requests
from requests import Request, Session
from requests.cookies import cookiejar_from_dict
import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()
#忽略请求过程的警告输出
import random
import time
import warnings

from Proxy import Proxy

sys.path.append("../")
from CommonLib import SendMail
from CommonLib.exceptutil import traceinfo

user_agent = [
    u"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36 SE 2.X MetaSr 1.0",
    u"Mozilla/5.0 (Windows NT 10.0; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0",
    u"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.11 (KHTML, like Gecko) Ubuntu/11.10 Chromium/27.0.1453.93 Chrome/27.0.1453.93 Safari/537.36",
    u"Mozilla/5.0 (compatible; WOW64; MSIE 10.0; Windows NT 6.2)",
    u"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.11 (KHTML, like Gecko) Ubuntu/11.10 Chromium/27.0.1453.93 Chrome/27.0.1453.93 Safari/537.36",
    ]

class DownLoader(object):
    """
    下载模块
    根据requests，Session，自动管理cookie, session保持连接
    外加代理管理模块
    """
    def __init__(self,province_name,log=None):
        """
        初始化代理，链接Session，ua
        :return:
        """
        self.ua = random.choice(user_agent)
        self.ss = Session()
        self.pro_name = province_name.lower()
        self.proxy_c=Proxy(self.pro_name)
        self.proxyInit()
        self.correct_http = 0
        self.error_http = 0
        self.log = log
        self.proxy = self.proxySet

    def firstInit(self):
        """
        在每次第一步请求之前初始化
        :return:
        """
        self.ss=Session()
        self.ua=random.choice(user_agent)
        self.proxy_num , self.proxy = self.proxy_c.firstPorxy(self.proxy_num)
        self.retry_flag=True
        self.status_code_ok = set()

    def proxyInit(self):
        """
        代理统计初始化
        :return:
        """
        self.proxy_num=0

    def get(self,url,**kwargs):
        """
        封装get请求
        :param url:
        :param kwargs:
        :return:
        """
        return self.request(url,method='GET',**kwargs)

    def post(self,url,**kwargs):
        """
        封装post请求
        :param url:
        :param kwargs:
        :return:
        """
        return self.request(url,method='POST',**kwargs)

    def request(self, url, method = 'GET', **kwargs):
        """
        下载模块：Constructs and sends a :class:`Request <Request>`.
        Returns :class:`Response <Response>` object.

        :param method: method for the new :class:`Request` object.
        :param url: URL for the new :class:`Request` object.
        :param params: (optional) Dictionary or bytes to be sent in the query string for the :class:`Request`.
        :param data: (optional) Dictionary, bytes, or file-like object to send in the body of the :class:`Request`.
        :param headers: (optional) Dictionary of HTTP Headers to send with the :class:`Request`.
        :param cookies: (optional) Dict or CookieJar object to send with the :class:`Request`.
        :param files: (optional) Dictionary of ``'name': file-like-objects`` (or ``{'name': ('filename', fileobj)}``) for multipart encoding upload.
        :param auth: (optional) Auth tuple to enable Basic/Digest/Custom HTTP Auth.
        :param timeout: (optional) How long to wait for the server to send data
            before giving up, as a float, or a (`connect timeout, read timeout
            <user/advanced.html#timeouts>`_) tuple.
        :type timeout: float or tuple
        :param allow_redirects: (optional) Boolean. Set to True if POST/PUT/DELETE redirect following is allowed.
        :type allow_redirects: bool
        :param proxies: (optional) Dictionary mapping protocol to the URL of the proxy.
        :param verify: (optional) if ``True``, the SSL cert will be verified. A CA_BUNDLE path can also be provided.
        :param stream: (optional) if ``False``, the response content will be immediately downloaded.
        :param cert: (optional) if String, path to ssl client cert file (.pem). If Tuple, ('cert', 'key') pair.
        """
        self.outputLog("DownLoader内部，进入request方法","debug")
        self.mail()
        def _get_values(strs,default = None):
            return kwargs[strs] if strs in kwargs else default

        use_proxy = _get_values('use_proxy',default = True)
        params = _get_values('params',default = None)
        data = _get_values('data')
        headers = kwargs['headers'] if 'headers' in kwargs else {"Host":urlparse.urlparse(url).netloc,"User-Agent":self.ua}
        ua = _get_values('ua',default=None)
        if ua :
            headers.update({"User-Agent":ua})
        allow_redirects = _get_values('allow_redirects',default = True)
        verify = _get_values('verify',default=False)
        stream = _get_values('stream',default=False)
        cert = _get_values('cert',default=None)
        de = DownLoaderException()
        exception = ''
        _retry = _get_values('retry')
        _retry = _retry+1 if _retry else (1 if _retry <= 0 and _retry != None else (30 if self.retry_flag else 2))
        _retry = _retry if _retry and _retry>=0 else 1
        if self.retry_flag == True:
            timeout = 30
        else:
            timeout = 120
        while _retry:
            _retry -= 1
            res = None
            try:
                self.outputLog("使用代理 %s" % self.proxy)
                req = Request(method.upper(),
                                url,
                                data=data or {},
                                headers=headers or {},
                                params=params or {}
                                )
                self.outputLog("DownLoader内部，即将prepare request","debug")
                prepped  = self.ss.prepare_request(req)
                self.outputLog("DownLoader内部，即将调用session.send","debug")
                if use_proxy == False:
                    self.outputLog('该步代理设置为空')
                    proxies = {}
                else:
                    proxies = {'http': 'http://' + self.proxy, 'https': 'http://' + self.proxy} if self.proxy else {}
                settings = self.ss.merge_environment_settings(prepped.url,proxies,stream, verify, cert)
                send_kwargs = {
                    'timeout': timeout,
                    'allow_redirects': allow_redirects,
                }
                send_kwargs.update(settings)
                resp = self.ss.send(prepped,
                                    **send_kwargs
                                    )
                self.outputLog("DownLoader内部，从session.send返回","debug")
                if resp and isinstance(resp,object) and resp.status_code == requests.codes.ok:
                    self.correct_http += 1
                    self.retry_flag = False
                    self.outputLog("DownLoader内部，调用成功，即将从request方法返回","debug")
                    return resp
                if resp.status_code in self.status_code_ok:
                    return resp
                else:
                    self.error_http += 1
                    if 500 <= resp.status_code < 600:#返回code为500和600之间时候是服务器的问题，故休眠1分钟
                        self.outputLog(u'返回码为%d，休眠一分钟'%resp.status_code)
                        time.sleep(60)
                    resp.raise_for_status()

            except Exception as e:
                self.outputLog("获取页面内容异常：%s" % traceinfo(e), "error")
                exception += str(e)
                de.exception = exception
                de.res = res
                de.time_out = True if not res else False
                if self.retry_flag:
                    self.proxy=self.proxySet

        if self.proxy:
            self.proxy = self.proxySet

        self.outputLog("DownLoader内部，调用失败，即将从request方法返回，同时抛出异常","debug")
        raise de

    def setNotRaise(self,*status_code):
        '''
        当某些时候返回是非200时候，但是这些返回的内容需要时候，把改返回码加入该集合，以便过滤
        :param status_code:
        :return:
        '''
        self.status_code_ok.update(status_code)

    def outputLog(self, msg, level='info'):
        print msg
        if not self.log:
            return
        try:
            func = eval('self.log.%s' % level)
            if not callable(func):
                return
            func(msg)
        except:
            return

    def cookieUpdate(self,cookie_dict):
        """
        更新cookie
        :param cookie_dict: 字典格式
        :return:
        """
        if not isinstance(cookie_dict,dict):
            warnings.warn(u"%s type not dict,Not Enabled Update."% str(type(cookie_dict)))
            return
        cookiejar_from_dict(cookie_dict,self.ss.cookies)

    @property
    def proxySet(self):
        """
        获取代理
        :return:
        """
        t1 = time.time()
        try:
            self.proxy_num=0
            self.outputLog(u"更换代理")
            return self.proxy_c.getPorxy
        finally:
            self.outputLog(u'代理更换完成耗时%d秒' % int(time.time()-t1))

    def changeProxy(self):
        """
        更换代理，外部接口调用
        :return:
        """
        self.proxy = self.proxySet

    def insertBlack(self,locktime = 3600*24):
        """
        加入黑名单
        :return:
        """
        self.proxy_c.insertBlack(self.proxy,locktime=locktime)
        self.proxy = self.proxySet

    def proxyCount(self):
        """
        统计代理次数
        :return:
        """
        self.proxy_num+=1



    def mail(self):
        """
        发送邮件，比例大于80%时间
        :return:
        """
        if self.correct_http>=100 and 100*self.error_http/(self.error_http+self.correct_http) > 80:
            spider_name=socket.getfqdn(socket.gethostname())
            code_id=os.getpid()
            title=u"布置在在【%s】上《%s》爬虫进程号为《%s》，HTTP请求错误比例大于百分之八十"%(spider_name,self.pro_name,code_id)
            titles=[u"错误次数",u"错误比例"]
            connt=[[self.error_http,100*self.error_http/(self.error_http+self.correct_http)]]
            sm=SendMail.SendMail()
            cc=sm.getContent(titles,connt)
            sm.sendMail(title,cc)
            self.error_http = 0
            self.correct_http = 0


class DownLoaderException(Exception):
    def __init__(self, **kwargs):
        self.exception = kwargs['exception'] if 'exception' in kwargs else None
        self.res = kwargs['res'] if 'res' in kwargs else None
        self.time_out = kwargs['time_out'] if 'time_out' in kwargs else False


if __name__ == '__main__':

    tt = DownLoader('liaoning')
    tt.firstInit()
    tt.setNotRaise(4223,2324,521,521)
    print tt.status_code_ok
    #url = "http://www.jsgsj.gov.cn:58888/province/"
    #tt.request(url)
    # from requests import get
    # get(url,verify= False)


