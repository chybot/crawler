# -*- coding: utf-8 -*-
"""布隆过滤器服务器端模块
"""
__author__ = 'xww'
import sys
reload(sys)
sys.path.append('../')
sys.setdefaultencoding("UTF-8")

from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TCompactProtocol
from bf.BloomFilterService.thrift import BloomFilterService
from common.functions import  get_logger


class BloomFilterClient():
    """布隆过滤器客户端类
    """
    logging=get_logger(u"bloomfilter_client.log")
    def __init__(self, host=u"192.168.2.41", port=8880):
        """
        构造器
        :param host:  (str) 域名或IP地址
        :param port:  (int) 端口
        :return: (BloomFilterClient)
        """
        #初始化连接，使用facebook的thrift框架，支持跨多门语言的RMI
        self.transport = TSocket.TSocket(host, port)
        self.transport = TTransport.TBufferedTransport(self.transport)
        protocol = TCompactProtocol.TCompactProtocol(self.transport)
        self.client = BloomFilterService.Client(protocol)
        #打开端口
        self.transport.open()

    def insert_if_not_exists(self,item):
        """判断布隆过滤器是否包含此元素
        如果不包含则新增元素并返回True，如果已包含则返回False
        :param item:  (str) 字符串
        :return:（bool)  是否包含此元素 -> True:是否包含此元素 False:不包含
        """
        self.logging.info(u"insert_if_not_exists ,item:%s"%item)
        return self.client.insert_if_not_exists(item)

    def insert_element(self,item):
        """
        插入元素
        :param item: （str) 元素
        :return:（None)
        """
        self.logging.info(u"insert_element ,item:%s"%item)
        self.client.insert_element(item)

    def is_element_exist(self,item):
        """
        判断布隆过滤器是否包含此元素
        :param item:（str) 元素
        :return:（bool)  是否包含此元素 -> True:是否包含此元素 False:不包含
        """
        self.logging.info(u"is_element_exist ,item:%s"%item)
        return self.client.is_element_exist(item)

    def write_file(self):
        """
        布隆过滤器数据强制持久化
        :return:（None)
        """
        self.logging.info(u"write_file")
        self.client.write_file()


if __name__ == "__main__":
    bloomFilterclient = BloomFilterClient("7.82.245.242",8880)
    print bloomFilterclient.insert_if_not_exists("http://www.baidu.com")
    bloomFilterclient.write_file()
    bloomFilterclient.insert_element("http://www.baidu.com")
    print bloomFilterclient.is_element_exist("http://www.baidu.com")
