# -*- coding: utf-8 -*-
# Created by wuyong on 2016/5/21.

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

class SichuanHandler(ParserBase):
    """
    ParserShanghai is used to parse the enterprise info from Shanghai
    @version:1.0
    @author: wuyong
    @modify:
    """
    def __init__(self, pinyin):
        """
        Initiate the parameters.
        """
        ParserBase.__init__(self, pinyin)
        self.ignore_key_list.extend(["gdxq_html",u'gdxx.详情'])
        self.rslt_mapper_config = {
            u"合伙人信息.*": u"gdxx.*",
            u"基本信息.*": ".*",
            u"股东信息.*": u"gdxx.*",
            u"股东及出资信息.*": u"gdxx.*",
            u"投资人信息.*": u"gdxx.*",
            u"投资人及出资信息.*": u"gdxq.*",
            u"发起人.*": u"gdxx.*",
            u"变更信息.*": u"bgxx.*",
            u"主要人员信息.*": u"baxx.*",
            u"备案信息.*": u"baxx.*",
            u"成员名册.*": u"baxx.*",
            u"分支机构信息.*": u"fzjg.*",
            u"行政处罚信息.*": u"xzcf.*"
        }




        self.log.info(u"SiChuanHandler 构造完成")

    def parse(self, html_dict, reslt_dict=None):
        if not html_dict or not isinstance(html_dict, dict):
            return None
        if 'company_name' in html_dict:
            self.log.info(u"开始解析 %s" % html_dict['company_name'])
        self.log.info(u"开始解析通用信息")
        company = self.parseCommon(html_dict, self.rslt_mapper_config)
        self.log.info(u"通用信息解析完成")
        top_dict = self.parseTop(html_dict)
        if top_dict:
            self.log.info(u"top信息解析成功")
            company.update(top_dict)
        else:
            self.log.info(u"top信息解析失败")
        if company.get('bgxx'):
            bgxx = self.parseBgxx(html_dict)
            if bgxx:
                company.update({'bgxx':bgxx})
        company = self.standardizeField(company)
        company_copied = copy.deepcopy(company)
        if reslt_dict and isinstance(reslt_dict, dict):
            reslt_dict.update(company_copied)
        result_json = json.dumps(reslt_dict, ensure_ascii=False)
        self.log.info(u"SiChuanHandler解析结果：\n" + result_json)
        return reslt_dict

    def standardizeField(self, company):
        self.log.info(u"开始清理、修复字段")
        zb = company.get(u'注册资本')
        if zb:
            company[u'注册资本'] = self.remove_all_space_char(zb)
        return company

    def remove_all_space_char(self, ss):
        """
        去掉所有的不可见字符，包括空格，换行等等
        :param ss:
        :return:
        """
        temp = re.sub(ur'[\x00-\x20]', '', unicode(ss))
        return re.sub(ur'\xa0', '', unicode(temp))


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
        self.log.info("开始解析top信息")
        dict_ = dict()
        try:
            top_str = tree.xpath(".//*[@id='details']/h2/text()")
            #print 'topstr,  ',  top_str
            if not top_str:
                #print 'topstr1,  ', top_str
                self.log.info(u"获取top信息失败")
                return None
            #.replace(u'\xa0', '')

            top_str = top_str[0].replace("该企业已列入经营异常名录", "").replace(u'“该企业为吊销状态”','').replace(u':', u'：')
            tops = top_str.split()
            if len(tops) >= 2:
                dict_[u'top_企业名称'] = tops[0].strip()
                zch = tops[1].split(u'：')
                if len(zch) == 2:
                    dict_[u'top_' + zch[0].strip()] = zch[1].strip()
        except:
                self.log.info(u"获取top信息异常")
        #print dict_
        return dict_

    def parseBgxx(self, html_dict):
        if 'jbxx_html' not in html_dict:
            return None
        jbxx_list = html_dict['jbxx_html']
        if not jbxx_list:
            return None
        if '_body' not in jbxx_list[0]:
            return None
        return self.parseBgxxHtml(jbxx_list[0]['_body'])

    #变更信息，解析有更多选项，需要手动解析
    def parseBgxxHtml(self, html):
        if not html:
            return None
        et = etree.HTML(html.replace("<br>", "").replace("</br>", ""))
        tab_bg = et.xpath('.//table[@id="table_bg"]')
        if not tab_bg:
            return None
        tab_bg = tab_bg[0]
        head = tab_bg.xpath('.//tr[1]/th/text()')
        bgrow = tab_bg.xpath('.//tr[2]/th/text()')
        rs_list = []
        if bgrow and len(bgrow) >= 4:
            bgrow = map(lambda x:x.strip(), bgrow)
            if bgrow[0] and bgrow[1] and bgrow[2] and bgrow[3]:
                rows = tab_bg.xpath('.//tr[@name="bg"]')
                for row in rows:
                    tmp_dict = {}
                    row_1 = row.xpath('.//td[1]/text()')
                    tmp_dict[bgrow[0]] = row_1[0] if row_1 else ''
                    row_2_xpah = row.xpath('.//td[2]/span')
                    if row_2_xpah:
                        row_2 = row_2_xpah[0].xpath('.//text()') if len(row_2_xpah) == 1 else row_2_xpah[1].xpath('.//text()')
                        tmp_dict[bgrow[1]] = row_2[0].strip() if row_2 else ''
                    else:
                        tmp_dict[bgrow[1]] = ''
                    row_3_xpah = row.xpath('.//td[3]/span')
                    if row_3_xpah:
                        row_3 = row_3_xpah[0].xpath('.//text()') if len(row_3_xpah) == 1 else row_3_xpah[1].xpath('.//text()')
                        tmp_dict[bgrow[2]] = row_3[0].strip() if row_3 else ''
                    else:
                        tmp_dict[bgrow[2]] = ''
                    row_4 = row.xpath('.//td[4]/text()')
                    tmp_dict[bgrow[3]] = row_4[0].strip() if row_4 else ''
                    rs_list.append(tmp_dict)
        return rs_list


if __name__ == "__main__":
    # top_dict = test_top()
    #handler = BeijingHandler("beijing")
    #tp_dict = handler.parseTopHtml(test.html_shanghai)
    pass


