# -*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding("UTF-8")

import time
import redis

sys.path.append('../')
from qyxx import config

class Vaild_Proxy(object):
    def __init__(self,queue_name):
        self.pinyin=queue_name
        self.__RedisDB=None
        self.proxy=None
        self.reids_conn()
        self.max_num=int(self.hash_data_get("hash:proxy_base:%s"%self.pinyin,"max_num"))
        self.wait_second=int(self.hash_data_get("hash:proxy_base:%s"%self.pinyin,"wait_second"))

    def reids_conn(self):
        """
        连接__RedisDB
        :return:
        """
        while True:
            try:
                self.__RedisDB=redis.Redis(host=config.redis_host,port=config.redis_port,password=config.redis_password)
                break
            except Exception as e:
                print u"链接__RedisDB错误：%s"%e
    def redis_set_srandmember(self,name,number=1):
        """
        返回一个集合里面的随机number数量，不删除数据
        :param name:
        :param number:
        :return:
        """
        while True:
            try:
                return self.__RedisDB.srandmember(name,number)
            except Exception as e:
                print e
                self.reids_conn()
    def size(self,key):
        """# 判断一个set长度为多少 不存在为0"""
        while True:
            try:
                 return self.__RedisDB.scard(key)
            except Exception as e:
                print e
                self.reids_conn()

    def have(self,key,item):
        """判断set中一个对象是否存在"""
        while True:
            try:
                return self.__RedisDB.sismember(key,item)
            except Exception as e:
                print e
                self.reids_conn()

    def hash_update(self,key,field,value):
        """
        将哈希表key中的域field的值设为value。如果key不存在，一个新的哈希表被创建并进行hset操作。如果域field已经存在于哈希表中，旧值将被覆盖
        :param key:
        :param field:
        :param value:
        :return:
        """
        while True:
            try:
                return self.__RedisDB.hset(key,field,value)
            except Exception as e:
                print e
                self.reids_conn()
    def hash_update_more(self,key,**mapping):
        #hmset(self.key,mapping)
        #插入多个
        while True:
            try:
                return self.__RedisDB.hmset(key,mapping)
            except Exception as e:
                print e
                self.reids_conn()
    def  hash_data_get(self,key,field):
        """
        返回哈希表key中指定的field的值
        :param key:
        :param field:
        :return:
        """
        while True:
            try:
                return self.__RedisDB.hget(key,field)
            except Exception as e:
                print e
                self.reids_conn()
    def hash_get_all(self,key):
        """
        返回哈希表key中，所有的域和值。在返回值里，紧跟每个域名(field name)之后是域的值(value)，所以返回值的长度是哈希表大小的两倍
        :return:
        """
        while True:
            try:
                return self.__RedisDB.hgetall(key)
            except Exception as e:
                print e
                self.reids_conn()
    def hash_add(self,key,field,amount=1):
        """
        为哈希表key中的域field的值加上增量increment。增量也可以为负数，相当于对给定域进行减法操作。如果key不存在，
        一个新的哈希表被创建并执行hincrby命令。如果域field不存在，那么在执行命令前，域的值被初始化为0。
        对一个储存字符串值的域field执行hincrby命令将造成一个错误。本操作的值限制在64位(bit)有符号数字表示之内
        :return:
        """
        while True:
            try:
                return self.__RedisDB.hincrby(key,field,amount)
            except Exception as e:
                print e
                self.reids_conn()
    def proxy_true(self):
        if self.proxy=="self_build_proxy":
            return False
        proxy=self.proxy.replace(":42271","")
        hash_values=self.hash_get_all("hash:%s:%s"%(self.pinyin,proxy))
        num=1
        is_use=hash_values.get("is_use")
        while is_use=="used":
            if num>100 and int(time.time())-int(hash_values.get("now_num",0))>120:
                self.hash_update("hash:%s:%s"%(self.pinyin,proxy),"is_use","unused")
            else:
                return False
            hash_values=self.hash_get_all("hash:%s:%s"%(self.pinyin,proxy))
            is_use=hash_values.get("is_use")
            num+=1
        returned=False
        self.hash_update("hash:%s:%s"%(self.pinyin,proxy),"is_use","used")
        uptime=float(hash_values.get("uptime",0))
        str_time=time.strftime("%Y%m%d",time.localtime(float(uptime)))
        if str_time==time.strftime("%Y%m%d",time.localtime(float(time.time()))):
            now_num=int(hash_values.get("now_num",0))
            if now_num<self.max_num and int(time.time())-int(uptime)>=self.wait_second:
                self.hash_add("hash:%s:%s"%(self.pinyin,proxy),"now_num")
                returned= True
        else:
            self.hash_update("hash:%s:%s"%(self.pinyin,proxy),"now_num",1)
            returned= True
        self.hash_update_more("hash:%s:%s"%(self.pinyin,proxy),uptime=time.time(),is_use="unused")
        return returned

    def valid_proxy(self):
        half_proxy=int(self.size("set:proxy:self_built"))/2
        proxys=self.redis_set_srandmember("set:proxy:self_built",half_proxy)
        for proxy in proxys:
            self.proxy=proxy
            if self.proxy_true():
                return
        from common.proxyutils import choice_proxy
        self.proxy=choice_proxy(is_debug=True,url="",area=u"中国",host=config.proxy_host,port=config.proxy_port)
def choice_proxy_form_self_built(queue_name):
    vp=Vaild_Proxy(queue_name)
    vp.valid_proxy()
    return vp.proxy
if __name__ == '__main__':
    print choice_proxy_form_self_built("chongqing")