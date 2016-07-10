# -*- coding: utf-8 -*-
# Created by Leo on 16/04/22
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
from CommonLib.retrying import retry
from CommonLib.ClassFactory import ClassFactory
from CommonLib.DB.DBManager import DBManager
from Seed.Seed import Seed
from CommonLib.WebContent import SeedAccessType
from CommonLib.UniField import UniField
from CommonLib.BbdSeedLogApi import get_logs,STATE

def work(pro_type,seed=None):
    def storeResult(src_dict, company_dict = None):
        # if company_dict.has_key(u"名称"):
        #     src_dict.update({"company_name": company_dict[u"名称"]})
        #     src_dict.update({"values":company_dict})

        src_dict = UniField.unifyRequestResult(src_dict, pro_type)
        if src_dict.has_key("rowkey"):

            rowkey = src_dict["rowkey"]
            print "统一字段后 rowkey=", rowkey
            src_dict.update({"BBD_SEED": seed.getDict()})
            if src_dict["status"] == 0:
                db_inst.changeTable("new_" + pro_type)
                db_inst.hset(rowkey,src_dict)
                db_inst.save(src_dict)
                
            else:
                db_inst.changeTable("new_" + pro_type + "_error")
                db_inst.hset(rowkey,src_dict)
                db_inst.save(src_dict)
            print "rowkey=", rowkey
        else:
            print "No Rowkey ,抓取后的结果为：", src_dict

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
                log_info = get_logs(STATE.BBD_SEED_IS_CRAWL_SUC, seed.getDict())
                log.info(log_info)
                break
            elif seed_status.access_type != SeedAccessType.OK and keyword_num > 0:
                keyword_num -= 1
                # log_info = get_logs(STATE.BBD_SEED_IS_CRAWL_ERO, seed.getDict())
                log.info("Use Key word [%s] get company failed", keyword)
                continue
            else:
                seed.update(status = seed_status.access_type)
                log_info = get_logs(STATE.BBD_SEED_IS_CRAWL_ERO, seed.getDict())
                log.info(log_info)
                seed.save()
    try:
        from CommonLib.Logging import Logging
        log=Logging(name = pro_type)
        log.info("Process begin for %s",pro_type)

        module_name = "Crawler" + pro_type.capitalize()
        pro_type=pro_type.lower()
        inst = ClassFactory.getClassInst(module_name, package_name = "qyxx_all", pinyin=pro_type,callbackFromOuterControl =storeResult )
        db_inst = DBManager.getInstance("ssdb", "new_"+pro_type, host = "spider5", port = 57888)
        if seed is None:
            seed = Seed(pro_type)
            seed.get()
        else:
            seed = seed

            # log_info = get_logs(STATE.BBD_SEED_IS_CRAWL_ING, seed.getDict())
            # log.info("start to a new seed %s",log_info)
            # if seed.url_status:
            #     seed_status = inst.crawlUrl(seed.url, seed.name)
            #     if seed_status.access_type == SeedAccessType.OK:  # 状态成功，打印消息
            #         log_info = get_logs(STATE.BBD_SEED_IS_CRAWL_SUC, seed.getDict())
            #         log.info(log_info)
            #     else:# 用url没有抓成功， 用keywordlist 抓
            #         log.info(" Url get company info failed  [%s]", pro_type)
            #         keyword_list = seed.values
            #         crawlerKeyWordList(keyword_list)
            # else:
            keyword_list = seed.values
            crawlerKeyWordList(keyword_list)

    except Exception as e:
        print str(e)

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
    pro_type="beijing"
    seed = Seed(pro_type)
    dic={"url_status":False}
    seed.update(dic)
    ll=[u"北京空港科技园区股份有限公司"]
    # seed.update(dic)
    # setattr(seed,"values",ll)
    while 1:
        seed.get()
        rowkey=work(pro_type,seed=seed)