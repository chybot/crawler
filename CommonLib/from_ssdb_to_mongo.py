#-*- coding:utf-8 -*-
__author__ = 'liang'

import sys
reload(sys)
sys.setdefaultencoding("UTF-8")
sys.path.append('../')
import time
import json
import os
import re
from common import mongoutil
from common import exceputil
from common import fileutil
from common import ssdbutil2
from common.functions import  get_logger
import config
import pickle
from json import JSONEncoder
import pymongo
import happybase

class SSDBToMongo(object):
    def __init__(self,queue_name):
        fileutil.mkdirs(queue_name)
        self.logging = get_logger(queue_name + '/' + 'ssdb_save')
        # if queue_name == u'shanghai_2':
        #     self.queue_name = 'shanghai_2'
        # else:
        self.queue_name = queue_name
        self.db_name = 'bigdata_higgs_' + queue_name

        self.logging.info(self.db_name)
        while True:
            try:
                self.logging.info(u'连接mongo')
                self.mongo = mongoutil.getmondbv2(config.mongo_host, config.mongo_port, self.db_name, config.table_name, username=config.mongo_username, password=config.mongo_passwd)
                break
            except Exception as e:
                self.logging.error(u'连接mongo异常 %s' % exceputil.traceinfo(e))
                time.sleep(60)
                continue

        while True:
            try:
                self.logging.info(u'连接ssdb')
                self.ssdb = ssdbutil2.getSSDBQueuev2(self.queue_name, host= config.ssdb_host, port= config.ssdb_port)
                break
            except Exception as e:
                self.logging.error(u'连接ssdb异常 %s' % exceputil.traceinfo(e))
                time.sleep(60)
                continue

    def get_all_from_ssdb(self):
        ssdb_list = []
        while True:
            try:
                data = self.ssdb.get()
                if data != None and len(data) > 0:
                    ssdb_list.append(pickle.loads(data[0]))

                if self.ssdb.size() == 0:
                    break
            except Exception as e:
                self.logging.error(u'获取剩余全部队列数据异常 %s' % exceputil.traceinfo(e))
                time.sleep(60)
                self.ssdb = ssdbutil2.getSSDBQueuev2(self.queue_name, host= config.ssdb_host, port= config.ssdb_port)
        return ssdb_list

    #从ssdb中获取数据
    def get_data_from_ssdb(self):
        ssdb_list = []
        count = 1000
        retry_count = 10
        while True:
            try:
                count -= 1
                if count >= 0:
                    data = self.ssdb.get()
                    if data != None and len(data) > 0:
                        ssdb_list.append(pickle.loads(data[0]))
                else:
                    break
            except Exception as e:
                self.logging.error(u'从ssdb中弹出数据异常 %s' % exceputil.traceinfo(e))
                retry_count -= 1
                if retry_count > 0:
                    time.sleep(60)
                    self.ssdb = ssdbutil2.getSSDBQueuev2(self.queue_name, host=config.ssdb_host, port=config.ssdb_port)

        return ssdb_list

    def save_single_data(self):
        while True:
            try:
                pass
            except Exception as e:
                self.logging.error()

    def get_index_and_other_list(self, key, data_list):
        try:
            i = 0
            for data in data_list:
                i += 1
                if key == data['_id']:
                    return data, data_list[i:]
        except Exception as e:
            self.logging.error(u'获取列表剩余异常 %s' % exceputil.traceinfo(e))

    def save_data(self, last_failure_file = 'ssdb_mongo.data', wait_time = 300):
        if os.path.exists(last_failure_file) == True:
            failed_list = []
            count = 0
            with open(last_failure_file, 'rb') as f:
                for line in f:
                    failed_list.append(self.json_to_dict(line.strip().strip('\n')))
                    count += 1
            while True:
                try:
                    self.logging.info('Last Failed File :%d' % len(failed_list))
                    if failed_list != None and len(failed_list) > 0:
                        for data in failed_list:
                            if data == None:
                                continue
                            if '_id' in data.keys():
                                _id = data['_id']
                            else:
                                _id = None
                            if isinstance(data,dict) and _id != None:
				try:
                                    self.mongo.table.update({'_id':_id},data,True)
                                    self.logging.info(u'成功update一条数据:%s' % _id)
				except Exception,e:
				    self.logging.info(u'fail-update一条数据:%s' % _id)
                        os.remove(last_failure_file)
                        # insert_ret = self.mongo.table.insert(failed_list,safe = True)
                        # if count - len(insert_ret) < 10 and count - len(insert_ret) >= 0:
                        #     os.remove(last_failure_file)
                        #     break
                        # else:
                        #     time.sleep(5)
                        #     continue
                    break
                except pymongo.errors.OperationFailure as e:
