# -*- coding:utf-8 -*-
# CreateTime 2016.6.6 by yangwen

import sys
import os
import json
import copy
import chardet
from lxml import etree
from ParserBase import ParserBase
import html4test as test
reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

class HainanHandler(ParserBase):

    # 备案信息中若出现以下KEY，解析到股东信息中
    # baxx_to_gdxx_keys = [u"股东类型", u"股东", u"投资人", u"投资人类型", u"出资人", u"出资人类型"]

    """
    ParserHainan is used to parse the enterprise info from Hainan
    @version:1.0
    @author:david ding
    @modify:
    """
    def __init__(self, pinyin):
        ParserBase.__init__(self, pinyin)
        self.ignore_key_list.extend([u"gdxq_html", u'gdxx.详情'])
        self.log.info(u"HainanHandler 构造完成")

    def parse(self,html_dict, result_dict=None):
        if not html_dict or not isinstance(result_dict,dict):
            return None
        if 'company_name' in html_dict:
            self.log.info(u"开始解析 %s" % html_dict['company_name'])
        self.log.info(u"开始解析通用信息")
        company = self.parseCommon(html_dict)


        # 获取股东信息、变更信息、备案信息、分支机构表头
        try:
            html_tree = etree.HTML(html_dict["jbxx_html"][0]["_body"])

            # 股东信息表头
            gdxx_html_list = []
            try:
                # gdxx_header_xpath = html_tree.xpath(".//div[@id='invDiv']/preceding-sibling::table[1]")
                # if gdxx_header_xpath:
                #     gdxx_header_html = etree.tostring(gdxx_header_xpath[0])
                #     if html_dict.has_key("gdxx_html") and html_dict["gdxx_html"]:
                #         gdxx_html_list = html_dict["gdxx_html"]
                #         for gdxx_num in range(0,len(gdxx_html_list)):
                #             html_dict["gdxx_html"][gdxx_num]["_body"] = gdxx_header_html + html_dict["gdxx_html"][gdxx_num]["_body"]
                html_dict, gdxx_html_list = self.htmlAppendTableHeader(html_dict,
                                                                       html_tree,
                                                                       ".//div[@id='invDiv']/preceding-sibling::table[1]",
                                                                       "gdxx_html")
            except Exception as e:
                self.log.info(str(e))

            # 变更信息表头
            bgxx_html_list = []
            try:
                html_dict, bgxx_html_list = self.htmlAppendTableHeader(html_dict,
                                                                       html_tree,
                                                                       ".//div[@id='altDiv']/preceding-sibling::table[1]",
                                                                       "bgxx_html")
            except Exception as e:
                self.log.info(str(e))

            # 备案信息表头
            baxx_html_list = []
            try:
                html_dict,baxx_html_list = self.htmlAppendTableHeader(html_dict,
                                                                      html_tree,
                                                                      ".//div[@id='memDiv']/preceding-sibling::table[1]",
                                                                      "baxx_html")
            except Exception as e:
                self.log.info(str(e))

            # 分支机构表头
            fzjg_html_list = []
            try:
                html_dict,fzjg_html_list = self.htmlAppendTableHeader(html_dict,
                                                                      html_tree,
                                                                      ".//div[@id='childDiv']/preceding-sibling::table[1]",
                                                                      "fzjg_html")
            except Exception as e:
                self.log.info(str(e))

            # 有分页数据，进行二次解析
            if gdxx_html_list or bgxx_html_list or baxx_html_list or fzjg_html_list:
                self.log.info(u"有分页数据，开始二次解析通用信息")
                company = self.parseCommon(html_dict)

        except Exception as e:
            self.log.info(str(e))


        baxx_lst=[]
        try:
            if company.has_key("baxx"):
                baxx_list = company["baxx"]
                if baxx_list:
                    for baxx in baxx_list:
                        if (baxx.has_key(u"序号") and baxx[u"序号"]) and ((baxx.has_key(u"姓名") and baxx[u"姓名"]) or (baxx.has_key(u"姓名（名称）") and baxx[u"姓名（名称）"])):
                            baxx_lst.append(baxx)
                    company["baxx"] = baxx_lst
        except Exception as e:
            self.log.error(str(e))

        # 判断当前的数据是否是股东信息【这里可能会有备案信息放在了股东信息中】
        # if len(company["baxx"]) > 0:
        #     temp_data = company["baxx"][0]
        #     esxx = list(set(temp_data) & set(self.baxx_to_gdxx_keys))
        #     if len(esxx) > 0:
        #         company['gdxx'] = company['baxx']
        #         company['baxx'] = []
        #     else:
        #         company['baxx'] = company['baxx']
        # else:
        #     company['baxx'] = []

        self.log.info(u"通用信息解析完成")
        top_dict = self.parseTop(html_dict)
        if top_dict:
            self.log.info(u"top信息解析成功")
            company.update(top_dict)
        else:
            self.log.info(u"top信息解析失败")
        self.standardizeField(company)
        company_copied = copy.deepcopy(company)
        if result_dict and isinstance(result_dict, dict):
            result_dict.update(company_copied)
        result_json = json.dumps(result_dict, ensure_ascii=False)
        self.log.info(u"HainanHandler 解析结果：\n" + result_json)
        return result_dict

    # 统一处理表头
    def htmlAppendTableHeader(self,html_dict,html_tree, header_xpath, append_type):
        type_html_list = []
        type_header_xpath = html_tree.xpath(header_xpath)
        if type_header_xpath:
            type_header_html = etree.tostring(type_header_xpath[0])
            if html_dict.has_key(append_type) and html_dict[append_type]:
                type_html_list = html_dict[append_type]
                for type_num in range(0, len(type_html_list)):
                    html_dict[append_type][type_num]["_body"] = type_header_html + html_dict[append_type][type_num]["_body"]
        return html_dict,type_html_list

    def standardizeField(self, company):
        self.log.info(u"开始清理、修复字段")
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
            top_str = tree.xpath(".//*[@id='details']/h2/text()")
            if not top_str:
                self.log.info(u"获取top信息失败")
                return None
            top_str = top_str[0].replace(u"该企业已列入经营异常名录", "").replace(u'\xa0', '').replace(u':', u'：')
            tops = top_str.split()
            if len(tops) >= 2:
                dict_[u'top_企业名称'] = tops[0].strip()
                zch = tops[1].split(u'：')
                if len(zch) == 2:
                    dict_[u'top_' + zch[0].strip()] = zch[1].strip()
        except:
            self.log.info(u"获取top信息异常")
        return dict_

if __name__ == "__main__":
    handler = HainanHandler(u"hainan")