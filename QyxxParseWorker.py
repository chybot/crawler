# -*- coding: utf-8 -*-
# Created by Leo on 16/04/20
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.append("Parser")
import time
from CommonLib.retrying import retry
from CommonLib.ClassFactory import ClassFactory
from CommonLib.DB.DBManager import DBManager
from CommonLib.UniField import UniField
from Fetcher import Fetcher
from CommonLib.BbdSeedLogApi import get_logs,STATE
from Config.ConfigGet import confGetterFunc

@retry(wait_fixed=2 * 1000)
def work(bbd_type):
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
    log=Logging(name = bbd_type)
    log.info("Process begin")

    bbd_type = bbd_type.lower()
    queue_name = bbd_type
    bbd_table = "qyxx_data"
    bbd_src_table = "qyxx_html"
    module_name = bbd_type.capitalize()+"Handler"
    handler = ClassFactory.getClassInst(module_name, package_name = "Parser", pinyin=bbd_type.lower())

    normal_table = bbd_type + "_data"
    err_table    = normal_table + "_error"
    # html_normal_table = bbd_type+"_src"
    

    des_db_inst = DBManager.getInstance(des_db_dict["type"], bbd_table, host = des_db_dict["host"], port = des_db_dict["port"]) #存 解析后数据
    err_db_inst = DBManager.getInstance(src_db_dict["type"], err_table, host = src_db_dict["host"],    port = src_db_dict["port"])

    fetch = Fetcher(queue_name, "qyxx",get_db_dict = src_db_dict, save_db_dict = des_db_dict) # debug

    while True:
        try:
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
                res_dict.update(seed_dict)
                log.info("start to a new seed %s",seed_dict)

                res_dict = handler.parse(source_dict,res_dict)
                if res_dict["status"]==0:
                    res_dict = UniField.unifyParseResult(res_dict, bbd_table = bbd_table)
                    des_db_inst.changeTable(bbd_table)
                    des_db_inst.save(res_dict)
                    log.info(u"插入数据到 [%s] 成功, 队列大小为: %s ", bbd_table, str(des_db_inst.size()))
                    des_db_inst.changeTable(bbd_src_table)
                    des_db_inst.save(source_dict)
                    log.info(u"插入数据到 [%s] 成功, 队列大小为: %s ", bbd_src_table, str(des_db_inst.size()))
                    log_info = get_logs(STATE.BBD_SEED_IS_CRAWL_PARSE_SUC, seed_dict)
                    log.info(log_info)
                else:
                    source_dict["data"] = res_dict
                    err_db_inst.save(source_dict)
                    log_info = get_logs(STATE.BBD_SEED_IS_CRAWL_PARSE_ERO, seed_dict)
                    log.info(log_info)
            else:
                log.info(u"解析%s队列为空， 等待10秒重试",bbd_type)
                time.sleep(10)
        except Exception as e:
            log.info(str(e))
            source_dict["data"] = res_dict
            err_db_inst.save(source_dict)
            raise Exception(e)
            # db_inst.hset(res_dict["rowkey"], source_dict)

if __name__ == "__main__":


    print "end"
    # print SeedAccessType.OK