# -*- coding: utf-8 -*-
# Created by David on 2016/5/21.
# modify by wuyong
import sys
import os
import re
import json
import copy
import chardet
from lxml import etree
from ParserBase import ParserBase
import html4test as test
reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

class JiangxiHandler(ParserBase):
    """
    JiangxiHandler is used to parse the enterprise info from Jiangxi
    @version:1.0
    @author:david ding
    @modify:
    """
    #TODO 股东详情？？？？
    def __init__(self, pinyin):
        """
        Initiate the parameters.
        """
        ParserBase.__init__(self, pinyin)
        self.ignore_key_list.extend(["gdxq_html",u'gdxx.详情'])
        self.log.info(u"JiangxiHandler 构造完成")

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
        bgxx_dict = self.parseBgxx(html_dict)
        if bgxx_dict:
            company.update(bgxx_dict)
            #print 'bgxx parse success, ', bgxx_dict
        company = self.standardizeField(company)
        company_copied = copy.deepcopy(company)
       #print 'com ', company
        if reslt_dict and isinstance(reslt_dict, dict):
            reslt_dict.update(company_copied)
        result_json = json.dumps(reslt_dict, ensure_ascii=False)
        self.log.info(u"JiangxiHandler解析结果：\n" + result_json)
        return reslt_dict

    def standardizeField(self, company):
        self.log.info(u"开始清理、修复字段")
        zb = company.get(u'注册资本')
        if zb:
            company[u'注册资本'] = self.remove_all_space_char(zb)
        return company

    def remove_all_space_char(self, ss):
        temp = re.sub(ur'[\x00-\x20]', '', unicode(ss))
        return re.sub(ur'\xa0', '', unicode(temp))

    def parseBgxx(self, html_dict):
        if 'bgxx_html' not in html_dict:
            return None
        bgxx_html = html_dict['bgxx_html']
        if not bgxx_html:
            return None
        if '_body' not in bgxx_html[0]:
            return None
        return self.parseBgxxHtml(bgxx_html[0]['_body'])

    def parseBgxxHtml(self, s):
        et = etree.HTML(re.sub(r'<tbody.*?>|</tbody>', '', s, re.S))  # .decode('gbk'))
        table = et.xpath('//table[@class="detailsList"]')
        if not table:
            return None
        table = table[0]
        res_list = []
        head_b = ''
        rows = table.xpath('./tr')
        if len(rows) <= 2:
            return None
        for row_index, row in enumerate(rows[0:-1]):
            if row_index == 0:
                head_b = table.xpath('./tr[1]/th/text()')
                if not head_b or not head_b[0].strip():
                    return None  # 设定表格肯定有头（第一行只有一条数据）
                head_b = head_b[0].strip()
                continue
            if row_index == 1:
                tit_ths = row.xpath('./th/text()')
                if not tit_ths:
                    return None
                continue
            tmp_dict = {}
            tit_th_cnt = len(tit_ths)
            for col_index in range(tit_th_cnt):
                col_val = ''
                col_val_td = row.xpath('./td[%s]/text()' % (col_index + 1))
                col_val_ahref = row.xpath('./td[%s]/a/@onclick' % (col_index + 1))
                if col_val_ahref:
                    col_val_pre = col_val_ahref[0].strip() if col_val_ahref else ''
                    #print 'val_pre ', col_val_pre
                    col_val = re.findall(r'showBg[h|q]nr\(\'(.*?)\',', col_val_pre, re.S)
                    col_val = col_val[0].strip() if col_val else ''
                    # col_val = re.findall(r'"showBgqnr(.*?)', col_val_pre, re.S)
                    print 're', col_val
                else:
                    col_val = col_val_td[0].strip() if col_val_td else ''
                tmp_dict.update({tit_ths[col_index]: col_val})
            res_list.append(tmp_dict)
        return {'bgxx':res_list} if res_list else None

    def parseTop(self, html_dict):
        if 'top_html' not in html_dict:
            return None
        top_list = html_dict['top_html']
        if not top_list:
            return None
        if '_body' not in top_list[0]:
            return None
        return self.parseTopHtml(top_list[0]['_body'])

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
            tops = tree.xpath(".//*[@id='gsh3']/text()")
            if not tops:
                self.log.info(u"获取top信息失败")
                return None
            info = tops[0]
            key = u'统一社会信用代码'
            if ur"注册号/统一社会信用代码" in info:
                key = ur"注册号/统一社会信用代码"
            infos = info.strip().replace(u'“该企业已列入经营异常名录”', "").replace(u"该企业已列入经营异常名录", "").replace(u'\xa0','').replace(u':',u'：').split(key)
            if len(infos) == 2:
                dict_[u'top_企业名称'] = infos[0].strip()
                if u'：' in infos[1]:
                    temp = (key + infos[1]).split(u'：')
                    dict_['top_' + temp[0].strip()] = temp[1].strip()
        except:
                self.log.info(u"获取top信息异常")
        return dict_

if __name__ == "__main__":
    # top_dict = test_top()
    handler = JiangxiHandler("jiangxi")
    tp_dict = handler.parseTopHtml(test.html_jiangxi_top)
    pass


