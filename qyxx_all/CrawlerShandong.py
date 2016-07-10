# -*- coding: utf-8 -*-
#Created by David on 2016/5/4.

import sys
import time
import random
from lxml import etree
import re
import hashlib
import PyV8
from HttpRequst.DownLoader import DownLoader
from CrawlerBase import CrawlerBase
from ModuleManager import Module,Event,Iterator,Sleep,ModuleInput,InputType, OutputParameterShowUpType
from util.crawler_util import CrawlerRunMode, OutputType, EventType
from CommonLib.WebContent import WebAccessType, SeedAccessType
from CommonLib.md5util import getMd5WithString
from CommonLib import dataretrieve
reload(sys)

#TODO 变更信息更多 公司(中国石化销售有限公司山东青岛即墨第六零八加油站)
class CrawlerShandong(CrawlerBase):
    def __init__(self, pinyin, callbackFromOuterControl):
        config_dict = dict()
        config_dict[CrawlerRunMode.COMPANY_KEY] = [self.initHomePage, self.initYzmPic, self.get_search_list, self.initConfigCompanyInfo]#, self.initYzmPic, self.check_company, self.get_search_list,self.initConfigCompanyInfo]
        check_dict = dict()
        check_dict['html_check_dict'] = {'操作过于频繁': WebAccessType.TOO_OFTEN, '非正常访问': WebAccessType.ACCESS_VIOLATION, '页面超时或拒绝访问':WebAccessType.NOT_EXPECTED_STRUCTURE}
        self.setNonCompanyConfig({u'暂未查询到相关记录'})
        CrawlerBase.__init__(self, pinyin, config_dict, check_dict, callbackFromOuterControl)
        # 关闭股东信息的解析
        self.parse_gdxx_on = False
        pass


    def initHomePage(self):
        module = Module(self.visitHomePage, u"访问首页")
        module.module_id = "home_page"
        module.appendUrl('http://218.57.139.24')
        module.appendHeaders(lambda ua: {
            "Host": '218.57.139.24',
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.8",
            "Accept-Encoding": "gzip, deflate, sdch",
            "Connection": "keep-alive",
            'User-Agent': ua})
        module.addSleep(Sleep(2))
        module.appendOutput("csrf", '//form[@id="searchform"]/input[@name="_csrf"]/@value', OutputType.LIST)
        module.addEvent(Event(EventType.OUTPUT_NOT_SATISFIED, retry_times=100))
        module.addEvent(Event(EventType.EXCEPTION_OCCURED, retry_times=5))
        self.module_manager.appendSubModule(module, True)


    def initYzmPic(self):
        module = Module(self.visitValidateCode, u'获取验证码图片')
        module.appendUrl('http://218.57.139.24/securitycode')
        module.appendHeaders(lambda ua:{
            "Host": "218.57.139.24",
            "User-Agent": ua,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
            "Accept-Encoding": "gzip, deflate",
            "Connection": "keep-alive"
        })
        module.addSleep(Sleep(2))
        module.addEvent(Event(EventType.EXCEPTION_OCCURED, retry_times=5, redo_module='home_page'))
        self.module_manager.appendSubModule(module, True)

    def get_search_list(self):
        module = Module(self.visitSearchList, u"搜索列表")
        module.appendUrl('http://218.57.139.24/pub/indsearch')
        module.appendHeaders(lambda ua : {
            "Host": "218.57.139.24",
            "User-Agent": ua,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
            "Accept-Encoding": "gzip, deflate",
            "Connection": "keep-alive",
            'Referer':'http://218.57.139.24/'
        })
        module.appendWebMethod("post")
        def assertCsrf(csrf):
            return True if isinstance(csrf, list) and len(csrf) > 0 else False
        module.addEvent(Event(EventType.ASSERT_FAILED, retry_times=100, assert_function=assertCsrf, redo_module="home_page"))
        def assertVaildCode(yzm, html=None):
            if not html:
                return False
            # print 'type(html)  ', type(html)
            # if u'计算错误' in html:
            #     print u'cout <<　计算错误'
            # elif u'验证码超时，请重新计算' in html:
            #     print u'cout << 验证码超时，请重新计算'
            # else:
            #     print 'yzm True, ', yzm
            return False if u'计算错误' in html or u'验证码超时，请重新计算' in html else True

        def md5(str):
            m = hashlib.md5()
            m.update(str)
            return m.hexdigest()
        module.appendPostData(lambda company_key, yzm, csrf: {'kw': company_key, '_csrf': csrf[0], 'secode':md5(str(yzm))})
        module.addEvent(Event(EventType.ASSERT_FAILED, retry_times=100, assert_function=assertVaildCode, redo_module="home_page"))
        def assertProxyStatus(html):
            if  u"每天最多可搜索" in html:
                #print u'切换代理'
                download = DownLoader('shandong')
                download.changeProxy()
                return False
            return True
        module.addEvent(Event(EventType.ASSERT_FAILED, retry_times=20, assert_function=assertProxyStatus, redo_module="home_page"))
        module.addEvent(Event(EventType.ASSERT_FAILED, retry_times=5, assert_function=lambda: False if self.report.access_type == SeedAccessType.NON_COMPANY else True))
        module.appendOutput("search_list_xpath", '//ul/li[@class="font16"]/a', OutputType.LIST)
        def getSearchList(search_list_xpath=None):
            ret_args = []
            if not search_list_xpath:
                return []
            for xpath_a in search_list_xpath:
                com_name = xpath_a.xpath('./text()')
                com_href = xpath_a.xpath('./@href')
               # print com_name,     com_href
                if com_name and com_href:
                    args = com_href[0].split('/')
                    if len(args) == 3:   #URL的参数个数变？
                        com_num = args[1].strip()
                        encrpripid = args[2].strip()
                        if com_num and encrpripid:
                            ret_args.append((com_name[0].strip(), com_href[0].strip(), encrpripid, com_num))
            return ret_args
        module.appendOutput(name="search_list", type=OutputType.FUNCTION, function=getSearchList, show_up=OutputParameterShowUpType.OPTIONAL)
        module.addEvent(Event(EventType.OUTPUT_NOT_SATISFIED, retry_times=100))
        module.addSleep(Sleep(2))
        module.addEvent(Event(EventType.EXCEPTION_OCCURED, retry_times=100, redo_module='home_page'))
        self.module_manager.appendSubModule(module, True)

    def initConfigCompanyInfo(self):
        iterator = Iterator("search_list", "com")
        module = Module(None, u"获取公司信息", iterator)
        self.module_manager.appendSubModule(module, True)
        self.initCompanyInfo(module)
        self.initBaxxInfo(module)
        self.initFzhgInfo(module)
        self.initXzcfxxInfo(module)
        self.initGdxqInfoPrepare(module)
        self.initAnnualReportPre(module)
        self.initAnnualReport(module)
        self.initResultCollect(module)


    def  initCompanyInfo(self, module_super):
        module = Module(self.visitJbxx, u"基本信息")
        module.appendUrl(lambda com : "http://218.57.139.24/pub/"+com[1])
        # def pri_com(com, company_zch):
        #     print 'COMMMMMMoC  ', com[0],  com[1], company_zch
        module.appendHeaders(lambda ua: {
            "Host": "218.57.139.24",
            "User-Agent": ua,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
            "Accept-Encoding": "gzip, deflate",
            "Connection": "keep-alive",
            'Referer':'http://218.57.139.24/'})
        module.appendOutput("company_zch_list", '//table[1]/tr[2]/td[1]/text()', OutputType.LIST)
        def setCompanyZch(company_zch_list=None):
            self.value_dict['company_zch'] = company_zch_list[0].strip() if company_zch_list else None
        module.appendOutput(type=OutputType.FUNCTION, function=setCompanyZch)
        module.addEvent(Event(EventType.OUTPUT_NOT_SATISFIED, retry_times=5, redo_module='home_page'))
        def getGdxxParms(html):
            return  re.findall(r'\,"recid":"(.+?)",', html, re.S) if html else []
        module.appendOutput(name="recid_list", type=OutputType.FUNCTION, function=getGdxxParms, show_up=OutputParameterShowUpType.OPTIONAL) #提取股东详情的list
        #module.appendOutput(type=OutputType.FUNCTION, function=pri_com)
        module.addSleep(Sleep(2))
        module.addEvent(Event(EventType.EXCEPTION_OCCURED, retry_times=5, redo_module='home_page'))
        module_super.appendSubModule(module, True)

    #枣庄环球印染有限责任公司  (测试股东详情和翻页公司)
    #TODO 没有详情，也会下载详情页面
    #TODO 有些有详情链接， 点进去没有详情数据
    def initGdxqInfoPrepare(self, module_super):
        iterator = Iterator("recid_list", "rid")
        module = Module(None, u"进入股东详情", iterator)
        module_super.appendSubModule(module, True)
        sub_module = Module(self.visitGdxq, u"获取股东详情")
        # def pri_c(rid, com):
        #     print 'xxxxxx===>>>', rid
        # sub_module.appendOutput(type=OutputType.FUNCTION, function=pri_c)
        sub_module.appendUrl(lambda rid, com: 'http://218.57.139.24/pub/gsnzczxxdetail/%s/%s'%(com[2], rid.strip()))
        sub_module.appendHeaders(lambda ua, com: {
            "Host": "218.57.139.24",
            "User-Agent": ua,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
            "Accept-Encoding": "gzip, deflate",
            "Connection": "keep-alive",
            'Referer':'http://218.57.139.24/pub/'+com[1],})
        module.addSleep(Sleep(2))
        module.addEvent(Event(EventType.EXCEPTION_OCCURED, retry_times=5, redo_module='home_page'))
        module.appendSubModule(sub_module, True)

    #TODO COOKIE失效会返回html， code403
    def initBaxxInfo(self, module_super):
        module = Module(self.visitBaxxJson, u"获取备案信息")
        module.appendUrl(lambda com:'http://218.57.139.24/pub/gsryxx/'+com[3])
        module.appendHeaders(lambda ua, com, csrf:{
            "Host": "218.57.139.24",
            "User-Agent": ua,
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
            "Accept-Encoding": "gzip, deflate",
            "Connection": "keep-alive",
            'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
            'Referer':'http://218.57.139.24/pub/'+com[1],
            'X-CSRF-TOKEN':csrf[0],
            'X-Requested-With':'XMLHttpRequest'})
        module.appendWebMethod("post")
        module.addSleep(Sleep(2))
        module.appendPostData(lambda com: {'encrpripid': com[2]})
        module.addEvent(Event(EventType.EXCEPTION_OCCURED, retry_times=5, redo_module='home_page'))
        module_super.appendSubModule(module, True)

    def initFzhgInfo(self, module_super):
        module = Module(self.visitFzjgJson, u"获取分支机构信息")
        module.appendUrl(lambda com:'http://218.57.139.24/pub/gsfzjg/'+ com[3])
        module.appendHeaders(lambda com, csrf, ua:{
            "Host": "218.57.139.24",
            "User-Agent": ua,
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
            "Accept-Encoding": "gzip, deflate",
            "Connection": "keep-alive",
            'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
            'Referer':'http://218.57.139.24/pub/'+com[1],
            'X-CSRF-TOKEN':csrf[0],
            'X-Requested-With':'XMLHttpRequest'})
        module.appendWebMethod("post")
        module.addSleep(Sleep(2))
        module.appendPostData(lambda com: {'encrpripid': com[2]})
        module.addEvent(Event(EventType.EXCEPTION_OCCURED, retry_times=5, redo_module='home_page'))
        module_super.appendSubModule(module, True)

    #TODO#行政处罚没数据测试
    def initXzcfxxInfo(self, module_super):
        module = Module(self.visitXzcfJson, u"获取行政处罚信息")
        module.appendUrl("http://218.57.139.24/pub/gsxzcfxx")
        module.appendHeaders(lambda com, csrf, ua:{
            "Host": "218.57.139.24",
            "User-Agent": ua,
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
            "Accept-Encoding": "gzip, deflate",
            "Connection": "keep-alive",
            'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
            'Referer':'http://218.57.139.24/pub/'+com[1],
            'X-CSRF-TOKEN':csrf[0],
            'X-Requested-With':'XMLHttpRequest'})
        module.appendWebMethod("post")
        module.addSleep(Sleep(2))
        module.addEvent(Event(EventType.EXCEPTION_OCCURED, retry_times=5, redo_module='home_page'))
        module.appendPostData(lambda com: {'encrpripid': com[2]})
        module_super.appendSubModule(module, True)


    #遍历企业年报列表
    def initAnnualReportPre(self, module_super):
        module = Module(self.getWebHtml, u"获取年报年份列表")
        module.module_id = "fetch_qynb_list"
        module.appendUrl(lambda com :"http://218.57.139.24/pub/qygsdetail/%s/%s"%(com[3], com[2]))
        module.appendHeaders(lambda ua, com: {
            "User-Agent": ua,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
            "Accept-Encoding": "gzip, deflate",
            "Host": "218.57.139.24",
            "Referer": "http://218.57.139.24/pub/"+com[1],
            "Connection": "keep-alive"})
        module.appendOutput("qynb_search_parms", '//table/tr/td/a', OutputType.LIST, show_up=OutputParameterShowUpType.OPTIONAL)
        def getQynbParms(qynb_search_parms=None):
            #print 'qynb_search_parms   :', qynb_search_parms
            if not qynb_search_parms:
                return []
            rt_list = []
            for tag_a in qynb_search_parms:
                href = tag_a.xpath('./@href')
                nb_name = tag_a.xpath('./text()')
               # print href, '---->' ,  nb_name
                if href and nb_name:
                    nb_year = re.findall(r'.*?(\d{4}).+?', nb_name[0].strip(), re.S)
                 #  print 'nb_year, ', nb_year
                    if nb_year:
                        rt_list.append((nb_year[0].strip(), href[0].strip()))
         #   print 'rt_lsit ', rt_list
            return rt_list
        module.appendOutput(name="qinb_param_list", type=OutputType.FUNCTION, function=getQynbParms, show_up=OutputParameterShowUpType.OPTIONAL)
        module.addSleep(Sleep(2))
        module_super.appendSubModule(module, True)

    def initAnnualReport(self, module_super):
        iterator = Iterator("qinb_param_list", "qynb_tuper")
        module = Module(None, u"遍历年报信息", iterator)
        module_super.appendSubModule(module, True)
        self.initQynbInfo(module)

    #获取年报
    def initQynbInfo(self, module_super):
        module = Module(None, u"设置年份")
        module.appendOutput(type=OutputType.FUNCTION, function=lambda qynb_tuper: {'nb_name':qynb_tuper[0]})
        module_super.appendSubModule(module, True)
        module = Module(self.visitQynb, u"获取企业年报")
        module.appendUrl(lambda qynb_tuper:"http://218.57.139.24%s" % qynb_tuper[1])
        module.appendHeaders(lambda ua, com:{
            "User-Agent": ua,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3",
            "Accept-Encoding": "gzip, deflate",
            "Host": "218.57.139.24",
            "Referer": "http://218.57.139.24/pub/qygsdetail/%s/%s" % (com[3], com[2]),
            "Connection": "keep-alive"})
        module.addEvent(Event(EventType.EXCEPTION_OCCURED, retry_times=5))
        module.addSleep(Sleep(2))
        module_super.appendSubModule(module, True)


    def initResultCollect(self, module_super):
        module = Module(self.resultCollect, u"结果收集")
        module_super.appendSubModule(module)


