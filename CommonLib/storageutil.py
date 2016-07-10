# -*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding("UTF-8")
sys.path.append("../")

import time
from abc import ABCMeta, abstractmethod
from ssdb import SSDB
from ssdb.connection import BlockingConnectionPool
import json
from kafka import KafkaClient, SimpleConsumer, SimpleProducer, common
from Queue import Queue
import storageutil
import redis
import pymongo
# from pykafka import SimpleConsumer,KafkaClient

def getdb_factory(table, type=None, port=27017, host="127.0.0.1",  **args):
    """
        get db factory
        :param table: tablename
        :param type: ssdb,mongodb...
        :return: db
        """
    if args.has_key("dbname") and (not type or type == 'ssdb'):
        args.pop("dbname")
    if args.has_key("password") and (not type or type == 'ssdb'):
        args.pop("password")
    if args.has_key("async") and (not type or type == 'ssdb'):
        args.pop("async")

    if not type:
        return ssdb(table_name=table, port=57878, host="spider5", **args)
    else:
        return getattr(storageutil, type)(table_name=table, port=port, host=host, **args)
            

class storage:
    
    __metaclass__ = ABCMeta
    
    @abstractmethod
    def save(self, data, **args):
        pass
    
    @abstractmethod
    def get(self, **args):
        pass
    
    @abstractmethod
    def size(self, **args):
        pass

    @abstractmethod
    def select_queue(self, name):
        pass


class rdb(storage):

    def __init__(self, host, port, table_name, **args):
        self.queue_name = table_name
        self.queue = redis.Redis(host=host, port=port, db=0, password=args['password'] if args.has_key('password') else None)
        print 'success init redis connection'

    def save(self,data, **args):
        """
        push data to redis queue back
        :param data: data of dict type
        :return:（None)
        """
        while True:
            try:
                if isinstance(data, dict) or isinstance(data, list):
                    self.queue.rpush(self.queue_name, json.dumps(data))
                else:
                    self.queue.rpush(self.queue_name, data)
                break
            except Exception as e:
                print e
                time.sleep(60)

    def get(self, **args):
         while True:
            try:
                return self.queue.lpop(self.queue_name)
            except Exception as e:
                print e
                time.sleep(60)

    # 切换队列
    def select_queue(self, name):
        self.queue_name = name

    def size(self, **args):
        return self.queue.llen(self.queue_name)

    
class ssdb(storage):
    
    def __init__(self, host, port, table_name, **args):
        self.queue_name = table_name
        pool = BlockingConnectionPool(host = host, port = port, **args)
        self.ssdb = SSDB(connection_pool=pool)
        print 'success init ssdb connection'
        
    def save(self,data, **args):
        """
        push data to ssdb queue back
        :param data: data of dict type
        :return:（None)
        """
        while True:
            try:
                if isinstance(data, dict) or isinstance(data, list):
                    self.ssdb.qpush_back(self.queue_name, json.dumps(data))
                else:
                    self.ssdb.qpush_back(self.queue_name, data)
                break
            except Exception as e:
                print e
                time.sleep(60)

    def get(self, **args):
         while True:
            try:
                data = self.ssdb.qpop_front(self.queue_name)
                if data:
                    return data[0]
                return data
            except Exception as e:
                print e
                time.sleep(60)

    # 切换队列
    def select_queue(self, name):
        self.queue_name = name
        
    def size(self, **args):
        return self.ssdb.qsize(self.queue_name)

    def len(self, **args):
        return self.ssdb.qsize(self.queue_name)

    def put(self,data, **args):
        """
        push data to ssdb queue back
        :param data: data of dict type
        :return:（None)
        """
        while True:
            try:
                if isinstance(data, dict) or isinstance(data, list):
                    self.ssdb.qpush_back(self.queue_name, json.dumps(data))
                else:
                    self.ssdb.qpush_back(self.queue_name, data)
                break
            except Exception as e:
                print e
                time.sleep(60)
    def put_data_back(self, data):
        return self.ssdb.qpush_back(self.queue_name, data)

    def put_data_front(self, data):
        return self.ssdb.qpush_front(self.queue_name, data)
    def ssdb_put_zset(self,field):
        #zset zset key score
        while True:
            try:
                return self.ssdb.zset(self.queue_name,field)
            except Exception as e:
                print e
                self.SSDB()
    def ssdb_zexists(self,field):
        while True:
            try:
                return self.ssdb.zexists(self.queue_name,field)
            except Exception as e:
                print e
                self.SSDB()
    def ssdb_zdel(self,field):
        while True:
            try:
                return self.ssdb.zdel(self.queue_name,field)
            except Exception as e:
                print e
                self.SSDB()
    
