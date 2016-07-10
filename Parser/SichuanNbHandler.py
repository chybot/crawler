# -*- coding: utf-8 -*-
# Created by wuyong on 2016/6/3.

import sys
import os
import json
import copy
import chardet
from lxml import etree
from ParserNbBase import ParserNbBase
from lxml import etree

import html4test as test
reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

class SichuanNbHandler(ParserNbBase):
    """
    BeijingNbHandler is used to parse the annual report
    @version:1.0
    @author:wuyong
    @modify:
    """
    def __init__(self, pinyin):
        """
        Initiate the parameters.
        """
        ParserNbBase.__init__(self, pinyin)
        self.log.info(u"SichuanNbHandler 构造完成")

    def parse(self, html_dict, reslt_dict=None):
        if not html_dict or not isinstance(html_dict, dict):
            return None
        if 'company_name' in html_dict:
            self.log.info(u"开始解析 %s" % html_dict['company_name'])
        self.log.info(u"开始解析通用信息")
        company = self.parseCommon(html_dict)
        self.log.info(u"通用信息解析完成")
        body = ''
        nb_year = ''
        for key in html_dict.keys():
            if key.endswith("_html") and "qynb_" in key:
                try:
                    body = html_dict[key][0]["_body"]
                    nb_year = key.replace("qynb_","").replace("_html","").replace("_json","")
                    break
                except Exception as e:
                    pass
        #单独解析股东及出资信息
        if body and nb_year:
            rs_dic = self.parseGdczxx(body)
            if rs_dic:
                    if  company['qynb'] and  company['qynb'].get(rs_dic.keys()[0]):#(company['qynb'].get(u'股东及出资信息') or ):
                        company['qynb'].update(rs_dic)
            rs_list =self.parseBgxx(body)
            if rs_list:
                head  = rs_list[0]
                bgxx_list = rs_list[1]
                if bgxx_list:
                    if company['qynb'] and company['qynb'].get(head):
                        company['qynb'].update({head:bgxx_list})
        company_copied = copy.deepcopy(company)
        if reslt_dict and isinstance(reslt_dict, dict):
            reslt_dict.update(company_copied)
        result_json = json.dumps(reslt_dict, ensure_ascii=False)
        #self.log.info(u"SichuanNbHandler解析结果：\n" + result_json)
        return reslt_dict

    #股东及出资信息
    def parseGdczxx(self, body):
        rs_dict = {}
        if not body:
            return rs_dict
        et = etree.HTML(body.replace("<br>", "").replace("</br>", ""))
        gdcz_list = []
        t_tab = et.xpath('.//table[@id="table_tzrxx"]')
        if t_tab:
            head = t_tab[0].xpath("./tr[1]/th/text()")
            if head and head[0].strip():
                l_col = t_tab[0].xpath("./tr[2]/th/text()")
                if len(l_col) >= 7:
                    cols = t_tab[0].xpath('./tr[@name="tzrxx"]')
                    for col in cols:
                        per_dict = {}
                        col_0 = col.xpath('./td[1]/div/text()')
                        per_dict[l_col[0]] = col_0[0].strip() if col_0 and col_0[0].strip() else ''
                        for i in range(2, 8, 1):
                            col_i = col.xpath('./td[%d]/ul/li/text()' % i)
                            per_dict[l_col[i - 1].strip()] = col_i[0].strip() if col_i and col_i[0].strip() else ''
                        gdcz_list.append(per_dict)
                    rs_dict = {head[0].strip(): gdcz_list}
        return rs_dict

    #解析备案信息
    def parseBgxx(self, body):
        if not body:
            return None
        et = etree.HTML(body.replace("<br>", "").replace("</br>", ""))
        tab_bg = et.xpath('.//table[@id="table_bgxx"]')
        if not tab_bg:
            return None
        tab_bg = tab_bg[0]
        head = tab_bg.xpath('.//tr[1]/th/text()')
        if not head or not head[0].strip():
            return None
        head = head[0].strip()
        bgrow = tab_bg.xpath('.//tr[2]/th/text()')
        rs_list = []
        if bgrow and len(bgrow) >= 5:
            bgrow = map(lambda x : x.strip(), bgrow)
            if  bgrow[0] and bgrow[1] and bgrow[2] and bgrow[3] and bgrow[4]:
                rows = tab_bg.xpath('.//tr[@name="bgxx"]')
                for row in rows:
                    tmp_dict = {}
                    row_1 = row.xpath('.//td[1]/text()')
                    tmp_dict[bgrow[0]] = row_1[0] if row_1 else ''
                    row_2 = row.xpath('.//td[2]/text()')
                    tmp_dict[bgrow[1]] = row_2[0] if row_2 else ''
                    row_3_xpah = row.xpath('.//td[3]/span')
                    if row_3_xpah:
                        row_3 = row_3_xpah[0].xpath('.//text()') if len(row_3_xpah) == 1 else row_3_xpah[1].xpath(
                            './/text()')
                        tmp_dict[bgrow[2]] = row_3[0].strip() if row_3 else ''
                    else:
                        tmp_dict[bgrow[2]] = ''
                    row_4_xpah = row.xpath('.//td[4]/span')
                    if row_4_xpah:
                        row_4 = row_4_xpah[0].xpath('.//text()') if len(row_4_xpah) == 1 else row_4_xpah[1].xpath(
                            './/text()')
                        tmp_dict[bgrow[3]] = row_4[0].strip() if row_4 else ''
                    else:
                        tmp_dict[bgrow[3]] = ''
                    row_5 = row.xpath('.//td[5]/text()')
                    tmp_dict[bgrow[4]] = row_5[0].strip() if row_5 else ''
                    rs_list.append(tmp_dict)
        return head ,rs_list


if __name__ == "__main__":
    pass
