# -*- coding: utf-8 -*-
# Created by John on 2016/6/21.

import sys
import os
import json
import copy
import chardet
import re
from lxml import etree
from ParserBase import ParserBase
from CommonLib.DB.DBManager import DBManager
import html4test as test
reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

class HeilongjiangHandler(ParserBase):
    """
    HeilongjiangHandler is used to parse the enterprise info from Shanghai
    @version:1.0
    @author:John Liu
    @modify:
    """
    def __init__(self, pinyin):
        """
        Initiate the parameters.
        """
        ParserBase.__init__(self, pinyin)
        self.log.info(u"HeilongjiangHandler 构造完成")

    def parse(self, html_dict, all_reslt_dict=None):
        if not html_dict or not isinstance(html_dict, dict):
            return None
        if 'company_name' in html_dict:
            self.log.info(u"开始解析 %s" % html_dict['company_name'])

        # TODO: 现在股东详情的表格是嵌套的, 调用通用方法解析时会抛异常, 暂时先不解析股东详情, 后续添加
        if html_dict.has_key("gdxq_html"):
            gdxq_html = html_dict.pop("gdxq_html")

        # 格式化翻页信息表头
        self.standardizeHeader(html_dict)

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
        self.log.info(u"HeilongjiangHandler解析结果：\n" + result_json)
        return all_reslt_dict

    def standardizeField(self, company):
        self.log.info(u"开始清理、修复字段")
        if u'注册号/' in company:
            company[u'注册号/统一社会信用代码'] = company[u'注册号/']
            del company[u'注册号/']

    def standardizeHeader(self, html_dict):
        jbxx_html = list()

        if html_dict.has_key("jbxx_html"):
            jbxx_html = html_dict["jbxx_html"]
        if not jbxx_html:
            return

        # 添加股东信息表头
        if html_dict.has_key("gdxx_html"):
            self.appendHeader(html_dict, jbxx_html[0]["_body"], ".//div[@id='invDiv']/preceding-sibling::table[1]",
                              "gdxx_html")

        # 添加变更信息表头
        if html_dict.has_key("bgxx_html"):
            self.appendHeader(html_dict, jbxx_html[0]["_body"], ".//div[@id='altDiv']/preceding-sibling::table[1]",
                              "bgxx_html")

        # 添加备案信息表头
        if html_dict.has_key("baxx_html"):
            self.appendHeader(html_dict, jbxx_html[0]["_body"], ".//div[@id='memDiv']/preceding-sibling::table[1]",
                              "baxx_html")

        # 添加分支机构表头
        if html_dict.has_key("fzjg_html"):
            self.appendHeader(html_dict, jbxx_html[0]["_body"], ".//div[@id='childDiv']/preceding-sibling::table[1]",
                              "fzjg_html")

        # 添加行政处罚表头
        if html_dict.has_key("xzcf_html"):
            self.appendHeader(html_dict, jbxx_html[0]["_body"], ".//div[@id='punDiv']/preceding-sibling::table[1]",
                              "xzcf_html")

    def appendHeader(self, html_dict, jbxx_html, xpath_rules, target_html):
        try:
            tree = etree.HTML(jbxx_html)
            header = tree.xpath(xpath_rules)
            header = etree.tostring(header[0])
            for target in html_dict[target_html]:
                target["_body"] = header + target["_body"]
            return

        except Exception as e:
            self.log.warning(u"为%s添加表头信息失败!" % target_html)

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
            top_texts = tree.xpath('.//*[@id="details"]/h2/text()')
            if not top_texts:
                self.log.info(u"获取top信息失败")
            else:
                if len(top_texts) == 1:
                    top_texts = "".join(map(lambda x: x.strip().replace(u'\xa0', u'\t'), top_texts)).replace(r"： ",":").replace(u"“该企业已列入经营异常名录”","")
                    top_texts=top_texts.split()
                    n = 0
                    for text in top_texts:
                        n += 1
                        text = text.replace(u'：', ':')
                        texts = text.split(':')
                        if texts[0] == text:
                            if n == 1:
                                dict_[u'top_企业名称'] = text.strip()
                        else:
                            if len(texts) >= 2:
                                dict_[u'top_' + texts[0].strip()] = texts[1].strip()
        except:
                self.log.info(u"获取top信息异常")
        return dict_

def testFromSSDB(db_inst, row_key):
    html_dict_str = db_inst.hget(row_key)
    if not html_dict_str:
        print(u"从SSDB获取数据失败！")
        return
    handler = HeilongjiangHandler("qinghai")
    html_dict = json.loads(html_dict_str)
    handler.parse(html_dict)


if __name__ == "__main__":
    db_inst = DBManager.getInstance("ssdb", "heilongjiang", host="spider5", port=57888)
    row_key = "d833488218278803eadb28d469cd6257|_|黑龙江柏杉林木业有限公司|_|91230184690719556X|_|2016-06-21|_|heilongjiang"
    testFromSSDB(db_inst, row_key)
    pass


