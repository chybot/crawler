# -*- coding: utf-8 -*-
# Created by David on 2016/5/9.

import sys
import random
import time
import re
import urllib
import PyV8
reload(sys)
from qyxx_all.CrawlerBase import CrawlerBase
from lxml import etree
from qyxx_all.util.common_util import substring
from qyxx_all.ModuleManager import Module,Event,Iterator,Adapter,Bypass
from qyxx_all.util.crawler_util import CrawlerRunMode, InputType, OutputType, EventType, OutputParameterShowUpType
from CommonLib.WebContent import WebAccessType
from CommonLib.exceptutil import traceinfo

class CrawlerGdQyxy(CrawlerBase):
    def __init__(self, pinyin, crawler_master):
        self.crawler_master = crawler_master
        config_dict = dict()
        config_dict[CrawlerRunMode.COMPANY_ADAPTER] = [self.initConfigBaseInfo, self.initGdxx, self.initGdxqByHtml, self.initGdxqByJson, self.initBgxx,
                                                       self.initArchiveInfo, self.initArchivePage, self.initPenaltyInfo,
                                                       self.initNbList, self.initNb, self.initResultCollect]
        CrawlerBase.__init__(self, pinyin, config_dict, None, None)
        self.initConfig()
        self.parse_gdxx_on = True
        pass

    def initConfigBaseInfo(self):
        module = Module(self.crawler_master.visitJbxx, u"基本信息")
        module.module_id = "module_base_info_gz"
        adapter = Adapter({"source": u"企业信用网"}, u"企业信用网")
        module.addAdapter(adapter)

        module.appendUrl("company_url")
        module.appendHeaders(self.header_qyxy)
        def prepareCommonInfo(html):
            tree = etree.HTML(html)
            values = tree.xpath('.//@value')
            if not values or len(values) < 3:
                self.crawler_master.value_dict['jbxx_redirect'] = True
                return None
            entNo = values[1]
            entType = values[2]
            regOrg = values[3]
            return {"entNo": entNo, "entType": entType, "regOrg": regOrg}
        def assert_fun(web, jbxx_redirect=None):
            if not web:
                return False
            if jbxx_redirect:
                url = substring(web.body, "href='", "';</script>")
                url = "http://gsxt.gzaic.gov.cn"+url
                module.repalceInput(input_type=InputType.URL, input_value=url)
                self.crawler_master.value_dict["company_url"] = url
                module.repalceInput(input_type=InputType.HEADERS, input_value=self.header_qyxy)
                web.access_type = WebAccessType.STAMP_OUT_OF_TIME
                self.crawler_master.value_dict['jbxx_redirect'] = False
                return self.bypass_fun(u'jbxx_html')
            return True
        module.appendOutput(type=OutputType.FUNCTION, function=prepareCommonInfo)
        module.appendOutput(name="gdxq_list", xpath=".//*[@id='touziren']//td/a", type=OutputType.LIST, show_up=OutputParameterShowUpType.OPTIONAL)
        module.addEvent(Event(EventType.EXCEPTION_OCCURED, retry_times=5))
        module.addEvent(Event(EventType.ASSERT_FAILED, retry_times=2, assert_function=assert_fun))
        module.addEvent(Event(event_type=EventType.ASSERT_FAILED, retry_times=5, assert_function=self.block_assert))
        self.module_manager.appendSubModule(module, True)
        def gdxx_bypass(html):
            no = self.getPageNo(html, ".//*[@id='invInfo']/table[@class='detailsList']//th/text()")
            if no >= 2:
                return False
            else:
                return True
        def gdxq_html_bypass(html):
            return not gdxx_bypass(html)
        def bgxx_bypass(html):
            no = self.getPageNo(html, ".//*[@id='biangeng']/table[@class='detailsList']//th/text()")
            if no >= 2:
                return False
            else:
                return True
        module.appendBypass(Bypass(condition_fuc=gdxx_bypass, module_id="module_gdxx", range_global=True))
        module.appendBypass(Bypass(condition_fuc=gdxx_bypass, module_id="module_gdxq_json", range_global=True))
        module.appendBypass(Bypass(condition_fuc=gdxq_html_bypass, module_id="module_gdxq_html", range_global=True))
        module.appendBypass(Bypass(condition_fuc=bgxx_bypass, module_id="module_bgxx", range_global=True))

    def initGdxx(self):
        module = Module(self.crawler_master.visitGdxxJson, u'股东信息')
        module.module_id = "module_gdxx"
        module.appendUrl("http://gsxt.gzaic.gov.cn/aiccips/GSpublicity/invInfoPage.html")
        module.appendHeaders(self.header_qyxy)
        module.appendWebMethod("post")
        module.appendPostData(lambda entNo,regOrg: {"entNo":entNo, "pageNo":2, "regOrg":regOrg})
        module.addMapper({'invType':u'gdxx.股东类型', 'inv':u'gdxx.股东', 'entNo':u'gdxx.证照/证件号码', "invNo":"invNo", 'primary_key':'inv, entNo' })
        self.module_manager.appendSubModule(module)

    def initGdxqByHtml(self):
        iterator = Iterator("gdxq_list", "gdxq")
        module = Module(None, "进入股东详情-html", iterator)
        module.module_id = "module_gdxq_html"
        self.module_manager.appendSubModule(module, True)

        sub_module = Module(self.crawler_master.visitGdxq, "获取股东详情信息")
        def getGdxqUrl(gdxq):
            onclick = ''.join(gdxq.xpath("@onclick"))
            if u'alert' in onclick:
                return None
            url = onclick.replace("window.open('","").replace("')","")
            return url
        sub_module.appendUrl(getGdxqUrl)
        module.appendSubModule(sub_module)

    def initGdxqByJson(self):
        iterator = Iterator("gdxx_list", "gdxx_rcd")
        module = Module(None, "进入股东详情-json", iterator)
        module.module_id = "module_gdxq_json"
        self.module_manager.appendSubModule(module, True)

        sub_module = Module(self.crawler_master.visitGdxq, "获取股东详情信息")

        def getGdxqUrl(gdxx_rcd, entNo, regOrg):
            if 'invNo' in gdxx_rcd:
                self.crawler_master.value_dict['invNo'] = gdxx_rcd['invNo']
                del gdxx_rcd['invNo']
            if 'invNo' not in self.crawler_master.value_dict:
                return None
            get_data = {
                'invNo': self.crawler_master.value_dict['invNo'],
                'entNo': entNo,
                'regOrg': regOrg
            }
            return 'http://gsxt.gzaic.gov.cn/aiccips/GSpublicity/invInfoDetails.html?' + urllib.urlencode(get_data)
        sub_module.appendInput(input_name="gdxq_url", input_type=InputType.FUNCTION, input_value=getGdxqUrl)
        sub_module.appendUrl("gdxq_url")
        sub_module.appendHeaders(lambda gdxq_url: {
            "Host": "gsxt.gzaic.gov.cn",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; rv:37.0) Gecko/20100101 Firefox/37.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
            "Accept-Encoding": "gzip, deflate",
            "Referer": gdxq_url,
            "Connection": "keep-alive"
        })
        module.appendSubModule(sub_module, True)

    def initBgxx(self):
        module = Module(self.crawler_master.visitBgxxJson, u'变更信息')
        module.module_id = "module_bgxx"
        module.appendUrl("http://gsxt.gzaic.gov.cn/aiccips/GSpublicity/entChaPage")
        module.appendHeaders(self.header_qyxy)
        module.appendWebMethod("post")
        module.appendPostData(lambda entNo,regOrg,entType: {"entNo":entNo, "pageNo":2, "regOrg":regOrg, "entType":entType})
        self.module_manager.appendSubModule(module)

    def initArchiveInfo(self):
        module = Module(self.crawler_master.visitBaxx, u"备案信息")
        module.module_id = "module_baxx"
        module.appendUrl("http://gsxt.gzaic.gov.cn/aiccips/GSpublicity/GSpublicityList.html?service=entCheckInfo")
        module.appendHeaders(self.header_qyxy)
        module.appendWebMethod("post")
        module.appendPostData(lambda entNo,entType,regOrg: {"entNo":entNo, "entType":entType, "regOrg":regOrg})
        module.addEvent(Event(event_type=EventType.ASSERT_FAILED, retry_times=5, redo_module="module_base_info_gz", assert_function=self.block_assert))
        self.module_manager.appendSubModule(module, True)
        def baxx_bypass(html):
            no = self.getPageNo(html, ".//*[@id='zyry']/table[@class='detailsList']//th/text()")
            if no >= 2:
                return False
            else:
                return True
        module.appendBypass(Bypass(condition_fuc=baxx_bypass, module_id="module_baxx_page"))

    def initArchivePage(self):
        module = Module(self.crawler_master.visitBaxxJson, u"备案信息翻页")
        module.module_id = "module_baxx_page"
        module.appendUrl("http://gsxt.gzaic.gov.cn/aiccips/GSpublicity/vipInfoPage")
        module.appendHeaders(self.header_qyxy)
        module.appendWebMethod("post")
        module.appendPostData(lambda entNo,regOrg: {"entNo":entNo, "pageNo":2, "regOrg":regOrg})
        self.module_manager.appendSubModule(module)

    def initFzjg(self):
        # TODO
        pass

    def initPenaltyInfo(self):
        module = Module(self.crawler_master.visitXzcf, u"抓取行政处罚信息")
        module.module_id = "module_xzcf"
        module.appendUrl("http://gsxt.gzaic.gov.cn/aiccips/GSpublicity/GSpublicityList.html?service=cipPenaltyInfo")
        module.appendHeaders(self.header_qyxy)
        module.appendWebMethod("post")
        module.appendPostData(lambda entNo,entType,regOrg: {"entNo":entNo, "entType":entType, "regOrg":regOrg})
        module.addEvent(Event(event_type=EventType.ASSERT_FAILED, retry_times=5, redo_module="module_base_info_gz", assert_function=self.block_assert))
        self.module_manager.appendSubModule(module, True)

    def initNbList(self):
        module = Module(self.crawler_master.visitQynbList, u"抓取年报列表")
        module.appendUrl("http://gsxt.gzaic.gov.cn/aiccips/BusinessAnnals/BusinessAnnalsList.html")
        module.appendHeaders(self.header_qyxy)
        module.appendWebMethod("post")
        module.appendPostData(lambda entNo,entType,regOrg: {"entNo":entNo, "entType":entType, "regOrg":regOrg})
        module.appendOutput("nb_list", ".//table//td/a", OutputType.LIST, show_up=OutputParameterShowUpType.OPTIONAL)
        module.addEvent(Event(event_type=EventType.ASSERT_FAILED, retry_times=5, redo_module="module_base_info_gz", assert_function=self.block_assert))
        self.module_manager.appendSubModule(module)

    def initNb(self):
        iterator = Iterator(seeds="nb_list", param_name="nb")
        module = Module(iterator=iterator, name=u"遍历年报列表")
        self.module_manager.appendSubModule(module)

        self.initNbOne(module)

    def initNbOne(self, module_super):
        module = Module(self.crawler_master.visitQynb, u"抓取企业年报信息")
        def prepare(nb):
            mv_dict = dict()
            mv_dict['nb_url'] = ''.join(nb.xpath('@href'))
            mv_dict['nb_name'] = ''.join(nb.xpath('text()')).replace(u'年度报告','').strip()
            return mv_dict
        module.appendInput(input_type=InputType.FUNCTION, input_value=prepare)
        module.appendUrl("nb_url")
        module.appendHeaders({
                            "Host": "gsxt.gzaic.gov.cn",
                            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; rv:37.0) Gecko/20100101 Firefox/37.0",
                            "Accept": "application/json, text/javascript, */*",
                            "Accept-Language": "zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3",
                            "Accept-Encoding": "gzip, deflate",
                            "Content-Type": "application/x-www-form-urlencoded",
                            "X-Requested-With": "XMLHttpRequest",
                            "Referer": "http://gsxt.gzaic.gov.cn/aiccips/BusinessAnnals/BusinessAnnalsList.html",
                            "Connection": "keep-alive"
                        })
        module.addEvent(Event(event_type=EventType.ASSERT_FAILED, retry_times=5, redo_module="module_base_info_gz", assert_function=self.block_assert))
        module_super.appendSubModule(module)

    def initResultCollect(self):
        module = Module(self.crawler_master.resultCollect, u"结果收集")
        self.module_manager.appendSubModule(module)

    def bypass_fun(self, page_dict_key):
        if page_dict_key in self.crawler_master.page_dict and self.crawler_master.page_dict[page_dict_key]:
            for web in self.crawler_master.page_dict[page_dict_key]:
                if web.access_type != WebAccessType.OK:
                    return False
            return True
        return False

    def block_assert(self, html=None):
        if not html:
            return False
        if u'errorinfo_new2.gif' in html:
            self.crawler_master.holder.logging.warning(u"页面timestamp已超时！")
            return False
        return True

    def getPageNo(self, html, xpath_pattern):
        page_no = 1
        try:
            html = html.replace('&nbsp;', '').replace('<<', '').replace('>>', '').replace('\n', '')
            tree = etree.HTML(html)
            ele = tree.xpath(xpath_pattern)
            pages = ''.join(ele).strip()
            arr = pages.split("/")
            if pages and len(arr) > 0:
                page_no = int(arr[-1])
        except Exception as e:
            self.holder.logging.warning(traceinfo(e))
        return page_no

    def header_qyxy(self, company_url):
        header = {
            "Host": "gsxt.gzaic.gov.cn",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; rv:37.0) Gecko/20100101 Firefox/37.0",
            "Accept": "application/json, text/javascript, */*",
            "Accept-Language": "zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3",
            "Accept-Encoding": "gzip, deflate",
            "Content-Type": "application/x-www-form-urlencoded",
            "X-Requested-With": "XMLHttpRequest",
            "Referer": company_url,
            "Connection": "keep-alive"
        }
        return header

