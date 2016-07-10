# -*- coding: utf-8 -*-
# Created by David on 2016/5/4.

import sys
import random
import time
import urlparse
reload(sys)
sys.path.append('./util')
from CrawlerBase import CrawlerBase
from lxml import etree
from ModuleManager import Module,Event,Iterator
from util.crawler_util import CrawlerRunMode, InputType, OutputType, EventType, OutputParameterShowUpType
from CommonLib.WebContent import WebAccessType, SeedAccessType

class CrawlerZhejiang(CrawlerBase):
    def __init__(self, pinyin, callbackFromOuterControl):
        config_dict = dict()
        config_dict[CrawlerRunMode.COMPANY_KEY] = [self.initConfigValidateCode, self.initConfigSearchList, self.initConfigCompanyInfo]
        config_dict[CrawlerRunMode.COMPANY_URL] = [self.initConfigBaseInfo, self.initTopInfo, self.initConfigShareHolderInfo, self.initShareHolderInfoPage,
                                                   self.initShareHolderDetail, self.initConfigChangeInfo, self.initChangeInfoPage, self.initArchiveInfo, self.initResultCollect]

        check_dict = dict()
        check_dict['html_check_dict'] = {u'过于频繁':WebAccessType.TOO_OFTEN, u'非正常访问':WebAccessType.ACCESS_VIOLATION }
        CrawlerBase.__init__(self, pinyin, config_dict, check_dict, callbackFromOuterControl)
        # 打开基本信息解析开关
        self.parse_jbxx_on = True
        # 临时打开其他解析开关，便于观察抓取情况
        self.parse_on = True
        pass

    def initConfigValidateCode(self):
        module = Module(self.visitValidateCode, u"验证码")
        module.module_id = "module_validate_code"
        module.appendUrl("http://gsxt.zjaic.gov.cn/common/captcha/doReadKaptcha.do")
        module.appendHeaders(
                                {
                                    "Host" : "gsxt.zjaic.gov.cn",
                                    "User-Agent" : "Mozilla/5.0 (Windows NT 6.1; rv:40.0) Gecko/20100101 Firefox/40.0",
                                    "Accept" : "image/png,image/*;q=0.8,*/*;q=0.5",
                                    "Accept-Language" : "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
                                    "Accept-Encoding" : "gzip, deflate",
                                    "Referer" : "http://gsxt.zjaic.gov.cn/search/doEnGeneralQueryPage.do"
                                }
                            )
        module.addEvent(Event(EventType.EXCEPTION_OCCURED, retry_times=100000))
        self.module_manager.appendSubModule(module)

    def initPostParam(self):

        def postSearchListData(json, yzm):
            if 'textfield' not in json:
                return None
            textfield = json['textfield']
            data = {
                "textfield": textfield,
                "code": yzm
            }
            return data

        def postDataJsonAssert(json = None):
            if not json:
                return False
            if 'flag' not in json or json['flag'] != '1':
                return False
            return True

        module = Module(self.getJson, "json中间结果")
        module.appendUrl("http://gsxt.zjaic.gov.cn/search/doValidatorVerifyCode.do")
        module.appendHeaders(
                                {
                                'Host': 'gsxt.zjaic.gov.cn',
                                'User-Agent': "Mozilla/5.0 (Windows NT 6.1; rv:40.0) Gecko/20100101 Firefox/40.0",
                                'Accept': 'application/json, text/javascript, */*; q=0.01',
                                'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
                                'Accept-Encoding': 'gzip, deflate',
                                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                                'X-Requested-With': 'XMLHttpRequest',
                                'Referer': 'http://gsxt.zjaic.gov.cn/search/doEnGeneralQueryPage.do',
                                'Connection': 'keep-alive',
                                'Pragma': 'no-cache',
                                'Cache-Control': 'no-cache'}
                            )
        module.appendWebMethod("post")
        module.appendPostData(lambda company_key, yzm: {"name": company_key, "verifyCode": yzm})

        # module.appendOutput(name = "post_data", type = OutputType.FUNCTION, function = postSearchListData)
        module.addEvent(Event(EventType.OUTPUT_NOT_SATISFIED, redo_module = "module_validate_code"))
        module.addEvent(Event(EventType.EXCEPTION_OCCURED, redo_module = "module_validate_code"))
        module.addEvent(Event(EventType.ASSERT_FAILED, assert_function = postDataJsonAssert, redo_module = "module_validate_code"))

        self.module_manager.appendSubModule(module)
    def initConfigSearchList(self):
        module = Module(self.visitSearchList, "搜索列表")
        module.appendUrl('http://gsxt.jxaic.gov.cn/ECPS/home/home_homeSearch.pt')
        module.appendHeaders({'Host': 'gsxt.jxaic.gov.cn', 'Referer': 'http://gsxt.jxaic.gov.cn/qyxxgsAction_queryXyxx.action',
                            'Accept-Encoding': 'gzip, deflate', 'Cache-Control': 'max-age=0',
                            'Accept-Language': 'en-US,en;q=0.8', 'Content-Type': 'application/x-www-form-urlencoded',
                            'Connection': 'keep-alive',
                            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.101 Safari/537.36'}
                            )
        module.appendWebMethod("post")
        module.appendPostData(lambda yzm, company_key:{"search": company_key,"yzm": yzm,})
        module.appendOutput("url_list", './/*[@class="list"]/div/a/@href', OutputType.LIST)
        module.appendOutput("name_list", './/*[@class="list"]/div/a/font/text()', OutputType.LIST)
        module.appendOutput(name="search_list", type=OutputType.FUNCTION, function=lambda url_list, name_list:zip(url_list, name_list))
        module.appendOutput("name_invalid_list", ".//*[@id='div0']/div[1]/text()", OutputType.LIST, show_up=OutputParameterShowUpType.OPTIONAL)
        module.appendOutput("status_invalid_list", ".//*[@id='div0']/div[2]/span[2]/text()", OutputType.LIST, show_up=OutputParameterShowUpType.OPTIONAL)
        module.appendOutput("page_nos", ".//*[@id='form1']//div//td[@align]/text()", show_up=OutputParameterShowUpType.OPTIONAL)
        # Todo 搜索列表页翻页
        def page_range(page_nos):
            if not page_nos:
                return None
            page_str = page_nos.strip()
            page_str = page_str[3:]
            page_str = page_str[page_str.find('共') + 3:page_str.find('页')]
            return range(2, int(page_str)+1)
        module.addEvent(Event(EventType.EXCEPTION_OCCURED, retry_times=2, redo_module="module_validate_code"))
        def assert_func(url_list, name_invalid_list, html):
            if not url_list and name_invalid_list:
                self.report.access_type = SeedAccessType.NO_VALID_COMPANY
                self.holder.logging.info("无有效公司列表！")
                return False
            if '无数据' in html:
                self.report.access_type = SeedAccessType.NON_COMPANY
                self.holder.logging.info("无此公司！")
                return False
            return True
        module.addEvent(Event(EventType.ASSERT_FAILED, retry_times=0, assert_function=assert_func))
        module.addEvent(Event(EventType.EXCEPTION_OCCURED, retry_times=100, redo_module="module_validate_code"))
        module.addEvent(Event(EventType.OUTPUT_NOT_SATISFIED, retry_times=100, redo_module="module_validate_code"))
        self.module_manager.appendSubModule(module)

    def initSearchPages(self):
        pass

    def initConfigCompanyInfo(self):
        iterator = Iterator("search_list", "com")
        module = Module(None, "获取公司信息", iterator)
        self.module_manager.appendSubModule(module, True)

        self.initCompanyInfoPrepare(module)
        self.initConfigBaseInfo(module)
        self.initTopInfo(module)

        self.initConfigShareHolderInfo(module)
        self.initShareHolderInfoPage(module)
        self.initShareHolderDetail(module)

        self.initConfigChangeInfo(module)
        self.initChangeInfoPage(module)

        self.initArchiveInfo(module)
        self.initResultCollect(module)

    def initCompanyInfoPrepare(self, module_super):
        module = Module(None, "抓取公司前的预处理")
        def prepare(com):
            query_ = {}
            if com and len(com) >= 2:
                query_["company_url"] = com[0]
                query_["search_company"] = com[1]
            return query_
        module.appendOutput(type=OutputType.FUNCTION, function=prepare)
        module_super.appendSubModule(module, True)

    def initConfigBaseInfo(self, module_super):
        module = Module(self.visitJbxx, "基本信息")
        def prepare(company_url):
            query_ = {}
            for qq in map(lambda x: x.split("="), urlparse.urlparse(company_url).query.split("&")):
                query_[qq[0]] = qq[1]
            print query_
            return query_
        module.appendInput(InputType.FUNCTION, prepare)
        module.appendUrl(lambda qyid, zch, qylx:"http://gsxt.jxaic.gov.cn/ECPS/ccjcgs/gsgs_viewDjxx.pt?qyid=%s&zch=%s&qylx=%s&num=undefined&showgdxx=true" % (qyid, zch, qylx))
        module.appendHeaders({'Accept-Language': 'en-US,en;q=0.5', 'Accept-Encoding': 'gzip, deflate',
                              'Connection': 'keep-alive',
                              'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                              'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.101 Safari/537.36',
                              'Host': 'gsxt.jxaic.gov.cn'})
        module_super.appendSubModule(module, True)

    def initTopInfo(self, module_super):
        module = Module(self.visitTopInfo, "Top信息")
        module.appendUrl(lambda qyid,zch,qylx:"http://gsxt.jxaic.gov.cn/ECPS/ccjcgs/ccjcgs_ccjcgsIndexDetail.pt?qylx=%s&qyid=%s&zch=%s&tabName=1" % (qylx,qyid,zch))
        module.appendHeaders({'Host' : 'gsxt.jxaic.gov.cn',
            'Connection' : 'keep-alive',
            'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.101 Safari/537.36',
            'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding' : 'gzip, deflate, sdch',
            'Accept-Language' : 'en-US,en;q=0.8,zh-CN;q=0.6,zh-TW;q=0.4'})
        module_super.appendSubModule(module, True)

    def initConfigShareHolderInfo(self, module_super):
        module = Module(self.visitGdxx, "股东信息")
        module.appendUrl(lambda qyid, zch:"http://gsxt.jxaic.gov.cn/ECPS/ccjcgs/gsgs_viewDjxxGdxx.pt?qyid=%s&zch=%s" % (qyid, zch))
        module.appendHeaders({'Accept-Language': 'en-US,en;q=0.8,zh-CN;q=0.6,zh-TW;q=0.4',
                              'Accept-Encoding': 'gzip, deflate, sdch', 'Connection': 'keep-alive',
                              'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                              'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.101 Safari/537.36',
                              'Host': 'gsxt.jxaic.gov.cn'})
        module.appendOutput("gdxx_pages", None, OutputType.FUNCTION, self.getPageNoPrepare, OutputParameterShowUpType.OPTIONAL)
        module_super.appendSubModule(module, True)

    def initShareHolderInfoPage(self, module_super):
        iterator = Iterator("gdxx_pages", "page_no")
        module = Module(None, "进入股东翻页", iterator)
        module_super.appendSubModule(module, True)

        sub_module = Module(self.visitGdxx, "获取股东翻页信息")
        sub_module.appendUrl(lambda qyid: "http://gsxt.jxaic.gov.cn/ECPS/ccjcgs/gsgs_viewDjxxGdxx.pt?qyid=%s" % qyid)
        sub_module.appendWebMethod("post")
        sub_module.appendPostData(lambda page_no:{'page':page_no,'limit':5,'mark':0})
        sub_module.appendHeaders({'Host' : 'gsxt.jxaic.gov.cn',
                                    'Connection' : 'keep-alive',
                                    'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.101 Safari/537.36',
                                    'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                                    'Accept-Encoding' : 'gzip, deflate, sdch',
                                    'Accept-Language' : 'en-US,en;q=0.8,zh-CN;q=0.6,zh-TW;q=0.4'})
        module.appendSubModule(sub_module)

    def initShareHolderDetail(self, module_super):
        iterator = Iterator("gdxx_list", "gdxx_rcd")
        module = Module(None, "进入股东详情", iterator)
        module_super.appendSubModule(module, True)

        sub_module = Module(self.visitGdxq, "获取股东详情信息")
        sub_module.appendUrl(self.getGdxqUrl)
        sub_module.appendHeaders({'Accept-Language': 'en-US,en;q=0.8,zh-CN;q=0.6,zh-TW;q=0.4', 'Accept-Encoding': 'gzip, deflate, sdch', 'Connection': 'keep-alive', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.101 Safari/537.36', 'Host': 'gsxt.jxaic.gov.cn', 'Cache-Control': 'max-age=0'})
        module.appendSubModule(sub_module)

    def initConfigChangeInfo(self, module_super):
        module = Module(self.visitBgxx, "变更信息")
        module.appendUrl(lambda qyid:"http://gsxt.jxaic.gov.cn/ECPS/ccjcgs/gsgs_viewDjxxBgxx.pt?qyid=%s" % qyid)
        module.appendHeaders({'Accept-Language': 'en-US,en;q=0.8,zh-CN;q=0.6,zh-TW;q=0.4',
                              'Accept-Encoding': 'gzip, deflate, sdch', 'Connection': 'keep-alive',
                              'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                              'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.101 Safari/537.36',
                              'Host': 'gsxt.jxaic.gov.cn'})
        module.appendOutput("bgxx_pages", None, OutputType.FUNCTION, self.getPageNoPrepare, OutputParameterShowUpType.OPTIONAL)
        module_super.appendSubModule(module, True)

    def initChangeInfoPage(self, module_super):
        iterator = Iterator("bgxx_pages", "page_no")
        module = Module(None, "进入变更信息翻页", iterator)
        module_super.appendSubModule(module)

        sub_module = Module(self.visitBgxx, "获取变更翻页信息")
        sub_module.appendUrl(lambda qyid: "http://gsxt.jxaic.gov.cn/ECPS/ccjcgs/gsgs_viewDjxxBgxx.pt?qyid=%s" % qyid)
        sub_module.appendWebMethod("post")
        sub_module.appendPostData(lambda page_no:{'page':page_no,'limit':5,'mark':0})
        sub_module.appendHeaders({  'Host' : 'gsxt.jxaic.gov.cn',
                                    'Connection' : 'keep-alive',
                                    'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.101 Safari/537.36',
                                    'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                                    'Accept-Encoding' : 'gzip, deflate, sdch',
                                    'Accept-Language' : 'en-US,en;q=0.8,zh-CN;q=0.6,zh-TW;q=0.4'})
        module.appendSubModule(sub_module)

    def initArchiveInfo(self, module_super):
        module = Module(self.visitBaxx, "获取备案信息")
        module.appendUrl(self.getZyryUrl)
        module.appendHeaders({'Accept-Language': 'en-US,en;q=0.8,zh-CN;q=0.6,zh-TW;q=0.4',
                              'Accept-Encoding': 'gzip, deflate, sdch', 'Connection': 'keep-alive',
                              'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                              'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.101 Safari/537.36',
                              'Host': 'gsxt.jxaic.gov.cn'})
        module_super.appendSubModule(module)

    def initResultCollect(self, module_super):
        module = Module(self.resultCollect, "结果收集")
        module_super.appendSubModule(module)

    def getPageNoPrepare(self, html):
        gdxx_tree = etree.HTML(html)
        gdxx_page = gdxx_tree.xpath(".//*[@id='totalPage']/@value")
        total_page = 0
        if gdxx_page:
            total_page = int("".join(gdxx_page))
        if total_page <= 1:
            return []
        return range(2, total_page+1)

    def getGdxqUrl(self, gdxx_rcd):
        for key in gdxx_rcd:
            if 'href' in gdxx_rcd[key]:
                href_dict = eval(gdxx_rcd[key]) if isinstance(gdxx_rcd[key],basestring) else gdxx_rcd[key]
                href = href_dict['href']
                xq_url="http://gsxt.jxaic.gov.cn%s" % href
                return xq_url
        return None

    def getZyryUrl(self, qyid, zch, qylx, company):
        '''
        获取主要人员信息的url，依赖于获取到的基本信息中的“类型”
        :param entId:
        :param company:
        :return:
        '''
        url = "http://gsxt.jxaic.gov.cn/ECPS/ccjcgs/gsgs_viewBaxx.pt?qyid=%s&zch=%s&qylx=%s&showgdxx=true" % (
            qyid, zch, qylx)
        if not company:
            return url
        for t_dict in company:
            if u"类型" in t_dict and t_dict[u"类型"] in [u"农民专业合作社", u"个体工商户"]:
                return "http://gsxt.jxaic.gov.cn/ECPS/ccjcgs/gsgs_viewBaxx.pt?qyid=%s&zch=%s&qylx=%s&&balx=%s" % (
                    qyid, zch, qylx, qylx)
        return url

if __name__ == "__main__":
    pass

