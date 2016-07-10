# -*- coding:utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import platform
if "Windows" not in platform.system():
    print "Linux System! Use epoll"
    from twisted.internet import epollreactor
    epollreactor.install()
from twisted.internet import reactor ,ssl,threads,defer
from twisted.web.resource import Resource
from twisted.web.server import Site
from twisted.python import log
import time,os
if not os.path.exists('log'):
    os.makedirs('log')
log.startLogging(open('log/proxyserver_%s'% time.strftime('%Y_%m_%d'),'a'))
from twisted.internet.threads import deferToThread
reactor.suggestThreadPoolSize(200000)
import socket
socket.setdefaulttimeout(80)

from twisted.web.server import NOT_DONE_YET

import json
import random
import re

from requests import get

sys.path.append('../')
from CommonLib.DB.DBManager import DBManager
from Config.ConfigGet import ConfigGet as C
from ProxyServer.util.functiontool import networkSegment
proxy_cf = 'ConfigProxyServer.ini'
f = lambda y,z:C(proxy_cf).get(y,z)
_type = f('db','type')
_host = f('db','host')
_port = f('db','port')

class NotFount(Resource):
    def getChild(self,name,request):
        return self
    def render_GET(self,request):
        return ResponseTpl().not_fount()

class ResponseTpl():

    def __init__(self,params={}):
        self._response_data = {"code":0,"msg":"ok","params":params,"rdata":[],"total":0}

    def loadrdata(self,rdata=[]):
        self._response_data["rdata"] = rdata
        self._response_data["total"] = len(self._response_data["rdata"])
        return json.dumps(self._response_data)
    def not_fount(self):
        self._response_data["code"] = -1
        self._response_data["msg"] = "Not Fount Resource."
        return json.dumps(self._response_data)
    def verify_failed(self):
        self._response_data["code"] = -2
        self._response_data["msg"] = "Host Ip Not In ProxyDB."
        return json.dumps(self._response_data)
    def verify_success(self):
        self._response_data["code"] = 1
        self._response_data["msg"] = "Verify OK."
        return json.dumps(self._response_data)

import threading
class th(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self._proxy=[]
    def run(self):
        self.get_proxys()
        threading.Timer(400, self.run).start()
    def get_proxys(self):
        urls={#u"代理666":u"http://kk.daili666.com/ip/?tid=558627580141255&num=50&operator=1",
                  u"代理666":u"http://kk.daili666.com/ip/?tid=558627580141255&num=1000",
                  u"快代理":u"http://www.kuaidaili.com/api/getproxy/?orderid=961829288597124&num=1000&area=&area_ex=&port=&port_ex=&ipstart=&carrier=0&an_ha=1&sp1=1&sp2=1&protocol=1&method=1&quality=2&sort=0&b_pcchrome=1&b_pcie=1&b_pcff=1&dedup=1&showtype=1",
                  #u"TK代理":u"http://www.tkdaili.com/api/getiplist.aspx?vkey=6DB9E6C9F412CF310B745A7916181A9B&num=50&password=bbd1234&country=CN&speed=100&high=1&style=6&high=1",
                  u"TK代理":u"http://www.tkdaili.com/api/getiplist.aspx?vkey=6DB9E6C9F412CF310B745A7916181A9B&num=100&password=bbd1234&country=CN&speed=100&high=1&style=6&high=1"
                  }
        pp=[]
        for k,v in urls.items():
            try:
                proxys=get(v,timeout=60).text
                pp.extend(proxys.split())
            except Exception as e:
                log.err(e)
        self._proxy=[]
        for proxy in pp:
            if len(proxy.split(":"))==2 and re.search("\d+?",proxy.split(":")[1]):
                if proxy not in self._proxy:
                    self._proxy.append(proxy)
    def get_proxy(self):
        #p_threadLock.acquire()
        if self._proxy:
            return random.choice(self._proxy)
        else:
            return None
        #p_threadLock.release()
class QYXX(Resource):
    __db = DBManager.getInstance(_type,'name',host = _host,port = _port)
    threading_proxy = th()
    threading_proxy.start()
    def getChild(self, path, request):
        if path=="":
            return self
        else:
            return NotFount()
        return Resource.getChild(path,request)

    def _render_write(self,request,res):
        request.write(str(res))
        request.finish()

    def getip(self,request):
        #url:http://spider7:9876/qyxx?area=jiangsu&last=127.0.0.1:8080
        #url:http://127.0.0.1:9876/qyxx?area=jiangsu&last=127.0.0.1:8080
        argss = request.args
        area = argss["area"][0] if "area" in argss else "common"
        last = argss["last"][0] if "area" in argss else None
        last = networkSegment(area, last)

        def _get_proxy():
            if last:
                self.__db.keyDel(area + '_' + last)
            self.__db.changeTable('%s_bbd_white_proxy' % area)
            bbd_proxy = self.__db.get()
            if bbd_proxy:
                name = area + '_' + networkSegment(area, bbd_proxy)
                self.__db.keySetx(name,300,ttl=300)
                self.__db.hincrHash(name,'now_num')
                self.__db.multi_hsetHash(name,uptime = int(float(time.time())))
                return bbd_proxy
            self.__db.changeTable('%s_white_proxy' % area)
            buy_proxy =  self.__db.get()
            if buy_proxy:
                return buy_proxy
            return self.threading_proxy.get_proxy()

        deferToThread(_get_proxy).addCallback(lambda x:self._render_write(request,x))

    def render_GET(self,request):
        self.getip(request)
        return NOT_DONE_YET

class ServerHandle(Resource):
    def getChild(self, path, request):
        if path=="qyxx":
            return QYXX()
        else:
            return NotFount()
    def render_GET(self, request):
        return "<h1>Welcome server!<h1>"

if __name__ == '__main__':
    root = ServerHandle()
    factory = Site(root,timeout=60)
    HTTPPORT=42273
    reactor.listenTCP(HTTPPORT,factory)
    reactor.run()