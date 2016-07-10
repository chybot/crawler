# -*- coding: utf-8 -*-
# Created by fml on 2016/6/3.

import sys
import os
import json
import copy
import time
from lxml import etree
from ParserNbBase import ParserNbBase

reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


class ChongqingNbHandler(ParserNbBase):
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
            {'base.tel': u'企业基本信息.企业联系电话', 'base.postalcode': u'企业基本信息.邮政编码',
             'base.addr': u'企业基本信息.企业通信地址', 'base.email': u'企业基本信息.电子邮箱',
              'base.istransfer': u'企业基本信息.有限责任公司本年度是否发生股东股权转让',
             'base.opstate': u'企业基本信息.企业存续状态',
             'base.haswebsite': u'企业基本信息.是否有网站或网店', 'base.hasbrothers': u'企业基本信息.企业是否有投资信息或购买其他公司股权', 'base.empnum': u'企业基本信息.从业人数',
             'base.hasexternalsecurity':u'企业基本信息.是否对外担保',
            })
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
        web_json = map(lambda x:html_dict[x],filter(lambda x:x.endswith('json'),html_dict.keys()))
        web_json = map(lambda x: json.loads(x) if not isinstance(x,(list,dict)) else x,web_json)
        web_json = map(lambda x:x.get('_body'),web_json[0])
        web_json = map(lambda x: json.loads(x) if not isinstance(x, (list, dict)) else x, web_json)
        json_zch,json_nbinfo = {},{}
        for dd in web_json:
            if 'gtjnz' in dd and 'nzfz' in dd:
                json_zch = dd
            else:json_nbinfo = dd
        qynb = company_copied[u'qynb']
        self.parse_jbxxvalues(qynb)
        jbxx = qynb.get(u'企业基本信息',{})
        jbxx.update(self.jbxx_parse(json_zch,json_nbinfo))
        jbxx.update(self.parseOtherjbxx(json_nbinfo))
        qynb[u'企业基本信息'] = jbxx
        qynb[u'网站或网店信息'] = self.parse_webSites(json_nbinfo)
        qynb[u'股东及出资信息'] = self.pasre_mNGsentinv(json_nbinfo)
        qynb[u'对外投资信息'] = self.parse_ngstzentinfos(json_nbinfo)
        qynb.update(self.parse_means(json_nbinfo))
        qynb.update(self.parsePermits(json_nbinfo))
        qynb[u'对外提供保证担保信息'] = self.parse_dbinfo(json_nbinfo)
        qynb[u'股权变更信息'] = self.parse_stocks(json_nbinfo)
        qynb[u'修改记录'] = self.parse_modifies(json_nbinfo)
        company_copied['qynb'] = qynb
        if reslt_dict and isinstance(reslt_dict, dict):
            reslt_dict.update(company_copied)
        result_json = json.dumps(reslt_dict, ensure_ascii=False)
        self.log.info(u"ChongqingNbHandler解析结果：\n" + result_json)
        return reslt_dict
    def parsePermits(self,json_nbinfo):
        '''
        添加行政许可情况
        :param json_nbinfo:
        :return:
        '''
        permits={}
        permits_list =[]
        if 'permits' in json_nbinfo:
            for item in json_nbinfo.get('permits', []):
                keys = [u'名称', u'有效期止']
                displaylicname = item.get('displaylicname', '')
                valto = item.get('valto', '')
                valto = self.time_change(valto)
                values = [displaylicname, valto]
                permits_list.append(dict(zip(keys, values)))
        if permits_list:
            permits={u"行政许可情况":permits_list}
        return permits

    def parseOtherjbxx(self,json_nbinfo):
        '''
        解析基本信息其他信息
        :param json_nbinfo:
        :return:
        '''
        _dict = dict()
        base = json_nbinfo.get('base',{})
        if 'name' in base:
            _dict[u'经营者姓名'] = base['name']
        if 'fundam' in base:
            _dict[u'资金数额'] = base['fundam'] +u'万元'
        if 'empnum' in base:
            empnum = base['empnum']
            if empnum != u'企业选择不公示':
                _dict[u'从业人数'] = base['empnum'] + u'人'
        return _dict

    def parse_modifies(self,json_nbinfo):
        modifies = []
        if 'modifies' in json_nbinfo:
            index = 1
            for item in json_nbinfo.get('modifies',[]):
                keys = [u'序号',u'修改事项',u'修改前',u'修改后',u'修改日期']
                modiitem = item.get('modiitem','')
                modibe = item.get('modibe','')
                modiaf = item.get('modiaf','')
                modidate = item.get('modidate','')
                values = [index,modiitem,modibe,modiaf,modidate]
                modifies.append(dict(zip(keys,values)))
                index += 1
        return modifies

    def parse_stocks(self,json_nbinfo):
        stocks = []
        if 'stocks' in json_nbinfo:
            for item in json_nbinfo['stocks']:
                keys = [u'股东',u'变更前股权比例',u'变更后股权比例',u'股权变更日期']
                stockholder = item.get('stockrightbeforebl','')
                stockrightbeforebl = item.get('stockrightbeforebl') + '%' if 'stockrightbeforebl' in item else ''
                stockrightafterbl = item.get('stockrightafterbl') + '%' if 'stockrightafterbl' in item else ''
                stockrightchangedate = self.time_change(item.get('stockrightchangedate',''))
                values = [stockholder,stockrightbeforebl,stockrightafterbl,stockrightchangedate]
                stocks.append(dict(zip(keys,values)))

        return stocks
    def parse_dbinfo(self,json_nbinfo):
        dbinfo = []
        if 'dbinfo' in json_nbinfo:
            for db in json_nbinfo['dbinfo']:
                if db.get('ispublish') != 1:
                    continue
                keys = [u'债权人',u'债务人',u'主债权种类',u'主债权数额',u'履行债务的期限',u'保证的期间',u'保证的方式',u'保证担保的范围']
                more = db.get('more','')
                mortgagor = db.get('mortgagor','')
                priclaseckind = u'合同' if db.get('priclaseckind') == 1 else u'其他'
                priclasecam = db.get('priclasecam','') + u'万元'
                pefperform = self.time_change(db.get('pefperform',''))
                pefperto = self.time_change(db.get('pefperto',''))
                pefpertime = pefperform + '-' + pefperto
                guaranperiod = u'期限' if db.get('guaranperiod') == 1 else u'未约定'
                gatype = u'一般保证' if db.get('gatype') == 1 else u'连带保证' if db.get('gatype') == 2 else u'未约定'
                rage = db.get('rage','')
                values = [more,mortgagor,priclaseckind,priclasecam,pefpertime,guaranperiod,gatype,rage]
                dbinfo.append(dict(zip(keys,values)))
        return dbinfo
    def parse_means(self,json_nbinfo):
        means = {}
        means_dict ={}
        if 'means' in json_nbinfo:
            dict_= json_nbinfo['means']
            if len(dict_)>10:
                means[u'资产总额'] = dict_.get('assgro','') + u'万元' if dict_.get('assgroispublish') == '1' and dict_.get('assgro','') != '' else u'企业选择不公示'
                means[u'所有者权益合计'] = dict_.get('totequ','') + u'万元' if dict_.get('totequispublish') == '1'  and dict_.get('totequ','')!= '' else u'企业选择不公示'
                means[u'营业总收入'] = dict_.get('vendinc','') + u'万元' if dict_.get('vendincispublish') == '1' and dict_.get('vendinc','')!= '' else u'企业选择不公示'
                means[u'利润总额'] = dict_.get('progro','') + u'万元' if dict_.get('progroispublish') == '1' and dict_.get('progro','')!= '' else u'企业选择不公示'
                means[u'营业总收入中主营业务收入'] = dict_.get('maibusinc','') + u'万元' if dict_.get('maibusincispublish') == '1' and dict_.get('maibusinc','')!= '' else u'企业选择不公示'
                means[u'净利润'] = dict_.get('netinc','') + u'万元' if dict_.get('netincispublish') == '1' and dict_.get('netinc','')!= '' else u'企业选择不公示'
                means[u'纳税总额'] = dict_.get('ratgro','') + u'万元' if dict_.get('ratgroispublish') == '1' and dict_.get('ratgro','')!= '' else u'企业选择不公示'
                means[u'负债总额'] = dict_.get('liagro','') + u'万元' if dict_.get('liagroispublish') == '1' and dict_.get('liagro','')!= '' else u'企业选择不公示'
                means_dict={u'企业资产状况信息':means}
            else:
                means[u'营业额或营业收入'] = dict_.get('assgro','') + u'万元' if dict_.get('assgroispublish') == '1' and dict_.get('assgro','') != '' else u'企业选择不公示'
                means[u'纳税总额'] = dict_.get('vendinc','') + u'万元' if dict_.get('vendincispublish') == '1' and dict_.get('vendinc','') != '' else u'企业选择不公示'
                means_dict={u'生产经营情况信息':means}
        return means_dict
    def parse_ngstzentinfos(self,json_nbinfo):
        ngstzentinfos = []

        if 'ngstzentinfos' in json_nbinfo:
            for item in json_nbinfo['ngstzentinfos']:
                ngstzentinfos.append(dict(zip([u'投资设立企业或购买股权企业名称', u'统一社会信用代码/注册号'],
                                    [item.get('entname', ''), item.get('tzregno', '')])))
        return ngstzentinfos
    def pasre_mNGsentinv(self,json_nbinfo):
        mNGsentinv = []
        if u'mNGsentinv' in json_nbinfo:
            for item in json_nbinfo['mNGsentinv']:
                keys = [u'股东',u'认缴出资额（万人民币）',u'认缴出资时间',u'认缴出资方式',u'实缴出资额（万人民币）',u'出资时间',u'出资方式']
                inv = item.get('inv','')
                subconam = item.get('mNGsentinvsubcon',{}).get('subconam','')
                condate = item.get('mNGsentinvsubcon', {}).get('condate', '')
                condate = self.time_change(condate)
                conform = item.get('mNGsentinvsubcon', {}).get('conform', '')
                acconam = item.get('mNGsentinvaccon', {}).get('acconam', '')
                accondate = item.get('mNGsentinvaccon', {}).get('accondate', '')
                accondate = self.time_change(accondate)
                acconform = item.get('mNGsentinvaccon', {}).get('acconform', '')
                values = [inv,subconam,condate,conform,acconam,accondate,acconform]
                mNGsentinv.append(dict(zip(keys,values)))
        return mNGsentinv
    def parse_webSites(self,json_nbinfo):
        website = []
        if 'webSites' in json_nbinfo:
            for item in json_nbinfo['webSites']:
                website.append(dict(zip([u'类型',u'名称',u'网址'],[item.get('webtypename',''),item.get('websitname',''),item.get('domain','')])))
        return website
    def parse_jbxxvalues(self,qynb):
        jbxx = qynb.get(u'企业基本信息',{})
        jbxx[u'有限责任公司本年度是否发生股东股权转让']  = u'是' if jbxx.get(u'有限责任公司本年度是否发生股东股权转让') == 1 else u'否'
        jbxx[u'企业存续状态'] = u'开业' if jbxx.get(u'企业存续状态') == 1 else u'歇业' if jbxx.get(u'企业存续状态') == 2 else u'清算'
        jbxx[u'是否有网站或网店'] = u'是' if jbxx.get(u'是否有网站或网店') == 1 else u'否'
        jbxx[u'企业是否有投资信息或购买其他公司股权'] = u'有' if jbxx.get(u'企业是否有投资信息或购买其他公司股权') == 1 else u'否'
        jbxx[u'是否对外担保'] = u'是' if jbxx.get(u'是否对外担保') == 1 else u'否'
        jbxx[u'从业人数'] = u'企业选择不公示' if u'从业人数' not in jbxx else jbxx.get(u'从业人数','')

    def jbxx_parse(self,json_zch,json_nbinfo):
        base = json_zch.get('base')
        base2 = json_nbinfo.get('base', {})
        if not base:return {}
        jbxx= {}
        creditcode = base.get('creditcode')
        if not creditcode:
            creditcode = base.get('regno','')
        jbxx[u'统一社会信用代码/注册号'] =creditcode
        traname = base2.get('traname')
        if traname:
            jbxx[u'名称'] = traname
        else:
            entname = base.get('entname','')
            if entname:
                jbxx[u'企业名称'] = entname
            else:
                jbxx[u'名称'] = base.get('name','')
        return jbxx

    def time_change(self,str_time):
        try:
            if not str_time:
                return ''
            timeArray = time.strptime(str_time, u"%Y-%m-%d")
            otherStyleTime = time.strftime(u"%Y年%m月%d日", timeArray)
            return otherStyleTime
        except:
            return str_time


