# -*- coding: utf-8 -*-
# Created on 2014/11/20 9:07.

import redis
import socket
import time

import  functions
import  exceputil


class RedisSet(object):
    """Simple Set with Redis Backend"""
    def __init__(self, name, namespace='set',**redis_kwargs):
        """The default connection parameters are: host='localhost', port=6379, db=0"""
        self.__db= redis.Redis(**redis_kwargs)
        self.key = '%s:%s' %(namespace, name)
        if "redis_host" in redis_kwargs:
            self.redis_host=redis_kwargs["redis_host"]
        else:
            self.redis_host="master1"
        if "redis_port" in redis_kwargs:
            self.redis_port=redis_kwargs["redis_host"]
        else:
            self.redis_port=57819
        if "redis_password" in redis_kwargs:
            self.redis_password=redis_kwargs["redis_password"]
        else:
            self.redis_password="bbdredis12344321qaz"
    def get(self):
        """随机移除set中的数据"""
        return self.__db.spop(self.key)

    def size(self):
        """# 判断一个set长度为多少 不存在为0"""
        return self.__db.scard(self.key)

    def empty(self):
        return self.size() == 0

    def add(self, item):
        """塞数据"""
        return self.__db.sadd(self.key, item)


    def have(self, item):
        """判断set中一个对象是否存在"""
        return self.__db.sismember(self.key, item)

    def delete(self, item):
        """删除某个元素"""
        return self.__db.srem(self.key, item)

    def save(self):
        """强制写磁盘"""
        return self.__db.save()

    def clear(self):
        """清空自己"""
        return self.__db.delete(self.key) #删除这个key

def getredisSet(key,redis_host="master1",redis_port=57819,redis_password="bbdredis12344321qaz"):
    if redis_host==None or len(redis_host)<1:
        host_name = socket.getfqdn(socket.gethostname())
        if "win2008r2" in host_name :#在windows自己机器上才使用本地mongodb ip和端口
            host='master'
        else:
            host='localhost'
    else:
        host=redis_host

    return  RedisSet(key, host=host,port=redis_port,password=redis_password)


def getredisSetv2(key,redis_host="master1",redis_port=57819,redis_password="bbdredis12344321qaz",sleep_time=10,retry=9,email_list=functions.mailto_list_ourselves):
    i=0
    count=retry+1
    while True:
        try:
            return getredisSet(key,redis_host=redis_host,redis_port=redis_port,redis_password=redis_password)
        except Exception as e:
            i+=1
            if i>=count:
                #发邮件
                functions.send_mail_old(email_list,u"redis集合连接异常",u"错误信息%s"%exceputil.traceinfo(e))
                time.sleep(3600)
                i=0
            else:
                time.sleep(sleep_time)

import random
if __name__ == "__main__":

    setQueue = getredisSetv2("zhejiang:valid_company_key")
    #setQueue.clear()
    print setQueue.size()
    for i in range(1000000):
        print time.time()
        ss = "中国123" + str(time.time()) + str(random.randint(1,1000000)) * 1000000
        #print ss
        print setQueue.add(ss);
        print time.time()
    print setQueue.size();
