# -*- coding: utf-8 -*-
# Created by David on 2016/5/4.

import sys
import random
import time
import re
import urllib

reload(sys)
sys.path.append('./util')
from CrawlerBase import CrawlerBase
from lxml import etree
from ModuleManager import Module, Event, Iterator, Router
from util.crawler_util import CrawlerRunMode, InputType, OutputType, EventType, OutputParameterShowUpType
from CommonLib.WebContent import WebAccessType, SeedAccessType
from guangdongs.CrawlerGdQyxx import CrawlerGdQyxx
from guangdongs.CrawlerGdQyxy import CrawlerGdQyxy
from guangdongs.CrawlerSzxy import CrawlerSzxy


class CrawlerGuangdong(CrawlerBase):
    def __init__(self, pinyin, callbackFromOuterControl):
        config_dict = dict()
        config_dict[CrawlerRunMode.COMPANY_KEY] = [self.initConfigValidateCode, self.initPostParam,
                                                   self.initConfigSearchList, self.initConfigCompanyInfo]
        config_dict[CrawlerRunMode.COMPANY_URL] = [self.initRouter]
        check_dict = dict()
        check_dict['html_check_dict'] = {'过于频繁':WebAccessType.TOO_OFTEN, '非正常访问':WebAccessType.ACCESS_VIOLATION }
        CrawlerBase.__init__(self, pinyin, config_dict, check_dict, callbackFromOuterControl)
        # 打开解析开关
        self.parse_on = True
        pass

    def initConfigValidateCode(self):
        module = Module(self.visitValidateCode, "验证码")
        module.module_id = "module_validate_code"
        module.appendUrl("http://gsxt.gdgs.gov.cn/aiccips/verify.html?random=" + str(random.random()))
        module.appendHeaders(
            {'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3', 'Accept-Encoding': 'gzip, deflate',
             'Connection': 'keep-alive', 'Accept': 'image/png,image/*;q=0.8,*/*;q=0.5',
             'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:37.0) Gecko/20100101 Firefox/37.0',
             'Host': 'gsxt.gdgs.gov.cn', 'Referer': 'http://gsxt.gdgs.gov.cn/aiccips/'})
        module.addEvent(Event(EventType.EXCEPTION_OCCURED, retry_times=100))
        self.module_manager.appendSubModule(module)

    def initPostParam(self):
        module = Module(self.getJson, "json中间结果")
        module.appendUrl('http://gsxt.gdgs.gov.cn/aiccips/CheckEntContext/checkCode.html')
        module.appendHeaders(
            {'Accept-Language': 'zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3', 'Accept-Encoding': 'gzip, deflate',
             'Connection': 'keep-alive', 'X-Requested-With': 'XMLHttpRequest',
             'Accept': 'application/json, text/javascript, */*; q=0.01',
             'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:37.0) Gecko/20100101 Firefox/37.0',
             'Host': 'gsxt.gdgs.gov.cn', 'Referer': 'http://gsxt.gdgs.gov.cn/aiccips/', 'Pragma': 'no-cache',
             'Cache-Control': 'no-cache', 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'})
        module.appendWebMethod("post")
        module.appendPostData(lambda company_key, yzm: {"textfield": company_key, "code": yzm})

        def postSearchListData(json, yzm):
            if 'textfield' not in json:
                return None
            textfield = json['textfield']
            data = {
                "textfield": textfield,
                "code": yzm
            }
            return data

        module.appendOutput(name="post_data", type=OutputType.FUNCTION, function=postSearchListData)
        module.addEvent(Event(EventType.OUTPUT_NOT_SATISFIED, redo_module="module_validate_code"))
        module.addEvent(Event(EventType.EXCEPTION_OCCURED, redo_module="module_validate_code"))

        def postDataJsonAssert(json=None):
            if not json:
                return False
            if 'flag' not in json or json['flag'] != '1':
                return False
            return True

        module.addEvent(
            Event(EventType.ASSERT_FAILED, retry_times=1000, assert_function=postDataJsonAssert, redo_module="module_validate_code"))
        self.module_manager.appendSubModule(module)

    def initConfigSearchList(self):
        module = Module(self.visitSearchList, "搜索列表")
        module.appendUrl('http://gsxt.gdgs.gov.cn/aiccips/CheckEntContext/showInfo.html')
        module.appendHeaders({'Host': 'gsxt.gdgs.gov.cn', 'Accept-Language': 'zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3',
                              'Accept-Encoding': 'gzip, deflate', 'Referer': 'http://gsxt.gdgs.gov.cn/aiccips/',
                              'Content-Type': 'application/x-www-form-urlencoded', 'Connection': 'keep-alive',
                              'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                              'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:37.0) Gecko/20100101 Firefox/37.0'})
        module.appendWebMethod("post")
        module.appendPostData("post_data")
        module.appendOutput("search_list", ".//*[@class='list']", OutputType.LIST)
        module.addEvent(Event(EventType.EXCEPTION_OCCURED, retry_times=100, redo_module="module_validate_code"))
        module.addEvent(Event(EventType.OUTPUT_NOT_SATISFIED, retry_times=100, redo_module="module_validate_code"))
        module.addEvent(Event(EventType.ASSERT_FAILED, retry_times=0, assert_function=lambda:False if self.report.access_type == SeedAccessType.NON_COMPANY else True))
        self.module_manager.appendSubModule(module)

    def initConfigCompanyInfo(self):
        iterator = Iterator("search_list", "info")
        module = Module(None, "获取公司信息", iterator)
        self.module_manager.appendSubModule(module, True)

        self.initCompanyPrepare(module)
        self.initRouter(module)

    def initCompanyPrepare(self, module_super):
        module = Module(name="抓取公司前的预处理")
        def company_info_prepare(info):
            try:
                company_list_name = info.xpath('.//a/text()')[0].strip()
            except Exception as e:
                company_list_name = ''

            company_url = ''
            company_url_list = info.xpath(".//a")
            if company_url_list:
                if isinstance(company_url_list, list):
                    company_url = company_url_list[0].get("href")

            if '../GSpublicity/' in company_url:
                company_url = 'http://gsxt.gdgs.gov.cn/aiccips' + company_url[2:]

            return {"company_url": company_url, "company_name": company_list_name,
                    "search_company": company_list_name}
        module.appendOutput(type=OutputType.FUNCTION, function=company_info_prepare)
        module_super.appendSubModule(module)

    def initRouter(self, module_super):
        module = Module(None, "广东公司适配", router=Router())

        def source_prepare(company_url):
            source = ''
            if 'gsxt.gzaic.gov.cn' in company_url:
                source = u"企业信用网"
            elif '/GSpublicity/' in company_url:
                source = u"企业信息网"
            elif 'szcredit' in company_url:
                source = u"深圳信用网"
            else:
                source = u"企业信用网"

            self.page_dict['source'] = source

            return {"source": source}

        module.appendInput(InputType.FUNCTION, source_prepare)

        qyxx = CrawlerGdQyxx(self.pinyin, self)
        module.appendSubModule(qyxx.module_manager.getFirstModule())
        qyxy = CrawlerGdQyxy(self.pinyin, self)
        module.appendSubModule(qyxy.module_manager.getFirstModule())
        szxy = CrawlerSzxy(self.pinyin, self)
        module.appendSubModule(szxy.module_manager.getFirstModule())
        def shenzhenAssert(source):
            if not source or source == u"深圳信用网":
                self.report.access_type = SeedAccessType.NO_TARGET_SOURCE
                return False
            return True
        module.addEvent(Event(event_type=EventType.ASSERT_FAILED, retry_times=0, assert_function=shenzhenAssert))
        module_super.appendSubModule(module, True)
