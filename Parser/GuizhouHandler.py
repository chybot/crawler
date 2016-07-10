# -*- coding: utf-8 -*-
# Created by John on 2016/6/6.

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

class GuizhouHandler(ParserBase):
    """
    ParserGuizhou is used to parse the enterprise info from Guizhou
    @version:1.0
    @author:John Liu
    @modify:
    """
    def __init__(self, pinyin):
        """
        Initiate the parameters.
        """
        ParserBase.__init__(self, pinyin)
        self.initMapper()
        self.log.info("GuizhouHandler 构造完成")

    def initMapper(self):
        self.appendJsonMapperConfig("jbxx_json", {'zch': u'注册号或统一社会信用代码', 'qymc': u'名称', 'zhmc': u'名称',
                                                  'qylxmc': u'类型', 'fddbr': u'法定代表人',
                                                  'zs': u'住所', 'zczb': u'注册资本',
                                                  'clrq': u'成立日期', 'yyrq1': u'经营期限自',
                                                  'yyrq2': u'经营期限至', 'jyfw': u'经营范围',
                                                  'djjgmc': u'登记机关', 'hzrq': u'核准日期',
                                                  'mclxmc': u'登记状态', 'jyzm': u'经营者',
                                                  'zcxsmc': u'组成形式'})

        self.appendJsonMapperConfig("gdxx_json", {'tzrlxmc': u'gdxx.股东类型', 'czmc': u'gdxx.股东',
                                                  'zzlxmc': u'gdxx.证照或证件类型', 'zzbh': u'gdxx.证照或证件号码'})

        # self.appendJsonMapperConfig("gdxq_json", {'czmc': u'gdxq.投资人名称', 'tzrlxmc': u'gdxq.投资人类型',
        #                                           'rjcze': u'gdxq.认缴出资额', 'rjczfsmc': u'gdxq.出资方式',
        #                                           'rjczrq': u'gdxq.出资时间', 'sjcze': u'gdxq.实缴出资额',
        #                                           'sjczfsmc': u'gdxq.实缴出资方式', 'sjczrq': u'gdxq.实缴出资时间'})

        self.appendJsonMapperConfig("bgxx_json", {'bghnr': u'bgxx.变更后内容', 'bcnr': u'bgxx.变更前内容',
                                                  'bcsxmc': u'bgxx.变更事项', 'hzrq': u'bgxx.变更日期'})

        self.appendJsonMapperConfig("baxx_json", {'xm': u'baxx.姓名', 'zwmc':u'baxx.职务', 'jyzm': u'baxx.姓名', 'rownum': u'baxx.序号'})

        self.appendJsonMapperConfig('fzjg_json', {'fgszch': u'fzjg.注册号', 'fgsmc': u'fzjg.名称',
                                                  'fgsdjjgmc': u'fzjg.登记机关'})

        self.appendJsonMapperConfig('xzcf_json', {'cfjdsh': u'xzcf.行政处罚决定书文号', 'wfxwlxmc': u'xzcf.违法行为类型',
                                                  'xzcfnr': u'xzcf.行政处罚内容', 'cfjgmc': u'xzcf.作出行政处罚决定机关名称',
                                                  'cfrq': u'xzcf.作出行政处罚决定日期', 'gsrq': u'xzcf.公示日期',
                                                  'rownum': u'xzcf.序号'})

    def parse(self, html_dict, all_reslt_dict=None):
        if not html_dict or not isinstance(html_dict, dict):
            return None
        if 'company_name' in html_dict:
            self.log.info("开始解析 %s" % html_dict['company_name'])

        # 贵州企业的特殊处理,先取出top_html,防止通用信息解析时对基本信息解析的影响
        top_html_contents = html_dict.pop("top_html")

        # 解析top_html中的特殊数据
        special_dict = dict()
        special_dict["top_html"] = top_html_contents
        special_fields = self.parseCommon(special_dict)

        self.log.info("开始解析通用信息")
        company = self.parseCommon(html_dict)
        self.log.info("通用信息解析完成")

        # 把top_html加回html_dict
        html_dict["top_html"] = top_html_contents

        # 处理HTML中的特殊数据
        self.parseSpecialFields(company, special_fields)

        top_dict = self.parseTop(html_dict)
        if top_dict:
            self.log.info("top信息解析成功")
            company.update(top_dict)
        else:
            self.log.info("top信息解析失败")
        self.standardizeField(company)
        company_copied = copy.deepcopy(company)
        if all_reslt_dict and isinstance(all_reslt_dict, dict):
            all_reslt_dict.update(company_copied)
        result_json = json.dumps(all_reslt_dict, ensure_ascii=False)
        self.log.info("GuizhouHandler解析结果：\n" + result_json)
        return all_reslt_dict

    def parseSpecialFields(self, company, special_fields):
        try:
            # 处理登记状态
            if not company.has_key(u"登记状态") and special_fields[u"登记状态"]:
                company[u"登记状态"] = special_fields[u"登记状态"]

            # 处理公司类型
            if not company.has_key(u"类型") and special_fields[u"类型"]:
                company[u"类型"] = special_fields[u"类型"]

        except Exception as e:
            self.log.warning(u"解析特殊字段失败: " % e)
            pass

    def standardizeField(self, company):
        pass

    def parseTop(self, html_dict):
        if 'top_html' not in html_dict:
            return None
        jbxx_list = html_dict['top_html']
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
            # tops = tree.xpath(".//*[@id='mct']")
            tops = tree.xpath(".//*[@id='pageTitle']")
            if tops:
                top = tops[0].text
                kks = top.replace(u'“该企业已列入经营异常名录”', "").replace(u"该企业已列入经营异常名录", "").strip().split()
                if len(kks) >= 2:
                    dict_[u'top_企业名称'] = kks[0].strip()
                    vvs = kks[1].split("：")
                    if len(vvs) == 2:
                        dict_['top_' + vvs[0].strip()] = vvs[1].strip()
        except:
                self.log.info("获取top信息异常")
        return dict_

if __name__ == "__main__":
    handler = GuizhouHandler("guizhou")
    top_dict = handler.parseTopHtml(test.html_guizhou)
    pass
