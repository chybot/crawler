# -*- coding:utf-8 -*-

import os
import sys
reload(sys)
sys.setdefaultencoding("UTF-8")
import random
import time
from requests import get
import logging
import re

sys.path.append("../../")
from CommonLib.DB.DBManager import DBManager
from Config.ConfigGet import ConfigGet as C

proxy_cf = 'ConfigProxyServer.ini'
f = lambda y,z:C(proxy_cf).get(y,z)

_type = f('db','type')
_host = f('db','host')
_port = f('db','port')


if not os.path.exists("./log"):
    os.makedirs("./log")
log = logging.getLogger(__name__)

def get_proxy_file(file_path):
    f=open(file_path,"r")
    return  [line.strip().decode('utf-8') for line in f.readlines()]
proxy_bbd=get_proxy_file('./proxy_bbd')
proxy_bbd =  random.sample(proxy_bbd, 10)

class ProxyQualityBuyServer(object):
    def __init__(self):
        self.__db = DBManager.getInstance(_type,'buy_tba_proxy_white_proxy',host = _host,port = _port)

    def get_ip(self):
        while True:
            print u"开始导入代理到相应的队列，time:%s"%time.strftime("%Y:%m:%d %H:%M:%S")
            log.info(u"开始导入代理到相应的队列，time:%s"%time.strftime("%Y:%m:%d %H:%M:%S"))
            urls={#u"代理666":u"http://kk.daili666.com/ip/?tid=558627580141255&num=50&operator=1",
                  u"proxy666":u"http://kk.daili666.com/ip/?tid=558627580141255&num=50",
                #http://www.kuaidaili.com/api/getproxy/?orderid=961829288597124&num=50&area=&area_ex=&port=&port_ex=&ipstart=&carrier=0&an_ha=1&sp1=1&sp2=1&protocol=1&method=1&quality=2&sort=0&b_pcchrome=1&b_pcie=1&b_pcff=1&showtype=1
                  u"kuaiproxy":u"http://www.kuaidaili.com/api/getproxy/?orderid=961829288597124&num=50&carrier=0&an_ha=1&an_an=1&protocol=1&method=2&quality=2&sort=2&b_pcchrome=1&b_pcie=1&b_pcff=1&showtype=1",
                  #u"TK代理":u"http://www.tkdaili.com/api/getiplist.aspx?vkey=6DB9E6C9F412CF310B745A7916181A9B&num=50&password=bbd1234&country=CN&speed=100&high=1&style=6&high=1",
                  u"tkproxy":u"http://www.tkdaili.com/api/getiplist.aspx?vkey=6DB9E6C9F412CF310B745A7916181A9B&num=50&password=bbd1234&country=CN&speed=600&high=1&style=6"
                  }
            for k,v in urls.items():
                print k,v
                proxys=""
                try:
                    proxy=random.choice(proxy_bbd)
                    proxies = {'http':'http://'+proxy, 'https':'http://'+proxy}
                    proxys=get(v,timeout=60,proxies=proxies).text

                except Exception as e:
                    print e
                    logging.error(e)
                    time.sleep(2)
                for proxy in proxys.split():
                    if re.search('\d+?\.\d+?\.\d+?\.\d+?\:\d+?',proxy):
                        try:
                            #此处在ssdb里面维护两个集合，一个是timeout的集合，一个可以网络访问的集合
                            time_flag = time.strftime('%Y%m%d')
                            timeout_flag = self.__db.zexistsSet('%s_timeoutbuyproxy'%time_flag,proxy)
                            use_flag = self.__db.zexistsSet('%s_usebuyproxy'%time_flag,proxy)
                            if timeout_flag or use_flag:
                                continue
                            _dict = {'proxy':proxy,'source':k}
                            self.__db.put(_dict)
                        except Exception as e:
                            print e
            print u"等待5秒"
            logging.info(u"等待5秒")
            time.sleep(5)
def main():
    proxy_buy=ProxyQualityBuyServer()
    proxy_buy.get_ip()
if __name__ == '__main__':
    main()