class mongodb(storage):
    def __init__(self, host, port, table_name, username=None, password=None, **args):
        """
        :param host
        :param port
        :param table_name
        :param dbname
        :return: mongo
        """
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
    
    def size(self, **args):
        return self.table.find().count()

    # 切换队列
    def select_queue(self, name):
        self.table = self.db[name]
    
class kafka:
    def __init__(self, host, port, table_name, **args):
        """
        :param host
        :param port
        :param table_name
        :return: kafka
        """
        self.queue = []
        self.queue_name = table_name.replace(":","_")
        # self.kafka = KafkaClient('%s:%d' % (host, port))
        self.kafka = KafkaClient(hosts=host,client_id=self.queue_name)
        self.producer = SimpleProducer(self.kafka, async=args['async'] if args.has_key('async') else False)
        self.producer.client.ensure_topic_exists(self.queue_name)
        self.consumer = SimpleConsumer(self.kafka, self.queue_name+"_consumer", self.queue_name, auto_commit_every_n=1, max_buffer_size=None)
        
        print 'success init kafka connection'

    def __del__(self):
        if self.kafka:
            [self.save(x.message.value) for x in self.queue]
            self.kafka.close()

        
    def save(self, data, **args):
        try:
            if isinstance(data, dict) or isinstance(data, list):
                self.producer.send_messages(self.queue_name, json.dumps(data))
            elif isinstance(data, unicode):
                self.producer.send_messages(self.queue_name, data.encode('utf-8'))
            else:
                self.producer.send_messages(self.queue_name, data)
        except Exception as e:
            print e
            time.sleep(60)
            
        
    def get(self, **args):
#         self.consumer.seek(369600, 0)
        if not self.queue:
            try:
                self.consumer._fetch()
            except Exception as e:
                print e
            kq = self.consumer.queue
            while not kq.empty():
                partition, result = kq.get_nowait()
                self.queue.append(result)
                self.consumer.offsets[partition] += 1
                self.consumer.count_since_commit += 1
            
            self.consumer.queue = Queue()
            self.consumer.commit()
            
        if self.queue:
            return self.queue.pop().message.value
        else:
            return None
         
        
    def size(self, **args):
        count = 0
        for k,v in self.consumer.offsets.items():
            reqs = [common.OffsetRequest(self.queue_name, k, -1, 1)]
            (resp, ) = self.consumer.client.send_offset_request(reqs)
            count += (resp.offsets[0] - v)
        return count + len(self.queue)

    # 切换队列
    def select_queue(self, name):
        self.queue_name = name.replace(":","_")
        self.consumer = SimpleConsumer(self.kafka, self.queue_name+"_consumer", self.queue_name, max_buffer_size=None)
            
if '__main__' == __name__:
#     storageutil.getdb_factory(table='test', type = "mongodb", dbname="test").save({"test":"test"})
#     storageutil.getdb_factory(table='test', type = "ssdb", dbname="test", port=57878, host="spider5").save({"test":"test"})
#     a = 0
#     aa = []
#     while True:
    db = storageutil.getdb_factory(table='bbd_queue_xgxx_test_47_qyxx_nyscqyzzcx', host='dataom3', port=9092, type = "kafka")
#         aa.append(db)
#         db.get()
#         a += 1
#         print a
#     count = 0
#     a = time.time()
#     while True:
#     with open("/home/wrstrs/Desktop/zyktgg_test", "r") as f:
#         for line in f:
#             db.save(line)
#         count += 1
#     print str(time.time()-a)
    
#     print db.consumer.client.send_fetch_request([common.FetchRequest('lvyouju_result', 1, 1, 1)])
#     db.consumer.seek(0,2)
    while True:
#         db = storageutil.getdb_factory(table='test', host='web14', port=51092, type = "kafka")
#         db.save("test 11 aa f aa".decode('utf-8'))
        print db.size()
        time.sleep(1)
        m = db.get()
        # db.__del__()
        print m
#         if m.startswith('wei'):
#             print m.split('d41d8cd98f00b204e9800998ecf8427e')
#         print db.size()
#         time.sleep(1)
#     kafka = KafkaClient('%s:%d' % ('web14', 51092))
#     consumer = SimpleConsumer(kafka, 'test', 'test')
#     print consumer.offsets[0] - consumer.fetch_offsets[0]

#     db = storageutil.getdb_factory(table='mongotest', type='mongodb', host='localhost', port=27017, dbname='test')
#     data = {'test': 'test'}
#     db.save(data)
#     print db.size()
#     data1 = {'_id':'fwefwerew', 'test': 'test'}
#     db.select_queue('test222')
#     db.save(data)
#     db.save(data1)
#     print db.size()

#     with open('testaa1','w') as f:
#         db = storageutil.getdb_factory(table='tourism')
#         while True:
#             time.sleep(1)
#             try:
#                 print db.get()
#             except:
#                 pass
#             f.write(db.get() + '\n')

