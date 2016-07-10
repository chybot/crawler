#-*- coding:utf-8 -*-
__author__ = 'liang'
import time
import sys
reload(sys)
sys.setdefaultencoding("UTF-8")
sys.path.append('../')
print sys.path
from ssdb import SSDB
import socket
try:
    from common import exceputil
except Exception as e:
    import exceputil
try:
    from common import functions
except Exception as e:
    import functions
from ssdb.connection import Connection, ConnectionPool,BlockingConnectionPool
import time
import pickle

class SSDBBase():
    def __init__(self, ssdb):
        self.ssdb = ssdb

    def dbsize(self):
        pass #return self.ssdb.dbsize()

    def info(self):
        pass #return self.ssdb.info()

class SSDBQueue(object):
    def __init__(self, queue_name, host, port, max_connections = 10, timeout = 60):
        self.queue_name = queue_name
        self.host = host
        self.port = port
        self.max_connections = max_connections
        self.timeout = timeout
        pool = BlockingConnectionPool(connection_class = Connection, max_connections= max_connections, timeout = timeout, host = host, port = port)
        self.ssdb = SSDB(connection_pool=pool)

    def queue_size(self):
        return self.ssdb.qsize(self.queue_name)

    def clear_queue(self):
        return self.ssdb.qclear(self.queue_name)

    def empty(self):
        return self.ssdb.qsize(self.queue_name) == 0

    def put_data(self,data):
        return self.ssdb.qpush_back(self.queue_name, data)

    def get_data(self):
        return self.ssdb.qpop_front(self.queue_name)

    def put(self, data, sleep_time=10,retry=9,email_list=functions.mailto_list_ourselves):
        i = 0
        count = retry + 1
        ssdb_queue = None
        while True:
            try:
                if data != None and ssdb_queue != None:
                    if isinstance(data, dict):
                        return ssdb_queue.put_data(pickle.dumps(data))
                else:
                    if isinstance(data,dict):
                        return self.put_data(pickle.dumps(data))
            except Exception as e:
                print u'插入队列异常 %s' % exceputil.traceinfo(e)
                i += 1
                if i >= count:
                    #发邮件
                    functions.send_mail_old(email_list,u"ssdb队列更新异常",u"错误信息%s \nqueue_name:%s"%(exceputil.traceinfo(e),self.queue_name))
                    time.sleep(600)
                    i=0
                else:
                    time.sleep(sleep_time)
                ssdb_queue = getSSDBQueuev2(self.queue_name, self.host, self.port, self.max_connections, self.timeout)

    def get(self,sleep_time=10,retry=9,email_list=functions.mailto_list_ourselves):
        i = 0
        count = retry + 1
        ssdb_queue = None
        while True:
            try:
                if ssdb_queue != None:
                    return ssdb_queue.get_data()
                else:
                    return self.get_data()
            except Exception as e:
                print u'查询数据异常 %s' % exceputil.traceinfo(e)
                i += 1
                if i >= count:
                    #发邮件
                    functions.send_mail_old(email_list,u"ssdb队列更新异常",u"错误信息%s"%exceputil.traceinfo(e))
                    time.sleep(600)
                    i=0
                else:
                    time.sleep(sleep_time)
                ssdb_queue = getSSDBQueuev2(self.queue_name, self.host, self.port, self.max_connections, self.timeout)

    def size(self,sleep_time=10,retry=9,email_list=functions.mailto_list_ourselves):
        i = 0
        count = retry + 1
        ssdb_queue = None
        while True:
            try:
                if ssdb_queue != None:
                    return ssdb_queue.queue_size()
                else:
                    return self.queue_size()
            except Exception as e:
                print u'查询队列中数异常 %s' % exceputil.traceinfo(e)
                i += 1
                if i >= count:
                    #发邮件
                    functions.send_mail_old(email_list,u"ssdb队列更新异常",u"错误信息%s"%exceputil.traceinfo(e))
                    time.sleep(600)
                    i=0
                else:
                    time.sleep(sleep_time)
                ssdb_queue = getSSDBQueuev2(self.queue_name, self.host, self.port, self.max_connections, self.timeout)

    def clear(self,sleep_time=10,retry=9,email_list=functions.mailto_list_ourselves):
        i = 0
        count = retry + 1
        ssdb_queue = None
        while True:
            try:
                if ssdb_queue != None:
                    return ssdb_queue.clear_queue()
                else:
                    return self.clear_queue()
            except Exception as e:
                print u'查询队列中数异常 %s' % exceputil.traceinfo(e)
                i += 1
                if i >= count:
                    #发邮件
                    functions.send_mail_old(email_list,u"ssdb队列更新异常",u"错误信息%s"%exceputil.traceinfo(e))
                    time.sleep(600)
                    i=0
                else:
                    time.sleep(sleep_time)
                ssdb_queue = getSSDBQueuev2(self.queue_name, self.host, self.port, self.max_connections, self.timeout)

