# -*- coding: utf-8 -*-
# Created by John on 2016/6/2.

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

class NeimengguHandler(ParserBase):
    """
    NeimengguHandler is used to parse the enterprise info from Shanghai
    @version:1.0
    @author:John Liu
    @modify:
    """
    def __init__(self, pinyin):
        """
        Initiate the parameters.
        """
        ParserBase.__init__(self, pinyin)
        self.log.info(u"NeimengguHandler 构造完成")

    def parse(self, html_dict, all_reslt_dict=None):
        if not html_dict or not isinstance(html_dict, dict):
            return None
        if 'company_name' in html_dict:
            self.log.info(u"开始解析 %s" % html_dict['company_name'])

        # TODO: 现在股东详情的表格是嵌套的, 调用通用方法解析时会抛异常, 暂时先不解析股东详情, 后续添加
        if html_dict.has_key("gdxq_html"):
            gdxq_html = html_dict.pop("gdxq_html")

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
        self.log.info(u"NeimengguHandler解析结果：\n" + result_json)
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
            tops = tree.xpath(".//*[@id='details']/div[1]/h2")
            if tops:
                top = tops[0].text
                key=u'注册号'
                infos = top.strip().replace(u'“该企业已列入经营异常名录”',"").replace(u"该企业已列入经营异常名录","").replace(u'\xa0', '').replace(u':', u'：').split(key)
                if len(infos) == 2:
                    dict_[u'top_企业名称'] = infos[0].strip()
                    if u'：' in infos[1]:
                        temp = (key+infos[1]).split(u'：')
                        dict_['top_'+temp[0].strip()] = temp[1].strip()
        except:
            self.log.info(u"获取top信息异常")
            dict_ = dict()
        return dict_

def testFromSSDB(db_inst, row_key):
    html_dict_str = db_inst.hget(row_key)
    if not html_dict_str:
        print(u"从SSDB获取数据失败！")
        return
    handler = NeimengguHandler("neimenggu")
    html_dict = json.loads(html_dict_str)
    handler.parse(html_dict)


if __name__ == "__main__":
    db_inst = DBManager.getInstance("ssdb", "neimenggu", host="spider5", port=57888)
    row_key = "1a7630b3a30addefcae6c3d092630a11|_|内蒙古蒙牛乳业包头有限责任公司|_|91150200701240234X|_|2016-06-22|_|neimenggu"
    testFromSSDB(db_inst, row_key)
    pass


