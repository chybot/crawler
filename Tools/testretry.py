# -*- coding: utf-8 -*-
# Created by Leo on 16/06/08
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
from CommonLib.retrying import retry
@retry(wait_fixed=2 * 1000)
def fun():
    try:
        raise Exception("xxxxx")
    except Exception as e:
        print str(e)
        raise Exception(e)
if __name__ == '__main__':
    fun()