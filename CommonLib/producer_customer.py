# -*- coding: utf-8 -*-
"""
公共生产者消费者模块
"""

__author__ = 'xww'
import sys
reload(sys)
sys.setdefaultencoding("UTF-8")
sys.path.append("../")

import time
import os

from abc import abstractmethod

from common import RedisQueue
from common import fileutil
from common.exceputil import  traceinfo
from common.functions import  get_logger
from common.bloomfilterclient import  BloomFilterClient

class Customer():
    """
    消费者
    """
    def __init__(self,name,queue_name,process_number=1,redis_host=None,redis_port=None):
        """
        消费者类构造器
        :param name:  (str) 名称
        :param queue_name: (str) redis队列名称
        :param redis_host: （str） redis 服务器域名
        :param redis_port: (int) 端口号
        :return:
        """
        self.process_number=process_number
        if not os.path.exists("./log"):
            os.makedirs("./log")
        self.customer_logging=get_logger("./log/%s"%name+"_%d"%self.process_number)
        self.customer_name=name
        self.last_file="%s_last_key_%d.txt"%(self.customer_name,self.process_number)
        self.customer_queue_name=queue_name
        self.customer_redis_host=redis_host
        self.customer_redis_port=redis_port
        self.customer_queue_conn=RedisQueue.getredisQueuev2(queue_name,redis_host)


    def get(self):
        """
        获取内容
        :return: （unicode） url地址或任何种子地址
        """
        return self.customer_queue_conn.getv2(self.customer_queue_name)

    @abstractmethod
    def run(self,item):
        """
        爬虫模块
        :param item: (unicode) url内容
        :return:（None)
        """
        pass

    def process_last_error(self):
        """
        读取last_key文件内容，并放到redis队列末尾
        :return: (None)
        """
        if fileutil.isfile(self.last_file):
            tmp_key=fileutil.read(self.last_file,"UTF-8").strip()
            if len(tmp_key) > 0:
                self.customer_queue_conn.putv2(tmp_key,self.customer_queue_name)
                fileutil.clear(self.last_file)


    def start(self):
        """
        启动消费者
        1。把上次处理失败的last_key文件内容，并放到redis队列末尾
        2。获取新的key值
        3。根据新的key值抓取。如果失败，则把失败的key放到last_file文件中
        4。回到第2步
        :return:
        """
        self.process_last_error()
        while True:
            try:
                item=self.get()
                if item==None or len(item)<1:
                    self.customer_logging.error(u"队列内容为空")
                    continue
            except Exception as e:
                self.customer_logging.error(u"读取redis集合错误,错误信息:%s"%(traceinfo(e)))
                time.sleep(10)
                continue
            fileutil.write(self.last_file,item.encode("UTF-8"))
            try:
                self.run(item)
                fileutil.clear(self.last_file)
            except Exception as e2:
                self.customer_logging.error(u"抓取异常,错误信息:%s"%(traceinfo(e2)))
                self.customer_queue_conn.putv2(item,self.customer_queue_name)
                fileutil.clear(self.last_file)
                time.sleep(10)
            time.sleep(1)


class Producer():
    """
    生产者类
    """
    def __init__(self,name,queue_names,process_number=1,redis_host=None,redis_port=None):
        """
        生产者类构造器
        :param name:  (str) 生产者名称
        :param queue_names: (str) redis队列名称列表
        :param redis_host: （str） redis 服务器域名
        :param redis_port: (int) redis服务器端口号
        :return:
        """
        self.process_number=process_number
        self.product_name=name
        if not os.path.exists("./log"):
            os.makedirs("./log")
        self.product_logging=get_logger("./log/%s"%name+"_%d"%self.process_number)
        self.product_queue_names=queue_names
        self.product_redis_host=redis_host
        self.product_redis_port=redis_port
        self.product_conns=list()
        self.bloomfilter_mode=False
        for queue_name in queue_names:
            queue_conn=RedisQueue.getredisQueuev2(queue_name,redis_host,redis_port)
            self.product_conns.append(queue_conn)

    def add_bloomfilter(self,bf_host,bf_port=9990):
        """
        增加bloomfilter服务器验证
        :param bf_host:  (str) bloomfilter服务器域名 ->  master
        :param bf_port:  (int) bloomfilter服务器端口号 ->  9990
        :return: (None)
        """
        self.bf_host=bf_host
        self.bf_port=bf_port
        self.bloomfilter_mode=True
        self.bloomFilterclient = BloomFilterClient(self.bf_host, self.bf_port)



    def product_real(self,item):
        """
         生产url，放到redis队列
        :param item: （str） url或种子
        :return:（None)
        """
        if item!=None and len(item)>0:
            i=0
            for conn in self.product_conns:
                self.product_logging.info(u"item=%s"%item)
                conn.putv2(item,self.product_queue_names[i])
                i+=1

    def product(self,item,unique=None):
        """
        生产url，放到redis队列,对唯一性进行判断
        :param item: （str） url或种子
        :return:（None)
        """
        if self.bloomfilter_mode:
            if unique==None:
                unique=item
            while True:
                try:
                    if self.bloomFilterclient.insert_if_not_exists(unique):
                        self.product_logging.info(u"此元素未处理,item:%s"%unique)
                        self.product_real(item)
                    else:
                        self.product_logging.info(u"此元素已处理,item:%s"%unique)
                    break
                except Exception as e:
                    self.product_logging.error(u"访问布隆过滤器发生错误!,错误信息:%s"%traceinfo(e))
                    while True:
                        try:
                            self.bloomFilterclient = BloomFilterClient(self.bf_host, self.bf_port)
                            break
                        except Exception as e1:
                            self.product_logging.error(u"布隆过滤器连接发生错误!,错误信息:%s"%traceinfo(e1))
                            time.sleep(5)
                            continue

        else:
             self.product_real(item)


    def sizes(self):
        """
        查询队列大小
        :return:size
        """
        self.product_logging.info(u"查询redis数据大小")
        ll=0
        for conn in self.product_conns:
            ll+=conn.size()
        return ll

    def clear(self):
        """
        清除redis队列
        :return: (None)
        """
        self.product_logging.info(u"清除redis队列")
        for conn in self.product_conns:
            conn.clear()




class CustomerProducer(Producer,Customer):
    def __init__(self,name,customer_queue,product_queues,process_number=1,redis_host=None,redis_port=None):
        Customer.__init__(self,"%s_customer"%name,customer_queue,process_number,redis_host,redis_port)
        Producer.__init__(self,"%s_producer"%name,product_queues,process_number,redis_host,redis_port)



