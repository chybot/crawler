# -*- coding: utf-8 -*-
# Created by David on 2016/4/15.

import sys
sys.path.append("../")
reload(sys)
import inspect
from CommonLib.exceptutil import traceinfo

def run_function(function, args, log=None):
    '''
    use reflection to run a function
    :param function:
    :param args: the args dictionary, only accept the string as the key value
    :param log: the log object
    :return:
    '''
    if not is_function(function):
        return None
    try:
        varnames = inspect.getargspec(function).args
        # "args['entId'], args['company']"
        var_str = ''
        for varname in varnames:
            # 忽略对象方法中的self参数
            if varname == 'self':
                continue
            # 某些可能不会出现在中间结果集的参数会带默认参数，例如page_no
            if varname not in args:
                continue
            var_str += "args['" + varname + "'], "
        var_str = var_str.rstrip(',')
        if log:
            log.info("使用参数 %s 执行方法 %s" % (','.join(varnames), function.func_name))
        if var_str:
            return apply(function, (eval(var_str)))
        else:
            return apply(function)
    except Exception as e:
        if log:
            log.error(traceinfo(e))
        return None

def is_function(obj):
    """
    determine whether the obj is a function
    :param obj:
    :return:
    """
    is_a_function = hasattr(obj, '__call__')
    return is_a_function

def substring(src, start, end):
    if not src or not start or not end:
        return None
    src = src.strip()
    idx1 = src.find(start)
    idx2 = src.find(end)
    if idx1<0 or idx2<0:
        return None
    return src[idx1+len(start):idx2]

if __name__ == "__main__":
    src = '<a target="_blank" href="/qynb/entinfoAction!qynbxx.dhtml?cid=72cc0c5319274ba8ac2a8ce3758d2eaa&entid=a1a1a1a0213dbb6001213eb6ecef20b4&credit_ticket=0387B24A3FA88371A70DD54FDBFC501D">2013年度</a>'
    start = '">'
    end = '</a'
    href = substring(src, start, end)
    pass
