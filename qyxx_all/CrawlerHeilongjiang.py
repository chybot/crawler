# -*- coding: utf-8 -*-
# Created by John on 2016/6/21.

import sys
import random
import re
import time
import PyV8
from CrawlerBase import CrawlerBase
from lxml import etree
from ModuleManager import Module, Event, Iterator, Sleep, ModuleInput, InputType
from util.crawler_util import CrawlerRunMode, OutputType, EventType, OutputParameterShowUpType
from CommonLib.WebContent import WebAccessType, SeedAccessType
from CommonLib.md5util import getMd5WithString
from CommonLib import dataretrieve
reload(sys)


class CrawlerHeilongjiang(CrawlerBase):
    def __init__(self, pinyin, callbackFromOuterControl):
        config_dict = dict()
        config_dict[CrawlerRunMode.COMPANY_KEY] = [self.precheckCmpyKey, self.initConfigValidateCode, self.checkValidateCode,
                                                   self.getCmpnySereachList, self.fetchCompanyInfo]
        config_dict[CrawlerRunMode.COMPANY_URL] = [self.getCompanyInfo, self.fetchStockholderDetail, self.fetchStockholderInfo,
                                                   self.fetchChangeInfo, self.fetchRecordInfo, self.fetchBranchInfo,
                                                   self.fetchPunishInfo, self.getAnnalsList, self.getAnnalsInfo,
                                                   self.initResultCollect]

        check_dict = dict()
        check_dict['html_check_dict'] = {'过于频繁': WebAccessType.TOO_OFTEN, '非正常访问': WebAccessType.ACCESS_VIOLATION}
        CrawlerBase.__init__(self, pinyin, config_dict, check_dict, callbackFromOuterControl)

        # 覆写父类该set集, 专门为黑龙江所用
        self.non_company_set = {"您搜索的条件无查询结果"}
        pass

    def precheckCmpyKey(self):
        module = Module(None, u"查询条件检查")

        def checkCmpyKey(company_key):
            if len(company_key) < 2 or len(company_key) > 60:
                self.holder.logging.warning(u"查询条件长度不能小于2个字符且不能大于60个字符!")
                return False
            if filter(lambda x: company_key.find(x) > 0, [",", "'", '"', "<", ">", ";", "_"]):
                return False
            company_key = company_key.replace(u"（", "").replace(u"）", "")
            if not re.match(u"^(\w|[\u4E00-\u9FA5])*$", company_key):
                return False
            return True

        module.addEvent(Event(EventType.ASSERT_FAILED, retry_times=2, assert_function=checkCmpyKey))

        self.module_manager.appendSubModule(module)

    def initConfigValidateCode(self):
        module = Module(self.visitValidateCode, u"获取验证码")
        module.module_id = "init_validate_code"

        module.appendUrl("http://gsxt.hljaic.gov.cn/validateCode.jspx?type=0&id=" + str(random.random()))
        module.appendHeaders({
            "Host" : "gsxt.hljaic.gov.cn",
            "User-Agent" : "Mozilla/5.0 (Windows NT 6.1; rv:37.0) Gecko/20100101 Firefox/37.0",
            "Accept" : "image/png,image/*;q=0.8,*/*;q=0.5",
            "Accept-Language" : "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
            "Accept-Encoding" : "gzip, deflate",
            "Referer" : "http://gsxt.hljaic.gov.cn/search.jspx"
            })
        module.addSleep(Sleep(3))
        module.appendEncoding("utf-8")

        def checkValidatecode(yzm):
            if not yzm:
                self.holder.logging.warning(u"获取验证码失败")
                return False
            return True

        module.addEvent(Event(EventType.ASSERT_FAILED, retry_times=100, assert_function=checkValidatecode))

        self.module_manager.appendSubModule(module, True)

    def checkValidateCode(self):
        module = Module(self.getJson, u"校验验证码")
        module.module_id = "check_validate_code"

        module.appendUrl('http://gsxt.hljaic.gov.cn/checkCheckNo.jspx')
        module.appendHeaders({
            "Host" : "gsxt.hljaic.gov.cn",
            "User-Agent" : "Mozilla/5.0 (Windows NT 6.1; rv:37.0) Gecko/20100101 Firefox/37.0",
            "Accept" : "image/png,image/*;q=0.8,*/*;q=0.5",
            "Accept-Language" : "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
            "Accept-Encoding" : "gzip, deflate",
            "Referer" : "http://gsxt.hljaic.gov.cn/search.jspx"
            })
        module.appendWebMethod("post")
        module.appendEncoding("utf-8")
        module.appendPostData(lambda yzm: {"checkNo": yzm})

        def checkValidatecode(json = None):
            if not json or "{success:true}" not in json:
                self.holder.logging.warning(u"验证码校验失败, 需要重新获取验证码")
                return False
            else:
                return True

        module.addEvent(Event(EventType.ASSERT_FAILED, retry_times=100, assert_function=checkValidatecode, redo_module="init_validate_code"))
        module.addEvent(Event(EventType.EXCEPTION_OCCURED, retry_times=100, redo_module="init_validate_code"))

        self.module_manager.appendSubModule(module, True)

    def getCmpnySereachList(self):
        module = Module(self.visitSearchList, u"抓取公司列表")
        module.module_id = "get_search_list"

        module.appendUrl("http://gsxt.hljaic.gov.cn/searchList.jspx")
        module.appendHeaders({
            "Host": "gsxt.hljaic.gov.cn",
            "User-Agent" : "Mozilla/5.0 (Windows NT 6.1; rv:37.0) Gecko/20100101 Firefox/37.0",
            "Accept" : "text/plain, */*; q=0.01",
            "Accept-Language" : "zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3",
            "Accept-Encoding" : "gzip, deflate",
            "Content-Type" : "application/x-www-form-urlencoded",
            "Referer" : "http://gsxt.hljaic.gov.cn/search.jspx"
        })
        module.appendWebMethod("post")
        module.appendEncoding("utf-8")
        module.appendPostData(lambda yzm, company_key: {"checkNo": yzm, "entName": company_key})
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
        self.fetchStockholderDetail(module)
        self.fetchStockholderInfo(module)
        self.fetchChangeInfo(module)
        self.fetchRecordInfo(module)
        self.fetchBranchInfo(module)
        self.fetchPunishInfo(module)
        self.getAnnalsList(module)
        self.getAnnalsInfo(module)
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
        """
        抓取公司信息, 并获取各个模块的翻页总页码
        :param module_super:
        :output: company_id, gdxx_page_range, bgxx_page_range, baxx_page_range, fzjg_page_range, xzcf_page_range
        """
        module = Module(self.visitJbxx, u"抓取公司信息")
        module.module_id = "get_cmpny_info"

        def getURL(company_url):
            if "http" in company_url:
                return company_url
            else:
                return u"http://gsxt.hljaic.gov.cn" + company_url
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

        def getCompanyID(company_url):
            query_dict = dict()

            try:
                query_dict["company_id"] = re.search(r'\?id\=([\s\S]*)', company_url).group().split("=")[1]
            except Exception as e:
                self.holder.logging.warning(u"获取company_id失败: %s" % e)
                query_dict = dict()

            return query_dict
        module.appendOutput(name="gdxq_list", xpath=".//*[@id='invDiv']/table/tr/td/a/@onclick", type=OutputType.LIST,
                            show_up=OutputParameterShowUpType.OPTIONAL)
        module.appendOutput(type=OutputType.FUNCTION, function=getCompanyID)

        # 股东信息页码获取
        def getGdxxPageno(html):
            try:
                fenye_xpath = ".//div[@id='invDiv']/following-sibling::table[1]|.//div[@id='invPagination']/table[1]"
                gdxx_tree = etree.HTML(html)
                fenye_table = gdxx_tree.xpath(fenye_xpath)
                if not fenye_table:
                    return []
                fenye_table = fenye_table[0]
                pageno = self.parse_total_pg(fenye_table)
                if pageno <= 1:
                    return []
                self.holder.logging.info(u"------------------股东信息页码: " + str(pageno) + u"---------------------")
                return range(2, int(pageno) + 1)
            except Exception as e:
                self.holder.logging.warning(u"获取股东信息页码失败: %s" % e)
                return []
        module.appendOutput(name="gdxx_page_range", type=OutputType.FUNCTION, function=getGdxxPageno,
                            show_up=OutputParameterShowUpType.OPTIONAL)

        # 变更信息页码获取
        def getBgxxPageno(html):
            try:
                fenye_xpath = ".//div[@id='altDiv']/following-sibling::table[1]|.//div[@id='altPagination']/table[1]"
                bgxx_tree = etree.HTML(html)
                fenye_table = bgxx_tree.xpath(fenye_xpath)
                if not fenye_table:
                    return []
                fenye_table = fenye_table[0]
                pageno = self.parse_total_pg(fenye_table)
                if pageno <= 1:
                    return []
                self.holder.logging.info(u"------------------变更信息页码: " + str(pageno) + u"---------------------")
                return range(2, int(pageno) + 1)
            except Exception as e:
                self.holder.logging.warning(u"获取变更信息页码失败: %s" % e)
                return []
        module.appendOutput(name="bgxx_page_range", type=OutputType.FUNCTION, function=getBgxxPageno,
                            show_up=OutputParameterShowUpType.OPTIONAL)

        # 备案信息页码获取
        def getBaxxPageno(html):
            try:
                fenye_xpath = ".//div[@id='memDiv']/following-sibling::table[1]|.//*[@id='beian']/table[2]"
                baxx_tree = etree.HTML(html)
                fenye_table = baxx_tree.xpath(fenye_xpath)
                if not fenye_table:
                    return []
                fenye_table = fenye_table[0]
                pageno = self.parse_total_pg(fenye_table)
                if pageno <= 1:
                    return []
                self.holder.logging.info(u"------------------备案信息页码: " + str(pageno) + u"---------------------")
                return range(2, int(pageno) + 1)
            except Exception as e:
                self.holder.logging.warning(u"获取备案信息页码失败: %s" % e)
                return []
        module.appendOutput(name="baxx_page_range", type=OutputType.FUNCTION, function=getBaxxPageno,
                            show_up=OutputParameterShowUpType.OPTIONAL)

        # 分支机构页码获取
        def getFzjgPageno(html):
            try:
                fenye_xpath = ".//div[@id='childPagination']/table[1]|.//div[@id='childDiv']/following-sibling::table[1]"
                fzfg_tree = etree.HTML(html)
                fenye_table = fzfg_tree.xpath(fenye_xpath)
                if not fenye_table:
                    return []
                fenye_table = fenye_table[0]
                pageno = self.parse_total_pg(fenye_table)
                if pageno <= 1:
                    return []
                self.holder.logging.info(u"------------------分支机构信息页码：" + str(pageno) + u"---------------------")
                return range(2, int(pageno) + 1)
            except Exception as e:
                self.holder.logging.warning(u"获取分支机构页码失败: %s" % e)
                return []
        module.appendOutput(name="fzjg_page_range", type=OutputType.FUNCTION, function=getFzjgPageno,
                            show_up=OutputParameterShowUpType.OPTIONAL)

        # 行政处罚页码获取
        def getXzcfPageno(html):
            try:
                fenye_xpath = ".//*[@id='xingzhengchufa']/table[2]"
                xzcf_tree = etree.HTML(html)
                fenye_table = xzcf_tree.xpath(fenye_xpath)
                if not fenye_table:
                    return []
                fenye_table = fenye_table[0]
                pageno = self.parse_total_pg(fenye_table)
                if pageno <= 1:
                    return []
                self.holder.logging.info(u"------------------行政处罚信息页码：" + str(pageno) + u"---------------------")
                return range(2, int(pageno) + 1)
            except Exception as e:
                self.holder.logging.warning(u"获取行政处罚页码失败: %s" % e)
                return []
        module.appendOutput(name="xzcf_page_range", type=OutputType.FUNCTION, function=getXzcfPageno,
                            show_up=OutputParameterShowUpType.OPTIONAL)

        def checkCompnayID(company_id = None):
            if not company_id:
                self.holder.logging.warning(u"company_id无效")
                return False
            return True

        module.addEvent(Event(EventType.ASSERT_FAILED, retry_times=10, assert_function=checkCompnayID))
        module.addEvent(Event(EventType.EXCEPTION_OCCURED, retry_times=100, redo_module="get_cmpny_info"))
        module.addEvent(Event(EventType.OUTPUT_NOT_SATISFIED, retry_times=100, redo_module="get_cmpny_info"))

        module_super.appendSubModule(module, True)

    def fetchStockholderDetail(self, module_super):
        """
        遍历股东详情
        :param module_super:
        :return:
        """
        iterator = Iterator(seeds="gdxq_list", param_name="gdxq")
        module = Module(iterator=iterator, name=u"遍历股东详情")
        module_super.appendSubModule(module)

        sub_module = Module(self.visitGdxq, u"抓取股东详情")

        def getURL(gdxq):
            if gdxq:
                gdxq_text = re.findall(r"(?<=\(').+?(?='\))", gdxq)
                if gdxq_text:
                    return u"http://gsxt.hljaic.gov.cn" + gdxq_text[0]
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

        sub_module.addEvent(Event(EventType.EXCEPTION_OCCURED, retry_times=100))

        module.appendSubModule(sub_module)

    def fetchStockholderInfo(self, module_super):
        """
        遍历股东信息分页, 并再次迭代股东详情列表
        :param module_super:
        :return:
        """
        iterator = Iterator(seeds="gdxx_page_range", param_name="pno")
        module = Module(iterator=iterator, name=u"遍历股东翻页")
        module.module_id = "gdxx_pages"
        module_super.appendSubModule(module)

        self.getStockholderInfo(module)
        self.fetchStockholderDetail(module)

    def getStockholderInfo(self, module_super):
        """
        抓取翻页的股东信息
        :param module_super:
        :return:
        """
        module = Module(self.visitGdxx, u"抓取股东信息")
        module.module_id = "get_stockholder_info"

        module.appendUrl(lambda pno, company_id: "http://gsxt.hljaic.gov.cn/QueryInvList.jspx?pno=%s&mainId=%s" % (pno, company_id))
        module.appendHeaders(lambda company_id: {
            "Host" : "gsxt.hljaic.gov.cn",
            "User-Agent" : "Mozilla/5.0 (Windows NT 6.1; rv:37.0) Gecko/20100101 Firefox/37.0",
            "Accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language" : "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
            "Accept-Encoding" : "gzip, deflate",
            'Referer': 'http://gsxt.hljaic.gov.cn/businessPublicity.jspx?id=' + str(company_id),
        })
        module.appendEncoding("utf-8")
        module.addSleep(Sleep(3))

        def getGdxqList(html):
            query_dict = dict()
            try:
                tree = etree.HTML(html)
                query_dict["gdxq_list"] = tree.xpath(".//*[@class='detailsList']/tr/td/a/@onclick")
            except Exception as e:
                self.holder.logging.warning(u"获取股东翻页中的股东详情列表失败: %s" % e)
                query_dict = dict()
            return query_dict

        module.appendOutput(type=OutputType.FUNCTION, function=getGdxqList, show_up=OutputParameterShowUpType.OPTIONAL)
        module.addEvent(Event(EventType.EXCEPTION_OCCURED, retry_times=50))

        module_super.appendSubModule(module, True)

    def fetchChangeInfo(self, module_super):
        """
        遍历变更信息
        :param module_super:
        :return:
        """
        iterator = Iterator(seeds="bgxx_page_range", param_name="pno")
        module = Module(iterator=iterator, name=u"遍历变更翻页")
        module_super.appendSubModule(module)

        sub_module = Module(self.visitBgxx, u"抓取变更信息")
        sub_module.appendUrl(lambda pno, company_id: "http://gsxt.hljaic.gov.cn/QueryAltList.jspx?pno=%s&mainId=%s" % (pno, company_id))
        sub_module.appendHeaders(lambda company_id: {
            "Host" : "gsxt.hljaic.gov.cn",
            "User-Agent" : "Mozilla/5.0 (Windows NT 6.1; rv:37.0) Gecko/20100101 Firefox/37.0",
            "Accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language" : "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
            "Accept-Encoding" : "gzip, deflate",
            'Referer': 'http://gsxt.hljaic.gov.cn/businessPublicity.jspx?id=' + str(company_id),
        })
        sub_module.appendEncoding("utf-8")
        sub_module.addSleep(Sleep(3))

        sub_module.addEvent(Event(EventType.EXCEPTION_OCCURED, retry_times=50))

        module.appendSubModule(sub_module)

    def fetchRecordInfo(self, module_super):
        """
        遍历备案信息
        :param module_super:
        :return:
        """
        iterator = Iterator(seeds="baxx_page_range", param_name="pno")
        module = Module(iterator=iterator, name=u"遍历备案信息翻页")
        module_super.appendSubModule(module)

        sub_module = Module(self.visitBaxx, u"抓取备案信息")
        sub_module.appendUrl(lambda pno, company_id: "http://gsxt.hljaic.gov.cn/QueryMemList.jspx?pno=%s&mainId=%s" % (pno, company_id))
        sub_module.appendHeaders(lambda company_id: {
            "Host" : "gsxt.hljaic.gov.cn",
            "User-Agent" : "Mozilla/5.0 (Windows NT 6.1; rv:37.0) Gecko/20100101 Firefox/37.0",
            "Accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language" : "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
            "Accept-Encoding" : "gzip, deflate",
            'Referer': 'http://gsxt.hljaic.gov.cn/businessPublicity.jspx?id=' + str(company_id),
        })
        sub_module.appendEncoding("utf-8")
        sub_module.addSleep(Sleep(3))

        sub_module.addEvent(Event(EventType.EXCEPTION_OCCURED, retry_times=50))

        module.appendSubModule(sub_module)

    def fetchBranchInfo(self, module_super):
        """
        遍历分支结构信息
        :param module_super:
        :return:
        """
        iterator = Iterator(seeds="fzjg_page_range", param_name="pno")
        module = Module(iterator=iterator, name=u"遍历分支机构翻页")
        module_super.appendSubModule(module)

        sub_module = Module(self.visitFzjg, u"抓取分支机构信息")
        sub_module.appendUrl(lambda pno, company_id: "http://gsxt.hljaic.gov.cn/QueryChildList.jspx?pno=%s&mainId=%s" % (pno, company_id))
        sub_module.appendHeaders(lambda company_id: {
            "Host" : "gsxt.hljaic.gov.cn",
            "User-Agent" : "Mozilla/5.0 (Windows NT 6.1; rv:37.0) Gecko/20100101 Firefox/37.0",
            "Accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language" : "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
            "Accept-Encoding" : "gzip, deflate",
            'Referer': 'http://gsxt.hljaic.gov.cn/businessPublicity.jspx?id=' + str(company_id),
        })
        sub_module.appendEncoding("utf-8")
        sub_module.addSleep(Sleep(3))

        sub_module.addEvent(Event(EventType.EXCEPTION_OCCURED, retry_times=50))

        module.appendSubModule(sub_module)

    def fetchPunishInfo(self, module_super):
        """
        遍历行政处罚
        :param module_super:
        :return:
        """
        iterator = Iterator(seeds="xzcf_page_range", param_name="pno")
        module = Module(iterator=iterator, name=u"遍历行政处罚翻页")
        module_super.appendSubModule(module)

        sub_module = Module(self.visitXzcf, u"抓取行政处罚信息")
        sub_module.appendUrl(lambda pno, company_id: "http://gsxt.hljaic.gov.cn/QueryPunList.jspx?pno=%s&mainId=%s&ran=%s" % (pno, company_id, str(random.random())))
        sub_module.appendHeaders(lambda company_id: {
            "Host" : "gsxt.hljaic.gov.cn",
            "User-Agent" : "Mozilla/5.0 (Windows NT 6.1; rv:37.0) Gecko/20100101 Firefox/37.0",
            "Accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language" : "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
            "Accept-Encoding" : "gzip, deflate",
            'Referer': 'http://gsxt.hljaic.gov.cn/businessPublicity.jspx?id=' + str(company_id),
        })
        sub_module.appendEncoding("utf-8")
        sub_module.addSleep(Sleep(3))

        sub_module.addEvent(Event(EventType.EXCEPTION_OCCURED, retry_times=50))

        module.appendSubModule(sub_module)

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

    def parse_total_pg(self, table):
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
            last_a = table.xpath(".//a[last()]")[0]
            href = last_a.attrib['href']
            g = re.findall(r'\d+', href)
            if g:
                return int(g[-1])
            return 1
        except Exception as e:
            self.holder.logging.warning(u'解析分页出错，可能页面结构已改变%s' % e)
            return 1