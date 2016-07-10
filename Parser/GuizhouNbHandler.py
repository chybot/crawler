# -*- coding: utf-8 -*-
# Created by David on 2016/6/3.

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


class GuizhouNbHandler(ParserNbBase):
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
            {'zch': u'企业基本信息.注册号或统一社会信用代码', 'qymc': u'企业基本信息.企业名称', 'lxdh': u'企业基本信息.企业联系电话', 'yzbm': u'企业基本信息.邮政编码',
             'dz': u'企业基本信息.企业通信地址', 'dzyx': u'企业基本信息.企业电子邮箱', 'sfzr': u'企业基本信息.有限责任公司本年度是否发生股东股权转让',
             'jyzt': u'企业基本信息.企业经营状态',
             'sfww': u'企业基本信息.是否有网站或网店', 'sfdw': u'企业基本信息.是否有投资信息或购买其他公司股权', 'cyrs': u'企业基本信息.从业人数',
             'primary_key': u'zch, qymc'})

        # 基本信息-企业类型:个体(内地)
        self.appendJsonMapperConfig(
            {'sjmc': u'基本信息.名称', 'sjjyz': u'基本信息.经营者姓名', 'sjzch': u'基本信息.营业执照注册号', 'lxdh': u'基本信息.联系电话', 'zjse': u'基本信息.资金数额',
             'cyrs': u'基本信息.从业人数',
             'primary_key': u'sjzch'})

        # 股东及出资信息
        self.appendJsonMapperConfig(
            {'tzr': u'出资信息.股东', 'rjcze': u'出资信息.认缴出资额', 'rjczrq': u'出资信息.认缴出资时间', 'rjczfs': u'出资信息.认缴出资方式',
             'sjcze': u'出资信息.实缴出资额', 'sjczrq': u'出资信息.出资时间', 'sjczfs': u'出资信息.出资方式',
             'primary_key': u'tzr, rjcze, rjczrq'})
        # 企业资产状况信息
        self.appendJsonMapperConfig(
            {'nsze': u'资产状况信息.纳税总额', 'xse': u'资产状况信息.销售额或营业收入',
             'primary_key': u'nsze, xse'})
        # 企业资产状况信息
        self.appendJsonMapperConfig(
            {'zcze': u'企业资产状况信息.资产总额', 'qyhj': u'企业资产状况信息.所有者权益合计', 'xsze': u'企业资产状况信息.销售总额', 'lrze': u'企业资产状况信息.利润总额',
             'zysr': u'企业资产状况信息.销售总额中主营业务收入', 'jlr': u'企业资产状况信息.净利润', 'nsze': u'企业资产状况信息.纳税总额',
             'fzze': u'企业资产状况信息.负债总额',
             'primary_key': u'zcze, fzze'})
        # 生产经营情况
        self.appendJsonMapperConfig(
            {'yysr': u'生产经营情况.主营业务收入', 'nsze': u'生产经营情况.纳税总额', 'jlr': u'生产经营情况.净利润',
             'primary_key': u'yysr'})
        # 对外投资信息
        self.appendJsonMapperConfig(
            {'mc': u'对外投资信息.投资设立企业或购买股权企业名称', 'zch': u'对外投资信息.注册号或统一社会信用代码',
             'primary_key': u'mc, zch'})
        # 网站或网店信息
        self.appendJsonMapperConfig(
            {'lx': u'网站或网店信息.类型', 'mc': u'网站或网店信息.名称', 'wz': u'网站或网店信息.网址',
             'primary_key': u'lx, mc, wz'})
        # 股权变更信息
        self.appendJsonMapperConfig(
            {'gd': u'股权变更信息.股东', 'bgqbl': u'股权变更信息.变更股权比例', 'bghbl': u'股权变更信息.变更后股权比例', 'bgrq': u'股权变更信息.股权变更日期',
             'primary_key': u'gd, bgqbl, bgrq'})
        # 对外提供保证担保信息
        self.appendJsonMapperConfig(
            {'zqr': u'对外提供保证担保信息.债权人', 'zwr': u'对外提供保证担保信息.债务人', 'zzqzl': u'对外提供保证担保信息.主债权种类',
             'zzqse': u'对外提供保证担保信息.主债权数额', 'zwqx': u'对外提供保证担保信息.履行债务的期限', 'bzqj': u'对外提供保证担保信息.保证的期间',
             'bzfs': u'对外提供保证担保信息.保证的方式',
             'primary_key': 'zqr, zwr, zzqzl, zzqse'})
        # 修改记录
        self.appendJsonMapperConfig(
            {'rownum': u'修改记录.序号', 'bgsxmc': u'修改记录.修改事项', 'bgq': u'修改记录.修改前', 'bgh': u'修改记录.修改后', 'bgrq': u'修改记录.修改日期',
             'primary_key': u'rownum, bgsxmc, bgrq'})
        self.log.info(u"GuizhouNbHandler 构造完成")

    def parse(self, html_dict, reslt_dict=None):
        if not html_dict or not isinstance(html_dict, dict):
            return None
        if 'company_name' in html_dict:
            self.log.info(u"开始解析 %s" % html_dict['company_name'])
        self.log.info(u"开始解析通用信息")
        company = self.parseCommon(html_dict)
        self.log.info(u"通用信息解析完成")
        company_copied = copy.deepcopy(company)
        if reslt_dict and isinstance(reslt_dict, dict):
            reslt_dict.update(company_copied)
        result_json = json.dumps(reslt_dict, ensure_ascii=False)
        self.log.info(u"GuizhouNbHandler解析结果：\n" + result_json)
        return reslt_dict


if __name__ == "__main__":
    pass
