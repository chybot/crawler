# -*- coding:utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding("UTF-8")
import re
sys.path.append("../")
from Config.ConfigGet import ConfigGet as C

proxy_cf = 'ConfigProxyServer.ini'
f = lambda y,z:C(proxy_cf).get(y,z)

def networkSegment( name, proxy):
    #获取某个省份的的当前代理的网段或者IP
    lockoutproxysegment = f('networklock', 'lock')
    locknetworksegment = True if name in lockoutproxysegment else False
    if locknetworksegment:
        segment = re.match(ur'(\d+?\.\d+?\.\d+?)\.\d+?\:\d+?', proxy)
        if segment:
            return segment.group(1)
        elif re.search(ur'\w+?\d+?\:42271', proxy):
            return '127.0.0'
    else:
        return proxy.split(":")[0]
    return None