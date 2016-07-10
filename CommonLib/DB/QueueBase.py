# -*- coding: utf-8 -*-
__author__ = 'Lvv'

from abc import ABCMeta, abstractmethod
import time
import warnings

def catch(func):
    def decorator(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            warnings.warn(str(e))
            if 'ProduceResponse' in str(e):
                return
            if '\'utf8\' codec can\'t decode byte' in str(e):
                return
            time.sleep(5)
    return decorator


class QueueBase(object):
    __metaclass__ = ABCMeta

    def __init__(self, name, host, port):
        self.name = name
        self.host = host
        self.port = port

    @abstractmethod
    def put(self, value, *args, **kwargs):
        pass

    @abstractmethod
    def get(self, *args, **kwargs):
        pass

    @abstractmethod
    def size(self, *args, **kwargs):
        pass