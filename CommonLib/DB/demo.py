# -*- coding: utf-8 -*-
__author__ = 'Lvv'

import sys

reload(sys)
sys.setdefaultencoding('utf-8')

from DBManager import DBManager

if __name__ == '__main__':

    db_inst = DBManager.getInstance("mongo","test_new",host = "localhost",port=27017)
    # 3 operate
    db_inst.save({'_id': 'test', 'name': 'BBD'})
    print db_inst.size()
    db_inst.changeTable("test2")
    db_inst.put({'_id': 'test', 'name': 'BBD'})
    # print db_inst.get()
    print db_inst.size()


