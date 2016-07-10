# -*- coding: utf-8 -*-
# Created by Leo on 16/04/25
import sys
import os
import inspect

reload(sys)
sys.setdefaultencoding('utf-8')
import inspect
import functools
from retrying import  retry
from Logging import Logging
import time

def catch(func):
    def decorator(*args, **kwargs):

        try:

            return func(*args, **kwargs)
        except Exception as e:
            print str(e)
            if 'ProduceResponse' in str(e):
                return
            if '\'utf8\' codec can\'t decode byte' in str(e):
                return
    return decorator

##################################################################################################

def log(func,logger):
    code = func.func_code
    argcount = code.co_argcount
    argnames = code.co_varnames[:argcount]

    @functools.wraps(func)
    def wrapped(*args, **kwargs):
        # try: log.info
        logger = Logging(name = "Decorator")
        s_time=time.time()
        logger.info('[Enter method: %s]',func.__name__)
        try:

            return func(*args, **kwargs)
        except Exception, e:
            print 'Exception in %s : %s' % (func.__name__, e)
            raise Exception(e)
        finally:
            e_time = time.time()
            logger.info('[Leave method: %s], %s seconds used', func.__name__,str(e_time - s_time) )
    wrapped.func_code.co_argcount = argcount
    wrapped.func_code.co_varnames = argnames
    return wrapped

def trace(cls):
    for name, m in inspect.getmembers(cls, inspect.ismethod):
        setattr(cls,name,log(m))
    return cls


###############Meta Class version######################################################################

class LogMetaclass(type):
    def __new__(cls, name, bases, dct):
        deco_method_dict = ((name, value) for name, value in dct.items() if callable(value))
        attr_dict = dict((name, log(value,"YYYYYYYYY")) for name, value in deco_method_dict)
        normal_member_dict = ((name, value) for name, value in dct.items() if not callable(value))
        attr_dict.update(normal_member_dict)

        return super(LogMetaclass, cls).__new__(cls, name, bases, attr_dict)


# # @trace



if __name__ == '__main__':
    class X(object):
        __metaclass__ = LogMetaclass

        # def __new__(cls, *args, **kwargs):
        #     print "XXXXX"

        def __init__(self, name, id, k1 = None, k2 = None):
            self.name = name
            self.id = id

        # @retry(stop_max_attempt_number =1,wait_fixed = 2 * 1000)
        def first_x_method(self, name):
            # print 'doing first_x_method stuff...',name
            # raise Exception("test")
            pass

        def second_x_method(self):
            # print 'doing second_x_method stuff...'
            # print self.name
            pass
    x = X("XXXXXXXXXX","123",k1="1",k2="2")
    x.first_x_method("first")
    x.second_x_method()