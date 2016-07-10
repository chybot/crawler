# -*- coding: utf-8 -*-
# Created by David on 2016/5/4.
# Modify by wuyong  2015/6.19

import sys
import re
import time
import random
import time
import urlparse
reload(sys)
sys.path.append('./util')
from CrawlerBase import CrawlerBase
from lxml import etree
from HttpRequst.DownLoader import DownLoader
from ModuleManager import Module,Event,Iterator, Sleep
from util.crawler_util import CrawlerRunMode, InputType, OutputType, EventType, OutputParameterShowUpType
from CommonLib.WebContent import WebAccessType, SeedAccessType

class CrawlerJiangxi(CrawlerBase):
    def __init__(self, pinyin, callbackFromOuterControl):
        config_dict = dict()
        config_dict[CrawlerRunMode.COMPANY_KEY] = [self.initConfigValidateCode, self.assertValidateCode, self.initConfigSearchList, self.initConfigCompanyInfo]
        config_dict[CrawlerRunMode.COMPANY_URL] = [self.initConfigBaseInfo, self.initTopInfo, self.initConfigShareHolderInfo, self.initShareHolderInfoPage,
                                                   self.initShareHolderDetail, self.initConfigChangeInfo, self.initChangeInfoPage, self.initArchiveInfo,
                                                   self.initPenaltyInfo, self.initResultCollect]
        check_dict = dict()
        # 无有效公司列表  华意压缩
        check_dict['html_check_dict'] = {'操作过于频繁':WebAccessType.TOO_OFTEN, '非正常访问':WebAccessType.ACCESS_VIOLATION, '未经授权的访问':WebAccessType.NO_CONTENT}
        CrawlerBase.__init__(self, pinyin, config_dict, check_dict, callbackFromOuterControl)
        # 打开基本信息解析开关
        self.parse_jbxx_on = True
        # 临时打开其他解析开关，便于观察抓取情况
        self.parse_on = True
        pass

    def initConfigValidateCode(self):
        module = Module(self.visitValidateCode, u"验证码")
        module.module_id = "module_validate_code"
        module.appendUrl('http://gsxt.jxaic.gov.cn/ECPS/common/common_getJjYzmImg.pt?yzmName=searchYzm&imgWidth=180&t=' + str(random.random()))
        module.appendHeaders({'Accept-Language': 'en-US,en;q=0.8,zh-CN;q=0.6,zh-TW;q=0.4',
                              'Accept-Encoding': 'gzip, deflate, sdch', 'Connection': 'keep-alive',
                              'Accept': 'image/webp,*/*;q=0.8',
                              'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.101 Safari/537.36',
                              'Host': 'gsxt.jxaic.gov.cn', 'Referer': 'http://gsxt.jxaic.gov.cn/'})
        module.addEvent(Event(EventType.EXCEPTION_OCCURED, retry_times=100))
        self.module_manager.appendSubModule(module, True)


    def assertValidateCode(self):
        module = Module(self.getJson, u"验证码")
        module.module_id = "checkValidateCode"
        module.appendUrl('http://gsxt.jxaic.gov.cn/ECPS/home/home_homeSearchYzm.pt')
        module.appendHeaders(lambda ua : {'Accept-Language': 'en-US,en;q=0.8,zh-CN;q=0.6,zh-TW;q=0.4',
                              'Accept-Encoding': 'gzip, deflate',
                              'Connection': 'keep-alive',
                              'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
                              'Accept': 'application/json, text/javascript, */*; q=0.01',
                              'User-Agent': ua,
                              'Host': 'gsxt.jxaic.gov.cn',
                              'Referer': 'http://gsxt.jxaic.gov.cn/ECPS/'})
        module.appendWebMethod("post")
        module.appendPostData(lambda yzm, company_key: {"search": company_key, "yzm": yzm})
        def assertVaildCode(json=None):
            if self.report.access_type == SeedAccessType.NON_COMPANY:
                self.report.access_type = SeedAccessType.ERROR
            return  True if json and (json.get("msg") == 'true') else False       #json {u'msg': u'true', u'success': True}
        module.addEvent(Event(EventType.ASSERT_FAILED, retry_times=100, assert_function=assertVaildCode, redo_module="module_validate_code"))
        module.addEvent(Event(EventType.EXCEPTION_OCCURED, retry_times=100))
        module.addSleep(Sleep(3))
        self.module_manager.appendSubModule(module, True)


    def getSearchList(self, search_list_xpath=None):
        ret_args = []
        if not search_list_xpath:
            return []
        for xpath_a in search_list_xpath:
            com_list = xpath_a.xpath('./font/text()')
            ock_list = xpath_a.xpath('./@href')
            if com_list and ock_list and com_list[0].strip() and ock_list[0].strip():
                ret_args.append((ock_list[0].strip(), com_list[0].strip()))
        return ret_args

    # TODO 修改zip函数
    def initConfigSearchList(self):
        module = Module(self.visitSearchList, u"搜索列表")
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
        # module.appendOutput("url_list", './/*[@class="list"]/div/a/@href', OutputType.LIST)
        # module.appendOutput("name_list", './/*[@class="list"]/div/a/font/text()', OutputType.LIST)
        module.appendOutput("search_list_xpath", './/*[@class="list"]/div/a', OutputType.LIST, show_up=OutputParameterShowUpType.OPTIONAL)
        module.appendOutput(name="search_list", type=OutputType.FUNCTION, function=self.getSearchList, show_up=OutputParameterShowUpType.OPTIONAL)
        #module.appendOutput(name="search_list", type=OutputType.FUNCTION, function=lambda url_list, name_list:zip(url_list, name_list))
        module.appendOutput("name_invalid_list", './/dl[@id="qyList"]/div/div[1]/text()', OutputType.LIST, show_up=OutputParameterShowUpType.OPTIONAL) # 无效公司名列表（优化了下xpath）
        module.appendOutput("status_invalid_list", './/dl[@id="qyList"]/div/div[2]/span[2]/text()', OutputType.LIST, show_up=OutputParameterShowUpType.OPTIONAL) #会显示\s+吊销\s+
        # module.appendOutput("name_invalid_list", ".//*[@id='div0']/div[1]/text()", OutputType.LIST,show_up=OutputParameterShowUpType.OPTIONAL)  #
        # module.appendOutput("status_invalid_list", ".//*[@id='div0']/div[2]/span[2]/text()", OutputType.LIST,show_up=OutputParameterShowUpType.OPTIONAL)  # 会显示\s+吊销\s+
        module.appendOutput("page_nos", ".//*[@id='form1']//div//td[@align]/text()", show_up=OutputParameterShowUpType.OPTIONAL) #TODO　xpath待验证
        # Todo 搜索列表页翻页
        def page_range(page_nos):
            if not page_nos:
                return None
            page_str = page_nos.strip()
            page_str = page_str[3:]
            page_str = page_str[page_str.find(u'共') + 3:page_str.find(u'页')]
            return range(2, int(page_str)+1)
        module.addEvent(Event(EventType.EXCEPTION_OCCURED, retry_times=2, redo_module="module_validate_code"))
        def assertNovalidCompany(search_list, name_invalid_list):#, html):
            if not search_list and name_invalid_list:
                self.report.access_type = SeedAccessType.NO_VALID_COMPANY
                self.holder.logging.info(u"无有效公司列表！")
                return False
            return True

        #TODO 有些公司有时候能收出结果，有时候收出无数据页面 (重试也会连续出现这种情况)
        def assertNocompany(html):
            if u'无数据' in html:
                time.sleep(2)
                download = DownLoader('shanxi')
                download.changeProxy()
                # with open('NODATA.html', 'wb') as f:
                #     f.write(html)
                self.report.access_type = SeedAccessType.NON_COMPANY
                self.holder.logging.info(u"无此公司！")
                return False
            return True
        module.addEvent(Event(EventType.ASSERT_FAILED, retry_times=0, assert_function=assertNovalidCompany))
        module.addEvent(Event(EventType.ASSERT_FAILED, retry_times=9, assert_function=assertNocompany, redo_module="module_validate_code"))
        module.addEvent(Event(EventType.EXCEPTION_OCCURED, retry_times=100, redo_module="module_validate_code"))
        module.addEvent(Event(EventType.OUTPUT_NOT_SATISFIED, retry_times=100, redo_module="module_validate_code"))
        self.module_manager.appendSubModule(module, True)

    def initSearchPages(self):
        pass

    def initConfigCompanyInfo(self):
        iterator = Iterator("search_list", "com")
        module = Module(None, u"获取公司信息", iterator)
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
        self.initPenaltyInfo(module)

        self.initAnnualReportPre(module)
        self.initAnnualReport(module)
        self.initResultCollect(module)

    def initCompanyInfoPrepare(self, module_super):
        module = Module(None, u"抓取公司前的预处理")
        def prepare(com):
            query_ = {}
            if com and len(com) >= 2 and com[0].strip() and com[1].strip():
                query_["company_url"] = com[0].strip()
                query_["company_name"] = com[1].strip() #修改公司名的key值
            return query_
        module.appendOutput(type=OutputType.FUNCTION, function=prepare)
        module.addEvent(Event(EventType.OUTPUT_NOT_SATISFIED, retry_times=5))
        module.addEvent(Event(EventType.EXCEPTION_OCCURED, retry_times=5, redo_module="module_validate_code"))
        module_super.appendSubModule(module, True)

    def initConfigBaseInfo(self, module_super):
        module = Module(self.visitJbxx, u"基本信息")
        def prepare(company_url):
            query_ = {}
            for qq in map(lambda x: x.split("="), urlparse.urlparse(company_url).query.split("&")):
                query_[qq[0]] = qq[1]
            return query_
        module.appendInput(InputType.FUNCTION, prepare)
        def assertReqArgs(zch):   #断言参数是否合法
            return True if zch else False
        module.addEvent(Event(EventType.ASSERT_FAILED, retry_times=5, assert_function=assertReqArgs, redo_module="module_validate_code"))
        module.appendOutput(name='company_zch', type=OutputType.FUNCTION, function=lambda zch: zch.strip(), show_up=OutputParameterShowUpType.OPTIONAL)
        module.appendUrl(lambda qyid, zch, qylx:"http://gsxt.jxaic.gov.cn/ECPS/ccjcgs/gsgs_viewDjxx.pt?qyid=%s&zch=%s&qylx=%s&num=undefined&showgdxx=true" % (qyid, zch, qylx))
        module.appendHeaders(lambda ua, qylx, qyid, zch:{
                'Accept-Language': 'en-US,en;q=0.5', 'Accept-Encoding': 'gzip, deflate',
                'Connection': 'keep-alive',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'User-Agent': ua,
                'Referer':'http://gsxt.jxaic.gov.cn/ECPS/ccjcgs/ccjcgs_ccjcgsIndexDetail.pt?qylx=%s&qyid=%s&zch=%s&tabName=1'%(qylx, qyid, zch),
                'Host': 'gsxt.jxaic.gov.cn'})
        module.addEvent(Event(EventType.EXCEPTION_OCCURED, retry_times=5, redo_module="module_validate_code"))
        module_super.appendSubModule(module, True)

    def initTopInfo(self, module_super):
        module = Module(self.visitTopInfo, u"Top信息")
        module.appendUrl(lambda qyid,company_zch,qylx:"http://gsxt.jxaic.gov.cn/ECPS/ccjcgs/ccjcgs_ccjcgsIndexDetail.pt?qylx=%s&qyid=%s&zch=%s&tabName=1" % (qylx,qyid,company_zch))
        module.appendHeaders(lambda ua: {
            'Host' : 'gsxt.jxaic.gov.cn',
            'Connection' : 'keep-alive',
            'User-Agent' : ua,
            'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding' : 'gzip, deflate, sdch',
            'Accept-Language' : 'en-US,en;q=0.8,zh-CN;q=0.6,zh-TW;q=0.4'})
        module_super.appendSubModule(module, True)

    def initConfigShareHolderInfo(self, module_super):
        module = Module(self.visitGdxx, u"股东信息")
        module.appendUrl(lambda qyid, company_zch:"http://gsxt.jxaic.gov.cn/ECPS/ccjcgs/gsgs_viewDjxxGdxx.pt?qyid=%s&zch=%s" % (qyid, company_zch))
        module.appendHeaders(lambda ua: {
            'Accept-Language': 'en-US,en;q=0.8,zh-CN;q=0.6,zh-TW;q=0.4',
            'Accept-Encoding': 'gzip, deflate, sdch', 'Connection': 'keep-alive',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'User-Agent': ua,
            'Host': 'gsxt.jxaic.gov.cn'})
        module.appendOutput("gdxx_pages", None, OutputType.FUNCTION, self.getPageNoPrepare, OutputParameterShowUpType.OPTIONAL)
        module_super.appendSubModule(module, True)

    def initShareHolderInfoPage(self, module_super):
        iterator = Iterator("gdxx_pages", "page_no")
        module = Module(None, u"进入股东翻页", iterator)
        module_super.appendSubModule(module, True)

        sub_module = Module(self.visitGdxx, u"获取股东翻页信息")
        sub_module.appendUrl(lambda qyid: "http://gsxt.jxaic.gov.cn/ECPS/ccjcgs/gsgs_viewDjxxGdxx.pt?qyid=%s" % qyid)
        sub_module.appendWebMethod("post")
        sub_module.appendPostData(lambda page_no:{'page':page_no,'limit':5,'mark':0}) #  mark可取0,-1,1 取值视点击的顺序定
        sub_module.appendHeaders(lambda ua:{
            'Host' : 'gsxt.jxaic.gov.cn',
            'Connection' : 'keep-alive',
            'User-Agent' : ua,
            'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding' : 'gzip, deflate, sdch',
            'Accept-Language' : 'en-US,en;q=0.8,zh-CN;q=0.6,zh-TW;q=0.4'})
        module.appendSubModule(sub_module, True)

    #TODO 股东详情待测，暂未找到股东详情公司 ww
    def initShareHolderDetail(self, module_super):
        iterator = Iterator("gdxx_list", "gdxx_rcd")
        module = Module(None, u"进入股东详情", iterator)
        module_super.appendSubModule(module, True)

        sub_module = Module(self.visitGdxq, u"获取股东详情信息")
        sub_module.appendUrl(self.getGdxqUrl)
        sub_module.appendHeaders(lambda ua:{
            'Accept-Language': 'en-US,en;q=0.8,zh-CN;q=0.6,zh-TW;q=0.4',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Connection': 'keep-alive',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'User-Agent': ua,
            'Host': 'gsxt.jxaic.gov.cn',
            'Cache-Control': 'max-age=0'})
        module.addEvent(Event(EventType.EXCEPTION_OCCURED, retry_times=5))
        module.appendSubModule(sub_module, True)

    #TODO 变更信息解析更多解析不全
    def initConfigChangeInfo(self, module_super):
        module = Module(self.visitBgxx, u"变更信息")
        module.appendUrl(lambda qyid:"http://gsxt.jxaic.gov.cn/ECPS/ccjcgs/gsgs_viewDjxxBgxx.pt?qyid=%s" % qyid)
        module.appendHeaders(lambda ua:{
            'Accept-Language': 'en-US,en;q=0.8,zh-CN;q=0.6,zh-TW;q=0.4',
            'Accept-Encoding': 'gzip, deflate, sdch', 'Connection': 'keep-alive',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'User-Agent': ua,
            'Host': 'gsxt.jxaic.gov.cn'})
        module.appendOutput("bgxx_pages", None, OutputType.FUNCTION, self.getPageNoPrepare, OutputParameterShowUpType.OPTIONAL)
        module_super.appendSubModule(module, True)


    def initChangeInfoPage(self, module_super):
        iterator = Iterator("bgxx_pages", "page_no")
        module = Module(None, u"进入变更信息翻页", iterator)
        module_super.appendSubModule(module)
        sub_module = Module(self.visitBgxx, u"获取变更翻页信息")
        sub_module.appendUrl(lambda qyid: "http://gsxt.jxaic.gov.cn/ECPS/ccjcgs/gsgs_viewDjxxBgxx.pt?qyid=%s" % qyid)
        sub_module.appendWebMethod("post")
        sub_module.appendPostData(lambda page_no:{'page':page_no,'limit':5,'mark':0})
        sub_module.appendHeaders(lambda ua:{
            'Host' : 'gsxt.jxaic.gov.cn',
            'Connection' : 'keep-alive',
            'User-Agent' : ua,
            'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Encoding' : 'gzip, deflate, sdch',
            'Accept-Language' : 'en-US,en;q=0.8,zh-CN;q=0.6,zh-TW;q=0.4'})
        module.appendSubModule(sub_module, True)

    # TODO 分支结构和备案信息有没有翻页
    def initArchiveInfo(self, module_super):
        module = Module(self.visitBaxx, u"获取备案信息")
        module.appendUrl(self.getZyryUrl)
        module.appendHeaders(lambda ua, qylx, qyid, company_zch:{
            'Accept-Language': 'en-US,en;q=0.8,zh-CN;q=0.6,zh-TW;q=0.4',
            'Accept-Encoding': 'gzip, deflate, sdch', 'Connection': 'keep-alive',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'User-Agent': ua,
            'Referer':'http://gsxt.jxaic.gov.cn/ECPS/ccjcgs/ccjcgs_ccjcgsIndexDetail.pt?qylx=%s&qyid=%s&zch=%s&tabName=1'%(qylx, qyid, company_zch), #NEW 新增Referer
            'Host': 'gsxt.jxaic.gov.cn'})
        module_super.appendSubModule(module, True)

    #TODO 数据待测
    def initPenaltyInfo(self, module_super):
        module = Module(self.visitXzcf, u"获取行政处罚信息")
        module.appendUrl(lambda qyid,company_zch,qylx: "http://gsxt.jxaic.gov.cn/ECPS/ccjcgs/gsgs_viewXzcfxx.pt?qyid=%s&zch=%s&qylx=%s&num=1&showgdxx=true" % (qyid, company_zch, qylx))
        module.appendHeaders(lambda ua, qylx, qyid, company_zch:{
            'Accept-Language': 'en-US,en;q=0.8,zh-CN;q=0.6,zh-TW;q=0.4',
            'Accept-Encoding': 'gzip, deflate, sdch', 'Connection': 'keep-alive',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'User-Agent': ua,
            'Referer': 'http://gsxt.jxaic.gov.cn/ECPS/ccjcgs/ccjcgs_ccjcgsIndexDetail.pt?qylx=%s&qyid=%s&zch=%s&tabName=1' % (qylx, qyid, company_zch),
            'Host': 'gsxt.jxaic.gov.cn'})
        module_super.appendSubModule(module, True)

    #遍历企业年报列表
    def initAnnualReportPre(self, module_super):
        module = Module(self.getWebHtml, u"获取年报年份列表")
        module.module_id = "fetch_qynb_list"
        module.appendUrl(lambda qyid, company_zch, qylx :"http://gsxt.jxaic.gov.cn/ECPS/ccjcgs/qygs_ViewQynb.pt?qyid=%s&zch=%s&qylx=%s&num=0" % (qyid, company_zch, qylx))
        module.appendHeaders(lambda ua, qylx, qyid,company_zch : {
            "User-Agent": ua,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3",
            "Accept-Encoding": "gzip, deflate",
            "Host": "gsxt.jxaic.gov.cn",
            "Connection": "keep-alive"})
        def getRightUrl(html=None):
            if not html:
                return []
            rs = re.findall(r'<a\s+href="(.*?\?.*?nbnd=\d{4}.*?)"', html, re.S)
            rs = list(set(rs))
            return ['http://gsxt.jxaic.gov.cn'+x for x in rs]

        module.appendOutput(name="qynb_param_list", type=OutputType.FUNCTION, function=getRightUrl, show_up=OutputParameterShowUpType.OPTIONAL)
        module_super.appendSubModule(module, True)


    #TODO 年报list 不合法， 有公司名，没连接  渝水区劳动北路易新电脑科技中心；； 该个体户已报送纸质年报，不在公示系统中公示
    def initAnnualReport(self, module_super):
        iterator = Iterator("qynb_param_list", "qynb_url")
        module = Module(None, u"遍历年报信息", iterator)
        module_super.appendSubModule(module, True)
        self.initQynbInfo(module)

    #获取年报
    def initQynbInfo(self, module_super):
        module = Module(None, u"设置年份")
        def saveNbyear(qynb_url):
            self.value_dict['nb_name'] = re.findall(r'nbnd=(\d{4})', qynb_url, re.S)[0]
        module.appendOutput(type=OutputType.FUNCTION, function=saveNbyear)
        module_super.appendSubModule(module, True)

        module = Module(self.visitQynb, u"获取企业年报")
        module.appendUrl(lambda qynb_url:qynb_url)
        module.appendHeaders(lambda ua, qyid, company_zch, qylx:{"User-Agent": ua,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3",
            "Accept-Encoding": "gzip, deflate",
            "Host": "gsxt.jxaic.gov.cn",
            "Referer": "http://gsxt.jxaic.gov.cn/ECPS/ccjcgs/qygs_ViewQynb.pt?qyid=%s&zch=%s&qylx=%s&num=0&showgdxx=true"%(qyid, company_zch, qylx),
            "Connection": "keep-alive"})
        module.addEvent(Event(EventType.OUTPUT_NOT_SATISFIED, retry_times=5))
        module.addEvent(Event(EventType.EXCEPTION_OCCURED, retry_times=5))
        module.addSleep(Sleep(2))
        module_super.appendSubModule(module, True)

    def initResultCollect(self, module_super):
        module = Module(self.resultCollect, u"结果收集")
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

    def getZyryUrl(self, qyid, company_zch, qylx, company):
        '''
        获取主要人员信息的url，依赖于获取到的基本信息中的“类型”
        :param entId:
        :param company:
        :return:
        '''
        url = "http://gsxt.jxaic.gov.cn/ECPS/ccjcgs/gsgs_viewBaxx.pt?qyid=%s&zch=%s&qylx=%s&showgdxx=true" % (
            qyid, company_zch, qylx)
        if not company:
            return url
        for t_dict in company:
            if u"类型" in t_dict and t_dict[u"类型"] in [u"农民专业合作社", u"个体工商户"]:
                return "http://gsxt.jxaic.gov.cn/ECPS/ccjcgs/gsgs_viewBaxx.pt?qyid=%s&zch=%s&qylx=%s&&balx=%s" % (
                    qyid, company_zch, qylx, qylx)
        return url

if __name__ == "__main__":
    pass

