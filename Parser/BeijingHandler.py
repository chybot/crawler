# -*- coding: utf-8 -*-
# Created by David on 2016/5/21.

import sys
import os
import json
import copy
import chardet
from lxml import etree
from ParserBase import ParserBase
import html4test as test
reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

class BeijingHandler(ParserBase):
    """
    BeijingHandler is used to parse the enterprise info from Beijing
    @version:1.0
    @author:david ding
    @modify:
    """
    def __init__(self, pinyin):
        """
        Initiate the parameters.
        """
        ParserBase.__init__(self, pinyin)
        self.ignore_key_list.extend(["gdxq_html",u'gdxx.详情'])
        self.log.info(u"BeijingHandler 构造完成")

    def parse(self, html_dict, reslt_dict=None):
        if not html_dict or not isinstance(html_dict, dict):
            return None
        if 'company_name' in html_dict:
            self.log.info(u"开始解析 %s" % html_dict['company_name'])
        self.log.info(u"开始解析通用信息")
        company = self.parseCommon(html_dict)
        self.log.info(u"通用信息解析完成")
        top_dict = self.parseTop(html_dict)
        if top_dict:
            self.log.info(u"top信息解析成功")
            company.update(top_dict)
        else:
            self.log.info(u"top信息解析失败")
        self.standardizeField(company)
        company_copied = copy.deepcopy(company)
        if reslt_dict and isinstance(reslt_dict, dict):
            reslt_dict.update(company_copied)
        result_json = json.dumps(reslt_dict, ensure_ascii=False)
        self.log.info(u"BeijingHandler解析结果：\n" + result_json)
        return reslt_dict

    def standardizeField(self, company):
        self.log.info(u"开始清理、修复字段")
        return

    def parseTop(self, html_dict):
        if 'jbxx_html' not in html_dict:
            return None
        jbxx_list = html_dict['jbxx_html']
        if not jbxx_list:
            return None
        if '_body' not in jbxx_list[0]:
            return None
        return self.parseTopHtml(jbxx_list[0]['_body'])

    def parseTopHtml(self, html):
        if not html:
            return None
        # 页面编码检测
        try:
            encoding = chardet.detect(html)['encoding']  # 此处检测有时会出异常
            tree = etree.HTML(html.decode(encoding))
        except:
            tree = etree.HTML(html)
        self.log.info(u"开始解析top信息")
        dict_ = dict()
        try:
            top_str = tree.xpath(".//*[@id='details']/h2/text()")
            if not top_str:
                self.log.info(u"获取top信息失败")
                return None
            top_str = top_str[0].replace(u"该企业已列入经营异常名录", "").replace(u'\xa0', '').replace(u':', u'：')
            tops = top_str.split()
            if len(tops) == 2:
                dict_[u'top_企业名称'] = tops[0].strip()
                zch = tops[1].split(u'：')
                if len(zch) == 2:
                    dict_[u'top_' + zch[0].strip()] = zch[1].strip()
        except:
                self.log.info(u"获取top信息异常")
        return dict_


if __name__ == "__main__":
    # top_dict = test_top()
    # handler = BeijingHandler("beijing")
    # tp_dict = handler.parseTopHtml(test.html_shanghai)
    pass


