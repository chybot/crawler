# -*- coding: utf-8 -*-
"""
企业信息网种子清理模块
"""
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import re
from seed_config import port,host
sys.path.append("../")
from CommonLib.DB.DBManager import DBManager

import logging

log = logging.getLogger(__name__)
class SeedClean(object):
    def __init__(self):
        self.__ssdb=DBManager.getInstance('ssdb','test',port=port,host=host)

    def run(self):
        keys=self.__ssdb.keyKeys()
        map(lambda x:self.run1(x),keys)
    def run1(self,key):
        if 'seed' in key:
            queue = re.sub(ur'seed\_\d*_','',key)+'_error'
            self.__ssdb.changeTable(queue)
            self.__ssdb.put(self.__ssdb.keyGet(key))
            self.__ssdb.keyDel(key)

if __name__ == '__main__':
    s=SeedClean()
    s.run()