#                    self.logging.error(exceputil.traceinfo(e))
                    if e != None and e != '':
                        self.logging.info(e)
                        _id = re.findall(r'.*?dup key:.*?\{.*?:.*?\"(.*?)\".*?\}', str(e))
                        self.logging.info('_id:%s' % _id[0])
                        if len(_id) > 0:
                            update_data,other_list = self.get_index_and_other_list(_id[0], failed_list)
                            if update_data != None:
                                self.mongo.table.update({'_id':update_data['_id']},update_data,True)
                                self.logging.info(u'update data:%s 成功' % _id[0])
                                if other_list != None and len(other_list) > 0:
                                    failed_list = other_list
                                else:
                                    break
                                continue
                            else:
                                break
                        else:
                            break
                except Exception as e:
                    self.logging.error(u'存mongo数据异常 %s' % exceputil.traceinfo(e))
                    time.sleep(5)
                    self.mongo = mongoutil.getmondbv2(config.mongo_host, config.mongo_port, self.db_name, config.table_name, username=config.mongo_username, password=config.mongo_passwd)

        count_time = 0
        while True:
            data_list = []
            while True:
                try:
                    if count_time * 60 > wait_time and self.ssdb.size() < 1000 and self.ssdb.size() > 0:
                        data_list = self.get_all_from_ssdb()
                        if data_list != None and len(data_list) > 0:
                            count_time = 0
                            with open(last_failure_file, 'wb') as f:
                                other_list = [JSONEncoder().encode(line)+'\n' for line in data_list]
                                f.writelines(other_list)
                        break

                    if self.ssdb.size() >= 1000:
                        start_time = time.time()
                        data_list = self.get_data_from_ssdb()
                        if data_list != None and len(data_list) > 0:
                            count_time = 0
                            with open(last_failure_file, 'wb') as f:
                                other_list = [JSONEncoder().encode(line) + '\n' for line in data_list]
                                f.writelines(other_list)
                        self.logging.info(u'获取一千个数据')
                        end_time = time.time()
                        self.logging.info(u'获取一千条数据消耗时间为:%d' % (end_time - start_time))
                        break
                    else:
                        self.logging.info(u'休眠5s,等待数据')
                        count_time += 1
                        time.sleep(5)
                        continue
                except Exception as e:
                    self.logging.error(u'取数据异常 %s' % exceputil.traceinfo(e))
                    time.sleep(30)
                    self.ssdb = ssdbutil2.getSSDBQueuev2(self.queue_name, host=config.ssdb_host, port=config.ssdb_port)

            start_time = None
            end_time_1 = None
            end_time_2 = None
            while True:
                try:
                    if data_list != None and len(data_list) > 0:
                        count = len(data_list)
                        start_time = time.time()
                        for data in data_list:
                            if data == None:
                                continue
                            if '_id' in data.keys():
                                _id = data['_id']
                            else:
                                _id = None
                            if isinstance(data,dict) and _id != None:
				try:
                                    self.mongo.table.update({'_id':_id}, data, True)

                                    # add hbase
                                    company_name = _id.split('|')[0]
                                    m = hashlib.md5()
                                    m.update(company_name.encode('utf-8'))
                                    row = m.hexdigest() + '|_|' + _id
                                    self.put(b, row, data)
                                    # add hbase

                                    self.logging.info(u'成功update一条数据:%s' % _id)
				except Exception,e:
				    self.logging.info(u'失败update一条数据:%s' % _id)
                        end_time_1 = time.time()
                        self.logging.info(u'update 1000 records count:%f' % (end_time_1 - start_time))
                        os.remove(last_failure_file)
                        # insert_ret = self.mongo.table.insert(data_list,safe=True)
                        # end_time_1 = time.time()
                        # self.logging.info('Insert time count: %f' (end_time_1 - start_time))
                        # self.logging.info(len(insert_ret))
                        # if count - len(insert_ret) < 10 and count - len(insert_ret) >= 0:
                        #     os.remove(last_failure_file)
                        #     break
                        # else:
                        #     time.sleep(10)
                        #     continue
                    break
                except pymongo.errors.OperationFailure as e:
                    end_time_2 = time.time()
                    self.logging.info(u'Bad time count:%f' % (end_time_2 - start_time))
                    self.logging.error(exceputil.traceinfo(e))
                    if e != None and e != '':
                        _id = re.findall(r'.*?dup key:.*?\{.*?:.*?\"(.*?)\".*?\}', str(e))
                        if len(_id) > 0:
                            update_data,other_list = self.get_index_and_other_list(_id[0], data_list)
                            if update_data != None:
                                self.mongo.table.update({'_id':update_data['_id']},update_data,True)

                                # add hbase
                                company_name = update_data['_id'].split('|')[0]
                                m = hashlib.md5()
                                m.update(company_name.encode('utf-8'))
                                row = m.hexdigest() + '|_|' + update_data['_id']
                                self.put(b, row, update_data)
                                # add hbase

                                self.logging.info(u'成功update一条数据')
                            if other_list != None and len(other_list) > 0:
                                data_list = other_list
                                continue
                            else:
                                break
                        else:
                            break
                except Exception as e:
                    self.logging.error(u'存mongo数据异常 %s' % exceputil.traceinfo(e))
                    time.sleep(5)
                    self.mongo = mongoutil.getmondbv2(config.mongo_host, config.mongo_port, self.db_name, config.table_name, username=config.mongo_username, password=config.mongo_passwd)

    def json_to_dict(self, data):
        try:
            if data != None:
                data_dict = json.loads(data)
                if data_dict != None:
                    return data_dict
            else:
                return None
        except Exception as e:
            self.logging.error(u'转换dict异常 %s' % exceputil.traceinfo(e))

    def put(table, row, map, charset='utf-8'):
        temp = {}
        for k,v in map.items():
            if isinstance(v, unicode): 
                temp[(u'f1:'+k).encode(charset)] = v.encode(charset)
            else:
                temp[(u'f1:'+k).encode(charset)] = str(v)
        table.put(row.encode(charset), temp)

def main():
    if len(sys.argv) < 2:
        print u'usage: python from_ssdb_to_mongo.py xxx'
        return
    province_name = sys.argv[1]
    print u'队列名为:%s' % province_name
    last_failure_file = province_name + '/ssdb_mongo.data'
    stm = SSDBToMongo(province_name)
    stm.save_data(last_failure_file=last_failure_file, wait_time=60)

if __name__ == '__main__':
    main()
#     data = {'_id':1,'ss':2}
#     data = pickle.dumps(data)
#
#     print pickle.loads(data)['_id']
