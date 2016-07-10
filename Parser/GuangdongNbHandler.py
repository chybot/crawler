# -*- coding: utf-8 -*-
# Created by David on 2016/6/13.

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

class GuangdongNbHandler(ParserNbBase):
    """
    GuangdongNbHandler is used to parse the annual report
    @version:1.0
    @author:david ding
    @modify:
    """
    def __init__(self, pinyin):
        """
        Initiate the parameters.
        """
        ParserNbBase.__init__(self, pinyin)
        self.log.info(u"GuangdongNbHandler 构造完成")

    def parse(self, html_dict, reslt_dict=None):
        if not html_dict or not isinstance(html_dict, dict):
            return None
        if 'company_name' in html_dict:
            self.log.info(u"开始解析 %s" % html_dict['company_name'])
        self.log.info(u"开始解析通用信息")
        company = self.parseCommon(html_dict)
        self.log.info(u"通用信息解析完成")
        self.clean(company)
        company_copied = copy.deepcopy(company)
        if reslt_dict and isinstance(reslt_dict, dict):
            reslt_dict.update(company_copied)
        result_json = json.dumps(reslt_dict, ensure_ascii=False)
        self.log.info(u"GuangdongNbHandler解析结果：\n" + result_json)
        return reslt_dict

    def clean(self, company):
        if u'qynb' not in company:
            return
        if u'对外投资信息' not in company[u'qynb']:
            return
        tzxx_list = list()
        tzxx_dict = dict()
        for info_dict in company[u'qynb'][u'对外投资信息']:
            for k,v in info_dict.items():
                if k in tzxx_dict and tzxx_dict[k] != v:
                    tzxx_list.append(tzxx_dict)
                    tzxx_dict = dict()
                else:
                    tzxx_dict[k] = v
        if tzxx_list:
            tzxx_list.append(tzxx_dict)
            company[u'qynb'][u'对外投资信息'] = tzxx_list
        elif tzxx_dict:
            company[u'qynb'][u'对外投资信息'] = tzxx_dict
        pass

if __name__ == "__main__":
    pass


