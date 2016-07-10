# -*- coding: utf-8 -*-
# Created by David on 2016/5/4.

import sys
import random
import re
import time
import PyV8
from CrawlerBase import CrawlerBase
from lxml import etree
from ModuleManager import Module,Event,Iterator,Sleep,ModuleInput,InputType
from util.crawler_util import CrawlerRunMode, OutputType, EventType, OutputParameterShowUpType
from CommonLib.WebContent import WebAccessType, SeedAccessType
from CommonLib.md5util import getMd5WithString
from CommonLib import dataretrieve
reload(sys)


class CrawlerJilin(CrawlerBase):
    def __init__(self, pinyin, callbackFromOuterControl):
        config_dict = dict()
        config_dict[CrawlerRunMode.COMPANY_KEY] = [self.initCookie, self.initConfigHomePage, self.initConfigValidateCode, self.initConfigSearchList, self.initConfigCompanyInfo]
        config_dict[CrawlerRunMode.COMPANY_URL] = [self.initCookie, self.initConfigHomePage, self.initConfigBaseInfo, self.initConfigShareHolderInfo, self.initConfigChangeInfo,
                                                   self.initArchiveInfo, self.initBranchInfo, self.initPenaltyInfo, self.initAnnalsList,
                                                   self.initAnnalsInfo, self.initResultCollect]

        check_dict = dict()
        check_dict['html_check_dict'] = {'body onload="challenge();"':WebAccessType.ACCESS_VIOLATION}
        CrawlerBase.__init__(self, pinyin, config_dict, check_dict, callbackFromOuterControl)
        # 关闭股东信息的解析、打开基本信息解析
        self.parse_gdxx_on = False
        self.parse_jbxx_on = True
        pass

    def initCookie(self):
        module = Module(self.getWebHtml, u"获取cookie")
        module.module_id = "module_cookie"
        module.appendUrl('http://211.141.74.198:8081/aiccips/')
        module.appendHeaders(lambda ua: {'Connection': 'keep-alive', 'Accept-Language': 'en-US,en;q=0.8,zh-CN;q=0.6,zh-TW;q=0.4', 'Accept-Encoding': 'gzip, deflate, sdch', 'Cache-Control': 'max-age=0', 'Referer': 'http://211.141.74.198:8081/aiccips/', 'Host': '211.141.74.198:8081', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8', 'User-Agent': ua})
        def getCookie(html):
            pattern = re.compile(r'\}\(([\s\S]*?\{\})\)\)', re.S)
            result = pattern.search(html).group(1)
            params = result.split(',')
            if len(params) != 6:
                raise Exception("cookie获取失败！")
            strstr = 'var document = {};var window = {};document[\'cookie\'] = "";window[\'location\'] ={}; \
                window[\'location\'][\'reload\'] = function(){};eval(function (p, a, c, k, e, r) { \
            	e = function(c) { \
            		return c.toString(a) \
            	}; \
            	if (!\'\'.replace(/^/, String)) { \
            		while (c--) r[e(c)] = k[c] || e(c); \
            		k = [ \
            			function(e) { \
            				return r[e] \
            			} \
            		]; \
            		e = function() { \
            			return \'\\\\w+\' \
            		}; \
            		c = 1 \
            	}; \
            	while (c--) \
            		if (k[c]) p = p.replace(new RegExp(\'\\\\b\' + e(c) + \'\\\\b\', \'g\'), k[c]); \
            	return p \
            }(' + params[0] + ',' + params[1] + ',' + params[2] + ',' + params[3] + ',' + params[4] + ',' + params[5] + ')); \
                challenge();var a = document[\'cookie\'];'
            with PyV8.JSContext() as se:
                se.eval(strstr)
                a = se.locals.a
                cookie = a.split('=')[1].split(';')[0]
                cookie_temp1 = dict({'ROBOTCOOKIEID': cookie})
                return cookie_temp1
        module.appendOutput(name="cookie", type=OutputType.FUNCTION, function=getCookie)
        module.appendMiddleValueMonitor("cookie")
        module.addSleep(Sleep(3))
        self.module_manager.appendSubModule(module, True)

    def initConfigHomePage(self):
        module = Module(self.visitHomePage, u"首页")
        module.module_id = "module_home_page"
        module.appendUrl("http://211.141.74.198:8081/aiccips/")
        module.appendHeaders({'Connection': 'keep-alive', 'Accept-Language': 'en-US,en;q=0.8,zh-CN;q=0.6,zh-TW;q=0.4', 'Accept-Encoding': 'gzip, deflate, sdch', 'Cache-Control': 'max-age=0', 'Referer': 'http://211.141.74.198:8081/aiccips/', 'Host': '211.141.74.198:8081', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:36.0) Gecko/20100101 Firefox/36.0'})
        module.appendCookie("cookie")
        module.appendOutput("csrf", ".//input[@name='_csrf']/@value", OutputType.LIST)
        module.appendMiddleValueMonitor("csrf")
        module.addSleep(Sleep(3))
        self.module_manager.appendSubModule(module, True)

    def initConfigValidateCode(self):
        module = Module(self.visitValidateCode, u"验证码")
        module.appendUrl('http://211.141.74.198:8081/aiccips/securitycode?'+str(random.random()))
        module.appendHeaders({'Accept-Language': 'en-US,en;q=0.8,zh-CN;q=0.6,zh-TW;q=0.4', 'Accept-Encoding': 'gzip, deflate, sdch', 'Host': '211.141.74.198:8081', 'Accept': 'image/webp,*/*;q=0.8', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:36.0) Gecko/20100101 Firefox/36.0', 'Connection': 'keep-alive', 'Referer': 'http://211.141.74.198:8081/aiccips/'})
        module.addSleep(Sleep(3))
        def assert_fun(yzm):
            if not yzm:
                return False
            return True
        module.addEvent(Event(EventType.ASSERT_FAILED, assert_function=assert_fun))
        self.module_manager.appendSubModule(module, True)

    def initConfigSearchList(self):
        module = Module(self.visitSearchList, u"搜索列表")
        module.appendUrl('http://211.141.74.198:8081/aiccips/pub/indsearch')
        module.appendHeaders({'Connection': 'keep-alive', 'Accept-Language': 'en-US,en;q=0.8,zh-CN;q=0.6,zh-TW;q=0.4', 'Accept-Encoding': 'gzip, deflate', 'Cache-Control': 'max-age=0', 'Referer': 'http://211.141.74.198:8081/aiccips/', 'Host': '211.141.74.198:8081', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:36.0) Gecko/20100101 Firefox/36.0'})
        module.appendWebMethod("post")
        module.appendPostData(lambda csrf, yzm, company_key:{
                                    'kw': company_key,
                                    '_csrf': csrf[-1], # 参数不为空由首页输出模块保证，且此参数为必选参数，故未做判断直接使用
                                    'secode': getMd5WithString(yzm)
                                })
        module.appendCookie("cookie")
        module.appendOutput("url_list", ".//*[@class='list']/ul/li/a/@href", OutputType.LIST)
        module.appendOutput("name_list", ".//*[@class='list']/ul/li/a/text()", OutputType.LIST)
        module.appendOutput(name="search_list", type=OutputType.FUNCTION, function=lambda url_list, name_list:zip(url_list, name_list))
        module.addEvent(Event(EventType.EXCEPTION_OCCURED, retry_times=100, redo_module="module_cookie"))
        module.addEvent(Event(EventType.OUTPUT_NOT_SATISFIED, retry_times=100, redo_module="module_cookie"))
        module.addEvent(Event(EventType.ASSERT_FAILED, retry_times=0, assert_function=lambda:False if self.report.access_type == SeedAccessType.NON_COMPANY else True))
        module.addSleep(Sleep(3))
        self.module_manager.appendSubModule(module)

    def initConfigCompanyInfo(self):
        iterator = Iterator("search_list", "com")
        module = Module(None, u"获取公司信息", iterator)
        # 保存验证码图片
        module.appendExtraFunction(self.yzmSave)
        self.module_manager.appendSubModule(module, True)

        self.initConfigBaseInfo(module)
        self.initConfigShareHolderInfo(module)
        self.initConfigChangeInfo(module)
        self.initArchiveInfo(module)
        self.initBranchInfo(module)
        self.initPenaltyInfo(module)
        self.initAnnalsList(module)
        self.initAnnalsInfo(module)
        self.initResultCollect(module)

    def initConfigBaseInfo(self, module_super):
        module = Module(self.visitJbxx, u"基本信息")
        def prepare(com):
            query_ = {}
            if com and len(com) >= 2:
                query_["company_url"] = com[0]
                query_["search_company"] = com[1]
            return query_

        module.appendInput(InputType.FUNCTION, prepare)
        def getUrl(company_url):
            if "http" in company_url:
                return company_url
            else:
                return u'http://211.141.74.198:8081/aiccips/pub/' + company_url
        module.appendUrl(getUrl)
        module.appendHeaders({'Accept-Language': 'en-US,en;q=0.8,zh-CN;q=0.6,zh-TW;q=0.4', 'Accept-Encoding': 'gzip, deflate, sdch', 'Host': '211.141.74.198:8081', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8', 'Connection': 'keep-alive', 'Cache-Control': 'max-age=0'})
        module.appendOutput(name="script", xpath=".//script/text()", type=OutputType.LIST)
        def parse(script):
            if not script or not isinstance(script, list):
                return None
            url_params_conf = {'regex': ['encrpripid = \'(.*)\'', 'enttype=\'(.*)\''] }
            params = dataretrieve.regex_parse(url_params_conf, self.holder.logging, script[0])
            gdxx_text = dataretrieve.regex_parse({'regex': "czxxliststr ='(.*)'"}, self.holder.logging, script[1])
            if gdxx_text:
                gdxx_text = gdxx_text.replace("\"inv\":null", "\"inv\":\"null\"").replace("\"blicno\":null","\"blicno\":\"null\"").replace(
                    "\"blictype\":null", "\"blictype\":\"null\"").replace("\"invtype\":null", "\"invtype\":\"null\"")
            return {"params":params, "gdxx_text":gdxx_text}
        module.appendOutput(type=OutputType.FUNCTION, function=parse)
        # 页面有表格及表头但无实际内容的情况
        def noContentAssert():
            if 'company' in self.result_dict:
                rows = self.result_dict['company']
                for row in rows:
                    for k,v in row.items():
                        if v and v.strip():
                            return True
                if rows:
                    time.sleep(3600)    # 休眠一小时
                    return False
            return True
        module.addEvent(Event(EventType.ASSERT_FAILED, retry_times=0, assert_function=noContentAssert))
        module_super.appendSubModule(module, True)

    def initConfigShareHolderInfo(self, module_super):
        module = Module(self.visitGdxxJson, u"股东信息")
        # 为模块动态添加输入
        def prepare(gdxx_text, csrf, params):
            if gdxx_text:
                module.appendWebContent("gdxx_text")
                return
            module.appendUrl("http://211.141.74.198:8081/aiccips/pub/gsczxx")
            module.appendHeaders({'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                        'Accept-Encoding' : 'gzip, deflate, sdch',
                        'Accept-Language' : 'en-US,en;q=0.8,zh-CN;q=0.6,zh-TW;q=0.4',
                        'Cache-Control' : 'max-age=0',
                        'Connection' : 'keep-alive',
                        'Host' : '211.141.74.198:8081',
                        'X-CSRF-TOKEN' : csrf[-1]})
            module.appendWebMethod("post")
            module.appendPostData({'encrpripid':params[0]})
            module.appendCookie("cookie")
        module.appendInput(InputType.FUNCTION, prepare)
        module.addMapper(
            {'blicno': u'股东信息.证照或证件号码', 'inv': u'股东信息.股东', 'blictype': u'股东信息.证照或证件类型', 'invtype': u'股东信息.股东类型',
             'primary_key': 'inv,blicno'})
        def parse4bgxx(script):
            if not script or not isinstance(script, list) or len(script) < 2:
                return None
            bgxx_text = dataretrieve.regex_parse({'regex': 'bgsxliststr =\'(.*)\''}, self.holder.logging, script[1])
            if not bgxx_text:
                bgxx_text = dataretrieve.regex_parse({'regex': 'bgsxliststr =\'(.*)\''}, self.holder.logging, script[2])
            return {"bgxx_text": bgxx_text}
        module.appendOutput(type=OutputType.FUNCTION, function=parse4bgxx)
        module_super.appendSubModule(module, True)

    def initConfigChangeInfo(self, module_super):
        module = Module(self.visitBgxxJson, u"变更信息")
        module.appendWebContent("bgxx_text")
        module.addMapper({'altaf': u'变更后内容', 'altbe': u'变更前内容', 'altitem': u'变更事项', 'altdate.time': u'变更日期'})
        module_super.appendSubModule(module, True)

    def initArchiveInfo(self, module_super):
        module = Module(self.visitBaxxJson, u"获取备案信息")
        module.appendUrl(lambda params: 'http://211.141.74.198:8081/aiccips/pub/gsryxx/' + params[1])
        module.appendHeaders(lambda csrf: {'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                                    'Accept-Encoding' : 'gzip, deflate, sdch',
                                    'Accept-Language' : 'en-US,en;q=0.8,zh-CN;q=0.6,zh-TW;q=0.4',
                                    'Cache-Control' : 'max-age=0',
                                    'Connection' : 'keep-alive',
                                    'Host' : '211.141.74.198:8081',
                                    'X-CSRF-TOKEN' : csrf[-1]})
        module.appendWebMethod("post")
        module.appendPostData(lambda params: {'encrpripid':params[0]})
        module.addMapper({'name': u'姓名', 'position':u'职务'})
        module_super.appendSubModule(module)

    def initBranchInfo(self, module_super):
        module = Module(self.visitFzjgJson, u"获取分支机构信息")
        module.appendUrl(lambda params: 'http://211.141.74.198:8081/aiccips/pub/gsfzjg/' + params[1])
        module.appendHeaders(lambda csrf: {'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                                    'Accept-Encoding' : 'gzip, deflate, sdch',
                                    'Accept-Language' : 'en-US,en;q=0.8,zh-CN;q=0.6,zh-TW;q=0.4',
                                    'Cache-Control' : 'max-age=0',
                                    'Connection' : 'keep-alive',
                                    'Host' : '211.141.74.198:8081',
                                    'X-CSRF-TOKEN' : csrf[-1]})
        module.appendWebMethod("post")
        module.appendPostData(lambda params: {'encrpripid':params[0]})
        module_super.appendSubModule(module)

    def initPenaltyInfo(self, module_super):
        module = Module(self.visitXzcf, u"获取行政处罚信息")
        module.appendUrl(lambda params: 'http://211.141.74.198:8081/aiccips/pub/gsxzcfxx')
        module.appendHeaders(lambda csrf: {'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                                    'Accept-Encoding' : 'gzip, deflate, sdch',
                                    'Accept-Language' : 'en-US,en;q=0.8,zh-CN;q=0.6,zh-TW;q=0.4',
                                    'Cache-Control' : 'max-age=0',
                                    'Connection' : 'keep-alive',
                                    'Host' : '211.141.74.198:8081',
                                    'X-CSRF-TOKEN' : csrf[-1]})
        module.appendWebMethod("post")
        module.appendPostData(lambda params: {'encrpripid':params[0]})
        module_super.appendSubModule(module)

    def initAnnalsList(self, module_super):
        module = Module(self.visitQynbList, u"获取年报列表")
        module.module_id = "get_annals_list"
        module.appendUrl(lambda params: 'http://211.141.74.198:8081/aiccips/pub/qygsdetail/' + params[1] + '/' + params[0])
        module.appendHeaders({
            'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding' : 'gzip, deflate, sdch',
            'Accept-Language' : 'en-US,en;q=0.8,zh-CN;q=0.6,zh-TW;q=0.4',
            'Cache-Control' : 'max-age=0',
            'Connection' : 'keep-alive',
            'Host' : '211.141.74.198:8081'})
        module.appendWebMethod("get")
        module.appendCookie("cookie")
        module.addSleep(Sleep(3))

        module.appendOutput("annals_urls", ".//*[@id='qiyenianbao']/table/tr/td[2]/a/@href", OutputType.LIST, show_up=OutputParameterShowUpType.OPTIONAL)
        module.appendOutput("annals_names", ".//*[@id='qiyenianbao']/table/tr/td[2]/a/text()", OutputType.LIST, show_up=OutputParameterShowUpType.OPTIONAL)
        module.appendOutput(name="annals_list", type=OutputType.FUNCTION, function=lambda annals_urls, annals_names: zip(annals_urls, annals_names),
                            show_up=OutputParameterShowUpType.OPTIONAL)

        module.addEvent(Event(EventType.EXCEPTION_OCCURED, retry_times=100, redo_module="get_annals_list"))
        module_super.appendSubModule(module)

    def initAnnalsInfo(self, module_super):
        iterator = Iterator("annals_list", "annal")
        module = Module(None, u"获取年报信息", iterator)
        module.module_id = "get_annals_info"

        module_super.appendSubModule(module, True)

        self.initAnnalsDetails(module)

    def initAnnalsDetails(self, module_super):
        module = Module(self.visitQynb, u"获取年报详情")
        module.module_id = "get_annals_detail"

        def prepare(annal):
            query_dict = {}
            if annal and len(annal) >= 2:
                query_dict["annals_url"] = str(annal[0])
                name = str(annal[1].strip('\r\n\t'))
                query_dict["nb_name"] = filter(str.isdigit, name)
            return query_dict
        module.appendInput(InputType.FUNCTION, prepare)

        def getUrl(annals_url):
            if "http" in annals_url:
                return annals_url
            else:
                return u'http://211.141.74.198:8081/' + annals_url
        module.appendUrl(getUrl)

        module.appendHeaders({
            'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding' : 'gzip, deflate, sdch',
            'Accept-Language' : 'en-US,en;q=0.8,zh-CN;q=0.6,zh-TW;q=0.4',
            'Cache-Control' : 'max-age=0',
            'Connection' : 'keep-alive',
            'Host' : '211.141.74.198:8081'})
        module.appendWebMethod("get")
        module.appendCookie("cookie")
        module.addSleep(Sleep(3))

        module.addEvent(Event(EventType.EXCEPTION_OCCURED, retry_times=100, redo_module="get_annals_list"))

        module_super.appendSubModule(module)

    def initResultCollect(self, module_super):
        module = Module(self.resultCollect, u"结果收集")
        module_super.appendSubModule(module)
