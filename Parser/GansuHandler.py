# -*- coding: utf-8 -*-
# Created by fml on 2016/6/27.

import sys
import os
import json
import copy
import chardet
from lxml import etree
from ParserBase import ParserBase
from CommonLib.DB.DBManager import DBManager
import html4test as test
reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

class GansuHandler(ParserBase):
    """
    ShanghaiHandler is used to parse the enterprise info from Shanghai
    @version:1.0
    @author:david ding
    @modify:
    """
    def __init__(self, pinyin):
        """
        Initiate the parameters.
        """
        ParserBase.__init__(self, pinyin)
        self.log.info(u"GansuHandler 构造完成")

    def parse(self, html_dict, all_reslt_dict=None):
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
        if all_reslt_dict and isinstance(all_reslt_dict, dict):
            all_reslt_dict.update(company_copied)
        result_json = json.dumps(all_reslt_dict, ensure_ascii=False)
        self.log.info(u"GansuHandler解析结果：\n" + result_json)
        return all_reslt_dict

    def standardizeField(self, company):
        self.log.info(u"开始清理、修复字段")
        if u'注册号/' in company:
            company[u'注册号/统一社会信用代码'] = company[u'注册号/']
            del company[u'注册号/']

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
            top_texts = tree.xpath('.//*[@id="gsh"]/text()')
            if not top_texts:
                self.log.info(u"获取top信息失败")
            else:
                if len(top_texts) == 2:
                    top_texts = top_texts[0].split()
                    if u'：' in top_texts[1] or ':' in top_texts[1]:
                        top_texts[1] = top_texts[1] + top_texts[2]
                        n = 0
                        for text in top_texts:
                            n += 1
                            text = text.replace(u'：', ':')
                            texts = text.split(':')
                            if texts[0] == text:
                                if n == 1:
                                    dict_[u'top_企业名称'] = text.strip()
                            else:
                                if len(texts) == 2:
                                    dict_[u'top_' + texts[0].strip()] = texts[1].strip()
        except:
                self.log.info(u"获取top信息异常")
        return dict_