def getSSDBQueue(queue_name, host, port, max_connections = 1, timeout = 30):
    return SSDBQueue(queue_name, host, port, max_connections, timeout)

def getSSDBQueuev2(queue_name, host = '127.0.0.1', port = 8888, max_connections = 1, timeout = 30, retry = 9, sleep_time = 30, email_list=functions.mailto_list_ourselves):
    i = 0
    count = retry + 1
    while True:
        try:
            return getSSDBQueue(queue_name,host = host, port = port, max_connections = max_connections, timeout = timeout)
        except Exception as e:
            print exceputil.traceinfo(e)
            i+=1
            if i>count:
                #发邮件
                functions.send_mail_old(email_list,u"redis队列连接异常",u"错误信息%s"%exceputil.traceinfo(e))
                time.sleep(600)
                i=0
            else:
                time.sleep(sleep_time)

class SSDBKV(object):
    def __init__(self, host = "127.0.0.1", port = 8888, max_connections = 10, timeout = 60):
        self.host = host
        self.port = port
        self.max_connections = max_connections
        self.timeout = timeout
        pool = BlockingConnectionPool(connection_class = Connection, max_connections= max_connections, timeout = timeout, host = host, port = port)
        self.ssdb = SSDB(connection_pool=pool)

    def set(self, key, value):
        return self.ssdb.set(key, value)

    def get(self, key):
        return self.ssdb.get(key)

    def delete(self, key):
        return self.ssdb.delete(key)

    def keys(self, name_start = 0, name_end = 0xFFFFFFFF, limit=10):
        return self.ssdb.keys(name_start, name_end, limit)

    def exists(self, key):
        return self.ssdb.exists(key)

class SSDBHashMap(object, SSDBBase):
    def __init__(self, hashmap_name, host = "127.0.0.1", port = 8888, max_connections = 10, timeout = 60):
        self.hashmap_name = hashmap_name
        self.host = host
        self.port = port
        self.max_connections = max_connections
        self.timeout = timeout
        pool = BlockingConnectionPool(connection_class = Connection, max_connections= max_connections, timeout = timeout, host = host, port = port)
        self.ssdb = SSDB(connection_pool=pool)
        SSDBBase.__init__(self, self.ssdb)

    def set(self, key, value):
        return self.ssdb.hset(self.hashmap_name, key, value)

    def get(self, key):
        return self.ssdb.hget(self.hashmap_name, key)

    def delete(self, key):
        return self.ssdb.hdel(self.hashmap_name, key)

    def keys(self, name_start = "", name_end = "", limit=10):
        return self.ssdb.hkeys(self.hashmap_name, name_start, name_end, limit)

    def exists(self, key):
        return self.ssdb.hexists(self.hashmap_name, key)

    def size(self):
        return self.ssdb.hsize(self.hashmap_name)

    def list(self, name_start = "", name_end = "", limit=10):
        #列出名字处于区间 (name_start, name_end] 的 hashmap
        return self.ssdb.hlist(name_start, name_end, limit)

    def scan(self, key_start, key_end = "", limit = 10):
        return self.ssdb.hscan(self.hashmap_name, key_start, key_end, limit)

    def clear(self):
        return self.ssdb.hclear(self.hashmap_name)

