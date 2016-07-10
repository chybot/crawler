# -*- coding: utf-8 -*-
# Created by David on 2016/5/4.

import sys
import random
import time
import re
import urlparse
reload(sys)
sys.path.append('./util')
from lxml import etree
from CrawlerBase import CrawlerBase
from ModuleManager import Module,Event,Iterator
from util.crawler_util import CrawlerRunMode, OutputType, EventType, OutputParameterShowUpType,InputType
from CommonLib.WebContent import WebAccessType, SeedAccessType

class CrawlerShanghai(CrawlerBase):
    def __init__(self, pinyin, callbackFromOuterControl):
        config_dict = dict()
        config_dict[CrawlerRunMode.COMPANY_KEY] = [self.initToken, self.initConfigSearchList, self.initConfigCompanyInfo]
        config_dict[CrawlerRunMode.COMPANY_URL] = [self.initConfigBaseInfo, self.initResultCollect]

        check_dict = dict()
        check_dict['html_check_dict'] = {'过于频繁':WebAccessType.TOO_OFTEN, '非正常访问':WebAccessType.ACCESS_VIOLATION }
        CrawlerBase.__init__(self, pinyin, config_dict, check_dict, callbackFromOuterControl)
        pass

    def initToken(self):
        module = Module(self.getWebHtml, u"令牌获取")
        module.module_id = "module_token"
        module.appendUrl('https://www.sgs.gov.cn/notice/search/popup_captcha')
        module.appendHeaders({
                            'Host' : 'www.sgs.gov.cn',
                            'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; rv:40.0) Gecko/20100101 Firefox/40.0',
                            'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                            'Accept-Language' : 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
                            'Accept-Encoding' : 'gzip, deflate',
                            'Referer' : 'https://www.sgs.gov.cn/notice/home'
                        })
        module.appendEncoding("utf-8")
        def getToken(html):
            if not html or '\"session.token\": \"' not in html:
                self.holder.logging.error(u'获取session.token失败！')
                return None
            token = re.search(r'\"session\.token\": \"(.*?)\"', html).group(1)
            if not token:
                self.holder.logging.error(u'提取token失败！')
            self.holder.logging.info('token: %s' % token)
            return token
        module.appendOutput(name="token", type=OutputType.FUNCTION, function=getToken)
        module.addEvent(Event(EventType.EXCEPTION_OCCURED, retry_times=100))
        module.addEvent(Event(EventType.OUTPUT_NOT_SATISFIED, retry_times=100))
        self.module_manager.appendSubModule(module)

    def initConfigSearchList(self):
        module = Module(self.visitSearchList, u"搜索列表")
        module.appendUrl('https://www.sgs.gov.cn/notice/search/ent_info_list')
        module.appendHeaders({
                            'Host' : 'www.sgs.gov.cn',
                            'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; rv:40.0) Gecko/20100101 Firefox/40.0',
                            'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                            'Accept-Language' : 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
                            'Accept-Encoding' : 'gzip, deflate',
                            'Referer' : 'https://www.sgs.gov.cn/notice/home',
                            'Content-Type' : 'application/x-www-form-urlencoded'
                        })
        module.appendWebMethod("post")
        module.appendPostData(lambda token,company_key:{
                                                            'searchType': '1',
                                                            'captcha': 0,
                                                            'session.token': token,
                                                            'condition.keyword': company_key
                                                        })
        module.appendOutput("search_list", './/div[@class="list-item"]', OutputType.LIST)
        module.appendOutput("page_list", '//div/ul/li/a[@rel]', OutputType.LIST, show_up=OutputParameterShowUpType.OPTIONAL)
        def page_nos(page_list=None):
            if not page_list or len(page_list) < 2:
                return range(0,0)
            a_tag = page_list[-2]
            page_no = a_tag[a_tag.find('>') + 1:a_tag.find('</a')]
            return range(2, int(page_no)+1)
        module.appendOutput("page_nos", type=OutputType.FUNCTION, function=page_nos, show_up=OutputParameterShowUpType.OPTIONAL)
        module.addEvent(Event(EventType.EXCEPTION_OCCURED, retry_times=100, redo_module="module_token"))
        def assert_func(url_list, name_invalid_list, html):
            if not url_list and name_invalid_list:
                self.report.access_type = SeedAccessType.NO_VALID_COMPANY
                self.holder.logging.info("无有效公司列表！")
                return False
            if self.report.access_type == SeedAccessType.NON_COMPANY:
                self.holder.logging.info("无此公司！")
                return False
            return True
        module.addEvent(Event(EventType.OUTPUT_NOT_SATISFIED, retry_times=100, redo_module="module_token"))
        self.module_manager.appendSubModule(module)

    # Todo 搜索列表页翻页，待测
    def initSearchListPages(self):
        iterator = Iterator("page_nos", "page_no")
        module = Module(None, u"处理搜索列页码信息", iterator)
        self.module_manager.appendSubModule(module)

        self.initSearchPage(module)

    # Todo 搜索列表页翻页，待测
    def initSearchPage(self, module_super):
        module = Module(self.visitSearchList, u"搜索列表-翻页")
        module.appendUrl('https://www.sgs.gov.cn/notice/search/ent_info_list')
        module.appendHeaders({
            'Host': 'www.sgs.gov.cn',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:40.0) Gecko/20100101 Firefox/40.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
            'Referer': 'https://www.sgs.gov.cn/notice/home',
            'Content-Type': 'application/x-www-form-urlencoded'
        })
        module.appendWebMethod("post")
        module.appendPostData(lambda token, company_key, page_no: {
            'searchType': '1',
            'captcha': 0,
            'session.token': token,
            'condition.keyword': company_key,
            'condition.pageNo': page_no
        })
        module.appendOutput("search_list", './/div[@class="list-item"]', OutputType.LIST)
        module.addEvent(Event(EventType.EXCEPTION_OCCURED, retry_times=2))
        module_super.appendSubModule(module)

    def initConfigCompanyInfo(self):
        iterator = Iterator("search_list", "info")
        module = Module(None, u"获取公司信息", iterator)
        self.module_manager.appendSubModule(module, True)

        self.initCompanyInfoPrepare(module)
        self.initConfigBaseInfo(module)
        self.initGdxq(module)
        self.initNianBao(module)
        self.initNbiter(module)
        self.initResultCollect(module)

    def initCompanyInfoPrepare(self, module_super):
        module = Module(None, u"抓取公司前的预处理")
        def prepare(info):
            query_ = dict()
            query_["company_url"] = info.xpath('.//a/@href')[0].strip()
            query_["search_company"] = info.xpath('.//a/text()')[0].strip()
            #query_['zch'] = info.xpath(".//*[@class='profile']/span[1]/text()")[0].strip()
            return query_
        module.appendOutput(type=OutputType.FUNCTION, function=prepare)
        module_super.appendSubModule(module, True)

    def initConfigBaseInfo(self, module_super):
        module = Module(self.visitJbxx, u"基本信息")
        module.appendUrl("company_url")
        module.appendHeaders({
                                'Host' : 'www.sgs.gov.cn',
                                'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; rv:40.0) Gecko/20100101 Firefox/40.0',
                                'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                                'Accept-Language' : 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
                                'Accept-Encoding' : 'gzip, deflate',
                                'Referer' : 'https://www.sgs.gov.cn/notice/search/ent_info_list'
                            })
        module.appendEncoding("utf-8")
        module.appendOutput(name="gdxq_list", xpath=".//*[@id='investorTable']//td/a/@href", type=OutputType.LIST, show_up=OutputParameterShowUpType.OPTIONAL)
        module_super.appendSubModule(module, True)

    def initGdxq(self, module_super):
        iterator = Iterator(seeds="gdxq_list", param_name="gdxq")
        module = Module(iterator=iterator, name=u"遍历股东详情")
        module_super.appendSubModule(module)

        sub_module = Module(self.visitGdxq, u"抓取股东详情")
        sub_module.appendUrl("gdxq")
        module.appendHeaders(lambda gdxq:{
                                'Host' : 'www.sgs.gov.cn',
                                'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; rv:40.0) Gecko/20100101 Firefox/40.0',
                                'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                                'Accept-Language' : 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
                                'Accept-Encoding' : 'gzip, deflate',
                                'Referer' : gdxq
                            })
        module.appendSubModule(sub_module)

    def initNianBao(self,module_super):
        module = Module(self.getWebHtml, u"抓取公司的年报信息")
        module.appendUrl(lambda company_url: company_url.replace('tab=01', 'tab=02'))
        module.appendHeaders({
            'Host': 'www.sgs.gov.cn',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive'
        })
        def xpaths(html):
            tree=etree.HTML(html)
            _list = tree.xpath('.//*[@class="info m-bottom m-top"]/tr/td/a')
            qynb_list = []
            for ll in _list:
                url = ''.join(ll.xpath('@href')).strip()
                name = ''.join(ll.xpath('text()')).replace(u'年度报告', '')
                if name !=  u'详情':
                    qynb_list.append([url ,name])
            return qynb_list
        module.appendOutput(name='qynb_list', type=OutputType.FUNCTION, function=xpaths,
                            show_up=OutputParameterShowUpType.OPTIONAL)
        module_super.appendSubModule(module, True)

    def initNbiter(self, module_super):
        iterator = Iterator("qynb_list","nianb")
        module = Module(None, u"获取公司年报", iterator)
        module_super.appendSubModule(module, True)

        sub_module = Module(self.visitQynb, u"获取年报详情")
        def prepare(nianb):
            mv_dict = dict()
            mv_dict['nb_url'] = nianb[0]
            mv_dict['nb_name'] = nianb[1]
            return mv_dict
        sub_module.appendInput(InputType.FUNCTION, input_value=prepare)
        sub_module.appendUrl('nb_url')
        sub_module.appendHeaders({'Host': 'www.sgs.gov.cn',
                                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0',
                                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                                    'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
                                    'Accept-Encoding': 'gzip, deflate',
                                    'Connection': 'keep-alive'})
        module.appendSubModule(sub_module)


    def initResultCollect(self, module_super):
        module = Module(self.resultCollect, u"结果收集")
        module_super.appendSubModule(module)





