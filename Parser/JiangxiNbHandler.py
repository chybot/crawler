# -*- coding: utf-8 -*-
# Created by wuyong on 2016/6/3.

import sys
import os
import re
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

class JiangxiNbHandler(ParserNbBase):
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
        self.log.info(u"JiangxiNbHandler 构造完成")

    def parse(self, html_dict, reslt_dict=None):
        if not html_dict or not isinstance(html_dict, dict):
            return None
        if 'company_name' in html_dict:
            self.log.info(u"开始解析 %s" % html_dict['company_name'])
        self.log.info(u"开始解析通用信息")
        html_dict= self.parseCommonPre(html_dict)
        company = self.parseCommon(html_dict)
        company = self.standardizeField(company) #
        self.log.info(u"通用信息解析完成")

        company_copied = copy.deepcopy(company)

        if reslt_dict and isinstance(reslt_dict, dict):
            reslt_dict.update(company_copied)
        result_json = json.dumps(reslt_dict, ensure_ascii=False)
        self.log.info(u"SichuanNbHandler解析结果：\n" + result_json)
        return reslt_dict


    #u'2015年10月20日%r%n%t%t%t%t%t%t%t%t%t%t-%r%n%t%t%t%t%t%t%t%t%t2016年12月31日',  江西长运股份有限公司  去掉\r\n\t
    def standardizeField(self, company):
        qynb = company.get('qynb')
        if qynb and qynb.get(u'对外提供保证担保信息'):
            dbxx_list = qynb.get(u'对外提供保证担保信息')
            #dbxx_rlist = []
            for index in range(len(dbxx_list)):
                if dbxx_list[index].get(u'履行债务的期限'):
                    dbxx_list[index][u'履行债务的期限'] = re.sub(r'\s+', '', dbxx_list[index][u'履行债务的期限'])
            company['qynb'][u'对外提供保证担保信息'] = dbxx_list
        return company

    def parseCommonPre(self, html_dict):
        body = ''
        nb_key = ''
        for key in html_dict.keys():
            if key.endswith("_html") and "qynb_" in key:
                nb_key = key
                try:
                    body = html_dict[key][0]["_body"]
                    nb_year = key.replace("qynb_", "").replace("_html", "").replace("_json", "")
                    break
                except Exception as e:
                    pass
        if body:
            body = re.sub(r'<span>|</span>|<b\s+.*?>|</b>', '', body, re.S)
            html_dict[nb_key][0]['_body'] = body
            return html_dict


    # def parseRowCommonTable(self, table, head_xpath):
    #     res_list = []
    #     head_b = ''
    #     rows = table.xpath('./tr')
    #     for row_index, row in enumerate(rows):
    #         if row_index == 0:
    #             head_b = table.xpath(head_xpath)
    #             if not head_b or not head_b[0].strip():
    #                 return None  # 设定表格肯定有头（第一行只有一条数据）
    #             head_b = head_b[0].strip()
    #             continue
    #         if row_index == 1:
    #             tit_ths = row.xpath('./th/text()')
    #             continue
    #         tmp_dict = {}
    #         tit_th_cnt = len(tit_ths)
    #         for col_index in range(tit_th_cnt):
    #             # print 'xxxx  ', col_index + 1
    #             col_val = row.xpath('./td[%s]/text()' % (col_index + 1))
    #             col_val = col_val[0].strip() if col_val else ''
    #             tmp_dict.update({tit_ths[col_index]: col_val})
    #         res_list.append(tmp_dict)
    #     return {head_b: res_list if res_list else ''}
    #
    # def parseRowKvTable(self, table, head_xpath):
    #     res_dict = {}
    #     head_b = ''
    #     rows = table.xpath('./tr')
    #     for row_index, row in enumerate(rows):
    #         if row_index == 0:
    #             head_b = table.xpath(head_xpath)
    #             if not head_b or not head_b[0].strip():
    #                 return None  # 设定表格肯定有头（第一行只有一条数据）
    #             head_b = head_b[0].strip()
    #             continue
    #         if row_index == 1:
    #             tit_ths_len = int(row.xpath('count(./th/text())'))
    #         tit_ths = row.xpath('./th/text()')
    #         val_tds = row.xpath('./td/text()')
    #         for index in range(tit_ths_len):
    #             res_dict.update({tit_ths[index].strip(): val_tds[index].strip() if val_tds[index] else ''})
    #     return {head_b: res_dict if res_dict else ''}
    #
    # def parseJiangxiTab(self, table, head_xpath):
    #     head_b = ''
    #     if not table:
    #         return None
    #     table_flag = 0 if table.xpath('./tr[2]/td') else 1
    #     return self.parseRowCommonTable(table, head_xpath) if table_flag else  self.parseRowKvTable(table, head_xpath)
    #
    # def parseJiangxiTabs(self, body):
    #     et = etree.HTML(body.decode('gbk'))
    #     tables = et.xpath('//table[@class="detailsList"]')
    #     ret_list = []
    #     for tab_index, tab in enumerate(tables):
    #         if tab_index == 4 or tab_index == 7:
    #             res_dic = parseJiangxiTab(tab, './tr[1]/th/b/text()')  # './tr[1]/th/span/b/text()')
    #         else:
    #             res_dic = parseJiangxiTab(tab, './tr[1]/th/span/b/text()')
    #         ret_list.append(res_dic)
    #     return ret_list

if __name__ == "__main__":
    pass
