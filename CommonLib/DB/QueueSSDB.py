# -*- coding: utf-8 -*-
__author__ = 'Lvv'

import QueueBase
from ssdb.connection import BlockingConnectionPool
from ssdb import SSDB
import json


class QueueSSDB(QueueBase.QueueBase):
    """
    base class , only provide interface for sub class to implement
    """
    def __init__(self, name, host='localhost', port=8888, **kwargs):
        QueueBase.QueueBase.__init__(self, name, host, port)
        self.__conn = SSDB(connection_pool=BlockingConnectionPool(host=self.host, port=self.port))


    #queue
    @QueueBase.catch
    def put(self, value, *args, **kwargs):
        """
        put an  item in the back of a queue
        :param value:
        :param args:
        :param kwargs:
        :return:
        """
        return self.__conn.qpush_back(self.name,
                                      json.dumps(value, ensure_ascii=False).encode('utf-8') if isinstance(value, dict) or isinstance(value, list) else value)

    def save(self, value, *args, **kwargs):
        """
        put an  item in the back of a queue
        :param value:
        :param args:
        :param kwargs:
        :return:
        """
        return self.__conn.qpush_back(self.name,
                                      json.dumps(value, ensure_ascii = False).encode('utf-8') if isinstance(value,
                                                                                                            dict) or isinstance(
                                          value, list) else value)

    @QueueBase.catch
    def get(self, *args, **kwargs):
        """
        get element from the from of queue
        :param args:
        :param kwargs:
        :return:
        """
        value = self.__conn.qpop_front(self.name)
        return value[0] if value else value

    @QueueBase.catch
    def getMore(self, *args, **kwargs):
        """
        get element from the from of queue
        :param args:
        :param kwargs:
        :return:
        """
        value = self.__conn.qpop_front(self.name, **kwargs)
        return value

    @QueueBase.catch
    def size(self, *args, **kwargs):
        return self.__conn.qsize(self.name)

    @QueueBase.catch
    def changeTable(self, name):
        """
        change the queue name to operate
        :param name:
        :return:
        """
        self.name = name

    @QueueBase.catch
    def select_queue(self, name):
        """
        change the queue name to operate
        :param name:
        :return:
        """
        self.name = name

    @QueueBase.catch
    def qclaerQueue(self):
        return self.__conn.qclear(self.name)


    #KV
    @QueueBase.catch
    def keySet(self,key,value):
        """
        Set the value at key ``name`` to ``value`` .
        :param key:
        :param value:
        :return:
        """
        value = json.dumps(value, ensure_ascii = False).encode('utf-8') if isinstance(value,dict) or isinstance(value, list) else value
        return self.__conn.set(key,value)

    @QueueBase.catch
    def keySetx(self,name, value, ttl=-1):
        """
        Set the value of key ``name`` to ``value`` that expires in ``ttl``
        seconds. ``ttl`` can be represented by an integer or a Python
        timedelta object.
        :param name:
        :param value:
        :param ttl:
        :return:
        """
        return self.__conn.setx(name,value,ttl=ttl)

    @QueueBase.catch
    def keyTtl(self,key):
        """
        Returns the number of seconds until the key ``name`` will expire.
        :return:
        """
        self.__conn.ttl(key)

    @QueueBase.catch
    def keyGet(self,key):
        """
        Return the value at key ``name``, or ``None`` if the key doesn't exist
        :param key:
        :return:
        """
        return self.__conn.get(key)

    @QueueBase.catch
    def keyDel(self,key):
        """
        Delete the key specified by ``name`` .
        :param key:
        :return:
        """
        return self.__conn.delete(key)

    @QueueBase.catch
    def keyKeys(self,key_start='',key_end=''):
        """
        Return a list of the top ``limit`` keys between ``name_start`` and
        ``name_end``
        :param key_start:
        :param key_end:
        :return:
        """
        return self.__conn.keys(name_start=key_start,name_end=key_end,limit=100000)
    @QueueBase.catch
    def keyexists(self,key):
        """
        :param key:
        :return:
        """
        return self.__conn.exists(key)
    #SET
    @QueueBase.catch
    def zsetSet(self,field,score = 1):
        if field:
            if isinstance(field, dict) or isinstance(field, list):
                field = json.dumps(field)
            field = field if len(field) < 100 else field[:100]
        return self.__conn.zset(self.name, field, score)
    @QueueBase.catch
    def zgetSet(self,key):
        return self.__conn.zget(self.name,key)
    @QueueBase.catch
    def zexistsSet(self,name,field):
        return self.__conn.zexists(name,field)
    @QueueBase.catch
    def zkeysSet(self):
        return self.__conn.zkeys(self.name,'','','',limit=100000000)
    @QueueBase.catch
    def zdelSet(self,key):
        return self.__conn.zdel(self.name,key)
    @QueueBase.catch
    def multi_zgetSet(self,*keys):
        return self.__conn.multi_zget(self.name,*keys)
    #Hash
    @QueueBase.catch
    def hgetallHash(self,key):
        return self.__conn.hgetall(key)
    @QueueBase.catch
    def hincrHash(self,name,key):
        return self.__conn.hincr(name,key,amount=1)
    @QueueBase.catch
    def multi_hsetHash(self,name,**mapping):
        return self.__conn.multi_hset(name, **mapping)

    @QueueBase.catch
    def hlistHash(self,start,end):
        return self.__conn.hlist(start, end, limit =  10000000)
    @QueueBase.catch
    def hclearHash(self,key):
        return self.__conn.hclear(key)

    @QueueBase.catch
    def hset(self, key,value):
        return self.__conn.hset(self.name, key,json.dumps(value, ensure_ascii = False).encode('utf-8')
                                if isinstance(value,dict) or isinstance(value, list) else value)

    @QueueBase.catch
    def hsize(self):
        return self.__conn.hsize(self.name)

    @QueueBase.catch
    def hget(self, key = None):
        if key:
            return self.__conn.hget(self.name, key)
        else:
            if self.__conn.hsize(self.name) > 0:
                keys=self.__conn.hkeys(self.name,"", "",limit=1)
                if keys:
                    key=keys[0]
                    v=self.__conn.hget(self.name, key)
                    self.__conn.hdel(self.name, key)
                    return v


