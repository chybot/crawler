# -*- coding: utf-8 -*-
# Created by John on 2016/6/21.

import sys
import os
import json
import copy
import chardet
from lxml import etree
from ParserNbBase import ParserNbBase
import html4test as test
reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

class HeilongjiangNbHandler(ParserNbBase):
    """
    HeilongjiangNbHandler is used to parse the annual report
    @version:1.0
    @author:John Liu
    @modify:
    """
    def __init__(self, pinyin):
        """
        Initiate the parameters.
        """
        ParserNbBase.__init__(self, pinyin)
        self.log.info(u"HeilongjiangNbHandler 构造完成")

    def parse(self, html_dict, reslt_dict=None):
        if not html_dict or not isinstance(html_dict, dict):
            return None
        if 'company_name' in html_dict:
            self.log.info(u"开始解析 %s" % html_dict['company_name'])
        self.log.info(u"开始解析通用信息")
        company = self.parseCommon(html_dict)
        self.log.info(u"通用信息解析完成")
        self.standardizeField(company)
        company_copied = copy.deepcopy(company)
        if reslt_dict and isinstance(reslt_dict, dict):
            reslt_dict.update(company_copied)
        result_json = json.dumps(reslt_dict, ensure_ascii=False)
        self.log.info(u"HeilongjiangNbHandler解析结果：\n" + result_json)
        return reslt_dict

    def standardizeField(self, company):
        self.log.info(u"开始清理、修复字段")

        # 青海年报中的表格中存在垃圾行:1. 无数据的表格中也会存在一些空行; 2. 有数据的表格中也会存在一些空行 这些都需要过滤掉
        try:
            qynb_dict = company["qynb"]

            for item_list in qynb_dict:
                if isinstance(qynb_dict[item_list], list):
                    new_list = []
                    for item in qynb_dict[item_list]:
                        ll = filter(lambda k: item[k], item.keys())
                        if ll:
                            new_list.append(item)

                    if not new_list:
                        qynb_dict[item_list] = []
                    else:
                        qynb_dict[item_list] = new_list
            self.log.info(u"清理、修复字段成功")
        except:
            self.log.error(u"清理、修复字段失败")


if __name__ == "__main__":
    pass


