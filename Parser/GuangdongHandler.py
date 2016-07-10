# -*- coding: utf-8 -*-
# Created by David on 2016/5/21.

import sys
import os
import json
import copy
import chardet
from lxml import etree
from ParserBase import ParserBase
from CommonLib.TimeUtil import TimeUtil
import html4test as test
reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

class GuangdongHandler(ParserBase):
    """
    GuangdongHandler is used to parse the enterprise info from Guangdong
    @version:1.0
    @author:david ding
    @modify:
    """
    def __init__(self, pinyin):
        """
        Initiate the parameters.
        """
        ParserBase.__init__(self, pinyin)
        self.ignore_key_list.extend([u"gdxq_html", u'gdxx.详情'])
        self.appendJsonMapperConfig(u'bgxx_json', {'altFiledName':u'bgxx.变更事项', 'altBe':u'bgxx.变更前内容', 'altAf':u'bgxx.变更后内容', 'altDate':u'bgxx.变更日期', 'primary_key':'altDate, altFiledName, altAf' })
        self.appendJsonMapperConfig(u'baxx_json', {'name':u'baxx.姓名', 'position':u'baxx.职务', 'primary_key':'name, position' })
        self.appendJsonMapperConfig(u'fzjg_json', {'regNO': u'fzjg.注册号', 'brName': u'fzjg.名称', 'regOrg': u'fzjg.登记机关', 'primary_key': 'regNO, brName'})
        self.log.info(u"GuangdongHandler 构造完成")

    def parse(self, html_dict, reslt_dict=None):
        if html_dict[u'source'] == u'企业信息网':
            self.appendJsonMapperConfig(u'gdxx_json',{'invType': u'gdxx.股东类型', 'inv': u'gdxx.股东', 'certNo': u'gdxx.证照/证件号码', 'primary_key': 'inv, certNo'})
        elif html_dict[u'source'] == u'企业信用网':
            self.appendJsonMapperConfig(u'gdxx_json', {'invType':u'gdxx.股东类型', 'inv':u'gdxx.股东', 'entNo':u'gdxx.证照/证件号码', 'primary_key':'inv, entNo' })
        self.log.info(u"开始解析通用信息")
        company = self.parseCommon(html_dict)
        self.log.info(u"通用信息解析完成")
        self.standardizeField(company)
        self.removeDuplicate(company, 'gdxx', [u'股东',u'股东类型'])
        self.removeDuplicate(company, 'bgxx', [u'变更日期',u'变更事项',u'变更后内容'])
        self.removeDuplicate(company, 'baxx', [u'姓名',u'职务'])
        top_dict = self.parseTop(html_dict)
        if top_dict:
            self.log.info(u"top信息解析成功")
            company.update(top_dict)
        else:
            self.log.info(u"top信息解析失败")
        # self.standardizeField(company)
        company_copied = copy.deepcopy(company)
        if reslt_dict and isinstance(reslt_dict, dict):
            reslt_dict.update(company_copied)
        result_json = json.dumps(reslt_dict, ensure_ascii=False)
        self.log.info(u"GuangdongHandler 解析结果：\n" + result_json)
        return reslt_dict

    def standardizeField(self, company):
        self.log.info(u"开始清理、修复字段")
        if u'bgxx' in company:
            for info_dict in company[u'bgxx']:
                if u'变更日期' in info_dict:
                    if u'年' in info_dict[u'变更日期']:
                        continue
                    fromFormat = info_dict[u'变更日期'].replace('PM','').replace('AM','').strip()
                    info_dict[u'变更日期'] = TimeUtil.convertDateFromat(fromFormat, u"%b %d, %Y %H:%M:%S", u"%Y年%m月%d日")
        if u'baxx' in company:
            temp_list = list(company[u'baxx'])
            for info_dict in temp_list:
                value = ''
                for k,v in info_dict.items():
                    value += v.strip()
                if not value:
                    company[u'baxx'].remove(info_dict)

    def removeDuplicate(self, company, item, key_list):
        if item not in company or not key_list:
            return
        cleared_list = list(company[item])
        temp_set = set()
        for info_dict in company[item]:
            info_str = ''
            for key in key_list:
                if key not in info_dict:
                    continue
                info_str += info_dict[key]
            if info_str and info_str in temp_set:
                cleared_list.remove(info_dict)
            temp_set.add(info_str)
        company[item] = cleared_list

    def parseTop(self, html_dict):
        if u'jbxx_html' not in html_dict:
            return None
        jbxx_list = html_dict[u'jbxx_html']
        if not jbxx_list:
            return None
        if '_body' not in jbxx_list[-1]:
            return None
        return self.parseTopHtml(jbxx_list[-1]['_body'])

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
            top_str = tree.xpath(".//*[@id='details']//h2/text()")
            if not top_str:
                self.log.info(u"获取top信息失败")
                return None
            top_str = top_str[0].replace(u"该企业已列入经营异常名录", "").replace(u':', u'：')
            tops = top_str.split()
            if len(tops) == 2:
                dict_[u'top_企业名称'] = tops[0].strip()
                zch = tops[1].split(u'：')
                if len(zch) == 2:
                    dict_[u'top_' + zch[0].strip()] = zch[1].strip()
        except:
                self.log.info(u"获取top信息异常")
        return dict_

if __name__ == "__main__":
    # top_dict = test_top()
    #handler = BeijingHandler("beijing")
    #tp_dict = handler.parseTopHtml(test.html_shanghai)
    pass


