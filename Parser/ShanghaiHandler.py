# -*- coding: utf-8 -*-
# Created by David on 2016/5/19.

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

class ShanghaiHandler(ParserBase):
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
        self.log.info(u"ShanghaiHandler 构造完成")

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
        self.log.info(u"ShanghaiHandler解析结果：\n" + result_json)
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
            top_texts = tree.xpath('.//div[@class="notice"]/ul/li/text()')
            if not top_texts:
                self.log.info(u"获取top信息失败")
            else:
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

def testFromSSDB(db_inst, row_key):
    html_dict_str = db_inst.hget(row_key)
    if not html_dict_str:
        print(u"从SSDB获取数据失败！")
        return
    handler = ShanghaiHandler("shanghai")
    html_dict = json.loads(html_dict_str)
    handler.parse(html_dict)


if __name__ == "__main__":
    db_inst = DBManager.getInstance("ssdb", "new_shanghai_data", host="spider5", port=57888)
    row_key = "c97ec20e493f366be44508f44001a583|_|上海乾辉工贸有限公司分公司|_|shanghai|_|2016-05-22"
    testFromSSDB(db_inst, row_key)
    pass


