# -*- coding: utf-8 -*-
__author__ = 'xww'
import sys
reload(sys)
sys.path.append('../')
sys.setdefaultencoding("UTF-8")
import time
from common import mongoutil
import csv

def insert_to_mongo():
    mongodb=mongoutil.getmondbv2("localhost",27017,"bigdata_higgs","qyxx_shangshihangyefenxi")
    reader = csv.DictReader(file(u'c:/企业分类数据.csv', 'r'))


    for d in reader:
        del d[""]
        id=d['股票代码']

        d['股票代码']=id.split(".")[0]
        d["交易所编号"]=id.split(".")[1]
        d["uptime"]=time.time()
        mongoutil.updatev3(mongodb,id,d)






if __name__=="__main__":
    insert_to_mongo()
