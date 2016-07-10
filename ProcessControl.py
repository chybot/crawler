# -*- coding: utf-8 -*-
# Created by Leo on 16/04/20
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
import time
from multiprocessing import Process

# from CommonLib.ClassFactory import ClassFactory
# from CommonLib.CalcMD5 import calcFileMD5
# from CommonLib.DB.DBManager import DBManager
# from Seed.Seed import Seed
# from CommonLib.WebContent import SeedAccessType
# from CommonLib.UniField import UniField
# from CommonLib.BbdSeedLogApi import get_logs,STATE
# from QyxxReqWorker import work
# from CommonLib.Logging import Logging
import logging
from Config.ConfigGet import ConfigGet

def work(name=None):
    print "Test:",name
    time.sleep(1)


class ProcessControl(object):
    """
    Class for control the processes under different bbd_types
    """

    def __init__(self,
                 work,
                 log_name = "ProcessControl",
                 conf_file = "ItemConfig.ini",
                 conf_key="qyxx",
                 seed_key=None):
        """
        初始化进程管理参数
        :param work:      进程调用的主函数
        :param log_name:  log文件名字
        :param conf_file: 配置文件名字
        :param conf_key:  从配置文件里面获取信息的key,该key定义了加载的爬虫类型和进程数量
        :param seed_key:  该key定义了加载的爬虫需不需要种子
        """
        self.work = work
        self.conf_file = conf_file
        self.logger = logging.getLogger(log_name)
        self.conf_getter = ConfigGet(self.conf_file)
        self.conf_key = conf_key
        self.seed_key = seed_key

    def loadConfig(self):
        """
        get md5 value of  config file use for compare
        :return:
        """
        # self.conf_md5=calcFileMD5(self.conf_file)
        # self.PROV_DICT = config.PROVINCE_INFO_DICT

        self.conf_md5 = self.conf_getter.cfMd5()
        self.PROV_DICT = self.conf_getter.itemsToDict(self.conf_key)
        if self.seed_key:
            self.SEED_DICT = self.conf_getter.itemsToDict(self.seed_key)
        else:
            self.SEED_DICT = None
        
    def startProcess(self,bbd_type, process_name):
        """
        start a process use the bbd_type and name
        :param bbd_type: use to load different kinds of crawlers
        :param process_name: process name for record the info of process
        :return: object which include process info
        """
        if self.SEED_DICT and bbd_type in self.SEED_DICT:
            p = Process(target = self.work, name = process_name, args = (bbd_type, self.SEED_DICT[bbd_type]))
        else:
            p = Process(target = self.work, name = process_name, args = (bbd_type,))
        p.start()
        return p
    def startBulkProcess(self, bbd_type, num,idx=0):
        """
        start a bulk of processes use the bbd_type and number, this method will call startProcess to create processes
        :param bbd_type: used to init instance
        :param num: process numer that want to start
        :param idx: default is 0 for new , if there are already some processes running, please pass the number of running processes here
        :return: a list include processes that succ created and running
        """
        p_list = []
        num=int(num)
        for index in range(0,num):
            p=self.startProcess(bbd_type, bbd_type+":"+str(index+idx))
            p_list.append(p)
        return p_list


    def endTypeProcess(self, bbd_type, p_dict):

        """
        terminate all processes under one bbd_type
        :param bbd_type: process bbd_type
        :param p_dict: dict that contains all process info
        :return: dict which deleted the key of bbd_type
        """
        for process in p_dict[bbd_type]:
            process.terminate()
            process.join()
            log_msg = "Type:" + bbd_type +" PID:"+ str(process.pid)+ " killed"
            self.logger.warning(log_msg)
        del p_dict[bbd_type]
        return p_dict

    def endBulkProcess(self, bbd_type, p_dict,num):
        """
        terminate the number of processes under bbd_type
        :param bbd_type: process bbd_type
        :param p_dict: dict that contains all process info
        :param num: the num of processes want to be killed
        :return: dict that removed the info of killed processes
        """
        p_list = p_dict[bbd_type]
        num = abs(num)
        for process in range(0,num):
            process = p_list.pop()
            process.terminate()
            process.join()
            log_msg = "Type:" + bbd_type + " PID:" + str(process.pid) + " killed"
            self.logger.warning(log_msg)
        p_dict[bbd_type] = p_list
        return p_dict
    # def work(self):
    #     pass
    def run(self):
        """
        main method , create all bbd_types of process and start the monitor
        :return: None
        """
        self.loadConfig()
        process_dict = {}
        for bbd_type, num in self.PROV_DICT.items():
            process_list=self.startBulkProcess(bbd_type,int(num))
            process_dict.update({bbd_type:process_list})
        self.processMonitor(process_dict)

    def processMonitor(self,p_dict):
        """
        monitor the process status
        1. if process is terminated unexpectedly, restart the process
        2. add new processes
        3. kill processes that usr want to kill
        the actions are defined in configuration file
        :param p_dict: dict that include all process infomation
        :return:
        """
        while True:
            self.conf_getter.reload()
            # new_conf_md5 = calcFileMD5(self.conf_file)
            new_conf_md5 = self.conf_getter.cfMd5()
            if self.conf_md5 == new_conf_md5:
                # print "***********************************Condif file no change , print info"
                self.logger.info("configuration file no change , print info, logger=%s",str(self.logger))
                for bbd_type, p_list in p_dict.items():
                    if p_list:
                        for p in p_list:
                            if p.is_alive():
                                log_msg = "[ "+p.name+" ]"+" status: "+ str(p.is_alive())+ " pid: "+ str(p.pid)
                                self.logger.info(log_msg)
                            if not p.is_alive():
                                log_msg = "[ " + p.name + " ]" + " status: Dead " + " pid: " + str(p.pid)
                                self.logger.info(log_msg)
                                new_p = self.startProcess(bbd_type,p.name)
                                log_msg = "Restart"+ "[ " + new_p.name + " ]" + " status: Dead " + " pid: " + str(new_p.pid)
                                self.logger.info(log_msg)
                                p_list.append(new_p)
                        updated_p_list = filter(lambda p:p.is_alive(),p_list)
                        p_dict[bbd_type] = updated_p_list

            else:
                # print "*************************************Condif file changed ,Reload "
                self.logger.info("configuration file changed ,Reload")
                # reload(config)
                # self.NEW_PROV_DICT = config.PROVINCE_INFO_DICT
                self.NEW_PROV_DICT = self.conf_getter.itemsToDict(self.conf_key)
                new_list = self.getNewProvs(self.PROV_DICT, self.NEW_PROV_DICT)
                del_list = self.getDelProvs(self.PROV_DICT, self.NEW_PROV_DICT)
                if not del_list:
                    update_dict = self.getUpdateProvs(self.PROV_DICT, self.NEW_PROV_DICT )
                if new_list:
                    for bbd_type in new_list:
                        p_list = self.startBulkProcess(bbd_type, self.NEW_PROV_DICT[bbd_type])
                        p_dict.update({bbd_type:p_list})
                if del_list:
                    for bbd_type in del_list:
                        p_dict = self.endTypeProcess(bbd_type, p_dict)
                for bbd_type,new_num in update_dict.items():
                    if new_num > 0:
                        p_list = self.startBulkProcess(bbd_type, new_num,idx=len(p_dict[bbd_type]))
                        p_dict[bbd_type].extend(p_list)
                    else:
                        p_dict =    self.endBulkProcess( bbd_type, p_dict,new_num)
                self.PROV_DICT = self.NEW_PROV_DICT
                self.conf_md5 = new_conf_md5
            time.sleep(5)




    def getNewProvs(self,pre_dict, new_dict):
        """
        get new bbd_types
        :param pre_dict: previous dict which include province info
        :param new_dict: new dict which include province info
        :return: new bbd_types stored in a list return [] of no new one
        """
        pre_set = set(pre_dict.keys())
        new_set = set(new_dict.keys())
        return list(new_set - pre_set)

    def getDelProvs(self, pre_dict, new_dict):
        """
        get delete bbd_types
        :param pre_dict: previous dict which include province info
        :param new_dict: new dict which include province info
        :return: deleted bbd_types stored in a list return [] of no delete one
        """
        pre_set = set(pre_dict.keys())
        new_set = set(new_dict.keys())
        return list(pre_set - new_set)
    def getUpdateProvs(self, pre_dict, new_dict):
        """
        get updated info for processes
        :param pre_dict: previous dict which include province info
        :param new_dict: new dict which include province info
        :return: dict include the updated bbd_type and number for processes
        """

        n_dict={}
        for k,v in pre_dict.items():
            if v != new_dict[k]:
                n_dict.update({k:int(new_dict[k])-int(v)})
        return n_dict



if __name__ == "__main__":

    sub= ProcessControl()
    sub.run()
    print "end"
    # print SeedAccessType.OK