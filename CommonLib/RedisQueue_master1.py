# -*- coding: utf-8 -*-
# Created on 2014/9/25 21:11.

import redis
import socket
import time

import exceputil
import functions

class RedisQueue(object):
    """Simple Queue with Redis Backend"""
    def __init__(self, name, namespace='queue', **redis_kwargs):
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


    def size(self):
        """Return the approximate size of the queue."""
        return self.__db.llen(self.key)

    def empty(self):
        """Return True if the queue is empty, False otherwise."""
        return self.size() == 0
    def all_keys(self):
        return self.__db.keys()
    def put(self, item):
        """Put item into the queue."""
        return self.__db.rpush(self.key, item)

    def insert(self,item):
        return self.__db.lpush(self.key,item)

    def putv2(self, item,key="",sleep_time=10,retry=9,email_list=functions.mailto_list_ourselves):
        """
        Put item into the queue.if ,retry if error ,send mail if retry Multiple retries
        :param item: （str)内容
        :param sleep_time: (int) 休眠时间
        :param retry:(int) 重试次数
        :param email_list: (list)  电子邮件列表
        :return: (None)
        """
        redis_queue=None
        i=0
        count=retry+1
        while True:
            try:
                if redis_queue!=None:
                    return redis_queue.put(item)
                else:
                    return self.put(item)
            except Exception as e:
                i+=1
                if i>=count:
                    #发邮件
                    functions.send_mail_old(email_list,u"redis队列更新异常",u"错误信息%s"%exceputil.traceinfo(e))
                    time.sleep(3600)
                    i=0
                else:
                    time.sleep(sleep_time)

                redis_queue = getredisQueuev2(self.key,email_list=email_list,redis_host=self.redis_host,redis_port=self.redis_port,redis_password=self.redis_password)





    def get(self, block=True, timeout=None):
        """Remove and return an item from the queue.

        If optional args block is true and timeout is None (the default), block
        if necessary until an item is available."""
        if block:
            item = self.__db.blpop(self.key, timeout=timeout)
        else:
            item = self.__db.lpop(self.key)
        if item:
            item = item[1]
        return item


    def getv2(self, key="",block=True, timeout=30,sleep_time=10,retry=9,email_list=functions.mailto_list_ourselves):
        """
        从队列头部获取一条数据
        :param key: (str) 队列名
        :param block: （bool)
        :param timeout：(int) 超时时间 ->30
        :param sleep_time: (int) 休眠时间 ->10
        :param retry:(int) 重试次数
        :param email_list: (list)  电子邮件列表
        :return: (str) 队列中刚开头内容
        """
        #redis_queue = getredisQueuev2(self.key,redis_host=self.redis_host,redis_port=self.redis_port,redis_password=self.redis_password,email_list=email_list)
        redis_queue=None
        i=0
        count=retry+1
        while True:
            try:
                if redis_queue!=None:
                    return redis_queue.get(block=block, timeout=timeout)
                else:
                    return self.get(block=block, timeout=timeout)
            except Exception as e:
                print str(e)
                i+=1
                if i>=count:
                    #发邮件
                    functions.send_mail_old(email_list,u"redis队列更新异常",u"错误信息%s"%exceputil.traceinfo(e))
                    time.sleep(3600)
                    i=0
                else:
                    time.sleep(sleep_time)

                redis_queue = getredisQueuev2(self.key,redis_host=self.redis_host,redis_port=self.redis_port,redis_password=self.redis_password,email_list=email_list)




    def get_nowait(self):
        """Equivalent to get(False)."""
        return self.get(False)

    def save(self):
        """强制写磁盘"""
        return self.__db.save()

    def clear(self):
        """清空自己"""
        return self.__db.delete(self.key) #删除这个key

def getredisQueue(key, redis_host="master1",redis_port=57819,redis_password="bbdredis12344321qaz"):
    """
    连接redis队列
    :param key: (str) 队列名称
    :return: (RedisQueue) redis队列
    """
    host = ""
    if redis_host==None or len(redis_host) <1:
        host_name = socket.getfqdn(socket.gethostname())
        if "win2008r2" in host_name:#在windows服务器上使用master
            host='master'
        else:
            host='localhost'
    else:
        host = redis_host

    return  RedisQueue(key, host=redis_host,port=redis_port,password=redis_password)


def getredisQueuev2(key, redis_host="master1",redis_port=57819,redis_password="bbdredis12344321qaz",sleep_time=10,retry=9,email_list=functions.mailto_list_ourselves):
    """
    连接redis队列，出错后会重试，重试一定次数会发报警邮件
    :param key: (str) 队列名
    :param sleep_time: (int) 休眠时间
    :param retry:(int) 重试次数
    :param email_list: (list)  电子邮件列表
    :return: (RedisQueue) redis队列
    """
    i=0
    count=retry+1
    while True:
        try:
            return getredisQueue(key,redis_host=redis_host,redis_port=redis_port,redis_password=redis_password)
        except Exception as e:
            print str(e)
            i+=1
            if i>=count:
                #发邮件
                functions.send_mail_old(email_list,u"redis队列连接异常",u"错误信息%s"%exceputil.traceinfo(e))
                time.sleep(3600)
                i=0
            else:
                time.sleep(sleep_time)



if __name__ == "__main__":

    # redisQueue = getredisQueue("zhejiang:company_name")
    redisQueue=getredisQueuev2("shanxixian:company_name",redis_host="hadoop6",redis_port=6845,redis_password="qetuoadkhxn7542")
    # print redisQueue.size()
    redisQueue.put(u"西乡县英派（南国）卫浴经营部")
    # print redisQueue.getv2("zhejiang:company_name")
    # print redisQueue.clear()
    # for i in range(4):
    #     print redisQueue.put(u"钢铁")
    # print redisQueue.size();