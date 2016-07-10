# -*- coding:utf-8 -*-

import os
import sys
reload(sys)
sys.setdefaultencoding("UTF-8")
import random
import time
import logging
import re
import json
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

if not os.path.exists("./log"):
    os.makedirs("./log")
log = logging.getLogger(__name__)

class ProxyQualityBuyServer(object):
    def __init__(self):
        self.__db = DBManager.getInstance(_type,'buy_proxy_test_results',host = _host,port = _port)

    def get_ip(self):
        while True:
            #每次获取可用代理100个
            self.__db.changeTable('buy_proxy_test_results')
            proxyes = self.__db.getMore(size = 100)
            if not proxyes:
                time.sleep(1)
            else:
                map(lambda x:self.oneIp(x),proxyes)

    def oneIp(self,proxy):
        print proxy
        proxy = json.loads(proxy)
        time_f = proxy.get('time')
        proxy = proxy.get('host')+':'+str(proxy.get('port')) if 'host' in proxy and 'port' in proxy else None
        if proxy and time_f:
            time_flag = time.strftime('%Y%m%d')
            if time_f == -1:

                self.__db.changeTable('%s_timeoutbuyproxy' % time_flag)
                self.__db.zsetSet(proxy)
            else:
                self.__db.changeTable('%s_usebuyproxy' % time_flag)
                self.__db.zsetSet(proxy)
                crawler_list = self.proxy_key()
                map(lambda x:self.into_queue(x,proxy),crawler_list)
                self.__db.put(proxy)

    def proxy_key(self):
        keys = C(proxy_cf).sections()
        if 'db' in keys:
            keys.remove('db')
        if 'networklock' in keys:
            keys.remove('networklock')
        return keys

    def into_queue(self,queue_name,proxy):
        self.__db.changeTable('%s_white_proxy' % queue_name)
        if queue_name!='common'and self.__db.size()>500:
            self.__db.qclaerQueue()
            log.info(u"%s_proxy队列大于500个，删除队列历史数据"%queue_name)
        network_segment = networkSegment(queue_name,proxy)
        if not network_segment:
            return
        #black_set_name = "%s_black_proxy" % queue_name
        #if not self.__db.zexistsSet(black_set_name,network_segment):
        if not self.__db.keyexists(queue_name+'_'+proxy):
            self.__db.changeTable('%s_white_proxy' % queue_name)
            self.__db.put(proxy)
            # if queue_name=='jilin' and proxy.split(":")[1] not in ['8888','8123','8118']:
            #     self.__db.put(proxy)
            # else:
            #     self.__db.put(proxy)
def main():
    proxy_buy=ProxyQualityBuyServer()
    proxy_buy.get_ip()
if __name__ == '__main__':
    main()

