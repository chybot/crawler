# -*- coding: utf-8 -*-
# Created by David on 2016/5/24.

import sys
import json
reload(sys)
sys.setdefaultencoding('utf-8')
from BeijingHandler import BeijingHandler
from BeijingNbHandler import BeijingNbHandler
from ShanghaiNbHandler import ShanghaiNbHandler
from JilinHandler import JilinHandler
from JiangxiHandler import JiangxiHandler
from ChongqingHandler import ChongqingHandler
from GuizhouNbHandler import GuizhouNbHandler
from CommonLib.DB.DBManager import DBManager
from GuangdongNbHandler import GuangdongNbHandler
from GuangdongHandler import GuangdongHandler

class ParserTester:
    """
    ParserTester is used to test the parser
    @version:1.0
    @author:david ding
    @modify:
    """

    def __init__(self):
        """
        Initiate the parameters.
        """
        pass

    def testFromSSDB(self, db_inst, row_key, handler):
        html_dict_str = db_inst.hget(row_key)
        if not html_dict_str:
            print("从SSDB获取数据失败！")
            return
        html_dict = json.loads(html_dict_str)
        handler.parse(html_dict)

    def beijingTest(self):
        pinyin = "beijing"
        db_inst = DBManager.getInstance("ssdb", pinyin, host="spider5", port=57888)
        #row_key = "6fbb174d364fdf67fdb96cab6048db11|_|北京艺海佳景广告有限公司|_|beijing|_|2016-05-21"
        #row_key = "8d32a8b1d67d1f1d6a165c5577ac3efb|_|北京盛德东兴投资管理公司|_|beijing|_|2016-05-25"
        row_key = "dc3094f66fa56ffed50955b3b149cfa7|_|中国光大银行股份有限公司|_|beijing|_|2016-05-25"
        row_key = "6203925f878305c2f1f5be5a80434e0d|_|北京伊美尔长岛医学美容门诊部有限公司|_|91110108797596955A|_|2016-06-16|_|beijing"
        handler = BeijingHandler(pinyin)
        self.testFromSSDB(db_inst, row_key, handler)

    def beijingNbTest(self):
        pinyin = "beijing"
        db_inst = DBManager.getInstance("ssdb", "%s_nbxx" % pinyin, host="spider5", port=57888)
        row_key = "473dff8aacd4ab651b932bc8a3bbfda3|_|北京崇尚兴业商贸有限公司|_|110108010048185|_|2016-06-23|_|beijing|_|2015"
        handler = BeijingNbHandler(pinyin)
        self.testFromSSDB(db_inst, row_key, handler)

    def shanghaiNbTest(self):
        pinyin = "shanghai"
        db_inst = DBManager.getInstance("ssdb", "%s_nbxx" % pinyin, host="spider5", port=57888)
        row_key = "70198bb285bc3e74898ed926a54aa5fa|_|上海佳吉快运有限公司|_|913101186074971991|_|2016-06-12|_|shanghai|_|2015"
        handler = ShanghaiNbHandler(pinyin)
        self.testFromSSDB(db_inst, row_key, handler)

    def guizhouNbTest(self):
        pinyin = "guizhou"
        db_inst = DBManager.getInstance("ssdb", "new_%s_nbxx" % pinyin, host="spider5", port=57888)
        row_key = "0ad1548ffe8ba00864126cc2c2a22619|_|锦屏县锦顺出租汽车有限公司|_|522628000053658|_|2016-06-10|_|guizhou|_|2015"
        handler = GuizhouNbHandler(pinyin)
        self.testFromSSDB(db_inst, row_key, handler)

    def jilinTest(self):
        pinyin = "jilin"
        db_inst = DBManager.getInstance("ssdb", "new_"+pinyin, host="spider5", port=57888)
        # row_key = "66be9a1cbec45fd17e281324fca7f2fc|_|延边爱丽思鞋业有限公司|_|jilin|_|2016-05-25"
        # row_key = "4129cb0108048b80faf34503cad6ecc9|_|延边华侨旅游侨汇服务公司|_|jilin|_|2016-05-25"
        row_key = ""
        row_key = "f1c17231377bb8c56591ba774c2aca56|_|中国旅游服务公司吉林省公司|_|jilin|_|2016-05-25"
        handler = JilinHandler(pinyin)
        self.testFromSSDB(db_inst, row_key, handler)

    def jiangxiTest(self):
        pinyin = "jiangxi"
        db_inst = DBManager.getInstance("ssdb", "new_" + pinyin, host="spider5", port=57888)
        row_key = ""
        row_key = "5994e3d1afbf82a9e526efae797d02db|_|乐平市新睦水稻种植专业合作社|_|jiangxi|_|2016-05-25"
        handler = JiangxiHandler(pinyin)
        self.testFromSSDB(db_inst, row_key, handler)

    def chongqingTest(self):
        pinyin = "chongqing"
        db_inst = DBManager.getInstance("ssdb", "new_" + pinyin, host="spider5", port=57888)
        row_key = ""
        row_key = "fc46237ff1f403b39ad199502cd338a3|_|武隆县仁武酒业有限公司|_|chongqing|_|2016-05-30"
        handler = ChongqingHandler(pinyin)
        self.testFromSSDB(db_inst, row_key, handler)

    def guangdongTest(self):
        pinyin = "guangdong"
        db_inst = DBManager.getInstance("ssdb", "new_%s" % pinyin, host="spider5", port=57888)
        row_key = "8effa8ebede5e87faa8157661c8d6555|_|广州顺丰速运有限公司|_|914401017248329968|_|2016-06-13|_|guangdong"
        # row_key = "23b441b3d17a26ef2e06ba79a4ed676a|_|广州广之旅国际旅行社股份有限公司|_|914401011904322413|_|2016-06-13|_|guangdong"
        row_key = "abb92dbbfaf77adafd1e98ddb100d076|_|佛山市南湖国际旅行社股份有限公司|_|91440604776910212C|_|2016-06-14|_|guangdong"
        handler = GuangdongHandler(pinyin)
        self.testFromSSDB(db_inst, row_key, handler)

    def guangdongNbTest(self):
        pinyin = "guangdong"
        db_inst = DBManager.getInstance("ssdb", "%s_nbxx" % pinyin, host="spider5", port=57888)
        row_key = "23b441b3d17a26ef2e06ba79a4ed676a|_|广州广之旅国际旅行社股份有限公司|_|914401011904322413|_|2016-06-13|_|guangdong|_|2015"
        row_key = "b64ffc239d74dc4ad0a59cd4f6218e27|_|佛山市南湖国际旅行社股份有限公司|_|91440604776910212C|_|2016-06-13|_|guangdong|_|2014"
        handler = GuangdongNbHandler(pinyin)
        self.testFromSSDB(db_inst, row_key, handler)


if __name__ == "__main__":
    test = ParserTester()
    test.beijingNbTest()
