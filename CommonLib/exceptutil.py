# -*- coding: utf-8 -*-
__author__ = 'xww'

import sys,chardet
import traceback

def  traceinfo(e):
    """
    获取异常堆栈信息
    :param e: (Exception) 异常
    :return:  （str) 异常堆栈信息
    """
    exceptionType, exceptionValue, exceptionTraceback = sys.exc_info()
    result=u""

    excep_list=traceback.format_exception(exceptionType, exceptionValue, exceptionTraceback)
    print excep_list

    for ex in  excep_list:
        info = chardet.detect(ex)
        enc= info['encoding']
        result+=ex.decode(enc,"ignore")
    return result

if __name__=="__main__":
    try:
       raise Exception(u"张三")
    except Exception as e:
        print traceinfo(e)





