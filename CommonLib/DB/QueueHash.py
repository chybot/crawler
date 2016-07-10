# -*- coding: utf-8 -*-
__author__ = 'Lvv'

import QueueBase
from ssdb.connection import BlockingConnectionPool
from ssdb import SSDB
import json
import uuid


class QueueHash(QueueBase.QueueBase):
    def __init__(self, name, host='localhost', port=8888, **kwargs):
        QueueBase.QueueBase.__init__(self, name, host, port)
        self.__conn = SSDB(connection_pool=BlockingConnectionPool(host=self.host, port=self.port))

    @QueueBase.catch
    def put(self, value, *args, **kwargs):
        if isinstance(value, dict):
            key = value.get('_id', str(uuid.uuid1()))
        elif isinstance(value, basestring):
            try:
                tmp = json.loads(value)
                if isinstance(tmp, dict):
                    key = tmp.get('_id', str(uuid.uuid1()))
                else:
                    key = str(uuid.uuid1())
            except:
                key = str(uuid.uuid1())
        else:
            key = str(uuid.uuid1())
        return self.__conn.hset(self.name, key, value if isinstance(value, basestring) else json.dumps(value, ensure_ascii=False).encode('utf-8'))

    @QueueBase.catch
    def get(self, *args, **kwargs):
        tmp = self.__conn.hscan(self.name, '', '', limit=1)
        if not tmp:
            return None
        try:
            self.__conn.hdel(self.name, tmp.keys()[0])
        except Exception as e:
            print str(e)
            return None
        return tmp.values()[0]

    @QueueBase.catch
    def size(self, *args, **kwargs):
        return self.__conn.hsize(self.name)