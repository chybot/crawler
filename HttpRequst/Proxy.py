# -*- coding: utf-8 -*-
"""
企业信息网代理模块
"""
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import time
from requests import get
import re
sys.path.append('../')
from Config.ConfigGet import ConfigGet
from CommonLib.DB.DBManager import DBManager


f = lambda x,y,z:ConfigGet(x).get(y,z)

cfpath = 'ConfigProxy.ini'

class Proxy(object):
    def __init__(self,pro_name):
        self.pro_name=pro_name
        self.proxyInit()
        host = f(cfpath,'db','host')
        port = f(cfpath,'db','port')
        self.__db= DBManager.getInstance('ssdb','%s_black_proxy' % self.pro_name,host = host,port = int(port))
        self.proxy = None

    def proxyInit(self):
        """
        代理统计初始化
        :return:
        """
        self.proxy_num=0

    @property
    def getPorxy(self):
        debug = ConfigGet('Config.ini').get('setting','debug').lower()
        if debug == 'true':
            return None
        else:
            self.proxy = self.httpProxyApi
            return self.proxy
    @property
    def httpProxyApi(self):
        try:
            return get('http://spider7:42273/qyxx?area=%s&last=%s'%(self.pro_name,self.proxy)).text.strip()
        except Exception as e:
            print u'%s获取代理错误' % self.pro_name,'\n',e

    def insertBlack(self,proxy,locktime = 3600*24):
        '''
        被封锁IP插入黑名单
        :param proxy:
        :param locktime:
        :return:
        '''
        proxy = self.networkSegment(self.pro_name,proxy)
        if proxy:
            self.__db.zsetSet(proxy,score = locktime+int(time.time()))

    def networkSegment(self, name, proxy):
        '''
        获取IP的网段或IP
        :param name:
        :param proxy:
        :return:
        '''
        networklock = f('ConfigProxyServer.ini', 'networklock', 'lock')
        locknetworksegment = True if name in networklock else False
        if locknetworksegment:
            segment = re.match(ur'(\d+?\.\d+?\.\d+?)\.\d+?\:\d+?', proxy)
            if segment:
                return segment.group(1)
            elif re.search(ur'\w+?\d+?\:42271', proxy):
                return '127.0.0'
        else:
            return proxy.split(":")[0]
        return None

    def firstPorxy(self,proxy_num):
        """
        连续访问：自建和非自建代理连续访问
        非连续访问：非自建代理连续访问
        :return:
        """
        if self.proxy:
            if not ConfigGet(cfpath).has_option('series_num',self.pro_name):
                if str(self.proxy.split(":")[-1]) in  ["42271","42272"]:
                    proxy_num = 0
                    self.proxy = self.getPorxy
                elif self.proxy_num >= 50:
                    proxy_num = 0
                    self.proxy = self.getPorxy
                else:
                    proxy_num += 1
            elif self.pro_name >= int(f(cfpath,'series_num',self.pro_name)):
                proxy_num = 0
                self.proxy = self.getPorxy
            else:
                self.proxy_num += 1
        else:
            proxy_num = 0
            self.proxy = self.getPorxy
        return proxy_num,self.proxy


if __name__ == '__main__':
    c= Proxy('anhui')
    c.networkSegment('anshui','127.0.0.1')