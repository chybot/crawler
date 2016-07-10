# -*- coding: utf-8 -*-
# Created by David on 2016/6/3.

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

class BeijingNbHandler(ParserNbBase):
    """
    BeijingNbHandler is used to parse the annual report
    @version:1.0
    @author:david ding
    @modify:
    """
    def __init__(self, pinyin):
        """
        Initiate the parameters.
        """
        ParserNbBase.__init__(self, pinyin)
        self.log.info(u"BeijingNbHandler 构造完成")

    def parse(self, html_dict, reslt_dict=None):
        if not html_dict or not isinstance(html_dict, dict):
            return None
        if 'company_name' in html_dict:
            self.log.info(u"开始解析 %s" % html_dict['company_name'])
        self.log.info(u"开始解析通用信息")
        company = self.parseCommon(html_dict)
        self.log.info(u"通用信息解析完成")
        company_copied = copy.deepcopy(company)
        if reslt_dict and isinstance(reslt_dict, dict):
            reslt_dict.update(company_copied)
        result_json = json.dumps(reslt_dict, ensure_ascii=False)
        self.log.info(u"BeijingNbHandler解析结果：\n" + result_json)
        return reslt_dict

if __name__ == "__main__":
    pass


