# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     ParserTester.py  
   Description :  
   Author :       JHao
   date：          2016/6/21
-------------------------------------------------
   Change Activity:
                   2016/6/21: 
-------------------------------------------------
"""
__author__ = 'JHao'

import sys
import json

from CommonLib.DB.DBManager import DBManager
from xgxx.qyxx_jyyc.parser.ZongjuJyycHandler import ZongjuJyycHandler
from xgxx.qyxx_jyyc.parser.BeijingJyycHandler import BeijingJyycHandler
from xgxx.qyxx_jyyc.parser.HebeiJyycHandler import HebeiJyycHandler
from xgxx.qyxx_jyyc.parser.TianjinJyycHandler import TianjinJyycHandler
from xgxx.qyxx_jyyc.parser.NeimengguJyycHandler import NeimengguJyycHandler
from xgxx.qyxx_jyyc.parser.LiaoningJyycHandler import LiaoningJyycHandler
from xgxx.qyxx_jyyc.parser.JilinJyycHandler import JilinJyycHandler
from xgxx.qyxx_jyyc.parser.HeilongjiangJyycHandler import HeilongjiangJyycHandler
from xgxx.qyxx_jyyc.parser.ShanghaiJyycHandler import ShanghaiJyycHandler
from xgxx.qyxx_jyyc.parser.JiangsuJyycHandler import JiangsuJyycHandler
from xgxx.qyxx_jyyc.parser.AnhuiJyycHandler import AnhuiJyycHandler
from xgxx.qyxx_jyyc.parser.FujianJyycHandler import FujianJyycHandler
from xgxx.qyxx_jyyc.parser.JiangxiJyycHandler import JiangxiJyycHandler
from xgxx.qyxx_jyyc.parser.ShandongJyycHandler import ShandongJyycHandler
from xgxx.qyxx_jyyc.parser.GuangdongJyycHandler import GuangdongJyycHandler
from xgxx.qyxx_jyyc.parser.HainanJyycHandler import HainanJyycHandler
from xgxx.qyxx_jyyc.parser.HenanJyycHandler import HenanJyycHandler
from xgxx.qyxx_jyyc.parser.HubeiJyycHandler import HubeiJyycHandler
from xgxx.qyxx_jyyc.parser.HunanJyycHandler import HunanJyycHandler
from xgxx.qyxx_jyyc.parser.ZhejiangJyycHandler import ZhejiangJyycHandler
from xgxx.qyxx_jyyc.parser.ChongqingJyycHandler import ChongqingJyycHandler
from xgxx.qyxx_jyyc.parser.SichuanJyycHandler import SichuanJyycHandler
from xgxx.qyxx_jyyc.parser.GuizhouJyycHandler import GuizhouJyycHandler
from xgxx.qyxx_jyyc.parser.YunnanJyycHandler import YunnanJyycHandler
from xgxx.qyxx_jyyc.parser.XizangJyycHandler import XizangJyycHandler
from xgxx.qyxx_jyyc.parser.ShanxixianJyycHandler import ShanxixianJyycHandler
from xgxx.qyxx_jyyc.parser.QinghaiJyycHandler import QinghaiJyycHandler
from xgxx.qyxx_jyyc.parser.NingxiaJyycHandler import NingxiaHandler
from xgxx.qyxx_jyyc.parser.XinjiangJyycHandler import XinjiangJyycHandler
from xgxx.qyxx_jyyc.parser.GansuJyycHandler import GansuJyycHandler


class ParserTester(object):
    def __init__(self):
        pass

    def saveMongo(self, data):
        from pymongo.mongo_client import MongoClient
        url = 'mongodb://spider7:27037'
        client = MongoClient(url)
        db = client.jinghao
        db.jyyc.insert(data)

    def testFromSSDB(self, db_inst, handler):
        html_dict_str = db_inst.get()
        while html_dict_str:
            html_dict = json.loads(html_dict_str)
            result = handler.parse(html_dict)
            self.saveMongo(result)
            html_dict_str = db_inst.get()
        print("队列为空")
        return

    def zongjuTester(self):
        pinyin = "zongju"
        db_inst = DBManager.getInstance("ssdb", 'jyyc_%s' % pinyin, host="spider5", port=57888)
        handler = ZongjuJyycHandler(pinyin)
        self.testFromSSDB(db_inst, handler)

    def beijingTester(self):
        pinyin = "beijing"
        db_inst = DBManager.getInstance("ssdb", 'jyyc_%s' % pinyin, host="spider5", port=57888)
        handler = BeijingJyycHandler(pinyin)
        self.testFromSSDB(db_inst, handler)

    def hebeiTester(self):
        pinyin = "hebei"
        db_inst = DBManager.getInstance("ssdb", 'jyyc_%s' % pinyin, host="spider5", port=57888)
        handler = HebeiJyycHandler(pinyin)
        self.testFromSSDB(db_inst, handler)

    def tianjinTester(self):
        pinyin = "tianjin"
        db_inst = DBManager.getInstance("ssdb", 'jyyc_%s' % pinyin, host="spider5", port=57888)
        handler = TianjinJyycHandler(pinyin)
        self.testFromSSDB(db_inst, handler)

    def neimengguTester(self):
        pinyin = "neimenggu"
        db_inst = DBManager.getInstance("ssdb", 'jyyc_%s' % pinyin, host="spider5", port=57888)
        handler = NeimengguJyycHandler(pinyin)
        self.testFromSSDB(db_inst, handler)

    def liaoningTester(self):
        pinyin = "liaoning"
        db_inst = DBManager.getInstance("ssdb", 'jyyc_%s' % pinyin, host="spider5", port=57888)
        handler = LiaoningJyycHandler(pinyin)
        self.testFromSSDB(db_inst, handler)

    def jilinTester(self):
        pinyin = "jilin"
        db_inst = DBManager.getInstance("ssdb", 'jyyc_%s' % pinyin, host="spider5", port=57888)
        handler = JilinJyycHandler(pinyin)
        self.testFromSSDB(db_inst, handler)

    def heilongjiangTester(self):
        pinyin = "heilongjiang"
        db_inst = DBManager.getInstance("ssdb", 'jyyc_%s' % pinyin, host="spider5", port=57888)
        handler = HeilongjiangJyycHandler(pinyin)
        self.testFromSSDB(db_inst, handler)

    def shanghaiTester(self):
        pinyin = "shanghai"
        db_inst = DBManager.getInstance("ssdb", 'jyyc_%s' % pinyin, host="spider5", port=57888)
        handler = ShanghaiJyycHandler(pinyin)
        self.testFromSSDB(db_inst, handler)

    def jiangsuTester(self):
        pinyin = "jiangsu"
        db_inst = DBManager.getInstance("ssdb", 'jyyc_%s' % pinyin, host="spider5", port=57888)
        handler = JiangsuJyycHandler(pinyin)
        self.testFromSSDB(db_inst, handler)

    def anhuiTester(self):
        pinyin = "anhui"
        db_inst = DBManager.getInstance("ssdb", 'jyyc_%s' % pinyin, host="spider5", port=57888)
        handler = AnhuiJyycHandler(pinyin)
        self.testFromSSDB(db_inst, handler)

    def fujianTester(self):
        pinyin = "fujian"
        db_inst = DBManager.getInstance("ssdb", 'jyyc_%s' % pinyin, host="spider5", port=57888)
        handler = FujianJyycHandler(pinyin)
        self.testFromSSDB(db_inst, handler)

    def jiangxiTester(self):
        pinyin = "jiangxi"
        db_inst = DBManager.getInstance("ssdb", 'jyyc_%s' % pinyin, host="spider5", port=57888)
        handler = JiangxiJyycHandler(pinyin)
        self.testFromSSDB(db_inst, handler)

    def shandongTester(self):
        pinyin = "shandong"
        db_inst = DBManager.getInstance("ssdb", 'jyyc_%s' % pinyin, host="spider5", port=57888)
        handler = ShandongJyycHandler(pinyin)
        self.testFromSSDB(db_inst, handler)

    def guangdongTester(self):
        pinyin = "guangdong"
        db_inst = DBManager.getInstance("ssdb", 'jyyc_%s' % pinyin, host="spider5", port=57888)
        handler = GuangdongJyycHandler(pinyin)
        self.testFromSSDB(db_inst, handler)

    def hainanTester(self):
        pinyin = "hainan"
        db_inst = DBManager.getInstance("ssdb", 'jyyc_%s' % pinyin, host="spider5", port=57888)
        handler = HainanJyycHandler(pinyin)
        self.testFromSSDB(db_inst, handler)

    def henanTester(self):
        pinyin = "henan"
        db_inst = DBManager.getInstance("ssdb", 'jyyc_%s' % pinyin, host="spider5", port=57888)
        handler = HenanJyycHandler(pinyin)
        self.testFromSSDB(db_inst, handler)

    def hubeiTester(self):
        pinyin = "hubei"
        db_inst = DBManager.getInstance("ssdb", 'jyyc_%s' % pinyin, host="spider5", port=57888)
        handler = HubeiJyycHandler(pinyin)
        self.testFromSSDB(db_inst, handler)

    def hunanTester(self):
        pinyin = "hunan"
        db_inst = DBManager.getInstance("ssdb", 'jyyc_%s' % pinyin, host="spider5", port=57888)
        handler = HunanJyycHandler(pinyin)
        self.testFromSSDB(db_inst, handler)

    def zhejiangTester(self):
        pinyin = "zhejiang"
        db_inst = DBManager.getInstance("ssdb", 'jyyc_%s' % pinyin, host="spider5", port=57888)
        handler = ZhejiangJyycHandler(pinyin)
        self.testFromSSDB(db_inst, handler)

    def chongqingTester(self):
        pinyin = "chongqing"
        db_inst = DBManager.getInstance("ssdb", 'jyyc_%s' % pinyin, host="spider5", port=57888)
        handler = ChongqingJyycHandler(pinyin)
        self.testFromSSDB(db_inst, handler)

    def sichuanTester(self):
        pinyin = "sichuan"
        db_inst = DBManager.getInstance("ssdb", 'jyyc_%s' % pinyin, host="spider5", port=57888)
        handler = SichuanJyycHandler(pinyin)
        self.testFromSSDB(db_inst, handler)

    def guizhouTester(self):
        pinyin = "guizhou"
        db_inst = DBManager.getInstance("ssdb", 'jyyc_%s' % pinyin, host="spider5", port=57888)
        handler = GuizhouJyycHandler(pinyin)
        self.testFromSSDB(db_inst, handler)

    def yunnanTester(self):
        pinyin = "yunnan"
        db_inst = DBManager.getInstance("ssdb", 'jyyc_%s' % pinyin, host="spider5", port=57888)
        handler = YunnanJyycHandler(pinyin)
        self.testFromSSDB(db_inst, handler)

    def xizangTester(self):
        pinyin = "xizang"
        db_inst = DBManager.getInstance("ssdb", 'jyyc_%s' % pinyin, host="spider5", port=57888)
        handler = XizangJyycHandler(pinyin)
        self.testFromSSDB(db_inst, handler)

    def shanxixianTester(self):
        pinyin = "shanxixian"
        db_inst = DBManager.getInstance("ssdb", 'jyyc_%s' % pinyin, host="spider5", port=57888)
        handler = ShanxixianJyycHandler(pinyin)
        self.testFromSSDB(db_inst, handler)

    def qinghaiTester(self):
        pinyin = "qinghai"
        db_inst = DBManager.getInstance("ssdb", 'jyyc_%s' % pinyin, host="spider5", port=57888)
        handler = QinghaiJyycHandler(pinyin)
        self.testFromSSDB(db_inst, handler)

    def ningxiaTester(self):
        pinyin = "ningxia"
        db_inst = DBManager.getInstance("ssdb", 'jyyc_%s' % pinyin, host="spider5", port=57888)
        handler = NingxiaHandler(pinyin)
        self.testFromSSDB(db_inst, handler)

    def xinjiangTester(self):
        pinyin = "xinjiang"
        db_inst = DBManager.getInstance("ssdb", 'jyyc_%s' % pinyin, host="spider5", port=57888)
        handler = XinjiangJyycHandler(pinyin)
        self.testFromSSDB(db_inst, handler)

    def gansuTester(self):
        pinyin = "gansu"
        db_inst = DBManager.getInstance("ssdb", 'jyyc_%s' % pinyin, host="spider5", port=57888)
        handler = GansuJyycHandler(pinyin)
        self.testFromSSDB(db_inst, handler)


if __name__ == '__main__':
    tester = ParserTester()
    # tester.zongjuTester()
    # tester.beijingTester()
    # tester.hebeiTester()
    # tester.tianjinTester()
    # tester.neimengguTester()
    tester.liaoningTester()
    # tester.jilinTester()
    # tester.heilongjiangTester()
    # tester.shanghaiTester()
    # tester.jiangsuTester()
    # tester.anhuiTester()
    # tester.fujianTester()
    # tester.jiangxiTester()
    # tester.shandongTester()
    # tester.guangdongTester()
    # tester.hainanTester()
    # tester.henanTester()
    # tester.hubeiTester()
    # tester.hunanTester()
    # tester.zhejiangTester()
    # tester.chongqingTester()
    # tester.sichuanTester()
    # tester.guizhouTester()
    # tester.yunnanTester()
    # tester.xizangTester()
    # tester.shanxixianTester()
    # tester.qinghaiTester()
    # tester.ningxiaTester()
    # tester.xinjiangTester()
    # tester.gansuTester()
