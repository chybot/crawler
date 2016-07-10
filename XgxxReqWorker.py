# -*- coding: utf-8 -*-
# Created by Leo on 16/04/22
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
from CommonLib.ClassFactory import ClassFactory
from CommonLib.DB.DBManager import DBManager
from Seed.Seed import Seed
from CommonLib.WebContent import SeedAccessType
from CommonLib.UniField import UniField
from CommonLib.BbdSeedLogApi import get_logs, STATE
from CommonLib.retrying import retry
from Config.ConfigGet import confGetterFunc


@retry(wait_fixed=2 * 1000)
def work(bbd_type, need_seed=True, value_list=None):
    """
    爬虫外部控制主函数，包括一下功能：
    1. 初始化爬虫类
    2. 初始化DB连接
    3. 获取种子
    4. 存储爬虫返回的数据
    5. 存储爬取异常的种子信息
    :param bbd_type: 爬虫存储的队列名，也会关联到爬虫模块名，注意*****
    :param value_list: 爬虫种子信息，手动调试使用
    :return:
    """
    conf_file = "DBConfig.ini"
    db_conf_dict = \
        {
            'type': confGetterFunc(conf_file, 'html_db', 'type').lower(),
            'host': confGetterFunc(conf_file, 'html_db', 'host').lower(),
            'port': int(confGetterFunc(conf_file, 'html_db', 'port'))
        }
    seed_db_dict = \
        {
            'type': confGetterFunc(conf_file, 'seed_db', 'type').lower(),
            'host': confGetterFunc(conf_file, 'seed_db', 'host').lower(),
            'port': int(confGetterFunc(conf_file, 'seed_db', 'port'))
        }

    def storeResult(src_dict, company_dict=None):
        """
        回调函数，由爬虫调用，存储数据到ssdb
        :param src_dict:
        :param company_dict:
        :return:
        """
        try:
            if "bbd_tmp_queue" in src_dict:
                queue_name = src_dict["bbd"]

            if src_dict["status"] == 0:
                src_dict = UniField.unifyRequestResult(src_dict, bbd_type)
                if "rowkey" in src_dict.keys():
                    src_dict.update({"bbd_seed": bbd_seed_dict})
                    if 'table_name' in src_dict:
                        table_name = src_dict.get('table_name')
                        db_inst.changeTable(table_name)
                    else:
                        db_inst.changeTable(bbd_type)
                    db_inst.save(src_dict)
                else:
                    raise Exception("No rowkey")
            else:
                db_inst.changeTable(bbd_type + "_error")
                db_inst.save(src_dict)
        except Exception as e:
            log.info(str(e))
            db_inst.changeTable(bbd_type + "_error")
            db_inst.save(src_dict)

    def crawlerKeyWordList(keyword_list):
        """
        一次抓取关键词，如果第一个抓不到，尝试第二个,如果最后一个还是没成功，记录种子信息到ssdb
        :param keyword_list:
        :return:
        """
        keyword_num = len(keyword_list)
        for keyword in keyword_list:
            seed_status = inst.crawl(keyword)
            if seed_status.access_type == SeedAccessType.OK:  # 状态成功，打印消息
                # log.info("End seed with keyword %s", keyword)
                log_info = get_logs(STATE.BBD_SEED_IS_CRAWL_SUC, bbd_seed_dict)
                log.info(log_info)
                break
            elif seed_status.access_type != SeedAccessType.OK and keyword_num > 0:
                keyword_num -= 1
                # log_info = get_logs(STATE.BBD_SEED_IS_CRAWL_ERO, bbd_seed_dict)
                log.info("Use Key word [%s] get company failed", keyword)
                continue
            else:
                seed.update(status=seed_status.access_type)
                log_info = get_logs(STATE.BBD_SEED_IS_CRAWL_ERO, bbd_seed_dict)
                log.info(log_info)
                seed.save()

    ##################################################################################################################################
    try:
        from CommonLib.Logging import Logging
        log = Logging(name=bbd_type)
        log.info("Process begin for %s,logger=%s", bbd_type, str(log))

        module_name = "Crawler" + bbd_type.capitalize()
        bbd_type = bbd_type.lower()
        inst = ClassFactory.getClassInst(module_name,
                                         package_name="xgxx",
                                         pinyin=bbd_type,
                                         callbackFromOuterControl=storeResult)
        db_inst = DBManager.getInstance(db_conf_dict["type"],
                                        bbd_type,
                                        host=db_conf_dict["host"],
                                        port=db_conf_dict["port"])
        if not need_seed:
            inst.crawl()
        else:
            bbd_seed_dict = {}
            if value_list:
                for keywd_list in value_list:
                    crawlerKeyWordList(keywd_list)
            else:
                seed_db_inst = DBManager.getInstance(seed_db_dict["type"],
                                                     bbd_type,
                                                     host=seed_db_dict["host"],
                                                     port=seed_db_dict["port"])
                while True:
                    bbd_seed_dict = seed_db_inst.get()
                    # log_info = get_logs(STATE.BBD_SEED_IS_CRAWL_ING, bbd_seed_dict)
                    # log.info("start to a new seed %s",log_info)
                    seed_status = inst.crawl(bbd_seed_dict)
                    if seed_status.access_type == SeedAccessType.OK:  # 状态成功，打印消息
                        log_info = get_logs(STATE.BBD_SEED_IS_CRAWL_SUC, bbd_seed_dict)
                        log.info(log_info)
                    else:  # 用url没有抓成功， 用keywordlist 抓
                        log.info(u"种子抓取失败，存取到相应队列 [%s]", bbd_type)
                        seed_db_inst.changeTable(bbd_type + "_error")
                        seed_db_inst.save(bbd_seed_dict)

    except Exception as e:
        raise Exception(e)


if __name__ == '__main__':
    """

    """

    bbd_type = "Jyyc"
    DEBUG = 1
    if DEBUG:
        ll = [['{"tianjin": "1"}']]
        rowkey = work(bbd_type, value_list=ll)
    else:
        # seed.get()
        rowkey = work(bbd_type)
