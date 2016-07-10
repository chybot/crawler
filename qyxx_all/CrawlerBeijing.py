# -*- coding: utf-8 -*-
# Created by David on 2016/5/4.

import sys
import random
import time
import urlparse
from CrawlerBase import CrawlerBase
from lxml import etree
from ModuleManager import Module,Event,Iterator,Sleep,Bypass
from util.crawler_util import CrawlerRunMode, InputType, OutputType, EventType, OutputParameterShowUpType
from util.common_util import substring
from CommonLib.WebContent import WebAccessType, SeedAccessType
reload(sys)

class CrawlerBeijing(CrawlerBase):
    def __init__(self, pinyin, callbackFromOuterControl):
        config_dict = dict()
        config_dict[CrawlerRunMode.COMPANY_KEY] = [self.initConfigHomePage, self.initConfigValidateCode, self.initConfigSearchList, self.initConfigCompanyInfo]

        check_dict = dict()
        check_dict['html_check_dict'] = {'非正常访问':WebAccessType.ACCESS_VIOLATION, '过于频繁':WebAccessType.TOO_OFTEN}
        CrawlerBase.__init__(self, pinyin, config_dict, check_dict, callbackFromOuterControl)
        # 临时打开其他解析开关，便于观察抓取情况
        self.parse_on = True
        pass

    def initConfigHomePage(self):
        module = Module(self.visitHomePage, u"首页")
        module.module_id = "module_home_page"
        module.appendInput(InputType.URL, "http://qyxy.baic.gov.cn/beijing")
        module.appendInput(InputType.HEADERS, lambda ua:{
                                                        "Host": "qyxy.baic.gov.cn",
                                                        "User-Agent": ua,
                                                        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                                                        "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
                                                        "Accept-Encoding": "gzip, deflate",
                                                        "Connection": "keep-alive",
                                                        })
        module.appendOutput("currentTimeMillis", ".//*[@id='currentTimeMillis']/@value")
        module.appendOutput("credit_ticket", ".//*[@id='credit_ticket']/@value")
        module.appendMiddleValueMonitor("currentTimeMillis", "credit_ticket")
        module.addSleep(Sleep(6))
        module.addEvent(Event(EventType.EXCEPTION_OCCURED, retry_times=100))
        module.addEvent(Event(EventType.OUTPUT_NOT_SATISFIED, retry_times=100))
        self.module_manager.appendSubModule(module, True)

    def initConfigValidateCode(self):
        module = Module(self.visitValidateCode, u"验证码")
        module.appendUrl(lambda currentTimeMillis:"http://qyxy.baic.gov.cn/CheckCodeCaptcha?currentTimeMillis=%s&num=%s" % \
                            (str(currentTimeMillis), str(int(random.random() * 100000))))
        module.appendHeaders(lambda ua:{
                                        "Host": "qyxy.baic.gov.cn",
                                        "User-Agent": ua,
                                        "Accept": "image/png,image/*;q=0.8,*/*;q=0.5",
                                        "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
                                        "Accept-Encoding": "gzip, deflate",
                                        "Referer": "http://qyxy.baic.gov.cn/gjjbj/gjjQueryCreditAction!getBjQyList.dhtml",
                                        "Connection": "keep-alive"
                                                        })
        module.addEvent(Event(EventType.EXCEPTION_OCCURED, retry_times=100, redo_module="module_home_page"))
        module.addSleep(Sleep(6))
        self.module_manager.appendSubModule(module)

    def initFilterYzm(self):
        module = Module(self.getWebHtml,u"过滤验证码")
        module.appendUrl('http://qyxy.baic.gov.cn/gjjbj/gjjQueryCreditAction!checkCode.dhtml')
        module.appendHeaders(lambda ua:{
                                        "Host": "qyxy.baic.gov.cn",
                                        "User-Agent": ua,
                                        "Accept": "*/*",
                                        "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
                                        "Accept-Encoding": "gzip, deflate",
                                        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                                        "X-Requested-With": "XMLHttpRequest",
                                        "Referer": "http://qyxy.baic.gov.cn/beijing",
                                        "Connection": "keep-alive",
                                        "Pragma": "no-cache",
                                        "Cache-Control": "no-cache"
                                    })
        module.appendWebMethod('post')
        module.appendPostData(lambda currentTimeMillis, credit_ticket, yzm, company_key:
                                {
                                    "credit_ticket": credit_ticket,
                                    "currentTimeMillis": currentTimeMillis,
                                    "checkcode": yzm,
                                    "keyword": company_key
                                })
        def assert_fun(html):
            if html.strip()=='success':
                return True
            return False
        module.addEvent(Event(EventType.ASSERT_FAILED, retry_times=100,
                          assert_function=assert_fun,redo_module="module_home_page"))
        module.addSleep(Sleep(6))
        module.appendMiddleValueMonitor("html")

        self.module_manager.appendSubModule(module)
    def initConfigSearchList(self):
        module = Module(self.visitSearchList, u"搜索列表")
        module.appendUrl("http://qyxy.baic.gov.cn/gjjbj/gjjQueryCreditAction!getBjQyList.dhtml")
        module.appendHeaders(lambda ua:{
                                        "Host": "qyxy.baic.gov.cn",
                                        "User-Agent": ua,
                                        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                                        "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
                                        "Accept-Encoding": "gzip, deflate",
                                        "Referer": "http://qyxy.baic.gov.cn/beijing",
                                        "Connection": "keep-alive",
                                        "Content-Type": "application/x-www-form-urlencoded",
                                        "Origin": "http://qyxy.baic.gov.cn",
                                        "Upgrade-Insecure-Requests": "1"
                                    })
        module.appendWebMethod("post")
        module.appendPostData(lambda currentTimeMillis, credit_ticket, yzm, company_key:
                                {
                                    "credit_ticket": credit_ticket,
                                    "currentTimeMillis": currentTimeMillis,
                                    "checkcode": yzm,
                                    "keyword": company_key
                                })
        module.appendOutput("search_list", "//*[@class='list']/ul/li/a/@onclick", OutputType.LIST)
        module.addEvent(Event(EventType.EXCEPTION_OCCURED, retry_times=100, redo_module="module_home_page"))
        module.addEvent(Event(EventType.OUTPUT_NOT_SATISFIED, retry_times=100, redo_module="module_home_page"))
        module.addEvent(Event(EventType.ASSERT_FAILED, retry_times=0, assert_function=lambda:False if self.report.access_type == SeedAccessType.NON_COMPANY else True))
        module.appendMiddleValueMonitor("search_list")
        module.addSleep(Sleep(6))
        self.module_manager.appendSubModule(module)

    def initConfigCompanyInfo(self):
        iterator = Iterator("search_list", "com")
        module = Module(None, u"获取公司信息", iterator)
        self.module_manager.appendSubModule(module, True)

        self.initConfigBaseInfo(module)

        self.initConfigShareHolderInfo(module)
        self.initShareHolderInfoPage(module)
        self.initShareHolderDetail(module)

        self.initConfigChangeInfo(module)
        self.initChangeInfoPage(module)

        self.initArchiveInfo(module)
        self.initArchivePage(module)
        self.initBranchInfo(module)
        self.initBranchPage(module)
        self.initPenaltyInfo(module)

        self.initAnnualReportList(module)
        self.initAnnualReport(module)

        self.initResultCollect(module)

    def initConfigBaseInfo(self, module_super):
        module = Module(self.visitJbxx, u"基本信息")
        module.appendInput(InputType.FUNCTION, lambda com: dict(zip(['search_company', 'entId', 'entNo', 'credit_ticket'], map(lambda x: x.strip(),
                                                          com[com.find("(") + 1:com.rfind(")")].replace("'", "").split(",")))))
        jbxx_url = lambda entId, credit_ticket, entNo: "http://qyxy.baic.gov.cn/gjjbj/gjjQueryCreditAction!openEntInfo.dhtml?entId=%s&credit_ticket=%s&entNo=%s&timeStamp=%s" % \
                        (entId, credit_ticket, entNo, str(int(time.time() * 1000)))
        module.appendInput(InputType.FUNCTION, jbxx_url, "jbxx_url")
        module.appendUrl("jbxx_url")
        module.appendHeaders(lambda ua:{
                            "Host": "qyxy.baic.gov.cn",
                            "User-Agent": ua,
                            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                            "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
                            "Accept-Encoding": "gzip, deflate",
                            "Referer": "http://qyxy.baic.gov.cn/gjjbj/gjjQueryCreditAction!getBjQyList.dhtml",
                            "Connection": "keep-alive"
                        })
        module_super.appendSubModule(module, True)

    def initConfigShareHolderInfo(self, module_super):
        module = Module(self.visitGdxx, u"股东信息")
        module.appendUrl(lambda entId:"http://qyxy.baic.gov.cn/gjjbj/gjjQueryCreditAction!tzrFrame.dhtml?ent_id=%s&entName=&clear=true&timeStamp=%s" % \
                        (entId, str(int(time.time() * 1000))))
        module.appendHeaders(self.post_headers)
        module.appendOutput("gdxx_pages", None, OutputType.FUNCTION, self.getPageNoPrepare, OutputParameterShowUpType.OPTIONAL)
        module_super.appendSubModule(module, True)

    def initShareHolderInfoPage(self, module_super):
        iterator = Iterator("gdxx_pages", "page_no")
        module = Module(None, u"进入股东翻页", iterator)
        module_super.appendSubModule(module, True)

        sub_module = Module(self.visitGdxx, u"获取股东翻页信息")
        # sub_module.appendUrl(lambda page_no:"http://qyxy.baic.gov.cn/"+"gjjbj/"*int(page_no)+"gjjQueryCreditAction!tzrFrame.dhtml")
        sub_module.appendUrl(lambda page_no:"http://qyxy.baic.gov.cn/"+"gjjbj/"*2+"gjjQueryCreditAction!tzrFrame.dhtml")
        sub_module.appendWebMethod("post")
        sub_module.appendPostData(lambda page_no,entId:{"pageNos":int(page_no),"ent_id":entId,"fqr":"","pageNo":int(page_no)-1,"pageSize":5,"clear":""})
        sub_module.addSleep(Sleep(3))
        def logPageInfo(page_no=None):
            if page_no:
                self.holder.logging.info("----股东信息已抓取 %s 页----" % page_no)
        module.appendExtraFunction(logPageInfo)
        module.appendSubModule(sub_module)

    def initShareHolderDetail(self, module_super):
        iterator = Iterator("gdxx_list", "gdxx_rcd")
        module = Module(None, u"进入股东详情", iterator)
        module_super.appendSubModule(module, True)

        sub_module = Module(self.visitGdxq, u"获取股东详情信息")
        def getGdxqUrl(gdxx_rcd):
            for key in gdxx_rcd:
                if 'onclick' in gdxx_rcd[key]:
                    onclick_dict = eval(gdxx_rcd[key]) if isinstance(gdxx_rcd[key], basestring) else gdxx_rcd[key]
                    onclick = onclick_dict['onclick']
                    chr_id = onclick[onclick.find("'") + 1:onclick.rfind("'")]
                    xq_url = "http://qyxy.baic.gov.cn/gjjbj/gjjQueryCreditAction!touzirenInfo.dhtml?chr_id=%s&entName=&timeStamp=%s&fqr=" % (
                    chr_id, str(int(time.time() * 1000)))
                    return xq_url
            return None
        sub_module.appendUrl(getGdxqUrl)
        sub_module.addSleep(Sleep(3))
        module.appendSubModule(sub_module)

    def initConfigChangeInfo(self, module_super):
        module = Module(self.visitBgxx, u"变更信息")
        module.appendUrl(lambda entId:"http://qyxy.baic.gov.cn/gjjbj/gjjQueryCreditAction!biangengFrame.dhtml?ent_id=%s&clear=true&timeStamp=%s" % \
                        (entId, str(int(time.time() * 1000))))
        module.appendHeaders(self.post_headers)
        module.appendOutput("bgxx_pages", None, OutputType.FUNCTION, self.getPageNoPrepare, OutputParameterShowUpType.OPTIONAL)
        module_super.appendSubModule(module, True)

    def initChangeInfoPage(self, module_super):
        iterator = Iterator("bgxx_pages", "page_no")
        module = Module(None, u"进入变更信息翻页", iterator)
        module_super.appendSubModule(module)

        sub_module = Module(self.visitBgxx, u"获取变更翻页信息")
        # sub_module.appendUrl(lambda page_no:"http://qyxy.baic.gov.cn/"+"gjjbj/"*int(page_no)+"gjjQueryCreditAction!biangengFrame.dhtml")
        sub_module.appendUrl(lambda page_no:"http://qyxy.baic.gov.cn/"+"gjjbj/"*2+"gjjQueryCreditAction!biangengFrame.dhtml")
        sub_module.appendWebMethod("post")
        sub_module.appendPostData(lambda page_no,entId:{"pageNos":int(page_no),"ent_id":entId,"fqr":"","pageNo":int(page_no)-1,"pageSize":5,"clear":""})
        sub_module.addSleep(Sleep(3))
        module.appendSubModule(sub_module)

    def initArchiveInfo(self, module_super):
        module = Module(self.visitBaxx, u"获取备案信息")
        def get_baxx_url(entId, company):
            '''
            获取备案信息的url，依赖于获取到的基本信息中的“类型”
            :param entId:
            :param company:
            :return:
            '''
            url = "http://qyxy.baic.gov.cn/gjjbj/gjjQueryCreditAction!zyryFrame.dhtml?ent_id=%s&clear=true&timeStamp=%s" % \
                  (entId, str(int(time.time() * 1000)))
            if not company:
                return url
            for t_dict in company:
                if u"类型" in t_dict and t_dict[u"类型"] in [u"全民所有制", u"股份有限公司"]:
                    return "http://qyxy.baic.gov.cn/gjjbj/gjjQueryCreditAction!zgbmFrame.dhtml?ent_id=%s&clear=true&timeStamp=%s" % \
                           (entId, str(int(time.time() * 1000)))
            return url
        module.appendUrl(get_baxx_url)
        module.appendHeaders(self.post_headers)
        module.appendOutput("baxx_pages", None, OutputType.FUNCTION, self.getPageNoPrepare, OutputParameterShowUpType.OPTIONAL)
        module_super.appendSubModule(module)

    def initArchivePage(self, module_super):
        iterator = Iterator("baxx_pages", "page_no")
        module = Module(None, u"进入备案信息翻页", iterator)
        module_super.appendSubModule(module)

        sub_module = Module(self.visitBaxx, u"获取备案翻页信息")
        sub_module.appendUrl(lambda page_no: "http://qyxy.baic.gov.cn/" + "gjjbj/" * 2 + "gjjQueryCreditAction!zyryFrame.dhtml")
        sub_module.appendWebMethod("post")
        sub_module.appendPostData(
            lambda page_no, entId: {"pageNos": int(page_no), "ent_id": entId, "fqr": "", "pageNo": int(page_no) - 1,
                                    "pageSize": 10, "clear": ""})
        sub_module.addSleep(Sleep(3))
        module.appendSubModule(sub_module)

    def initBranchInfo(self, module_super):
        module = Module(self.visitFzjg, u"获取分支机构信息")
        module.appendUrl(lambda entId: "http://qyxy.baic.gov.cn/gjjbj/gjjQueryCreditAction!fzjgFrame.dhtml?ent_id=%s&clear=true&timeStamp=%s" % \
                                       (entId, str(int(time.time() * 1000))))
        module.appendHeaders(self.post_headers)
        module.appendOutput("fzjg_pages", None, OutputType.FUNCTION, self.getPageNoPrepare, OutputParameterShowUpType.OPTIONAL)
        module_super.appendSubModule(module)

    def initBranchPage(self, module_super):
        iterator = Iterator("fzjg_pages", "page_no")
        module = Module(None, u"进入分支机构翻页", iterator)
        module_super.appendSubModule(module)

        sub_module = Module(self.visitFzjg, u"获取分支机构翻页信息")
        sub_module.appendUrl(lambda page_no: "http://qyxy.baic.gov.cn/" + "gjjbj/" * 2 + "gjjQueryCreditAction!fzjgFrame.dhtml")
        sub_module.appendWebMethod("post")
        sub_module.appendPostData(
            lambda page_no, entId: {"pageNos": int(page_no), "ent_id": entId, "fqr": "", "pageNo": int(page_no) - 1,
                                    "pageSize": 5, "clear": ""})
        sub_module.addSleep(Sleep(3))
        module.appendSubModule(sub_module)

    def initPenaltyInfo(self, module_super):
        module = Module(self.visitXzcf, u"获取行政处罚信息")
        module.appendUrl(lambda entId: "http://qyxy.baic.gov.cn/gsgs/gsxzcfAction!list.dhtml?entId=%s&clear=true&timeStamp=%s" % (entId, str(int(time.time() * 1000))))
        module.appendHeaders(self.post_headers)
        module.addSleep(Sleep(3))
        module_super.appendSubModule(module)
        # 设置bypass直接跳过企业年报抓取
        module.appendBypass(Bypass(condition_fuc=self.bypassQynb, jump_to_module="module_result_collect"))

    def initAnnualReportList(self, module_super):
        module = Module(self.visitQynbList, u"获取企业年报列表")
        module.appendUrl(lambda entId: "http://qyxy.baic.gov.cn/qynb/entinfoAction!qyxx.dhtml?entid=%s&clear=true&timeStamp=%s" % (entId, str(int(time.time() * 1000))))
        module.appendHeaders(self.post_headers)
        module.appendOutput(name="nb_list", xpath=".//*[@id='qiyenianbao']/table//td/a", type=OutputType.LIST, show_up=OutputParameterShowUpType.OPTIONAL)
        module.addSleep(Sleep(3))
        module_super.appendSubModule(module)

    def initAnnualReport(self, module_super):
        iterator = Iterator(seeds="nb_list", param_name="nb")
        module = Module(None, u"遍历企业年报列表", iterator)
        # 过滤年报列表
        module.appendExtraFunction(self.filterQynbList)
        module_super.appendSubModule(module)

        self.initNbReportOne(module)
        self.initNbPart(module)

    def initNbReportOne(self, module_super):
        module = Module(self.visitQynb, u"获取企业年报信息")
        def prepare(nb):
            mv_dict = dict()
            mv_dict['nb_url'] = "http://qyxy.baic.gov.cn%s" % ''.join(nb.xpath('@href'))
            mv_dict['nb_name'] = ''.join(nb.xpath('text()')).replace(u'年度','')
            return mv_dict
        module.appendInput(InputType.FUNCTION, input_value=prepare)
        module.appendUrl('nb_url')
        module.appendHeaders(self.post_headers)
        module.appendOutput(name='nb_part_list', xpath='.//iframe/@src', type=OutputType.LIST, show_up=OutputParameterShowUpType.OPTIONAL)
        module.addSleep(Sleep(3))
        module_super.appendSubModule(module)

    def initNbPart(self, module_super):
        iterator = Iterator(seeds="nb_part_list", param_name="nb_part")
        module = Module(None, u"遍历各部分年报", iterator)
        module_super.appendSubModule(module)

        sub_module = Module(self.visitQynb, u"获取部分年报")
        sub_module.appendUrl(lambda nb_part: "http://qyxy.baic.gov.cn%s" % nb_part)
        sub_module.appendHeaders(self.post_headers)
        sub_module.appendOutput("qynb_pages", None, OutputType.FUNCTION, self.getPageNoPrepare, OutputParameterShowUpType.OPTIONAL)
        def cid(nb_part):
            para = urlparse.parse_qs(nb_part)
            if not para:
                return None
            return para.get('cid','')
        sub_module.appendOutput(name='cid', type=OutputType.FUNCTION, function=cid)
        sub_module.addSleep(Sleep(3))
        module.appendSubModule(sub_module)

        self.initNbPartPage(module)

    def initNbPartPage(self, module_super):
        iterator = Iterator("qynb_pages", "page_no")
        module = Module(None, u"进入部分年报翻页", iterator)
        module_super.appendSubModule(module)

        sub_module = Module(self.visitQynb, u"获取部分年报翻页信息")
        sub_module.appendUrl(lambda nb_part: "http://qyxy.baic.gov.cn%s" % nb_part)
        sub_module.appendWebMethod("post")
        sub_module.appendPostData(
            lambda page_no, cid: {"pageNos": int(page_no), "cid": cid, "pageNo": int(page_no) - 1,
                                    "pageSize": 5, "clear": ""})
        sub_module.addSleep(Sleep(3))
        module.appendSubModule(sub_module)

    def initResultCollect(self, module_super):
        module = Module(self.resultCollect, u"结果收集")
        module.module_id = "module_result_collect"
        module_super.appendSubModule(module)

    def post_headers(self, ua, jbxx_url):
        return {
            "Host": "qyxy.baic.gov.cn",
            "User-Agent": ua,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
            "Accept-Encoding": "gzip, deflate",
            "Referer": jbxx_url,
            "Connection": "keep-alive"
        }

    def getPageNoPrepare(self, html):
        gdxx_tree = etree.HTML(html)
        gd_page_list = filter(lambda x: x.strip().isdigit(),gdxx_tree.xpath(".//*[@id='pagescount']/@value"))
        pageNos = map(lambda x: int(x), gd_page_list)
        if not pageNos:
            return []
        total_page = max(pageNos)
        return range(2, total_page+1)







