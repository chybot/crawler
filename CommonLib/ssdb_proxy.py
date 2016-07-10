# -*- coding: utf-8 -*-
# ---------------------------------------
#   程序：ssdb_proxy.py
#   版本：0.1
#   作者：diven
#   日期：2015-10-19
#   语言：Python 2.7
#
#   版本列表：
#   0.1：实现对SSDB的基本操作
# ---------------------------------------

import sys
reload(sys)
sys.setdefaultencoding("UTF-8")
sys.path.append('../')

from ssdb import SSDB
from ssdb.connection import Connection, BlockingConnectionPool

class ssdb_proxy(object):

    def __init__(self, set_name, host, port, max_connections=2, timeout=60):
        """数据库初始化"""
        self.set_name = set_name
        self.host = host
        self.port = port
        self.max_connections = max_connections
        self.timeout = timeout
        pool = BlockingConnectionPool(connection_class=Connection, max_connections=max_connections, timeout=timeout, host=host, port=port)
        self.ssdb = SSDB(connection_pool=pool)
        pass

    def hset(self, key, value):
        """添加集合"""
        return self.ssdb.hset(self.set_name, key, value)

    def hget(self, key):
        """获取key所对应的值"""
        return self.ssdb.hget(self.set_name, key)

    def hgetall(self):
        """获取所有的数据"""
        return self.ssdb.hgetall(self.set_name)

    def hdel(self, key):
        """删除数据"""
        return self.ssdb.hdel(self.set_name, key)

    def hexists(self, key):
        """判断Key是否存在"""
        return self.ssdb.hexists(self.set_name, key)

    def size(self):
        """获取结合的大小"""
        return self.ssdb.hsize(self.set_name)

    def clean(self):
        """清楚所有数据"""
        return self.ssdb.hclear(self.set_name)


if __name__ == '__main__':
    proxy = ssdb_proxy(u"%s_%s" % (u"proxy", u"qyxx_sichuan"), u"spider8", 58433, 1, 300)
    print proxy.size()