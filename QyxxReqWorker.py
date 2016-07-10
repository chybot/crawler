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
from CommonLib.BbdSeedLogApi import get_logs,STATE
from CommonLib.retrying import retry
from Config.ConfigGet import confGetterFunc
from CommonLib.NbxxApiControler import NbxxApiControler


@retry(wait_fixed=2 * 1000)
def work(bbd_type, value_list = None):
    conf_file = "DBConfig.ini"
    db_conf_dict = \
        {
            'type':confGetterFunc(conf_file, 'html_db', 'type').lower(),
            'host':confGetterFunc(conf_file, 'html_db', 'host').lower(),
            'port':int(confGetterFunc(conf_file, 'html_db', 'port'))
        }

    def getNbxxDict(src_dict):
        nbxx_key_list = filter(lambda x:x.startswith("qynb_"), src_dict.keys())
        nbxx_list = map(lambda x:{x:src_dict.pop(x)}, nbxx_key_list)
        return nbxx_list
    def getYear(nb_dict):
        key = nb_dict.keys()[0]
        year = key.split("_")[1]
        return year
    def storeResult(src_dict,company_dict=None):
        """
        回调函数，由爬虫调用，存储数据到ssdb
        :param src_dict:
        :param company_dict:
        :return:
        """
        try:
            if src_dict["status"] == 0:
                src_dict = UniField.unifyRequestResult(src_dict,bbd_type)
                if src_dict.has_key("rowkey"):
                    rowkey = src_dict["rowkey"]

                    nbxx_list = getNbxxDict(src_dict)
                    nb_year_list = []   # 用来向solr接口发送信息
                    for nb_item in nbxx_list:
                        # 拆分年报成单独的数据条目，使用不同的rowkey, 放入hash
                        year = getYear(nb_item)
                        nb_year_list.append(year)
                        nbxx_dict = UniField.cloneNeedColumns(src_dict)
                        nbxx_dict.update({"bbd_seed": bbd_seed_dict})
                        nbxx_dict.update(nb_item)
                        db_inst.changeTable(bbd_type + "_nbxx")
                        nb_rk = rowkey+"|_|"+year
                        nbxx_dict["rowkey"] = nb_rk
                        nbxx_dict["year"] = year
                        db_inst.hset(nb_rk, nbxx_dict)
                        log.info(u"存储 %s 年年报 成功，rowkey 为 [ %s ]",year, nb_rk)
                    zch=src_dict["rowkey_dict"]["company_zch"]
                    company_name= src_dict["rowkey_dict"]["company_name"]

                    log_info = get_logs(STATE.BBD_SEED_IS_CRAWL_ING, bbd_seed_dict)
                    log.info(log_info)
                    src_dict.update({"bbd_seed":bbd_seed_dict})
                    db_inst.changeTable(bbd_type)
                    db_inst.save(src_dict)
                    log.info(u" ，rowkey 为 [ %s ]", rowkey)
                    NbxxApiControler().nbUpdate(company_name = company_name, pinyin = bbd_type, zch = zch,
                                            years_list = nb_year_list)

                else:
                    raise Exception("No rowkey")
            else:
                db_inst.changeTable(bbd_type + "_error")
                db_inst.save(src_dict)
        except Exception as e:
            log.info(str(e))
            db_inst.changeTable(bbd_type + "_error")
            db_inst.save(src_dict)

            log.info(u"存储抓取网页原文 失败，rowkey 为 [ %s ]", rowkey)

    def crawlerKeyWordList(keyword_list):
        """
        一次抓取关键词，如果第一个抓不到，尝试第二个,如果最后一个还是没成功，记录种子信息到ssdb
        :param keyword_list:
        :return:
        """
        try:
            keyword_num = len(keyword_list)
            for keyword in keyword_list:
                keyword_num -= 1
                seed_status = inst.crawl(keyword)
                if seed_status.access_type == SeedAccessType.OK: # 状态成功，打印消息
                    # log.info("End seed with keyword %s", keyword)
                    log_info = get_logs(STATE.BBD_SEED_IS_CRAWL_SUC, bbd_seed_dict)
                    log.info(log_info)
                    log.info(u"种子抓取成功:)")
                    break
                elif seed_status.access_type != SeedAccessType.OK and keyword_num >0:

                    # log_info = get_logs(STATE.BBD_SEED_IS_CRAWL_ERO, bbd_seed_dict)
                    log.info(u"种子抓取失败，关键字 [%s]",keyword)
                    continue
                else:
                    seed.update(status = seed_status.access_type)
                    log_info = get_logs(STATE.BBD_SEED_IS_CRAWL_ERO, bbd_seed_dict)
                    log.info(log_info)
                    log.info(u"种子抓取失败，存储到队列，种子状态为 %s",str(seed_status))
                    seed.save()
        except Exception as e:
            log.info(str(e))
            raise Exception(u"种子抓取过程中遇到异常")
    ##################################################################################################################################
    try:
        from CommonLib.Logging import Logging
        log=Logging(name = bbd_type)
        log.info("Process begin for %s,logger=%s",bbd_type,str(log))

        module_name = "Crawler" + bbd_type.capitalize()
        bbd_type=bbd_type.lower()
        inst = ClassFactory.getClassInst(module_name, package_name = "qyxx_all", pinyin=bbd_type,callbackFromOuterControl =storeResult )
        db_inst = DBManager.getInstance(db_conf_dict["type"], bbd_type, host = db_conf_dict["host"], port = db_conf_dict["port"])
        bbd_seed_dict = {}
        if value_list:
            for keywd_list in value_list:
                crawlerKeyWordList(keywd_list)
        else:
            seed = Seed(bbd_type)

            while True:
                seed.get()
                bbd_seed_dict = seed.getDict()
                log_info = get_logs(STATE.BBD_SEED_IS_CRAWL_ING, bbd_seed_dict)
                log.info("starting a new seed %s",log_info)
                if seed.url_status:
                    seed_status = inst.crawlUrl(seed.url, seed.name)
                    if seed_status.access_type == SeedAccessType.OK:  # 状态成功，打印消息
                        log_info = get_logs(STATE.BBD_SEED_IS_CRAWL_SUC, bbd_seed_dict)
                        log.info(log_info)
                    else:  # 用url没有抓成功， 用keywordlist 抓
                        log.info(" Url get company info failed  [%s]", bbd_type)
                        keyword_list = seed.values
                        crawlerKeyWordList(keyword_list)
                else:
                    keyword_list = seed.values
                    crawlerKeyWordList(keyword_list)
    except Exception as e:
        log.info(str(e))
        seed.save()
        raise Exception(e)

if __name__ == '__main__':
    """
    北京天星资本股份有限公司
    北京奇虎三六零投资管理有限公司
    北京梅牡易贷科技服务有限公司
    北京掌众金融信息服务有限公司
    中国光大银行股份有限公司
    北京铭峰科技有限公司
    民航投资管理有限公司
    胜道（北京）科技有限公司
    中国石油天然气股份有限公司
    核建清洁能源有限公司
    中国中化集团公司
    北京奥博华电子电器有限责任公司
    北京空港科技园区股份有限公司
    中国石油天然气股份有限公司
    核建清洁能源有限公司
    中国中化集团公司

    """

    bbd_type="shanghai"
    DEBUG = 1
    if DEBUG:
        ll = [ [u"91310115630468169D"],  [u"小米科技"],]
        rowkey=work(bbd_type,value_list = ll)
    else:
        # seed.get()
        rowkey = work(bbd_type)