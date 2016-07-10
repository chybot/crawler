# -*- coding: utf-8 -*-
"""
代理黑名单清理
"""
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import logging
import time

from gevent import monkey
monkey.patch_all()
import gevent
from gevent import Greenlet

from apscheduler.schedulers.background import BlockingScheduler

# from twisted.internet import reactor
# # from twisted.python import log
# from twisted.internet.threads import deferToThread
# sys.setrecursionlimit(1000000)
#
# reactor.suggestThreadPoolSize(50000)
# import functools

sys.path.append("../../")
from CommonLib.DB.DBManager import DBManager
from Config.ConfigGet import ConfigGet as C

proxy_cf = 'ConfigProxyServer.ini'
f = lambda y,z:C(proxy_cf).get(y,z)

_type = f('db','type')
_host = f('db','host')
_port = f('db','port')

log = logging.getLogger(__name__)

class ProxyBlackCleanServer(object):
    def __init__(self):
        self.__proxydb = DBManager.getInstance(_type, 'name', host=_host, port=_port)
        self.appends=[]
    def run(self,name):
        self.__proxydb.changeTable("%s_black_proxy" % name)
        keys = self.__proxydb.zkeysSet()
        for key in keys:
            # f = functools.wraps(self.run1,name,key)
            # deferToThread(f).callback(lambda x:x)
            self.appends.append(Greenlet.spawn(self.run1,name,key))
    def run1(self,name,key):
        self.__proxydb.changeTable("%s_black_proxy" % name)
        value = self.__proxydb.zgetSet(key)
        if value:
            if  int(time.time()) >= int(value):
                self.__proxydb.zdelSet(key)
        else:
            self.__proxydb.zdelSet(key)
    def proxy_key(self):
        keys = C(proxy_cf).sections()
        if 'db' in keys:
            keys.remove('db')
        if 'networklock' in keys:
            keys.remove('networklock')
        return keys

    def start(self):
        crawler_list = self.proxy_key()
        for key in crawler_list:
            print u"Clean %s"% key
            log.info(u"Clean %s"% key)
            self.run(key)
    def starts(self):
        #self.start()
        #reactor.callWhenRunning(self.start)
        # reactor.run()
        self.start()
        gevent.joinall(self.appends)

def main():
    blackclean = ProxyBlackCleanServer()
    blackclean.starts()

if __name__ == '__main__':
    #main()
    scheduler = BlockingScheduler()
    scheduler.add_job(main(),'cron',second='0', minute='0',hour='1,14')
    scheduler.start()