class SSDBZset(object, SSDBBase):
    def __init__(self, zset_name, host = "127.0.0.1", port = 8888, max_connections = 10, timeout = 60):
        self.zset_name = zset_name
        self.host = host
        self.port = port
        self.max_connections = max_connections
        self.timeout = timeout
        pool = BlockingConnectionPool(connection_class = Connection, max_connections= max_connections, timeout = timeout, host = host, port = port)
        self.ssdb = SSDB(connection_pool=pool)
        SSDBBase.__init__(self, self.ssdb)

    def set(self, key, value, score):
        return self.ssdb.zset(self.zset_name, key, score)

    def get(self, key):
        return self.ssdb.zget(self.zset_name, key)

    def delete(self, key):
        return self.ssdb.zdel(self.zset_name, key)

    def keys(self, key_start = "", score_start = "", score_end = "", limit=10):
        return self.ssdb.zkeys(self.zset_name, key_start, score_start, score_end, limit)

    def exists(self, key):
        return self.ssdb.zexists(self.zset_name, key)

    def size(self):
        return self.ssdb.zsize(self.zset_name)

    def list(self, name_start = "", name_end = "", limit=10):
        #列出名字处于区间 (name_start, name_end] 的 hashmap
        return self.ssdb.zlist(name_start, name_end, limit)

    def clear(self):
        return self.ssdb.zclear(self.zset_name)

if __name__ == '__main__':

    """
    ssd = getSSDBQueuev2('queue_1','127.0.0.1',8888, 10, 30)
    data = {'_id':'成都数联铭品科技有限公司|_|2015_04_24'}
    ssd.put(data)
    #print str(ssd.get())"""

    """
    kvdb = SSDBKV()
    print kvdb.get("123ab")
    print kvdb.set("123ab", "成都数联铭品科技有限公司|_|2015_04_24")
    print kvdb.set("123ab1", 123)
    print kvdb.get("123ab")
    print kvdb.get("123ab1")
    print kvdb.exists("123ab")
    print kvdb.keys()
    print kvdb.delete("123ab")
    print kvdb.delete("123ab1")"""

    hashmapdb = SSDBHashMap(hashmap_name = "test")
    print hashmapdb.get("bb")
    print hashmapdb.set("bb", "成都数联铭品科技有限公司|_|2015_04_24")

    "test_data.txt"
    """import random
    for i in range(100):
        print hashmapdb.set("%s"%random.random(), "%d"%random.random())"""

    """for fileline in open("ag1512.csv"):
        print hashmapdb.set(fileline.split(",")[1], fileline.strip("\r\n "))"""



    #print hashmapdb.set("bb", 123)
    print hashmapdb.get("bb")
    print hashmapdb.exists("bb")
    print hashmapdb.size()
    print hashmapdb.list()
    print hashmapdb.keys()
    #print hashmapdb.delete("bb")
    #print hashmapdb.clear()
    for kv in hashmapdb.scan("a", limit=4):
        print kv, hashmapdb.get(kv)
    """
    print hashmapdb.clear()

    zsetdb = SSDBZset(zset_name = "test")
    print zsetdb.get("bb")
    print zsetdb.set("bb", "成都数联铭品科技有限公司|_|2015_04_24", 1)
    print zsetdb.set("bb", "bbbbb|_|2015_04_24", 3)
    print zsetdb.set("bbc", "bbbbb|_|2015_04_24", -1)
    #print hashmapdb.set("bb", 123)
    print zsetdb.get("bb")
    print zsetdb.exists("bb")
    print zsetdb.size()
    print zsetdb.list()
    print zsetdb.keys()
    print zsetdb.delete("bb")
    print zsetdb.clear()"""
