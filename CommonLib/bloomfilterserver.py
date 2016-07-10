# -*- coding: utf-8 -*-
"""布隆过滤器服务器
"""
__author__ = 'xww'
import sys
reload(sys)
sys.path.append('../')
sys.setdefaultencoding("UTF-8")

import socket
import time

from threading import Thread

from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TCompactProtocol
from thrift.server import TServer
from common.bf.BloomFilterService.thrift import BloomFilterService
from common.functions import  get_logger
from common.exceputil import traceinfo
from common.BloomFilter import BloomFilter
from common import fileutil

#服务器端日志
logger=get_logger("bloom_filters_server.log")



class BloomFilterServer(Thread):
    """布隆过滤器服务器管理类
    """
    def __init__(self,error_rate,element_num,storeable,storefile):
        """构造器
        :param error_rate:(float) 错误率 ->0.001
        :param element_num:(long) 容量 ->10000000
        :param store: (bool) 是否持久化
        :param storefile: (str) 持久化文件名
        :return:(BloomFilterServer)
        """
        Thread.__init__(self)
        #初始化布隆过滤器
        logger.info(u"初始化布隆过滤器,error_rate=%s,element=%s"%(error_rate,element_num))
        self.bloomfilter=BloomFilter(error_rate,element_num)
        self.storeable=storeable
        self.storefile=storefile
        self.store_last_time=time.time()
        if storeable:
            #从文件中读取
            if fileutil.isfile(storefile) and  fileutil.size(storefile)>0:
                logger.info(u"从文件中加载数据,文件名:%s"%storefile)
                self.bloomfilter.open_from_file(storefile)
                logger.info(u"加载数据成功")

    def run(self):
        """线程主函数
        1天持久化1次布隆过滤器
        :return:(None)
        """
        while True:
            try:
                now=time.time()
                subtime=now-self.store_last_time
                if subtime>=3600*24:
                    self.bloomfilter.write_file(self.storefile)
                    self.store_last_time=time.time()
                    time.sleep(24*3600)
                else:
                    time.sleep(3600)
            except BaseException as e:
                logger.error(u"错误信息:%s"%traceinfo(e))

    def insert_element(self,url):
        """插入元素
        :param url: (str) 元素内容
        :return:（None)
        """
        logger.info(u"远程调用insert_element方法,参数:%s"%url)
        self.bloomfilter.insert_element(url)

    def is_element_exist(self,url):
        """判断元素是否存在
        :param url: (str) 元素内容
        :return:(bool) True -> 存在 False-> 不存在
        """
        logger.info(u"远程调用is_element_exist方法, 参数:%s"%url)
        return self.bloomfilter.is_element_exist(url)

    def insert_if_not_exists(self,url):
        """插入不存在元素
        如果元素存在返回False，如果元素不存在则插入元素并返回True
        :param url:  (str)元素内容
        :return: (bool)
        """
        logger.info(u"远程调用insert_if_not_exists方法,参数:%s"%url)
        if self.is_element_exist(url):
            return False
        else:
            self.insert_element(url)
            return True

    def write_file(self):
        """持久化布隆过滤器数据
        :return:（None)
        """
        logger.info(u"远程调用write_file方法")
        if self.storeable:
            logger.info(u"写入数据至%s"%self.storefile)
            self.bloomfilter.write_file(self.storefile)
            self.store_last_time=time.time()
            logger.info(u"写入数据成功")
        else:
            logger.info(u"服务器不支持持久化")
            raise Exception(u"服务器不支持持久化")


def main():
    arglen=len(sys.argv)
    i=1
    #默认端口号
    port = 9990
    #默认不持久化
    store=False
    #默认持久化文件
    store_file=u"bloom_filter.dat"
    #默认错误率
    error_rate=0.001
    #默认最大元素数量
    element_num=10000000
    try:
        while i<arglen:
            if sys.argv[i]=="-port" or sys.argv[i]=="-p":
                port=int(sys.argv[i+1])
                if port<1:
                    raise Exception(u"端口号格式错误")
                i+=2
            elif sys.argv[i]=="--store":
                store=True
                i+=1
            elif sys.argv[i]=="-file":
                store_file=sys.argv[i+1]
                i+=2
            elif sys.argv[i]=="--version":
                print u"bloom filter server  v1.00."
                quit(0)
            elif sys.argv[i]=="--help":
                print u"""\
Usage: python bloomfilterserver.py [options]
布隆过滤器服务器

-port, -p           设置端口号,默认9990
--store             开启持久化功能，默认不开启
-file               持久化文件名，默认bloom_filter_store.data
-error-rate         错误率，默认为0.001
-element-num        元素最大数，默认为10,000,000
--version           查看版本号
--help              查看帮助信息

退出状态：
0   正常
-1  程序出错
-2  参数错误
                """
                quit(0)
            elif sys.argv[i]==u"-error-rate":
                temp_error_rate=float(sys.argv[i+1])
                if  0<error_rate<1:
                    error_rate=temp_error_rate
                else:
                    raise  Exception(u"错误率设置错误.")
                i+=2

            elif sys.argv[i]==u"-element-num":
                element_num=int(sys.argv[i+1])
                if element_num<10000:
                    raise Exception(u"最大元素数量设置错误。")
                i+=2
            else:
                raise Exception(u"无效的参数:%s"%sys.argv[i])
    except Exception as e:
        logger.error(u"参数错误,%s."%e.message)
        quit(-2)

    logger.info(u"布隆过滤器启动参数,port:%s,store:%s,store_file:%s,element_num:%s,error_rate:%s"%(port,store,store_file,element_num,error_rate))
    handler = BloomFilterServer(error_rate,element_num,store,store_file)
    #启动
    handler.start()
    processor = BloomFilterService.Processor(handler)
    hostname = socket.gethostbyname(socket.gethostname())

    logger.info(u"service %s running listen on %s:%d"%(handler.__class__.__name__, hostname, port))

    transport = TSocket.TServerSocket(hostname,port)

    tfactory = TTransport.TBufferedTransportFactory()

    #Protocol
    #Protocol用于对数据格式抽象，在rpc调用时序列化请求和响应。
    #TProtocol的实现包括：TJSONProtocol，TSimpleJSONProtocol，TBinaryProtocol，TBinaryPotocolAccelerated，TCompactProtocol。
    #上面每种类型，都有对应的Factory类，用于创建该类对象。
    #pfactory = TBinaryProtocol.TBinaryProtocolFactory()
    pfactory = TCompactProtocol.TCompactProtocolFactory()

    #server = TServer.TSimpleServer(processor, transport, tfactory, pfactory)
    server = TServer.TThreadPoolServer(processor, transport, tfactory, pfactory)
    server.setNumThreads(2048)

    logger.info(u"BloomFilter server Starting!")
    server.serve()
    logger.infou(u"BloomFilter server done!")



if __name__=="__main__":
    main()