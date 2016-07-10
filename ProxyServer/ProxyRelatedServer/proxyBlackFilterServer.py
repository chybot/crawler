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
log.startLogging(open('log/blackfilter_%s'% time.strftime('%Y_%m_%d'),'a'))
from twisted.internet.threads import deferToThread
reactor.suggestThreadPoolSize(200000)
import socket
socket.setdefaulttimeout(80)
import json
from twisted.web.server import NOT_DONE_YET

all_proxy = set()
black_proxy = set()
import threading

def func():
    all_proxy.clear()
    black_proxy.clear()
    threading.Timer(3600*24, func).start()
func()

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


class BlackFilter(Resource):
    def getChild(self, path, request):
        if path=="":
            return self
        else:
            return NotFount()
        return Resource.getChild(path,request)

    def _render_write(self,request,res):
        request.write(str(res))
        request.finish()

    def filterblack(self,request):
        #url:http://spider7:3785/blackfilter?proxy=127.0.0.1:8080
        argss = request.args
        proxy = argss["proxy"][0] if "proxy" in argss else None
        types = argss["type"][0] if "type" in argss else 'all'

        def filterb():
            if types == 'all':
                if proxy in all_proxy:
                    return 1
                else:
                    return 0
            elif types == 'black':
                if proxy in black_proxy:
                    return 1
                else:
                    return 0
            else:
                return 0

        deferToThread(filterb).addCallback(lambda x:self._render_write(request,x))

    def render_GET(self,request):
        self.filterblack(request)
        return NOT_DONE_YET

class BlackPut(Resource):
    def getChild(self, path, request):
        if path == "":
            return self
        else:
            return NotFount()
        return Resource.getChild(path, request)

    def _render_write(self, request, res):
        request.write(str(res))
        request.finish()

    def blackput(self,request):
        # url:http://spider7:3785/putblack?proxy=127.0.0.1:8080&type=black
        # url:http://127.0.0.1:3785/putblack?proxy=127.0.0.1:8080
        argss = request.args
        proxy = argss["proxy"][0] if "proxy" in argss else None
        types = argss["type"][0] if "type" in argss else 'all'
        def blackp():
            if types == 'all':
                all_proxy.add(proxy)
            elif types == 'black':
                black_proxy.add(proxy)
            else:
                pass
            return 1

        deferToThread(blackp).addCallback(lambda x: self._render_write(request, x))

    def render_GET(self, request):
        self.blackput(request)
        return NOT_DONE_YET
class ServerHandle(Resource):
    def getChild(self, path, request):
        if path == "blackfilter":
            return BlackFilter()
        elif path == 'putblack':
            return BlackPut()
        else:
            return NotFount()
    def render_GET(self, request):
        return "<h1>Welcome server!<h1>"

if __name__ == '__main__':
    root = ServerHandle()
    factory = Site(root,timeout=60)
    HTTPPORT=3785
    reactor.listenTCP(HTTPPORT,factory)
    reactor.run()