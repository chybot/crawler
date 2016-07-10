# -*- coding: utf-8 -*-
"""
代理白名单获取
"""
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import re
import logging
import time
import platform
import json
import warnings
from requests import get
if "Windows" not in platform.system():
    print "Linux System! Use epoll"
    from twisted.internet import epollreactor
    epollreactor.install()
from twisted.internet import reactor
from twisted.internet.threads import deferToThread
import functools
reactor.suggestThreadPoolSize(20000000)



sys.path.append("../../")
from CommonLib.DB.DBManager import DBManager
from Config.ConfigGet import ConfigGet as C
from ProxyServer.util.functiontool import networkSegment
proxy_cf = 'ConfigProxyServer.ini'
f = lambda y,z:C(proxy_cf).get(y,z)

_type = f('db','type')
_host = f('db','host')
_port = f('db','port')
lockoutproxysegment = f('networklock','lock')

log = logging.getLogger(__name__)

class ProxyWhiteGetServer(object):
    """
    从一系列自建代理中过滤黑名单，灰名单
    并验证当前的时间和次数是否合法
    名词解释：
        黑名单：被封的IP的集合
        灰名单：当前正在使用的IP的KV
        白名单：当前能使用的IP队列
    """
    def __init__(self):
        self.__proxydb = DBManager.getInstance(_type,'proxy',host = _host,port = _port)
        self.bbd_proxy={}
        self.readProxy('./proxy_bbd')
        self.readProxy(('./proxy_42272'))

    def timeCompare(self,kv):
        """
        对代理的超时时间进行判断处理
        :param k:
        :param v:
        :return:
        """
        k,v = kv
        if v == -1 :
            return
        if int(v) - int(time.time()) <= 180:
            del self.bbd_proxy[k]

    def proxyGetIps(self):
        """
        获取运维提供的api代理接口
        :return:
        """
        while True:
            map(lambda kv:self.timeCompare(kv),self.bbd_proxy.items())
            try:
                url = 'http://192.168.2.238:8080/bbd/spider/api/ips'
                proxy_json = get(url).text
                proxy_json = json.loads(proxy_json)
                print 'Get proxy Api.'
                for proxies in proxy_json:
                    proxy_list = proxies.get('eips')
                    timestamp = proxies.get('expireL1Timestamp')
                    if proxy_list == None or timestamp == None:
                        warnings.warn('Get bbd proxy api keys error.')
                        continue
                    timestamp = int(timestamp)
                    map(lambda x:self.bbd_proxy.update({x+':42272':timestamp}),proxy_list)
                break
            except Exception as e:
                warnings.warn(str(e))
                time.sleep(1)

    def readProxy(self,file_path):
        with open(file_path,'r') as f:
            map(lambda x:self.bbd_proxy.update({x.strip():-1}),f.readlines())


    def proxy_key(self):
        keys = C(proxy_cf).sections()
        if 'db' in keys:
            keys.remove('db')
        if 'networklock' in keys:
            keys.remove('networklock')
        return keys
    def run(self):
        print 'begin running'
        keies = self.proxy_key()
        #self.proxyGetIps()
        #TODO
        #因为当前运维端口没有提供IP，所以目前关闭这个端口
        for name in keies:
            self.__proxydb.changeTable('%s_bbd_white_proxy' % name)
            if self.__proxydb.size()==0:
                for proxy in self.bbd_proxy:
                    f = functools.partial(self.run1,name,proxy)
                    deferToThread(f).addBoth(lambda x:x)
                time.sleep(2)
        reactor.callLater(60, self.run)

    def run1(self,name,proxy):
        print name+':'+proxy
        if self.proxyFilter(name,proxy):
            self.__proxydb.changeTable('%s_bbd_white_proxy' % name)
            self.__proxydb.put(proxy)

    def proxyFilter(self,name,proxy):
        proxy_black_flag_key = networkSegment(name,proxy)
        if not proxy_black_flag_key:
            #获取的网段或者IP是否合法
            return False
        # key = "%s_black_proxy" % name
        # if self.__proxydb.zexistsSet(key,proxy_black_flag_key):
        #     #是否存在于黑名单
        #     return False
        #现在不存在单独的黑名单，黑名单由之前的set改为现在的kv,故只有当前一个判断
        if self.__proxydb.keyexists(name+'_'+proxy_black_flag_key):
            #是否存在于灰名单
            return False
        if not self.proxyValid(name,proxy_black_flag_key):
            #最大次数和间隔是否合法
            return False
        return True



    def proxyValid(self,name,proxy):
        '''
        最大间隔时间判断
        :param name:
        :param proxy:
        :return:
        '''
        key = name + '_' + proxy
        info = self.__proxydb.hgetallHash(key)
        if not info:
            return True
        uptime = int(float(info.get("uptime", 0)))
        now_num = int(info.get("now_num", 0))
        config = self.proxy_pro_value(name)
        if int(float(time.time())) - int(uptime) > int(config[1]) and now_num < int(config[0]):
            return True
        return False

    def proxy_pro_value(self,name):
        num = f(name,'maxnum')
        intervals = f(name,'intervals')
        num = 1000 if num == None else num
        intervals = 120 if intervals == None else intervals
        return num,intervals

    def start(self):
        self.run()
        reactor.run()

if __name__ == '__main__':
    proxy = ProxyWhiteGetServer()
    proxy.start()
    # proxy.proxyGetIps()
    # print proxy.bbd_proxy




