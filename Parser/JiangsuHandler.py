# -*- coding: utf-8 -*-
# Created by fml on 2016/5/19.

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
import re
import json
import warnings
class JiangsuHandler(ParserBase):
    """
    ParserShanghai is used to parse the enterprise info from Shanghai
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
        self.log.info("JiangsuHandler 构造完成")

    def initMapper(self):
        self.appendJsonMapperConfig("gdxx_json", {'C2': u'gdxx.股东/发起人', 'C1': u'gdxx.股东/发起人类型', 'C3': u'gdxx.证照/证件类型', 'C4': u'gdxx.证照/证件号码'})
        self.appendJsonMapperConfig("bgxx_json", {'C1': u'bgxx.变更事项', 'C2': u'bgxx.变更前内容', 'C3': u'bgxx.变更后内容', 'C4': u'bgxx.变更日期'})
        self.appendJsonMapperConfig('fzjg_json',{'RN':u'fzjg.序号','C1':u'fzjg.注册号','C2':u'fzjg.名称','C3':u'fzjg.登记机关',})

    def parse(self, html_dict, all_reslt_dict=None):
        if not html_dict or not isinstance(html_dict, dict):
            return None
        if 'company_name' in html_dict:
            self.log.info("开始解析 %s" % html_dict['company_name'])
        self.log.info("开始解析通用信息")
        company = self.parseCommon(html_dict)
        self.log.info("通用信息解析完成")
        jbxx = html_dict['jbxx_json']
        all_reslt_dict.update(self.parseJbxx(jbxx))
        if html_dict.has_key('baxx_json'):
            baxx = self.parseBaxx(html_dict['baxx_json'])
            all_reslt_dict.update({'baxx':baxx})
        if html_dict.has_key('top_json'):
            top_json = html_dict['top_json']
            all_reslt_dict.update(self.parseTop(top_json))

        company_copied = copy.deepcopy(company)
        if all_reslt_dict and isinstance(all_reslt_dict, dict):
            all_reslt_dict.update(company_copied)
        result_json = json.dumps(all_reslt_dict, ensure_ascii=False)
        self.log.info("JiangsuHandler解析结果：\n" + result_json)
        return all_reslt_dict

    def parseTop(self,top_json):
        top = {}
        if not isinstance(top_json,dict) and  not isinstance(top_json,list):
            top_json = json.loads(top_json)
        if not top_json:
            return top
        topjson = json.loads(top_json[0]['_body'])
        topjson = topjson[0] if isinstance(topjson,list) else topjson
        top[u"top_企业名称"] = topjson.get('C1','')
        temp_zhc_top = topjson.get('C2','')
        if len(temp_zhc_top) == 18:
            top[u"top_统一社会信用代码"] = temp_zhc_top
        else:
            top[u"top_注册号"] = temp_zhc_top
        return top

    def parseJbxx(self,jbxx_json):
        jbxx_result = {}
        if isinstance(jbxx_json,list):
            jbxx_json = jbxx_json[0]
        url = jbxx_json.get('url')
        body = jbxx_json.get('_body')
        if not url and body:
            raise Exception(u'基本信息网页原文有错误')
        _type = self.getType(url)
        if not _type:
            raise Exception(u'获取公司基本信息类型错误')
        if not isinstance(body,list):
            body = json.loads(body)
        map(lambda x:jbxx_result.update(self.parse_company_jbxx(x,_type)),body)
        return jbxx_result

    def parse_company_jbxx(self, jsons,company_type):
        """解析公司的基本信息"""
        jbxx_data = {}
        if company_type == 'ci':
            jbxx_data[u'注册号'] = jsons.get('C1', '')
            jbxx_data[u'名称'] = jsons.get('C2', '')
            jbxx_data[u'类型'] = jsons.get('C3', '')
            jbxx_data[u'法定代表人'] = jsons.get('C5', '')
            jbxx_data[u'注册资本'] = jsons.get('C6', '')
            jbxx_data[u'成立日期'] = jsons.get('C4', '')
            jbxx_data[u'住所'] = jsons.get('C7', '')
            jbxx_data[u'营业期限自'] = jsons.get('C9', '')
            jbxx_data[u'营业期限至'] = jsons.get('C10', '')
            jbxx_data[u'经营范围'] = jsons.get('C8', '')
            jbxx_data[u'登记机关'] = jsons.get('C11', '')
            jbxx_data[u'核准日期'] = jsons.get('C12', '')
            jbxx_data[u'登记状态'] = jsons.get('C13', '')
        elif company_type == "nccci":
            jbxx_data[u'注册号'] = jsons.get('C1', '')
            jbxx_data[u'名称'] = jsons.get('C2', '')
            jbxx_data[u'类型'] = jsons.get('C3', '')
            jbxx_data[u'法定代表人'] = jsons.get('C5', '')
            jbxx_data[u'住所'] = jsons.get('C7', '')
            jbxx_data[u'经营场所'] = jsons.get('C8', '')
            jbxx_data[u'注册资本'] = jsons.get('C6', '')
            jbxx_data[u'成立日期'] = jsons.get('C4', '')
            jbxx_data[u'经营期限自'] = jsons.get('C10', '')
            jbxx_data[u'经营期限至'] = jsons.get('C11', '')
            jbxx_data[u'经营范围'] = jsons.get('C9', '')
            jbxx_data[u'登记机关'] = jsons.get('C12', '')
            jbxx_data[u'核准日期'] = jsons.get('C13', '')
            jbxx_data[u'登记状态'] = jsons.get('C14', '')
        elif company_type == "cb":
            jbxx_data[u'注册号'] = jsons.get('C1', '')
            jbxx_data[u'名称'] = jsons.get('C2', '')
            jbxx_data[u'类型'] = jsons.get('C3', '')
            jbxx_data[u'负责人'] = jsons.get('C4', '')
            jbxx_data[u'营业场所'] = jsons.get('C5', '')
            jbxx_data[u'营业期限自'] = jsons.get('C7', '')
            jbxx_data[u'营业期限至'] = jsons.get('C8', '')
            jbxx_data[u'经营范围'] = jsons.get('C6', '')
            jbxx_data[u'登记机关'] = jsons.get('C9', '')
            jbxx_data[u'核准日期'] = jsons.get('C11', '')
            jbxx_data[u'成立日期'] = jsons.get('C10', '')
            jbxx_data[u'登记状态'] = jsons.get('C12', '')
        elif company_type == 'fiei':
            jbxx_data[u'注册号'] = jsons.get('C1', '')
            jbxx_data[u'名称'] = jsons.get('C2', '')
            jbxx_data[u'类型'] = jsons.get('C3', '')
            jbxx_data[u'法定代表人'] = jsons.get('C5', '')
            jbxx_data[u'注册资本'] = jsons.get('C6', '')
            jbxx_data[u'成立日期'] = jsons.get('C4', '')
            jbxx_data[u'住所'] = jsons.get('C7', '')
            jbxx_data[u'营业期限自'] = jsons.get('C9', '')
            jbxx_data[u'营业期限至'] = jsons.get('C10', '')
            jbxx_data[u'经营范围'] = jsons.get('C8', '')
            jbxx_data[u'登记机关'] = jsons.get('C11', '')
            jbxx_data[u'核准日期'] = jsons.get('C12', '')
            jbxx_data[u'登记状态'] = jsons.get('C13', '')
        elif company_type == 'fieib':
            jbxx_data[u'注册号'] = jsons.get('C1', '')
            jbxx_data[u'名称'] = jsons.get('C2', '')
            jbxx_data[u'类型'] = jsons.get('C3', '')
            jbxx_data[u'负责人'] = jsons.get('C4', '')
            jbxx_data[u'营业场所'] = jsons.get('C5', '')
            jbxx_data[u'营业期限自'] = jsons.get('C7', '')
            jbxx_data[u'营业期限至'] = jsons.get('C8', '')
            jbxx_data[u'经营范围'] = jsons.get('C6', '')
            jbxx_data[u'登记机关'] = jsons.get('C9', '')
            jbxx_data[u'核准日期'] = jsons.get('C11', '')
            jbxx_data[u'成立日期'] = jsons.get('C10', '')
            jbxx_data[u'登记状态'] = jsons.get('C12', '')
        elif company_type == 'gtgsh':
            jbxx_data[u'注册号'] = jsons.get('C1', '')
            jbxx_data[u'名称'] = jsons.get('C2', '')
            jbxx_data[u'类型'] = jsons.get('C3', '')
            jbxx_data[u'经营者'] = jsons.get('C5', '')
            jbxx_data[u'经营场所'] = jsons.get('C7', '')
            jbxx_data[u'组成形式'] = jsons.get('C6', '')
            jbxx_data[u'注册日期'] = jsons.get('C4', '')
            jbxx_data[u'经营范围'] = jsons.get('C8', '')
            jbxx_data[u'登记机关'] = jsons.get('C9', '')
            jbxx_data[u'核准日期'] = jsons.get('C10', '')
            jbxx_data[u'经营状态'] = jsons.get('C11', '')
        elif company_type == "pb":
            jbxx_data[u'注册号'] = jsons.get('C1', '')
            jbxx_data[u'名称'] = jsons.get('C2', '')
            jbxx_data[u'类型'] = jsons.get('C3', '')
            jbxx_data[u'执行事务合伙人'] = jsons.get('C4', '')
            jbxx_data[u'主要经营场所'] = jsons.get('C5', '')
            jbxx_data[u'合伙期限自'] = jsons.get('C7', '')
            jbxx_data[u'合伙期限至'] = jsons.get('C8', '')
            jbxx_data[u'经营范围'] = jsons.get('C6', '')
            jbxx_data[u'登记机关'] = jsons.get('C9', '')
            jbxx_data[u'核准日期'] = jsons.get('C11', '')
            jbxx_data[u'成立日期'] = jsons.get('C10', '')
            jbxx_data[u'登记状态'] = jsons.get('C12', '')
        elif company_type == "pspc":
            jbxx_data[u'注册号'] = jsons.get('C1', '')
            jbxx_data[u'名称'] = jsons.get('C2', '')
            jbxx_data[u'类型'] = jsons.get('C3', '')
            jbxx_data[u'投资人'] = jsons.get('C4', '')
            jbxx_data[u'住所'] = jsons.get('C5', '')
            jbxx_data[u'经营范围'] = jsons.get('C6', '')
            jbxx_data[u'登记机关'] = jsons.get('C7', '')
            jbxx_data[u'核准日期'] = jsons.get('C9', '')
            jbxx_data[u'成立日期'] = jsons.get('C8', '')
            jbxx_data[u'登记状态'] = jsons.get('C10', '')
        elif company_type == "pfc":
            jbxx_data[u'注册号'] = jsons.get('C1', '')
            jbxx_data[u'名称'] = jsons.get('C2', '')
            jbxx_data[u'类型'] = jsons.get('C3', '')
            jbxx_data[u'法定代表人'] = jsons.get('C5', '')
            jbxx_data[u'住所'] = jsons.get('C7', '')
            jbxx_data[u'成员出资总额'] = jsons.get('C6', '')
            jbxx_data[u'成立日期'] = jsons.get('C4', '')
            jbxx_data[u'业务范围'] = jsons.get('C8', '')
            jbxx_data[u'登记机关'] = jsons.get('C9', '')
            jbxx_data[u'核准日期'] = jsons.get('C10', '')
            jbxx_data[u'登记状态'] = jsons.get('C11', '')
        return jbxx_data

    def getType(self,url):
        types = re.sub('http.+?json\?','',url)
        _type = filter(lambda x:re.match(x,types),['ci','cb','fieib','fiei','gtgsh','nccci','pb','pspc','pfc'])
        if _type:
            return _type[0]
        return False

    def parseBaxx(self,baxx_jsons):
        baxx_result = []
        for baxx_json in baxx_jsons:
            url = baxx_json.get('url')
            body = baxx_json.get('_body')
            if not url and body:
                warnings.warn(u'baxx没有url和body')
                return baxx_result
            _type = self.getType(url)
            if not _type:
                return baxx_result
            body = json.loads(body)['items']
            for ba_dict in body:
                baxx_result.extend(self.parseBaxxdict(ba_dict,_type))
        return baxx_result

    def parseBaxxdict(self,ba_dict,company_type):
        _list = []
        if company_type == 'gtgsh':
            ba_dic = {}
            ba_dic[u'序号'] = ba_dict.get('VALUES1RN', '')
            ba_dic[u'姓名'] = ba_dict.get('VALUES1', '')
            _list.append(ba_dic)
            if 'VALUES2RN' in ba_dict.keys():
                ba_dic[u'序号'] = ba_dict.get('VALUES2RN', '')
                ba_dic[u'姓名'] = ba_dict.get('VALUES2', '')
                _list.append(ba_dic)

        elif company_type == 'nccci':
            ba_dic = {}
            ba_dic[u'序号'] = ba_dict.get('RN', '')
            ba_dic[u'出资人类型'] = ba_dict.get('C1', '')
            ba_dic[u'出资人'] = ba_dict.get('C2', '')
            ba_dic[u'证照/证件类型'] = ba_dict.get('C3', '')
            ba_dic[u'证照/证件号码'] = ba_dict.get('C4', '')
            _list.append(ba_dic)

        elif company_type == 'ci' or company_type == 'fiei':
            ba_dic = {}
            ba_dic[u'序号'] = ba_dict.get('VALUES1RN', '')
            ba_dic[u'姓名'] = ba_dict.get('PERSON_NAME1', '')
            ba_dic[u'职务'] = ba_dict.get('POSITION_NAME1', '')
            _list.append(ba_dic)
            if 'VALUES2RN' in ba_dict.keys():
                ba_dic = {}
                ba_dic[u'序号'] = ba_dict.get('VALUES2RN', '')
                ba_dic[u'姓名'] = ba_dict.get('PERSON_NAME2', '')
                ba_dic[u'职务'] = ba_dict.get('POSITION_NAME2', '')
                _list.append(ba_dic)
        return _list

if __name__ == "__main__":
    handler = JiangsuHandler("Jiangsu")
