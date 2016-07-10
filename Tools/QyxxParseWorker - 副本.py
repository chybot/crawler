# -*- coding: utf-8 -*-
# Created by Leo on 16/04/20
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.append("Parser")
import time
from multiprocessing import Process
from CommonLib.retrying import retry
import QyxxParseControlConfig as config
from CommonLib.ClassFactory import ClassFactory
from CommonLib.CalcMD5 import calcFileMD5
from CommonLib.DB.DBManager import DBManager
from CommonLib.UniField import UniField
from Fetcher import Fetcher
from CommonLib.BbdSeedLogApi import get_logs,STATE
from Config.ConfigGet import confGetterFunc

@retry(wait_fixed=2 * 1000)
def work(self, pro_type):
    conf_file = "DBConfig.ini"
    src_db_dict = \
        {
            'type': confGetterFunc(conf_file, 'html_db', 'type').lower(),
            'host': confGetterFunc(conf_file, 'html_db', 'host').lower(),
            'port': int(confGetterFunc(conf_file, 'html_db', 'port'))
        }
    des_db_dict = \
        {
            'type': confGetterFunc(conf_file, 'data_db', 'type').lower(),
            'host': confGetterFunc(conf_file, 'data_db', 'host').lower(),
            'port': int(confGetterFunc(conf_file, 'data_db', 'port'))
        }

    from CommonLib.Logging import Logging
    log=Logging(name = pro_type)

    log.info("Process begin")

    pro_type = pro_type.lower()
    queue_name = pro_type

    module_name = pro_type.capitalize()+"Handler"
    handler = ClassFactory.getClassInst(module_name, package_name = "Parser", pinyin=pro_type.lower())

    # nb_module_name = pro_type.capitalize() +"Nb" + "Handler"
    # nb_handler  = ClassFactory.getClassInst(module_name, package_name = "Parser", pinyin=pro_type.lower())

    normal_table = pro_type + "_data"
    err_table    = normal_table + "_error"

    # db_inst = DBManager.getInstance(des_db_dict["type"], normal_table, host = des_db_dict["host"], port = des_db_dict["port"]) #ssdb 存 解析后数据

    # kfk_inst = DBManager.getInstance("kafka", "qyxx_html", host = "spider7", port = 9092)
    # debug_normal_table =  "new_"+pro_type.lower()+"_data"
    # db_debug = DBManager.getInstance("mongo",debug_normal_table, host = "spider7", port = 27037)# mongo, 数据存本地，用于调试

    # fetch=Fetcher(queue_name.lower() ,"qyxx") enable this if not debug

    fetch = Fetcher(queue_name, "qyxx",get_db_dict = src_db_dict, save_db_dict = des_db_dict) # debug

    while True:
        try:
            # source_dict = fetch.hget()
            source_dict = fetch.get()

            if source_dict:
                # 拷贝 种子信息到解析后的数据里面
                if source_dict.has_key("bbd_seed"):
                    seed_dict = {"bbd_seed": source_dict["bbd_seed"]}
                if source_dict.has_key("BBD_SEED"):
                    seed_dict = {"bbd_seed": source_dict["BBD_SEED"]}
                log_info = get_logs(STATE.BBD_SEED_IS_CRAWL_PARSE_ING, seed_dict)
                log.info(log_info)
                # fetch.backup() # 避免进程异常退出引起的数据丢失
                res_dict = UniField.cloneNeedColumns(source_dict)
                log.info("start to a new seed %s",source_dict)

                #debug
                # db_inst.changeTable("new_"+pro_type.lower())
                # db_inst.save(source_dict);
                # rowkey=source_dict["rowkey"]
                # db_inst.hset(rowkey,source_dict)
                # db_inst.changeTable("new_"+pro_type.lower()+"_processed")
                # db_inst.save(source_dict)
                res_dict = handler.parse(source_dict,res_dict)

                if res_dict["status"]==0:
                    db_inst.changeTable(normal_table)
                    res_dict = UniField.unifyParseResult(res_dict)

                    #for debug
                    db_debug.save(res_dict)

                    # db_inst.save(res_dict)
                    # kfk_inst.save(source_dict)
                    # print "kfk size:",kfk_inst.size()
                    log_info = get_logs(STATE.BBD_SEED_IS_CRAWL_PARSE_SUC, seed_dict)
                    log.info(log_info)
                else:
                    db_inst.changeTable(err_table)
                    res_dict["html"] = source_dict

                    # db_inst.save(res_dict)
                    db_debug.save(res_dict)

                    log_info = get_logs(STATE.BBD_SEED_IS_CRAWL_PARSE_ERO, seed_dict)
                    log.info(log_info)
            else:
                log.info(u"解析%s队列为空， 等待10秒重试",pro_type)
                time.sleep(10)
        except Exception as e:
            print str(e)
            raise Exception(e)
            # db_inst.hset(res_dict["rowkey"], source_dict)

if __name__ == "__main__":

    sub= QyxxParseControl()
    sub.run()
    print "end"
    # print SeedAccessType.OK