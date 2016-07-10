# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     CrawlerJyycTester.py
   Description :  
   Author :       JHao
   date：          2016/6/17
-------------------------------------------------
   Change Activity:
                   2016/6/17: 
-------------------------------------------------
"""
__author__ = 'JHao'
import sys
import json

reload(sys)
sys.path.append('../../')
sys.setdefaultencoding('utf-8')

from xgxx.qyxx_jyyc.crawler.CrawlerJyycHebei import CrawlerJyycHebei
from xgxx.qyxx_jyyc.crawler.CrawlerJyycZongju import CrawlerJyycZongju
from xgxx.qyxx_jyyc.crawler.CrawlerJyycBeijing import CrawlerJyycBeijing
from xgxx.qyxx_jyyc.crawler.CrawlerJyycTianjin import CrawlerJyycTianjin
from xgxx.qyxx_jyyc.crawler.CrawlerJyycNeimenggu import CrawlerJyycNeimenggu
from xgxx.qyxx_jyyc.crawler.CrawlerJyycLiaoning import CrawlerJyycLiaoning
from xgxx.qyxx_jyyc.crawler.CrawlerJyycJilin import CrawlerJyycJilin
from xgxx.qyxx_jyyc.crawler.CrawlerJyycHeilongjiang import CrawlerJyycHeilongjiang
from xgxx.qyxx_jyyc.crawler.CrawlerJyycShanghai import CrawlerJyycShanghai
from xgxx.qyxx_jyyc.crawler.CrawlerJyycJiangsu import CrawlerJyycJiangsu
from xgxx.qyxx_jyyc.crawler.CrawlerJyycZhejiang import CrawlerJyycZhejiang
from xgxx.qyxx_jyyc.crawler.CrawlerJyycAnhui import CrawlerJyycAnhui
from xgxx.qyxx_jyyc.crawler.CrawlerJyycFujian import CrawlerJyycFujian
from xgxx.qyxx_jyyc.crawler.CrawlerJyycJiangxi import CrawlerJyycJiangxi
from xgxx.qyxx_jyyc.crawler.CrawlerJyycShandong import CrawlerJyycShandong
from xgxx.qyxx_jyyc.crawler.CrawlerJyycGuangdong import CrawlerJyycGuangdong
from xgxx.qyxx_jyyc.crawler.CrawlerJyycHainan import CrawlerJyycHainan
from xgxx.qyxx_jyyc.crawler.CrawlerJyycHenan import CrawlerJyycHenan
from xgxx.qyxx_jyyc.crawler.CrawlerJyycHubei import CrawlerJyycHubei
from xgxx.qyxx_jyyc.crawler.CrawlerJyycHunan import CrawlerJyycHunan
from xgxx.qyxx_jyyc.crawler.CrawlerJyycChongqing import CrawlerJyycChongqing
from xgxx.qyxx_jyyc.crawler.CrawlerJyycSichuan import CrawlerJyycSichuan
from xgxx.qyxx_jyyc.crawler.CrawlerJyycGuizhou import CrawlerJyycGuizhou
from xgxx.qyxx_jyyc.crawler.CrawlerJyycYunnan import CrawlerJyycYunnan
from xgxx.qyxx_jyyc.crawler.CrawlerJyycXizang import CrawlerJyycXizang
from xgxx.qyxx_jyyc.crawler.CrawlerJyycShanxixian import CrawlerJyycShanxixian
from xgxx.qyxx_jyyc.crawler.CrawlerJyycGansu import CrawlerJyycGansu
from xgxx.qyxx_jyyc.crawler.CrawlerJyycQinghai import CrawlerJyycQinghai
from xgxx.qyxx_jyyc.crawler.CrawlerJyycNingxia import CrawlerJyycNingxia
from xgxx.qyxx_jyyc.crawler.CrawlerJyycXinjiang import CrawlerJyycXinjiang
from CommonLib.DB.DBManager import DBManager
from CommonLib.UniField import UniField


class CrawlerTester(object):
    seed_dict = None
    pinyin = None
    db_inst = None


def callbackFromOuterControl(html_dict, company_dict):
    print "开始执行外部回调方法"
    result_json = json.dumps(company_dict, ensure_ascii=False)
    html_json = json.dumps(html_dict, ensure_ascii=False)
    print("企业信息抓取结果：\n" + result_json)
    print("企业信息页面内容：\n" + html_json)
    pass


def testBySeed(crawler, pinyin, seed):
    CrawlerTester.pinyin = pinyin
    CrawlerTester.seed_dict = seed
    CrawlerTester.db_inst = DBManager.getInstance("ssdb", "jyyc_" + CrawlerTester.pinyin, host="spider5", port=57888)
    return crawler.crawl(CrawlerTester.seed_dict['page'])


def storeResult(src_dict, company_dict=None):
    src_dict = UniField.unifyRequestResult(src_dict, CrawlerTester.pinyin)
    src_dict.update({"BBD_SEED": CrawlerTester.seed_dict})
    if src_dict["status"] == 0:
        CrawlerTester.db_inst.changeTable("jyyc_" + CrawlerTester.pinyin)
        CrawlerTester.db_inst.save(src_dict)
    else:
        CrawlerTester.db_inst.changeTable("jyyc_" + CrawlerTester.pinyin + "_error")
        CrawlerTester.db_inst.save(src_dict)


def zongjuTest():
    crawler = CrawlerJyycZongju('zongju', storeResult)
    return testBySeed(crawler, 'zongju', {"province": 'zongju', "page": '1'})


def beijingTest():
    crawler = CrawlerJyycBeijing('beijing', storeResult)
    return testBySeed(crawler, 'beijing', {"province": 'beijing', "page": '1'})


def hebeiTest():
    crawler = CrawlerJyycHebei('hebei', storeResult)
    return testBySeed(crawler, 'hebei', {"province": 'hebei', "page": '11'})


def tianjinTest():
    crawler = CrawlerJyycTianjin('tianjin', storeResult)
    return testBySeed(crawler, 'tianjin', {"province": 'tianjin', "page": '10'})


def neimengguTest():
    crawler = CrawlerJyycNeimenggu('neimenggu', storeResult)
    return testBySeed(crawler, 'neimenggu', {"province": 'neimenggu', "page": '112'})


def liaoningTest():
    crawler = CrawlerJyycLiaoning('liaoning', storeResult)
    return testBySeed(crawler, 'liaoning', {"province": 'liaoning', "page": '112'})


def jilinTest():
    crawler = CrawlerJyycJilin('jilin', storeResult)
    return testBySeed(crawler, 'jilin', {"province": 'jilin', "page": '1112'})


def heilongjiangTest():
    crawler = CrawlerJyycHeilongjiang('heilongjiang', storeResult)
    return testBySeed(crawler, 'heilongjiang', {"province": 'heilongjiang', "page": '112'})


def shanghaiTest():
    crawler = CrawlerJyycShanghai('shanghai', storeResult)
    return testBySeed(crawler, 'shanghai', {"province": 'shanghai', "page": '11'})


def jiangsuTest():
    crawler = CrawlerJyycJiangsu('jiangsu', storeResult)
    return testBySeed(crawler, 'jiangsu', {"province": 'jiangsu', "page": '112'})


def zhejiangTest():
    crawler = CrawlerJyycZhejiang('zhejiang', storeResult)
    return testBySeed(crawler, 'zhejiang', {"province": 'zhejiang', "page": '112'})


def anhuiTest():
    crawler = CrawlerJyycAnhui('anhui', storeResult)
    return testBySeed(crawler, 'anhui', {"province": 'anhui', "page": '121'})


def fujianTest():
    crawler = CrawlerJyycFujian('fujian', storeResult)
    return testBySeed(crawler, 'fujian', {"province": 'fujian', "page": '121'})


def jiangxiTest():
    crawler = CrawlerJyycJiangxi('jiangxi', storeResult)
    return testBySeed(crawler, 'jiangxi', {"province": 'jiangxi', "page": '121'})


def shandongTest():
    crawler = CrawlerJyycShandong('shandong', storeResult)
    return testBySeed(crawler, 'shandong', {"province": 'shandong', "page": '121'})


def guangdongTest():
    crawler = CrawlerJyycGuangdong('guangdong', storeResult)
    return testBySeed(crawler, 'guangdong', {"province": 'guangdong', "page": '121'})


def hainanTest():
    crawler = CrawlerJyycHainan('hainan', storeResult)
    return testBySeed(crawler, 'hainan', {"province": 'hainan', "page": '112'})


def henanTest():
    crawler = CrawlerJyycHenan('henan', storeResult)
    return testBySeed(crawler, 'henan', {"province": 'henan', "page": '121'})


def hubeiTest():
    crawler = CrawlerJyycHubei('hubei', storeResult)
    return testBySeed(crawler, 'hubei', {"province": 'hubei', "page": '121'})


def hunanTest():
    crawler = CrawlerJyycHunan('hunan', storeResult)
    return testBySeed(crawler, 'hunan', {"province": 'hunan', "page": '12'})


def chongqingTest():
    crawler = CrawlerJyycChongqing('chongqing', storeResult)
    return testBySeed(crawler, 'chongqing', {"province": 'chongqing', "page": '112'})


def sichuanTest():
    crawler = CrawlerJyycSichuan('sichuan', storeResult)
    return testBySeed(crawler, 'sichuan', {"province": 'sichuan', "page": '1112'})


def guizhouTest():
    crawler = CrawlerJyycGuizhou('guizhou', storeResult)
    return testBySeed(crawler, 'guizhou', {"province": 'guizhou', "page": '1222'})


def yunnanTest():
    crawler = CrawlerJyycYunnan('yunnan', storeResult)
    return testBySeed(crawler, 'yunnan', {"province": 'yunnan', "page": '1112'})


def xizangTest():
    crawler = CrawlerJyycXizang('xizang', storeResult)
    return testBySeed(crawler, 'xizang', {"province": 'xizang', "page": '112'})


def shanxixianTest():
    crawler = CrawlerJyycShanxixian('shanxixian', storeResult)
    return testBySeed(crawler, 'shanxixian', {"province": 'shanxixian', "page": '1212'})


def gansuTest():
    crawler = CrawlerJyycGansu('gansu', storeResult)
    return testBySeed(crawler, 'gansu', {"province": 'gansu', "page": '1212'})


def qinghaiTest():
    crawler = CrawlerJyycQinghai('qinghai', storeResult)
    return testBySeed(crawler, 'qinghai', {"province": 'qinghai', "page": '123'})


def ningxiaTest():
    crawler = CrawlerJyycNingxia('ningxia', storeResult)
    return testBySeed(crawler, 'ningxia', {"province": 'ningxia', "page": '1221'})


def xinjiangTest():
    crawler = CrawlerJyycXinjiang('xinjiang', storeResult)
    return testBySeed(crawler, 'xinjiang', {"province": 'xinjiang', "page": '112'})


if __name__ == '__main__':
    # zongjuTest()
    # beijingTest()
    # hebeiTest()
    tianjinTest()
    # neimengguTest()
    # liaoningTest()
    # jilinTest()
    # heilongjiangTest()
    # shanghaiTest()
    # jiangsuTest()
    # zhejiangTest()
    # anhuiTest()
    # fujianTest()
    # jiangxiTest()
    # shandongTest()
    # guangdongTest()
    # hainanTest()
    # henanTest()
    # hubeiTest()
    # hunanTest()
    # chongqingTest()
    # sichuanTest()
    # guizhouTest()
    # yunnanTest()
    # xizangTest()
    # shanxixianTest()
    # gansuTest()
    # qinghaiTest()
    # ningxiaTest()
    # xinjiangTest()
    crawler = QyxxJyyc("beijing",2)
    crawler.crawl(1)
