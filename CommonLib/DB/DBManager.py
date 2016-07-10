# -*- coding: utf-8 -*-
__author__ = 'Leo'

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
# print "DB manager ABS path:",os.path.dirname(os.path.abspath(__file__))

class DBManager(object):
    """
    Class used to create DB instance for different types of DB
    """
    # def create(self, type, name, host='localhost', port=0, **kwargs):
    #     return getattr(__import__(type), type)(name, host=host, port=port, **kwargs)

    @staticmethod
    def mapType(type):
        __type = None
        if "ssdb" in type.lower():
            __type = "QueueSSDB"
        if "kafka" in type.lower():
            __type = "QueueKafka"
        if "mongo" in type.lower():
            __type = "QueueMongo"
        if 'solr' in type.lower():
            __type = 'QueueSolr'
        assert __type != None,'type error,Not in [ssdb,kafka,mongo,solr]'
        return __type

    @staticmethod
    def getInstance(type, name, host = 'localhost', port = 0, **kwargs):
        """
        static method, return a db instance use the input parameters
        support ssdb ,kafka , mongo
        :param type: DB type such as ssdb ,kafka
        :param name: table name
        :param host: host name or ip
        :param port:
        :param kwargs:
        :return: DB instance
        """
        type = DBManager.mapType(type)
        return getattr(__import__(type), type)(name, host=host, port=port, **kwargs)

if __name__ =="__main__":
    d={"1":"1111","2":[]}
    import json
    import time
    import uuid
    # import sys
    # import zlib
    # from gzip import GzipFile
    # from StringIO import StringIO
    # import chardet
    # print sys.getsizeof(json.dumps(d))
    # compress_str = zlib.compress(json.dumps(d))
    # print sys.getsizeof(compress_str)
    # print chardet.detect(compress_str)
    # gd = GzipFile(fileobj = StringIO(json.dumps(d)),mode="r")
    # print gd.len
    # print gd.__sizeof__()
    # print gd.read()
    # print dir(gd)
    # print sys.getsizeof(gd.readlines())
    ssdb_inst = DBManager.getInstance("ssdb", "new_beijing", host = "spider5", port = 57888)
    key= "ffedab09ea2d96d7763e7d5f2997bcb2|_|北京众肯世纪商贸有限公司|_|beijing|_|2016-05-26"
    data_item = ssdb_inst.hget(key)

    db_inst = DBManager.getInstance("kafka", "qyxx_html_nb", host = "125.65.78.18", port = 9092)
    print db_inst.size()
    # for x in xrange(1, 100 * 100000):
    #     uid=uuid.uuid1()
    #     rk = key + "|_|" + uuid.uuid1().hex
    #     data_item["rowkey"] = rk
    #     db_inst.changeTable("qyxx_test3")
    #     db_inst.save(data_item)
    #     print "save ok for tst1, couter=", x
    #     db_inst.changeTable("qyxx_test4")
    #     rk = key + "|_|" + uuid.uuid1().hex
    #     data_item["rowkey"] = rk
    #     db_inst.save(data_item)
    #     print "save ok for tst22, couter=", x


