# -*- coding: utf-8 -*-
# Created by Leo on 16/04/26
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
import time
import pymongo
import QueueBase
class QueueMongo(QueueBase.QueueBase):
    def __init__(self,table_name, host, port , username=None, password=None, **args):
        """
        table_name: table name in DB
        :param host
        :param port
        :param table_name
        :param dbname
        :return: mongo instance
        """
        QueueBase.QueueBase.__init__(self, table_name, host, port)
        while True:
            try:
                # 连接mongodb
                self.conn = pymongo.MongoClient(host=host, port=port)
                # 连接数据库
                self.db = self.conn[args['dbname'] if args.has_key('dbname') else 'bigdata_higgs']
                if username or password:
                    self.db.authenticate(username, password=password)
                # 连接聚集
                self.table = self.db[table_name]
                print 'success init mongodb connection'
                break
            except Exception as e:
                print e
                time.sleep(60)

    def save(self, data, **args):
        """
        save data to mongodb
        :param data: data of dict type
        :param id: if None: auto gen ObjectId
        :param is_update: whether to update or not
        :return:（None)
        """
        while True:
            try:
                self.table.save(data, manipulate=True, check_keys=True, **args)
                break
            except Exception as e:
                print e
                time.sleep(60)

    def get(self, **args):
        # TO-DO
        pass
    def put(self, **args):
        # TO-DO
        pass

    def size(self, **args):
        return self.table.find().count()

    # 切换队列
    def changeTable(self, name):
        self.table = self.db[name]
if __name__ == '__main__':
    pass