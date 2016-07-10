# -*- coding: utf-8 -*-
__author__ = 'xww'
import pymongo
import socket
import time

import functions
import exceputil
#分割符,mongo字段中存取多个内容时以此分割
split_key="|_|"

def get_id_key(*key):
    """
    把元组中的字符串用split_key分割符连接起来
    :param key: （tuple） id的构成元组
    :return: (str)用split_key 分割后的字符串
    """
    result=""
    i=0
    for k in key:
        if i>0:
            result=result+split_key
        i=i+1
        result=result+k
    return result

def get_id_first(key):
    """
    返回用split_key分割的mongo数据库_id内容的第一个元素
    :param key: (str) 用split_key分割的mongo数据库_id内容
    :return:  (str) 第一个元素
    """
    keys=key.split(split_key)
    if len(keys)>0:
        return keys[0]
    else:
        return ""

class mongodb:
    """
    mongo对象，封装一些对mongo的操作
    """
    def __init__(self, host="localhost", port=27017, username=None,password=None,db=None, table=None, timeout=None):
        self.host=host
        self.port=port

        default_time_out = 30.0
        if timeout != None:
            default_time_out = timeout
        self.conn=pymongo.Connection(host, port, network_timeout=default_time_out)

        self.username=username
        self.password=password
        if username!=None and len(username)>0 and password!=None and len(password)>0:
            #权限验证
            self.conn[db].authenticate(username,password)

        self.db=db
        self.table_name=table
        self.table = self.conn[db][table]

    def find(self,data):
        return self.table.find(data)

    def count(self,data):
        return self.table.find(data).count()

    def find_one(self, data):
        return self.table.find_one(data)

    def  like(self,item,q):
        return self.table.find({item:{'$regex':".*%s.*"%q}})

    def close(self):
        try:
            self.conn.close()
        except Exception as e:
            print str(e)

def  getmondb(host,port,dbname,tablename,username=None,password=None,timeout=None):
    """
    根据指定内容初始化mongo数据库访问对象并返回
    :param host:  （str) 域名地址
    :param port:  （str) 端口
    :param dbname: (str) mongo数据库名
    :param tablename: (str) mongo文档集合名
    :return: (mongodb)
    """
    return mongodb(host,port,db=dbname,table=tablename,username=username,password=password,timeout=timeout)

def  getmondbv2(host,port,dbname,tablename,sleep_time=10,retry=9,username=None,password=None,email_list=functions.mailto_list_ourselves,timeout=None):
    """
    根据指定内容初始化mongo数据库访问对象并返回
    :param host:  （str) 域名地址
    :param port:  （str) 端口
    :param dbname: (str) mongo数据库名
    :param tablename: (str) mongo文档集合名
    :return: (mongodb)
    """
    count=retry+1
    while True:
        try:
            count-=1
            result= getmondb(host,port,dbname,tablename,username=username,password=password,timeout=timeout)
            if result!=None:
                return result
        except Exception as e:
            print(u"mongo数据库连接异常，错误信息%s"%str(e))
            if count==0:
                #发送邮件
                #functions.send_mail_old(email_list,u"mongo数据库连接异常",u"错误信息%s"%exceputil.traceinfo(e))
                time.sleep(3600)
                count=retry+1
            else:
                time.sleep(sleep_time)






def  getmondbbyhostv2(db,table,sleep_time=10,retry=9,email_list=functions.mailto_list_ourselves):
    """
    获取操作mongo数据库和文档集合的对象。遇到错误会重试指定次数
    :param db:  mongo数据库
    :param table:  （str) 文档集合
    :param sleep_time:  休眠时间
    :param retry:  重试次数
    :return: (mongodb) mongodb对象
    """
    count=retry+1
    while True:
        try:
            count-=1
            result= getmondbbyhost(db, table)
            if result!=None:
                return result
        except Exception as e:
            print(u"mongo数据库连接异常，错误信息%s"%str(e))
            if count==0:
                #发送邮件
                functions.send_mail_old(email_list,u"mongo数据库连接异常",u"错误信息%s"%exceputil.traceinfo(e))
                time.sleep(3600)
                count=retry+1
            else:
                time.sleep(sleep_time)

def  getmondbbyhost(dbname,table_name):
    """
    获取操作mongo数据库和文档集合的对象
    :param dbname: (str) mongo数据库名
    :param table_name:(str) mongo数据库文档集合
    :return: (mongodb) mongodb对象
    """
    host_name = socket.getfqdn(socket.gethostname())
    if "win2008r2" not in host_name:#在windows自己机器上才使用本地mongodb ip和端口
        db = getmondb("localhost", 27017, dbname, table_name)
    else:
        db = getmondb("master", 25017, dbname, table_name)
    return db

def update(db,idkey,valueset,flag=True):
    """
    更新数据库
    :param db:  (mongodb)数据库
    :param idkey: (str) mongo数据库_id 主键内容
    :param valueset: (dict) 内容字典
    :param flag: (bool) 是否覆盖
    :return: (None)
    """
    db.table.update({'_id':idkey}, {"$set":valueset}, flag);

def updatev2(db,id,valueset,dbname,table,flag=True,retry=9,sleep_time=10,email_list=functions.mailto_list_ourselves):
    """
    更新数据库,错误会一直尝试
    :param db: (mongodb)数据库
    :param id:  (str) mongo数据库_id 主键内容
    :param valueset:(dict) 内容字典
    :param dbname: (str) 数据库名
    :param table: (str) 文档集合名
    :param retry (int) 重试次数
    :param sleep_time (int) 睡眠时间
    :return:（None)
    """
    count=retry+1
    while True:
        try:
            count-=1
            update(db,id,valueset,flag)
            break
        except Exception as e:
            print (u"更新mongo数据库异常,错误信息：%s"%str(e))
            if count==0:
                 #发送邮件
                functions.send_mail_old(email_list,u"mongo数据库更新异常",u"错误信息%s"%exceputil.traceinfo(e))
                time.sleep(3600)
                count=retry+1

            #重新连接mongo数据库
            time.sleep(sleep_time)
            db=getmondbbyhostv2(dbname, table)

def updatev3(db,id,valueset,flag=True,retry=9,sleep_time=10,email_list=functions.mailto_list_ourselves):
    """
    更新数据库,错误会一直尝试
    :param db: (mongodb)数据库
    :param id:  (str) mongo数据库_id 主键内容
    :param valueset:(dict) 内容字典
    :param dbname: (str) 数据库名
    :param table: (str) 文档集合名
    :param retry (int) 重试次数
    :param sleep_time (int) 睡眠时间
    :return:（None)
    """
    count=retry+1
    while True:
        try:
            count-=1
            update(db,id,valueset,flag)
            break
        except Exception as e:
            print (u"更新mongo数据库异常,错误信息：%s"%str(e))
            if count==0:
                 #发送邮件
                functions.send_mail_old(email_list,u"mongo数据库更新异常",u"错误信息%s"%exceputil.traceinfo(e))
                time.sleep(3600)
                count=retry+1

            #重新连接mongo数据库
            time.sleep(sleep_time)
            db=getmondbv2(db.host,db.port,db.db, db.table_name)


if __name__=='__main__':
    # print get_id_key('http://www.baidu.com','http://www.baidu.com','2012-12-21')

    mongo=mongodb(host="master1", port=25017,username="bbdqyxxrw",password="bbdmg123!@#",db="bigdata_higgs",table="abc")

    ret=mongo.find({})
    for dict_ret in ret:
        print dict_ret["_id"]

    print mongo.table.update({'_id':"123"}, {"$set":{}}, True);


