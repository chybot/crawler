# -*- coding: utf-8 -*-
"""
企业信息网种子模块
"""
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import json
import re
import time
import os

sys.path.append("../")
from CommonLib.DB.DBManager import DBManager
from CommonLib.Logging import Logging
import json


class Fetcher(object):
    def __init__(self,queue_name, sub_type,get_db_dict=None, save_db_dict=None):
        # config = __import__("FetchConfig")
        # get_db_dict = config.QYXX_GET_DB
        # save_db_dict = config.QYXX_PUT_DB
        self.logger = Logging(__name__)
        # queue_name = queue_name # for debug
        self.__get_db = DBManager.getInstance(get_db_dict["type"],
                                              queue_name,
                                              port = get_db_dict["port"],
                                              host=get_db_dict["host"])
        # self.__save_db = DBManager.getInstance(get_db_dict["type"],
        #                                        queue_name,
        #                                        port = get_db_dict["port"],
        #                                        host = get_db_dict["host"])
        self.queue_name=queue_name
        self.__data_dic={}

    def get(self):
        item = self.__get_db.get()
        # self.__get_db.save(item) # 临时存放一下，debug
        if item:
            self.__data_dic = json.loads(item)
            return self.__data_dic



    def update(self,*args,**kwargs):
        if args:
            data=filter(lambda x:isinstance(x,dict),args)
            map(lambda x:self.__data_dic.update(x),data)
        if kwargs:
            self.__data_dic.update(kwargs)


    def save(self,data_dict=None):
        if data_dict:
            self.__get_db.save(data_dict)
        else:
            self.__get_db.save(self.__data_dic)
    def backup(self):
        k="html_"+str (os.getpid())+"_" + self.queue_name
        self.__get_db.keySet(k, self.__data_dic)
    def hget(self,key=None):
        
       item = self.__get_db.hget(key = key)
       if item:
           self.__data_dic = json.loads(item)
           return self.__data_dic
       else:
           self.logger.warning("%s hash is empty ,please check",self.queue_name)

if __name__ == '__main__':
    fetcher = Fetcher('shanghai',"qyxx")
    gt=fetcher.get()
    fetcher.save()