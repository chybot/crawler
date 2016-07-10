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
from CommonLib.WebContent import SeedAccessType
from Config.ConfigGet import ConfigGet
import warnings
seed_cf = 'DBConfig.ini'
f = lambda x,y,z:ConfigGet(x).get(y,z)

class Seed(object):
    def __init__(self,queue_name):
        self.__db=DBManager.getInstance( f(seed_cf,'seed_db','type'),queue_name,port=f(seed_cf,'seed_db','port'),host=f(seed_cf,'seed_db','host'))
        #self.__solr = DBManager.getInstance('solr','seed',server=["spider7:8983","spider7:8984","spider7:8985"])
        self.queue_name=queue_name
        from CommonLib.Logging import Logging
        self.log = Logging(name = queue_name)
        self.__data_dic={}

    def get(self):
        self.__data__()

    @property
    def __get__(self):
        assert hasattr(self.__db,'get') ,'%s has no attribute get' % self.__db
        for flag in ['_temp','_bug', '_nonstatic', '_static', '_error', '_manyan']:
            self.__db.changeTable(self.queue_name + flag)
            data = self.__db.get()
            if data:
                self.__backup__(data)
                return data
            warnings.warn(self.queue_name + flag + u"队列为空")
        time.sleep(100)
        self.__get__()
    def __backup__(self,data):
        pid = os.getpid()
        self.__db.keySet('seed_%s' % str(pid) + '_' + self.queue_name, data)
    def getDict(self):
        return self.__data_dic
    def __data__(self):
        self.__data_dic={}
        data=self.__get__.decode("UTF-8", "ignore").strip()
        if not isinstance(data,dict):
            if data.startswith('{') and data.endswith('}'):
                self.__data_dic.update(json.loads(data))
            elif len(data)<2 and len(data)>100:
                self.log.error('%s Seed length Error!'%data)
                return
            elif re.match(r"^\d{%d}" % len(data), data):
                self.__data_dic[u"zch"] = data
            elif re.search(u'[\u4e00-\u9fa5].+',unicode(data)):
                self.__data_dic['name'] = data
            elif re.match(u'[\d|\w]{%d}' % len(data),data):
                self.__data_dic['xydm'] = data
            else:
                self.__data_dic['name'] = data
        else:
            self.__data_dic.update(data)

        if 'url' in self.__data_dic:
            self.url_status=True
            self.__setattr__('url',self.__data_dic['url'])
            if 'data' in self.__data_dic:
                self.__setattr__('data',self.__data_dic['data'])
        else:
            self.url_status=False
            self.__setattr__('values',map(lambda x:self.__data_dic[x],filter(lambda x:self.__data_dic.get(x),['xydm','zch','name',])))

    def update(self,*args,**kwargs):
        if args:
            data=filter(lambda x:isinstance(x,dict),args)
            map(lambda x:self.__data_dic.update(x),data)
        if kwargs:
            self.__data_dic.update(kwargs)

    def __save__(self,flag_name):
        """
        for ssdb
        :param flag_name:
        :return:
        """
        self.__db.select_queue(self.queue_name+flag_name)
        self.__db.save(self.__data_dic)
        self.__data_dic={}

    # def __savesolr__(self):
    #     self.__data_dic['do_time'] = time.strftime("%Y-%m-%d")
    #     self.__data_dic['type'] = self.queue_name
    #     for old_k in self.__data_dic:
    #         if old_k == 'id' or old_k.endswith('_seed'):
    #             continue
    #         else:
    #             self.__data_dic[old_k+'_seed'] = self.__data_dic.pop(old_k)
    #
    #     if 'id' not in self.__data_dic:
    #         key_list=['xydm_seed','zch_seed','name_seed','url_seed']
    #         ids = filter(lambda x:x in self.__data_dic,key_list)
    #         if ids:
    #             ids = map(lambda x:self.__solr.find({x:self.__data_dic[x]})['docs'],ids)[0]
    #             if ids:
    #                 self.__data_dic['id']=ids[0][0]['id']
    #     self.__solr.update(self.__data_dic)
    #     self.__data_dic = {}

    def save(self):
        status=int(self.__data_dic.get('status',0))
        if status == 0:
            pass
            #self.__savesolr__()
        elif status == SeedAccessType.ERROR:
            self.__save__('_error')
        elif status == SeedAccessType.NON_COMPANY:
            self.__save__('_noncompany')
        elif status == SeedAccessType.INCOMPLETE:
            self.__save__('_temp')
        elif status == SeedAccessType.NO_TARGET_SOURCE:
            self.__save__('_nosource')
        else:
            self.log.info('Status Error!')
            self.__save__('_unknown')
if __name__ == '__main__':
    solr = Seed('beijing')
    solr.get()
    solr.save()
    print os.getpid()