# -*- coding: utf-8 -*-
# Created by John on 2016/6/22.

import sys
import random
import re
import time
import PyV8
from CrawlerBase import CrawlerBase
from lxml import etree
from ModuleManager import Module, Event, Iterator, Sleep, ModuleInput, InputType, Bypass
from util.crawler_util import CrawlerRunMode, OutputType, EventType, OutputParameterShowUpType
from CommonLib.WebContent import WebAccessType, SeedAccessType
from CommonLib.md5util import getMd5WithString
from CommonLib import dataretrieve
reload(sys)


class CrawlerNeimenggu(CrawlerBase):
    def __init__(self, pinyin, callbackFromOuterControl):
        config_dict = dict()
        config_dict[CrawlerRunMode.COMPANY_KEY] = [self.initConfigValidateCode, self.checkValidateCode, self.getCmpnySereachList, self.fetchCompanyInfo]
        config_dict[CrawlerRunMode.COMPANY_URL] = [self.getCompanyInfo, self.fetchCmpnyGdxq, self.getAnnalsList, self.getAnnalsInfo, self.initResultCollect]

        check_dict = dict()
        check_dict['html_check_dict'] = {'过于频繁': WebAccessType.TOO_OFTEN, '非正常访问': WebAccessType.ACCESS_VIOLATION}
        CrawlerBase.__init__(self, pinyin, config_dict, check_dict, callbackFromOuterControl)

        self.non_company_set = {"查询条件中含有非法字符", "不能以该关键字作为条件", "暂未查询到相关记录"}
        # 关闭股东信息的解析、打开基本信息解析
        self.parse_gdxx_on = False
        self.parse_jbxx_on = True
        pass

    def initConfigValidateCode(self):
        module = Module(self.visitValidateCode, u"获取验证码")
        module.module_id = "init_validate_code"

        module.appendUrl("http://www.nmgs.gov.cn:7001/aiccips/verify.html?random=" + str(random.random()))
        module.appendHeaders({
            'Host' : 'www.nmgs.gov.cn:7001',
            'Connection' : 'keep-alive',
            'Accept' : 'image/webp,*/*;q=0.8',
            'Referer' : 'http://www.nmgs.gov.cn:7001/aiccips/',
            'Accept-Encoding' : 'gzip, deflate, sdch',
            'Accept-Language' : 'en-US,en;q=0.8,zh-CN;q=0.6,zh-TW;q=0.4'
            })
        module.addSleep(Sleep(3))
        module.appendEncoding("utf-8")

        def checkValidatecode(yzm):
            if not yzm:
                return False
            return True

        module.addEvent(Event(EventType.ASSERT_FAILED, retry_times=100, assert_function=checkValidatecode))

        self.module_manager.appendSubModule(module, True)

    def checkValidateCode(self):
        module = Module(self.getJson, u"检验验证码")
        module.module_id = "check_validate_code"

        module.appendUrl("http://www.nmgs.gov.cn:7001/aiccips/CheckEntContext/checkCode.html")
        module.appendHeaders({
            'Host' : 'www.nmgs.gov.cn:7001',
            'Connection' : 'keep-alive',
            'Accept' : 'application/json, text/javascript, */*; q=0.01',
            'Origin' : 'http://www.nmgs.gov.cn:7001',
            'X-Requested-With' : 'XMLHttpRequest',
            'Content-Type' : 'application/x-www-form-urlencoded; charset=UTF-8',
            'Referer' : 'http://www.nmgs.gov.cn:7001/aiccips/',
            'Accept-Encoding' : 'gzip, deflate',
            'Accept-Language' : 'en-US,en;q=0.8,zh-CN;q=0.6,zh-TW;q=0.4'
            })
        module.appendWebMethod("post")
        module.addSleep(Sleep(3))
        module.appendEncoding("utf-8")
        module.appendPostData(lambda yzm, company_key: {"code": yzm, "textfield": company_key})

        def checkValidatecode(web = None):
            if not web:
                return False
            else:
                pattern = re.compile(r'\"([\s\S]*?)\"')
                flags = pattern.findall(str(web.body))
                if (len(flags) != 4 or flags[2] != 'textfield') or (flags[0] == 'flag' and flags[1] != str(1)):
                    self.holder.logging.warning(u"验证码校验失败!")
                    return False
                else:
                    self.value_dict["textfield"] = flags[3].decode('raw_unicode_escape')
            return True

        module.addEvent(Event(EventType.ASSERT_FAILED, retry_times=100, assert_function=checkValidatecode, redo_module="init_validate_code"))

        self.module_manager.appendSubModule(module, True)

    def getCmpnySereachList(self):
        module = Module(self.visitSearchList, u"抓取公司列表")
        module.module_id = "get_search_list"

        module.appendUrl("http://www.nmgs.gov.cn:7001/aiccips/CheckEntContext/showInfo.html")
        module.appendHeaders({
            'Host' : 'www.nmgs.gov.cn:7001',
            'Connection' : 'keep-alive',
            'Cache-Control' : 'max-age=0',
            'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Origin' : 'http://www.nmgs.gov.cn:7001',
            'Content-Type' : 'application/x-www-form-urlencoded',
            'Referer' : 'http://www.nmgs.gov.cn:7001/aiccips/',
            'Accept-Encoding' : 'gzip, deflate',
            'Accept-Language' : 'en-US,en;q=0.8,zh-CN;q=0.6,zh-TW;q=0.4'
        })
        module.appendWebMethod("post")
        module.appendEncoding("utf-8")
        module.appendPostData(lambda yzm, textfield: {"code": yzm, "textfield": textfield.replace(r"\n", "")})
        module.addSleep(Sleep(3))

        module.appendOutput("url_list", ".//*[@class='list']/ul/li/a/@href", OutputType.LIST)
        module.appendOutput("name_list", ".//*[@class='list']/ul/li/a/text()", OutputType.LIST)
        module.appendOutput(name="search_list", type=OutputType.FUNCTION, function=lambda url_list, name_list: zip(url_list, name_list))

        module.addEvent(Event(EventType.ASSERT_FAILED, retry_times=0, assert_function=lambda: False if self.report.access_type == SeedAccessType.NON_COMPANY else True))
        module.addEvent(Event(EventType.EXCEPTION_OCCURED, retry_times=100, redo_module="init_validate_code"))
        module.addEvent(Event(EventType.OUTPUT_NOT_SATISFIED, retry_times=100, redo_module="init_validate_code"))

        self.module_manager.appendSubModule(module)

    def fetchCompanyInfo(self):
        iterator = Iterator("search_list", "com")
        module = Module(None, u"处理公司列表", iterator)
        # 保存验证码图片
        module.appendExtraFunction(self.yzmSave)
        self.module_manager.appendSubModule(module, True)

        self.prepareCompnanyParms(module)
        self.getCompanyInfo(module)
        self.fetchCmpnyGdxq(module)
        self.getCompanyRecordInfo(module)
        self.getCompanyPunishInfo(module)
        # self.getAnnalsList(module)
        # self.getAnnalsInfo(module)
        self.initResultCollect(module)

    def prepareCompnanyParms(self, module_super):
        module = Module(None, u"抓取公司前的预处理")

        def prepareParams(com):
            query_dict = {}
            if com and len(com) >= 2:
                query_dict["company_url"] = com[0]
                query_dict["search_company"] = com[1]
            return query_dict

        module.appendOutput(type=OutputType.FUNCTION, function=prepareParams)
        module_super.appendSubModule(module, True)

    def getCompanyInfo(self, module_super):
        module = Module(self.visitJbxx, u"抓取公司信息")
        module.module_id = "get_cmpny_info"

        def getURL(company_url):
            if "http" in company_url:
                return company_url
            else:
                return u"http://www.nmgs.gov.cn:7001/aiccips" + company_url.replace('..', '')
        module.appendUrl(getURL)

        module.appendHeaders({
            'Host' : 'www.nmgs.gov.cn:7001',
            'Connection' : 'keep-alive',
            'Cache-Control' : 'max-age=0',
            'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Origin' : 'http://www.nmgs.gov.cn:7001',
            'Content-Type' : 'application/x-www-form-urlencoded',
            'Accept-Encoding' : 'gzip, deflate',
            'Accept-Language' : 'en-US,en;q=0.8,zh-CN;q=0.6,zh-TW;q=0.4'
        })
        module.appendEncoding("utf-8")
        module.addSleep(Sleep(3))

        module.appendOutput(name="gdxq_list", xpath=".//*[@id='invInfo']/table/tr/td/a/@onclick", type=OutputType.LIST,
                            show_up=OutputParameterShowUpType.OPTIONAL)
        module.appendOutput(name="params_list", xpath='.//input[@type=\'hidden\']/@value', type=OutputType.LIST,
                            show_up=OutputParameterShowUpType.OPTIONAL)

        module.addEvent(Event(EventType.EXCEPTION_OCCURED, retry_times=100))
        module.addEvent(Event(EventType.OUTPUT_NOT_SATISFIED, retry_times=100))

        module_super.appendSubModule(module, True)

        def checkParmsList(params_list = None):
            if params_list:
                return False
            return True

        module.appendBypass(Bypass(condition_fuc=checkParmsList, module_id="get_record_info", range_global=True))
        module.appendBypass(Bypass(condition_fuc=checkParmsList, module_id="get_punish_info", range_global=True))

    def fetchCmpnyGdxq(self, module_super):
        iterator = Iterator(seeds="gdxq_list", param_name="gdxq")
        module = Module(iterator=iterator, name=u"遍历股东详情")
        module_super.appendSubModule(module)

        sub_module = Module(self.visitGdxq, u"抓取股东详情")

        # TODO: 添加try exception
        def getURL(gdxq):
            if gdxq:
                gdxq_text = re.findall(r"(?<=\(').+?(?='\))", gdxq)
                if gdxq_text:
                    return gdxq_text[0]
            return None

        sub_module.appendUrl(getURL)
        sub_module.appendHeaders({
            'Host' : 'www.nmgs.gov.cn:7001',
            'Connection' : 'keep-alive',
            'Cache-Control' : 'max-age=0',
            'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Origin' : 'http://www.nmgs.gov.cn:7001',
            'Content-Type' : 'application/x-www-form-urlencoded',
            'Accept-Encoding' : 'gzip, deflate',
            'Accept-Language' : 'en-US,en;q=0.8,zh-CN;q=0.6,zh-TW;q=0.4'
        })
        sub_module.appendEncoding("utf-8")
        sub_module.addSleep(Sleep(3))

        sub_module.addEvent(Event(EventType.EXCEPTION_OCCURED, retry_times=100))

        module.appendSubModule(sub_module)

    def getCompanyRecordInfo(self, module_super):
        module = Module(self.visitBaxx, u"抓取备案信息")
        module.module_id = "get_record_info"

        module.appendUrl("http://www.nmgs.gov.cn:7001/aiccips/GSpublicity/GSpublicityList.html?service=entCheckInfo")
        module.appendHeaders({
            'Host' : 'www.nmgs.gov.cn:7001',
            'Connection' : 'keep-alive',
            'Cache-Control' : 'max-age=0',
            'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Origin' : 'http://www.nmgs.gov.cn:7001',
            'Content-Type' : 'application/x-www-form-urlencoded',
            'Referer' : "http://www.nmgs.gov.cn:7001/aiccips/GSpublicity/GSpublicityList.html?service=entInfo",
            'Accept-Encoding' : 'gzip, deflate',
            'Accept-Language' : 'en-US,en;q=0.8,zh-CN;q=0.6,zh-TW;q=0.4'
        })
        module.appendEncoding("utf-8")
        module.addSleep(Sleep(3))
        module.appendWebMethod("post")
        module.appendPostData(lambda params_list: {"entNo": str(params_list[1]), "entType": str(params_list[2]), "regOrg": str(params_list[3])})

        module.addEvent(Event(EventType.EXCEPTION_OCCURED, retry_times=100))

        module_super.appendSubModule(module, True)

    def getCompanyPunishInfo(self, module_super):
        module = Module(self.visitXzcf, u"抓取行政处罚信息")
        module.module_id = "get_punish_info"

        module.appendUrl("http://www.nmgs.gov.cn:7001/aiccips/GSpublicity/GSpublicityList.html?service=cipPenaltyInfo")
        module.appendHeaders({
            'Host' : 'www.nmgs.gov.cn:7001',
            'Connection' : 'keep-alive',
            'Cache-Control' : 'max-age=0',
            'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Origin' : 'http://www.nmgs.gov.cn:7001',
            'Content-Type' : 'application/x-www-form-urlencoded',
            'Referer' : 'http://www.nmgs.gov.cn:7001/aiccips/GSpublicity/GSpublicityList.html?service=entInfo',
            'Accept-Encoding' : 'gzip, deflate',
            'Accept-Language' : 'en-US,en;q=0.8,zh-CN;q=0.6,zh-TW;q=0.4'
        })
        module.appendEncoding("utf-8")
        module.addSleep(Sleep(3))
        module.appendPostData(lambda params_list: {"entNo": str(params_list[1]), "entType": str(params_list[2]), "regOrg": str(params_list[3])})

        module.addEvent(Event(EventType.EXCEPTION_OCCURED, retry_times=100))

        module_super.appendSubModule(module, True)

    def getAnnalsList(self, module_super):
        module = Module(self.getWebHtml, u"抓取年报列表")
        module.module_id = "get_annals_list"

        def prepareParams(company_url):
            query_dict = {}
            if company_url:
                query_dict["url_id"] = company_url.split("=")[1]
            return query_dict
        module.appendInput(InputType.FUNCTION, prepareParams)

        def getURL(url_id = None):
            if url_id:
                return u'http://gsxt.hljaic.gov.cn/enterprisePublicity.jspx?id=' + url_id
            return None
        module.appendUrl(getURL)

        module.appendHeaders({
            "Host" : "gsxt.hljaic.gov.cn",
            "User-Agent" : "Mozilla/5.0 (Windows NT 6.1; rv:37.0) Gecko/20100101 Firefox/37.0",
            "Accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language" : "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
            "Accept-Encoding" : "gzip, deflate",
            "Referer" : "http://gsxt.hljaic.gov.cn/searchList.jspx"
        })
        module.appendEncoding("utf-8")
        module.addSleep(Sleep(3))

        def getAnnalsList(html = None):
            qynb_list = []

            try:
                tree=etree.HTML(html)
                _list = tree.xpath(".//*[@id='qiyenianbao']/table/tr/td/a")

                for ll in _list:
                    url = ''.join(ll.xpath('@href')).strip()
                    name = ''.join(ll.xpath('text()')).replace(u'年度报告', '')
                    if name !=  u'详情':
                        qynb_list.append([url ,name])
            except:
                qynb_list = []
            return qynb_list

        module.appendOutput(name='annals_list', type=OutputType.FUNCTION, function=getAnnalsList, show_up=OutputParameterShowUpType.OPTIONAL)
        module.addEvent(Event(EventType.EXCEPTION_OCCURED, retry_times=100, redo_module="get_annals_list"))

        module_super.appendSubModule(module, True)

    def getAnnalsInfo(self, module_super):
        iterator = Iterator("annals_list","annals")
        module = Module(None, u"遍历年报列表", iterator)
        module_super.appendSubModule(module, True)

        sub_module = Module(self.visitQynb, u"抓取年报详情")
        sub_module.module_id = "get_annals_info"

        def prepareParams(annals):
            mv_dict = dict()
            if annals and len(annals) >= 2:
                mv_dict['nb_url'] = annals[0]
                mv_dict['nb_name'] = annals[1]
            return mv_dict
        sub_module.appendInput(InputType.FUNCTION, input_value=prepareParams)

        def getURL(nb_url = None):
            if nb_url:
                return u'http://gsxt.hljaic.gov.cn' + nb_url
            return None
        sub_module.appendUrl(getURL)

        sub_module.appendHeaders({
            "Host" : "gsxt.hljaic.gov.cn",
            "User-Agent" : "Mozilla/5.0 (Windows NT 6.1; rv:37.0) Gecko/20100101 Firefox/37.0",
            "Accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language" : "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
            "Accept-Encoding" : "gzip, deflate",
            "Referer" : "http://gsxt.hljaic.gov.cn/searchList.jspx"
        })
        sub_module.appendEncoding("utf-8")
        sub_module.addSleep(Sleep(3))

        sub_module.addEvent(Event(EventType.EXCEPTION_OCCURED, retry_times=100, redo_module="get_annals_info"))

        module.appendSubModule(sub_module)

    def initResultCollect(self, module_super):
        module = Module(self.resultCollect, u"结果收集")
        module_super.appendSubModule(module)
