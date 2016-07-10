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

class CrawlerHubei(CrawlerBase):
    def __init__(self, pinyin, callbackFromOuterControl):
        config_dict = dict()
        config_dict[CrawlerRunMode.COMPANY_KEY] = [self.initConfigYzm, self.initConfigSearchList, self.initConfigCompanyInfo]
        config_dict[CrawlerRunMode.COMPANY_URL] = [self.initConfigBaseInfo, self.initResultCollect]

        check_dict = dict()
        check_dict['html_check_dict'] = {'过于频繁':WebAccessType.TOO_OFTEN, '非正常访问':WebAccessType.ACCESS_VIOLATION }
        CrawlerBase.__init__(self, pinyin, config_dict, check_dict, callbackFromOuterControl)

    def initConfigYzm(self):
        module = Module(self.visitValidateCode, u"验证码")
        module.module_id = "module_yzm"
        module.appendUrl(lambda radom_val: "http://xyjg.egs.gov.cn/ECPS_HB/validateCode.jspx?type=1&_=%s" % (str(int(random.random()))))
        module.appendHeaders(lambda ua: {
            "Host": "xyjg.egs.gov.cn",
            "User-Agent": ua,
            "Accept": "image/png,image/*;q=0.8,*/*;q=0.5",
            "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
            "Accept-Encoding": "gzip, deflate",
            "Referer": "http://xyjg.egs.gov.cn/ECPS_HB/search.jspx"
        })
        # Todo  不指定redo module，是不是重试自己？？
        module.addEvent(Event(EventType.EXCEPTION_OCCURED, retry_times = 10000))  # redo_module
        self.module_manager.appendSubModule(module)

    def initConfigSearchList(self):
        module = Module(self.visitSearchList, u"搜索列表")
        module.appendUrl('http://xyjg.egs.gov.cn/ECPS_HB/searchList.jspx')
        module.appendHeaders(lambda ua: {
            "Host": "xyjg.egs.gov.cn",
            "User-Agent": ua,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
            "Accept-Encoding": "gzip, deflate",
            "Content-Type": "application/x-www-form-urlencoded",
            "Referer": "http://xyjg.egs.gov.cn/ECPS_HB/search.jspx"
        }
        )
        module.appendWebMethod("post")
        module.appendPostData(lambda company_key,yzm:
                                    {
                                        'checkNo': yzm,
                                        'entName': company_key
                                    }
                              )
        module.appendOutput("search_list", "//*[@class='list']/ul/li/a/@href", OutputType.LIST)
        module.addEvent(Event(EventType.EXCEPTION_OCCURED, retry_times = 100, redo_module = "module_home_page"))
        module.addEvent(Event(EventType.OUTPUT_NOT_SATISFIED, retry_times = 100, redo_module = "module_home_page"))
        module.addEvent(Event(EventType.ASSERT_FAILED, retry_times = 0,
                              assert_function = lambda: False if self.report.access_type == SeedAccessType.NON_COMPANY else True))
        module.appendMiddleValueMonitor("search_list")
        self.module_manager.appendSubModule(module)

        # def assert_func(url_list, name_invalid_list, html):
        #     if not url_list and name_invalid_list:
        #         self.report.access_type = SeedAccessType.NO_VALID_COMPANY
        #         self.holder.logging.info("无有效公司列表！")
        #         return False
        #     if self.report.access_type == SeedAccessType.NON_COMPANY:
        #         self.holder.logging.info("无此公司！")
        #         return False
        #     return True

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





