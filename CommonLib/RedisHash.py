# -*- coding: utf-8 -*-
# Created on 2014/9/25 21:11.

import redis
import socket
import time

import exceputil
import functions

class RedisHash(object):
    """Simple Hash with Redis Backend"""
    def __init__(self, name, namespace='hash', **redis_kwargs):
        """The default connection parameters are: host='localhost', port=6379, db=0"""
        self.db= redis.Redis(**redis_kwargs)
        self.key = '%s:%s' %(namespace, name)
        if "redis_host" in redis_kwargs:
            self.redis_host=redis_kwargs["redis_host"]
        else:
            self.redis_host="118.123.9.70"
        if "redis_port" in redis_kwargs:
            self.redis_port=redis_kwargs["redis_host"]
        else:
            self.redis_port=57819
        if "redis_password" in redis_kwargs:
            self.redis_password=redis_kwargs["redis_password"]
        else:
             self.redis_password="bbdredis12344321qaz"

    def hash_update(self,field,value):
        """
        hset
        # HSET key field value
        # 将哈希表key中的域field的值设为value。如果key不存在，一个新的哈希表被创建并进行hset操作。如果域field已经存在于哈希表中，旧值将被覆盖
        :param field:
        :param value:
        :return:
        """
        self.db.hset(self.key,field,value)
    def get(self,field):
        """
        # hget
        # HGET key field
        # 返回哈希表key中指定的field的值。
        :param field:
        :return:
        """
        return self.db.hget(self.key,field)
    def hash_insert(self,field,value):
        """
        # hsetnx
        # HSETNX key field value
        # 将哈希表key中的域field的值设置为value，当且仅当域field不存在。若域field已经存在，该操作无效。如果key不存在，一个新哈希表被创建并执行hsetnx命令
        :param field:
        :param value:
        :return:
        """
        self.db.hsetnx(self.key,field,value)
    def hash_insert_more(self,**mapping):
        """
        # hmset
        # HMSET key field value [field value ...]
        # 同时将多个field - value(域-值)对设置到哈希表key中。此命令会覆盖哈希表中已存在的域。如果key不存在，一个空哈希表被创建并执行hmset操作
        :param args:
        :return:
        """
        # mapping=list(mapping)
        # print mapping
        self.db.hmset(self.key,mapping)


    def hash_get_more(self,keys):
        """
        # hmget
        # HMGET key field [field ...]
        # 返回哈希表key中，一个或多个给定域的值。如果给定的域不存在于哈希表，那么返回一个nil值。因为不存在的key被当作一个空哈希表来处理，所以对一个不存在的key进行hmget操作将返回一个只带有nil值的表
        :param keys:
        :return:
        """
        return self.db.hmget(self.key,keys)
    def get_keys(self):
        """
        # hgetall
        # HGETALL key
        # 返回哈希表key中，所有的域和值。在返回值里，紧跟每个域名(field name)之后是域的值(value)，所以返回值的长度是哈希表大小的两倍
        :return:
        """
        return self.db.hgetall(self.key)
    def dell(self,*keys):
        """
        # hdel
        # HDEL key field [field ...]
        # 删除哈希表key中的一个或多个指定域，不存在的域将被忽略
        :param field:
        :return:
        """
        self.db.hdel(self.key,*keys)
    def size(self):
        """
        # hlen
        # HLEN key
        # 返回哈希表key对应的field的数量
        :return:
        """
        return self.db.hlen(self.key)
    def exist(self,field):
        """
        # hexists
        # HEXISTS key field
        # 查看哈希表key中，给定域field是否存在
        :param field:
        :return:
        """
        return self.db.hexists(self.key,field)
    def keys(self):
        """
        # hkeys
        # HKEYS key
        # 获得哈希表中key对应的所有field
        :return:
        """
        return self.db.hkeys(self.key)
    def values(self):
        """
        # hvals
        # HVALS key
        # 获得哈希表中key对应的所有values
        :return:
        """
        return self.db.hvals(self.key)
    def add(self,field,amount=1):
        """
        # hincrby
        # 为哈希表key中的域field的值加上增量increment。增量也可以为负数，相当于对给定域进行减法操作。如果key不存在，
        一个新的哈希表被创建并执行hincrby命令。如果域field不存在，那么在执行命令前，域的值被初始化为0。
        对一个储存字符串值的域field执行hincrby命令将造成一个错误。本操作的值限制在64位(bit)有符号数字表示之内
        :param field:
        :return:
        """
        self.db.hincrby(self.key,field,amount)




if __name__ == "__main__":
    provice_dict_unicode={
    u"广东":u"guangdong",u"湖北":u"hubei",u"湖南":u"hunan",u"河南":u"henan",u"黑龙江":u"heilongjiang",
    u"河北":u"hebei",u"海南":u"hainan",u"贵州":u"guizhou",u"广西":u"guangxi",u"福建":u"fujian",
    u"重庆":u"chongqing",u"北京":u"beijing",u"安徽":u"anhui",u"江苏":u"jiangsu",u"甘肃":u"gansu",
    u"新疆":u"xinjiang",u"天津":u"tianjin",u"四川":u"sichuan",u"陕西":u"shanxixian",u"山西":u"shanxitaiyuan",
    u"上海":u"shanghai_2",u"山东":u"shandong",u"青海":u"qinghai",u"宁夏":u"ningxia",u"内蒙古":u"neimenggu",
    u"辽宁":u"liaoning",u"吉林":u"jilin",u"江西":u"jiangxi",u"西藏":u"xizang",u"浙江":u"zhejiang",
    u"云南":u"yunnan",u"总局":u"zongju"
}
    for kk in provice_dict_unicode.values():
        h=RedisHash("proxy_base:%s"%kk,host="118.123.9.70",port=57819,password="bbdredis12344321qaz")
        # h.hash_update("max_num",50)
        # h.hash_update("wait_minute",5)
        #h.hash_update("is_use",False)
        h.hash_insert_more(max_num=50,wait_second=1)
        #h.add("wait_seconds")
        #print h.get("is_use")=="False"


