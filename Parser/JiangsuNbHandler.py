# -*- coding: utf-8 -*-

import sys
import os
import json
import copy
import chardet
from lxml import etree
from ParserNbBase import ParserNbBase
import html4test as test

reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


class JiangsuNbHandler(ParserNbBase):
    """
    ShanghaiNbHandler is used to parse the annual report
    @version:1.0
    @author:david ding
    @modify:
    """

    def __init__(self, pinyin):
        """
        Initiate the parameters.
        """
        ParserNbBase.__init__(self, pinyin)
        # 企业基本信息
        self.appendJsonMapperConfig(
            {'REG_NO': u'企业基本信息.注册号/统一社会信用代码', 'CORP_NAME': u'企业基本信息.企业名称', 'TEL': u'企业基本信息.企业联系电话', 'ZIP': u'企业基本信息.邮政编码',
             'ADDR': u'企业基本信息.企业通信地址', 'E_MAIL': u'企业基本信息.企业电子邮箱', 'IF_EQUITY': u'企业基本信息.有限责任公司本年度是否发生股东股权转让',
             'PRODUCE_STATUS': u'企业基本信息.企业经营状态',
             'IF_WEBSITE': u'企业基本信息.是否有网站或网店', 'IF_INVEST': u'企业基本信息.企业是否有投资信息或购买其他公司股权', 'PRAC_PERSON_NUM': u'企业基本信息.从业人数',
             'primary_key':u'REG_NO,CORP_NAME'})
        # 股东（发起人）及出资信息
        self.appendJsonMapperConfig(
            {'STOCK_NAME': u'出资信息.股东/发起人', 'SHOULD_CAPI': u'出资信息.认缴出资额(万元)', 'SHOULD_CAPI_DATE': u'出资信息.认缴出资时间', 'SHOULD_CAPI_TYPE_NAME': u'出资信息.认缴出资方式',
             'REAL_CAPI': u'出资信息.实缴出资额(万元)', 'REAL_CAPI_DATE': u'出资信息.实缴出资时间', 'REAL_CAPI_TYPE_NAME': u'出资信息.实缴出资方式',
             'primary_key': u'STOCK_NAME,SHOULD_CAPI'})
        # 企业资产状况信息
        # self.appendJsonMapperConfig(
        #     {'NET_AMOUNT': u'企业资产状况信息.资产总额', 'TOTAL_EQUITY': u'企业资产状况信息.所有者权益合计', 'SALE_INCOME': u'企业资产状况信息.营业总收入', 'PROFIT_TOTAL': u'企业资产状况信息.利润总额',
        #      'SERV_FARE_INCOME': u'企业资产状况信息.营业总收入中主营业务收入', 'PROFIT_RETA': u'企业资产状况信息.净利润', 'TAX_TOTAL': u'企业资产状况信息.纳税总额',
        #      'DEBT_AMOUNT': u'企业资产状况信息.负债总额',
        #      'primary_key':u'NET_AMOUNT,TOTAL_EQUITY'})
        # # 生产经营情况
        # self.appendJsonMapperConfig(
        #     {'yysr': u'生产经营情况.主营业务收入', 'nsze': u'生产经营情况.纳税总额', 'jlr': u'生产经营情况.净利润',
        #      'primary_key': u'yysr'})
        # 对外投资信息
        self.appendJsonMapperConfig(
            {'INVEST_NAME': u'对外投资信息.投资设立企业或购买股权企业名称', 'INVEST_REG_NO': u'对外投资信息.注册号/统一社会信用代码',
             'primary_key':u'INVEST_NAME,INVEST_REG_NO'})
        # 网站或网店信息
        self.appendJsonMapperConfig(
            {'WEB_TYPE': u'网站或网店信息.类型', 'WEB_NAME': u'网站或网店信息.名称', 'WEB_URL': u'网站或网店信息.网址'})
        # 股权变更信息
        self.appendJsonMapperConfig(
            {'STOCK_NAME': u'股权变更信息.股东/发起人', 'CHANGE_BEFORE': u'股权变更信息.变更前股权比例', 'CHANGE_AFTER': u'股权变更信息.变更后股权比例', 'CHANGE_DATE': u'股权变更信息.股权变更日期',
             'primary_key':u'STOCK_NAME,CHANGE_BEFORE'})
        # 对外提供保证担保信息
        self.appendJsonMapperConfig(
            {'CRED_NAME': u'对外提供保证担保信息.债权人', 'DEBT_NAME': u'对外提供保证担保信息.债务人', 'CRED_TYPE': u'对外提供保证担保信息.主债权种类',
             'CRED_AMOUNT': u'对外提供保证担保信息.主债权数额', 'GUAR_DATE': u'对外提供保证担保信息.履行债务的期限', 'GUAR_PERIOD': u'对外提供保证担保信息.保证的期间',
             'GUAR_TYPE': u'对外提供保证担保信息.保证的方式',
             'primary_key':u'CRED_NAME,DEBT_NAME'})
        # 修改记录
        self.appendJsonMapperConfig(
            {'NO_': u'修改记录.序号', 'CHANGE_ITEM_NAME': u'修改记录.修改事项', 'OLD_CONTENT': u'修改记录.修改前', 'NEW_CONTENT': u'修改记录.修改后', 'CHANGE_DATE': u'修改记录.修改日期'})
        self.log.info(u"JiangsuNbHandler构造完成")

    def parse(self, html_dict, reslt_dict=None):
        if not html_dict or not isinstance(html_dict, dict):
            return None
        if 'company_name' in html_dict:
            self.log.info(u"开始解析 %s" % html_dict['company_name'])
        self.log.info(u"开始解析通用信息")
        company = self.parseCommon(html_dict)
        self.log.info(u"通用信息解析完成")
        company_copied = copy.deepcopy(company)
        qyzcinfo = self.parse_qyzcinfo(html_dict)
        company_copied['qynb'][u'企业资产状况信息'] = qyzcinfo
        if reslt_dict and isinstance(reslt_dict, dict):
            reslt_dict.update(company_copied)
        result_json = json.dumps(reslt_dict, ensure_ascii=False)
        self.log.info(u"JiangsuNbHandler解析结果：\n" + result_json)
        return reslt_dict

    def parse_qyzcinfo(self,html_dict):
        json_keys = filter(lambda x:x.endswith('json'),html_dict)
        if not json_keys:return {}
        jsons =html_dict[json_keys[0]]
        qyzc = filter(lambda x:'REG_NO' in x.get('_body') and 'NET_AMOUNT' in x.get('_body'),jsons)
        if not qyzc:return {}
        qyzc = qyzc[0].get('_body')
        if not qyzc:return {}
        qyzc = json.loads(qyzc)
        if not qyzc:return {}
        qyzc = qyzc[0]
        keys = [u'资产总额',u'所有者权益合计',u'营业总收入',u'利润总额',u'营业总收入中主营业务收入',u'净利润',u'纳税总额',u'负债总额']
        NET_AMOUNT = qyzc.get('NET_AMOUNT','')
        TOTAL_EQUITY = qyzc.get('TOTAL_EQUITY', '')
        SALE_INCOME = qyzc.get('SALE_INCOME', '')
        PROFIT_TOTAL = qyzc.get('PROFIT_TOTAL', '')
        SERV_FARE_INCOME = qyzc.get('SERV_FARE_INCOME', '')
        PROFIT_RETA = qyzc.get('PROFIT_RETA', '')
        TAX_TOTAL = qyzc.get('TAX_TOTAL', '')
        DEBT_AMOUNT = qyzc.get('DEBT_AMOUNT', '')
        values = [NET_AMOUNT,TOTAL_EQUITY,SALE_INCOME,PROFIT_TOTAL,SERV_FARE_INCOME,PROFIT_RETA,TAX_TOTAL,DEBT_AMOUNT]
        return dict(zip(keys,values))
if __name__ == "__main__":
    pass
