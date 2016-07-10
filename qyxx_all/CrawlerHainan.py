# -*- coding:utf-8 -*-
# CreateTime 2016-05-30 17:55 by yangwen

import sys
reload(sys)
sys.path.append('./util')
from CrawlerBase import CrawlerBase
from lxml import etree
from ModuleManager import Module,Event,Iterator,Sleep,Bypass
from util.crawler_util import CrawlerRunMode, InputType, OutputType, EventType, OutputParameterShowUpType
from CommonLib.WebContent import WebAccessType, SeedAccessType
import random
import urllib
import urlparse
import re

class CrawlerHainan(CrawlerBase):
    def __init__(self, pinyin, callbackFromOuterControl):
        config_dict = dict()
        config_dict[CrawlerRunMode.COMPANY_KEY] = [self.initYzm, self.initSubmitYzm, self.initSearchList, self.initCompanyInfo]
        config_dict[CrawlerRunMode.COMPANY_URL] = []

        check_dict = dict()
        check_dict['html_check_dict'] = {'{success:false}': WebAccessType.VALIDATE_FAILED}

        CrawlerBase.__init__(self, pinyin, config_dict, check_dict, callbackFromOuterControl)

    # 下载验证码并识别
    def initYzm(self):
        module = Module(self.visitValidateCode, u"第一步_获取验证码")
        module.module_id = "hn_yzm_pic"
        module.appendUrl("http://aic.hainan.gov.cn:1888/validateCode.jspx?type=0&id=%s" % random.random())
        module.appendHeaders(
            {

                "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                "Accept-Encoding":"gzip, deflate",
                "Accept-Language":"zh-CN,zh;q=0.8",
                "Cache-Control":"max-age=0",
                "Connection":"keep-alive",
                "Host":"aic.hainan.gov.cn:1888",
                "Referer":"http://aic.hainan.gov.cn:1888/search.jspx",
                "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36"
            }
        )
        module.appendWebMethod("get")
        module.addSleep(Sleep(2))
        module.addEvent(Event(EventType.EXCEPTION_OCCURED, retry_times=2))
        self.module_manager.appendSubModule(module, supportDefaultEvent=True)

    # 提交验证码验证正确性
    def initSubmitYzm(self):
        module = Module(self.getJson, u"第二步_提交验证码验证")
        module.appendUrl("http://aic.hainan.gov.cn:1888/checkCheckNo.jspx")
        module.appendHeaders(
            {
                "Accept": "application/json, text/javascript, */*; q=0.01",
                "Accept-Encoding": "gzip, deflate",
                "Accept-Language": "zh-CN,zh;q=0.8",
                "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                "Host": "aic.hainan.gov.cn:1888",
                "Origin": "http://aic.hainan.gov.cn:1888",
                "Proxy-Connection": "keep-alive",
                "Referer": "http://aic.hainan.gov.cn:1888/search.jspx",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36",
                "X-Requested-With": "XMLHttpRequest"
            }
        )
        module.appendWebMethod("post")
        module.appendPostData(lambda yzm: {"checkNo": yzm})
        module.addSleep(Sleep(3))
        module.addEvent(Event(EventType.EXCEPTION_OCCURED, retry_times=0, redo_module="hn_yzm_pic"))

        # 验证码判断条件
        def submitYzmResult(json=None):
            if not json:
                return False
            if '{success:true}' not in json:
                return False
            return True
        module.addEvent(Event(EventType.ASSERT_FAILED, assert_function=submitYzmResult, retry_times=0, redo_module="hn_yzm_pic"))
        self.module_manager.appendSubModule(module)

    # 搜索公司列表
    def initSearchList(self):
        module = Module(self.visitSearchList,u"第三步_开始搜索公司列表")
        module.appendUrl("http://aic.hainan.gov.cn:1888/searchList.jspx")
        module.appendHeaders(
            {
                "Host": "aic.hainan.gov.cn:1888",
                "Connection": "keep-alive",
                "Cache-Control": "max-age=0",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                "Origin": "http://aic.hainan.gov.cn:1888",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36",
                "Content-Type": "application/x-www-form-urlencoded",
                "Referer": "http://aic.hainan.gov.cn:1888/search.jspx",
                "Accept-Encoding": "gzip, deflate",
                "Accept-Language": "zh-CN,zh;q=0.8"
            }
        )
        module.appendWebMethod("post")
        module.appendPostData(lambda yzm, company_key:{
            "checkNo": yzm,
            "entName": company_key
        })
        module.appendOutput("url_list", ".//div[@class='list']//a/@href", OutputType.LIST)
        module.appendOutput("name_list", ".//div[@class='list']//a/text()", OutputType.LIST)
        module.appendOutput(name="search_list", type=OutputType.FUNCTION, function=lambda url_list, name_list: zip(url_list, name_list))
        module.addEvent(Event(EventType.EXCEPTION_OCCURED, retry_times=20, redo_module="hn_yzm_pic"))
        module.addEvent(Event(EventType.OUTPUT_NOT_SATISFIED, retry_times=20, redo_module="hn_yzm_pic"))
        module.addEvent(Event(EventType.ASSERT_FAILED, retry_times=0, assert_function=lambda :False if self.report.access_type == SeedAccessType.NON_COMPANY else True))
        module.appendMiddleValueMonitor("search_list")
        module.addSleep(Sleep(1))
        self.module_manager.appendSubModule(module)

    # 公司信息统一处理函数
    def initCompanyInfo(self):
        iterator = Iterator("search_list", "com")
        module = Module(None, u"获取公司信息", iterator)
        self.module_manager.appendSubModule(module, True)

        self.initUrlParams(module)

        self.initBasicInfo(module)

        self.initShareholderInfoPage(module)
        self.initShareholderInfoDetail(module)

        self.initChangeInfoPage(module)

        self.initArchiveInfoPage(module)
        # self.initArchiveInfoTwoPage(module)

        self.initBranchInfoPage(module)

        self.initAnnualReportList(module)
        self.initAnnualReport(module)
        # self.initAnnualReportInfo(module)

        self.initResultCollect(module)

    # 参数提取，公司名称、详情地址链接
    def initUrlParams(self,module_super):
        module = Module(None, u"公司详情链接参数值提取")

        def initReady(com):
            params = {}
            if com and len(com)>=2:
                params["company_url"] = com[0]
                params["search_company"] = com[1]
            return params
        module.appendOutput(type=OutputType.FUNCTION, function=initReady)
        module_super.appendSubModule(module, True)

    # 公司基本信息
    def initBasicInfo(self, module_super):
        module = Module(self.visitJbxx, u"第四步_获取基本信息")

        def getparams(company_url):
            query = {}
            for quy in map(lambda par: par.split("="), urlparse.urlparse(company_url).query.split("&")):
                query[quy[0]] = quy[1]
            print query
            return query
        module.appendInput(InputType.FUNCTION, getparams)
        module.appendUrl(lambda id: "http://aic.hainan.gov.cn:1888/businessPublicity.jspx?id=%s" % id)

        module.appendHeaders(
            {
                "Host": "aic.hainan.gov.cn:1888",
                "Connection": "keep-alive",
                "Cache-Control": "max-age=0",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36",
                "Referer": "http://aic.hainan.gov.cn:1888/searchList.jspx",
                "Accept-Encoding": "gzip, deflate",
                "Accept-Language": "zh-CN,zh;q=0.8"
            }
        )
        module.addSleep(Sleep(2))

        module_super.appendSubModule(module, True)

        # 股东信息页码获取
        def getGdxxPageno(html):
            fenye_xpath = ".//div[@id='invDiv']/following-sibling::table[1]|.//div[@id='invDiv']/following-sibling::div[1]"
            gdxx_tree = etree.HTML(html)
            fenye_table = gdxx_tree.xpath(fenye_xpath)
            if not fenye_table:
                return []
            fenye_table = fenye_table[0]
            pageno = self.parse_pageno(fenye_table)
            if pageno <= 1:
                return []
            self.holder.logging.info("------------------股东信息页码：" + str(pageno) + "---------------------")
            return range(2, int(pageno) + 1)

        module.appendOutput(name="gdxx_page_range", type=OutputType.FUNCTION, function=getGdxxPageno, show_up=OutputParameterShowUpType.OPTIONAL)
        def bypass_fun_gdxx(gdxx_page_range=None):
            if not gdxx_page_range:
                return True
            else:
                return False
        module.appendBypass(Bypass(condition_fuc=bypass_fun_gdxx, module_id="gdxx_pages"))

        # 变更信息页码获取
        def getBgxxPageno(html):
            fenye_xpath = ".//div[@id='altPagination']/table[1]|.//div[@id='altDiv']/following-sibling::table[1]"
            bgxx_tree = etree.HTML(html)
            fenye_table = bgxx_tree.xpath(fenye_xpath)
            if not fenye_table:
                return []
            fenye_table = fenye_table[0]
            pageno = self.parse_pageno(fenye_table)
            if pageno <= 1:
                return []
            return range(2, pageno + 1)
        module.appendOutput(name="bgxx_page_range", type=OutputType.FUNCTION, function=getBgxxPageno, show_up=OutputParameterShowUpType.OPTIONAL)
        def bypass_fun_bgxx(bgxx_page_range=None):
            if not bgxx_page_range:
                return True
            else:
                return False
        module.appendBypass(Bypass(condition_fuc=bypass_fun_bgxx,module_id="bgxx_pages"))

        # 备案信息页码提取
        def getbaxxPageno(html):
            fenye_xpath = ".//div[@id='memDiv']/following-sibling::table[1]|.//*[@id='beian']/table[2]"
            baxx_tree = etree.HTML(html)
            fenye_table = baxx_tree.xpath(fenye_xpath)
            if not fenye_table:
                return []
            fenye_table = fenye_table[0]
            pageno = self.parse_pageno(fenye_table)
            if pageno <= 1:
                return []
            return range(2, pageno + 1)
        module.appendOutput(name="baxx_page_range",type=OutputType.FUNCTION,function=getbaxxPageno,show_up=OutputParameterShowUpType.OPTIONAL)
        def bypass_fun_baxx(baxx_page_range=None):
            if not baxx_page_range:
                return  True
            else:
                return False
        module.appendBypass(Bypass(condition_fuc=bypass_fun_baxx,module_id="baxx_pages"))

        # 备案信息url区分，如果没有备案信息数据则不请求分页网址
        # def getbaxx_url(html):
        #     data_xpath = ".//div[@id='memDiv']"
        #     tree = etree.HTML(html)
        #     data_trs = tree.xpath(data_xpath)
        #     if not data_trs:
        #         return True
        #     else:
        #         return False
        # module.appendBypass(Bypass(condition_fuc=getbaxx_url,module_id="baxx_pages"))

        # 分支机构页码提取
        def getfzjgPageno(html):
            fenye_xpath = ".//div[@id='childPagination']/table[1]|.//div[@id='childDiv']/following-sibling::table[1]"
            fzjg_tree = etree.HTML(html)
            fenye_table = fzjg_tree.xpath(fenye_xpath)
            if not fenye_table:
                return []
            fenye_table = fenye_table[0]
            pageno = self.parse_pageno(fenye_table)
            if pageno <= 1:
                return []
            return range(2, pageno + 1)
        module.appendOutput(name="fzjg_page_range",type=OutputType.FUNCTION,function=getfzjgPageno,show_up=OutputParameterShowUpType.OPTIONAL)
        def bypass_fun_fzjg(fzjg_page_range=None):
            if not fzjg_page_range:
                return True
            else:
                return False
        module.appendBypass(Bypass(condition_fuc=bypass_fun_fzjg,module_id="fzjg_pages"))

    # 股东信息翻页
    def initShareholderInfoPage(self, module_super):
        iterator = Iterator("gdxx_page_range", "pno")
        module = Module(None, u"第五步_获取股东信息_开始翻页数据", iterator)
        module.module_id = "gdxx_pages"
        module_super.appendSubModule(module, True)

        sub_module = Module(self.visitGdxx, u"第五步_获取股东信息翻页数据")
        sub_module.appendUrl(lambda id, pno: "http://aic.hainan.gov.cn:1888/QueryInvList.jspx?mainId=%s&pno=%s" % (id, pno))
        sub_module.appendHeaders(lambda company_url:
            {
                'Host': "aic.hainan.gov.cn:1888",
                'Connection': 'keep-alive',
                'Cache-Control': 'max-age=0',
                'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:39.0) Gecko/20100101 Firefox/39.0",
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Referer': "http://aic.hainan.gov.cn:1888" + company_url,
                'Accept-Encoding': 'gzip, deflate',
                "Accept-Language": "zh-CN,zh;q=0.8"
            }
        )
        module.addSleep(Sleep(2))
        module.appendSubModule(sub_module)

    # 股东信息详情
    def initShareholderInfoDetail(self, module_super):
        iterator = Iterator("gdxx_list", "gdxx_rcd")
        module = Module(None, u"开始获取股东详情", iterator)
        module_super.appendSubModule(module, True)

        sub_module = Module(self.visitGdxq, u"获取股东详情信息")
        def getGdxqUrl(gdxx_rcd):
            for key in gdxx_rcd:
                if 'onclick' in gdxx_rcd[key]:
                    onclick_dict = eval(gdxx_rcd[key]) if isinstance(gdxx_rcd[key], basestring) else gdxx_rcd[key]
                    onclick = onclick_dict["onclick"]
                    xq_link = onclick[onclick.find('(')+1:onclick.find(')')].replace("'", "")
                    xq_url = "http://aic.hainan.gov.cn:1888" + xq_link
                    return xq_url
            return None
        sub_module.appendUrl(getGdxqUrl)
        sub_module.addSleep(Sleep(2))
        module.appendSubModule(sub_module)

    # 变更信息翻页
    def initChangeInfoPage(self, module_super):
        iterator = Iterator("bgxx_page_range", "pno")
        module = Module(None, u"第六步_获取变更信息_开始翻页数据", iterator)
        module.module_id = "bgxx_pages"
        module_super.appendSubModule(module, True)

        sub_module = Module(self.visitBgxx, u"第六步_获取变更信息翻页数据")
        sub_module.appendUrl(lambda id, pno: "http://aic.hainan.gov.cn:1888/QueryAltList.jspx?mainId=%s&pno=%s" % (id, pno))
        sub_module.appendHeaders(lambda company_url:
            {
                'Host': "aic.hainan.gov.cn:1888",
                'Connection': 'keep-alive',
                'Accept': '*/*',
                'Referer': "http://aic.hainan.gov.cn:1888" + company_url,
                'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:39.0) Gecko/20100101 Firefox/39.0",
                'Accept-Encoding': 'gzip, deflate, sdch',
                "Accept-Language": "zh-CN,zh;q=0.8"
            }
        )
        module.addSleep(Sleep(2))
        module.appendSubModule(sub_module)

    # 备案信息翻页
    def initArchiveInfoPage(self, module_super):
        iterator = Iterator("baxx_page_range", "pno")
        module = Module(None, u"第七步_获取备案信息_开始翻页数据", iterator)
        module.module_id = "baxx_pages"
        module_super.appendSubModule(module, True)

        sub_module = Module(self.visitBaxx, u"第七步_获取备案信息翻页数据")
        sub_module.appendUrl(lambda id, pno: "http://aic.hainan.gov.cn:1888/QueryMemList.jspx?mainId=%s&pno=%s" % (id, pno))
        # sub_module.appendUrl(lambda id, pno: "http://aic.hainan.gov.cn:1888/QueryCountryList.jspx?mainId=%s&pno=%s" % (id, pno))
        sub_module.appendHeaders(lambda company_url:
            {
                'Host': "aic.hainan.gov.cn:1888",
                'Connection': 'keep-alive',
                'Accept': '*/*',
                'Referer': "http://aic.hainan.gov.cn:1888" + company_url,
                'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:39.0) Gecko/20100101 Firefox/39.0",
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'zh-CN,zh;q=0.8'
            }
        )
        module.addSleep(Sleep(2))
        module.appendSubModule(sub_module)

    # 备案信息翻页-第二中情况
    # def initArchiveInfoTwoPage(self, module_super):
    #     iterator = Iterator("baxx_page_range", "pno")
    #     module = Module(None, u"第七步_获取备案信息_开始翻页数据", iterator)
    #     module.module_id = "baxx_pages_two"
    #     module_super.appendSubModule(module, True)
    #
    #     sub_module = Module(self.visitBaxx, u"第七步_获取备案信息翻页数据")
    #     # sub_module.appendUrl(lambda id, pno: "http://aic.hainan.gov.cn:1888/QueryMemList.jspx?mainId=%s&pno=%s" % (id, pno))
    #     sub_module.appendUrl(lambda id, pno: "http://aic.hainan.gov.cn:1888/QueryCountryList.jspx?mainId=%s&pno=%s" % (id, pno))
    #     sub_module.appendHeaders(lambda company_url:
    #                             {
    #                                 'Host': "aic.hainan.gov.cn:1888",
    #                                 'Connection': 'keep-alive',
    #                                 'Accept': '*/*',
    #                                 'Referer': "http://aic.hainan.gov.cn:1888" + company_url,
    #                                 'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:39.0) Gecko/20100101 Firefox/39.0",
    #                                 'Accept-Encoding': 'gzip, deflate',
    #                                 'Accept-Language': 'zh-CN,zh;q=0.8'
    #                             }
    #                         )
    #     module.addSleep(Sleep(2))
    #     module.appendSubModule(sub_module)

    # 分支机构翻页
    def initBranchInfoPage(self, module_super):
        iterator = Iterator("fzjg_page_range", "pno")
        module = Module(None, u"第八步_获取分支机构_开始翻页数据", iterator)
        module.module_id = "fzjg_pages"
        module_super.appendSubModule(module, True)

        sub_module = Module(self.visitFzjg, u"第八步_获取分支机构翻页数据")
        sub_module.appendUrl(lambda id, pno: "http://aic.hainan.gov.cn:1888/QueryChildList.jspx?mainId=%s&pno=%s" %(id, pno))
        sub_module.appendHeaders(lambda company_url:
            {
                'Host': "aic.hainan.gov.cn:1888",
                'Connection': 'keep-alive',
                'Accept': '*/*',
                'Referer': "http://aic.hainan.gov.cn:1888" + company_url,
                'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:39.0) Gecko/20100101 Firefox/39.0",
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'zh-CN,zh;q=0.8'
            }
        )
        module.addSleep(Sleep(2))
        module.appendSubModule(sub_module)



    def parse_pageno(self, table_page):
        """
            解析总页数
            将href内容 反序，取第一次出现的数字，即是总页数。样例如下：
            1 <a href='javascript:slipFive("child",5,8,"next");'><span>&gt;&gt;</span></a>
            2 <a id="achild5" href='javascript:goPage3("child",5);' style="text-decoration: underline;">
                <span id="spanchild5">5</span>
            </a>
            样例1和2中 最后出现的数字即可认为是总页数
        """
        try:
            last_a = table_page.xpath(".//a[last()]")[0]
            href = last_a.attrib['href']
            g = re.findall(r'\d+', href)
            if g:
                return int(g[-1])
            return 1
        except Exception as e:
            return 1


    # 海南年报数据处理
    def initAnnualReportList(self, module_super):
        module = Module(self.visitQynbList, u"第九步_获取企业年报列表")
        module.appendUrl(lambda id: "http://aic.hainan.gov.cn:1888/enterprisePublicity.jspx?id=%s" % id)
        module.appendHeaders(
            lambda company_url:
            {
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                "Accept-Encoding": "gzip, deflate",
                "Accept-Language": "zh-CN,zh;q=0.8",
                "Cache-Control": "max-age=0",
                "Connection": "keep-alive",
                "Host": "aic.hainan.gov.cn:1888",
                "Referer": company_url,
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36"
            }
        )
        module.appendOutput(name="nb_list", xpath=".//*[@id='qiyenianbao']/table//td/a", type=OutputType.LIST, show_up=OutputParameterShowUpType.OPTIONAL)
        module.addSleep(Sleep(2))
        module_super.appendSubModule(module)

    def initAnnualReport(self, module_super):
        iterator = Iterator(seeds="nb_list",param_name="nb")
        module=Module(None, u"遍历企业年报列表获取Url",iterator)
        module_super.appendSubModule(module)

    #     self.initAnnualReportInfo(module)
    #
    # def initAnnualReportInfo(self, module_super):
    #     module = Module(self.visitQynb, u"获取企业年报详细信息")

        sub_module = Module(self.visitQynb, u"获取企业年报详细信息")
        def annual_convert(nb):
            con_dict = dict()
            con_dict["nb_url"] = "http://aic.hainan.gov.cn:1888%s" % ''.join(nb.xpath("@href"))
            con_dict["nb_name"] = ''.join(nb.xpath("text()")).replace(u"年度报告", "")
            return con_dict
        sub_module.appendInput(InputType.FUNCTION, input_value=annual_convert)
        sub_module.appendUrl("nb_url")
        sub_module.appendHeaders(
            lambda company_url:
            {
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                "Accept-Encoding": "gzip, deflate",
                "Accept-Language": "zh-CN,zh;q=0.8",
                "Cache-Control": "max-age=0",
                "Connection": "keep-alive",
                "Host": "aic.hainan.gov.cn:1888",
                "Referer": company_url,
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36"
            }
        )
        sub_module.addSleep(Sleep(2))
        module.appendSubModule(sub_module)

    def initResultCollect(self, module_super):
        module = Module(self.resultCollect, u"结果收集")
        module_super.appendSubModule(module)





