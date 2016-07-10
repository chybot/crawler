# -*- coding: utf-8 -*-
# Created by David on 2016/5/19.

import sys
import os
import json
import chardet
import copy
from lxml import etree
from ParserBase import ParserBase
import html4test as test
from CommonLib.TimeUtil import TimeUtil
reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

class JilinHandler(ParserBase):
    """
    JilinHandler is used to parse the enterprise info from Jilin
    @version:1.0
    @author:david ding
    @modify:
    """
    def __init__(self, pinyin):
        """
        Initiate the parameters.
        """
        ParserBase.__init__(self, pinyin)
        self.initMapper()
        self.log.info(u"JilinHandler 构造完成")

    def initMapper(self):
        self.appendJsonMapperConfig("gdxx_json", {'blicno': u'gdxx.证照或证件号码', 'inv': u'gdxx.股东', 'blictype': u'gdxx.证照或证件类型', 'invtype': u'gdxx.股东类型',
             'primary_key': 'inv,blicno'})
        self.appendJsonMapperConfig("bgxx_json", {'altaf': u'bgxx.变更后内容', 'altbe': u'bgxx.变更前内容', 'altitem': u'bgxx.变更事项', 'altdate.time': u'bgxx.变更日期'})
        self.appendJsonMapperConfig("baxx_json", {'name': u'baxx.姓名', 'position':u'baxx.职务'})

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
        self.log.info(u"JilinHandler解析结果：\n" + result_json)
        return all_reslt_dict

    def standardizeField(self, company):
        self.log.info(u"开始清理、修复字段")
        if u'bgxx' in company and isinstance(company[u'bgxx'], list):
            for bg in company[u'bgxx']:
                if u'变更日期' not in bg:
                    continue
                try:
                    bg[u'变更日期'] = unicode(TimeUtil.stamp2Date(bg[u'变更日期'], u'%Y年%m月%d日'))
                except:
                    self.log.warning(u"转换timestamp为标准日期时出错！")
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
            tops = tree.xpath(".//*[@id='mct']")
            if tops:
                top = tops[0].text
                kks = top.replace(u'“该企业已列入经营异常名录”', "").replace(u"该企业已列入经营异常名录", "").strip().split()
                if len(kks) >= 2:
                    dict_[u'top_企业名称'] = kks[0].strip()
                    vvs = kks[1].split("：")
                    if len(vvs) == 2:
                        dict_['top_' + vvs[0].strip()] = vvs[1].strip()
        except:
                self.log.info(u"获取top信息异常")
        return dict_

if __name__ == "__main__":
    handler = JilinHandler("jilin")
    top_dict = handler.parseTopHtml(test.html_jilin)
    pass
