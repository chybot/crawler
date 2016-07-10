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
from qyxx_all.ModuleManager import Module,Event,Iterator,Adapter
from qyxx_all.util.crawler_util import CrawlerRunMode, InputType, OutputType, EventType, OutputParameterShowUpType

class CrawlerGdQyxy(CrawlerBase):
    def __init__(self, pinyin, crawler_master):
        self.crawler_master = crawler_master
        config_dict = dict()
        config_dict[CrawlerRunMode.COMPANY_ADAPTER] = [self.initConfigBaseInfo, self.initConfigShareHolderPage,
                                                       self.initConfigChangeInfoPage, self.initArchiveInfoPage, self.initBranchInfoPage, self.initResultCollect]
        CrawlerBase.__init__(self, pinyin, config_dict, None, None)
        self.initConfig()
        pass

    def initConfigBaseInfo(self):
        module = Module(self.crawler_master.visitJbxx, "基本信息")
        adapter = Adapter({"source": u"企业信用网"}, u"企业信用网")
        module.addAdapter(adapter)

        module.appendUrl("company_url")
        module.appendHeaders(lambda company_url:{'Host': 'gsxt.gzaic.gov.cn',
                                                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:46.0) Gecko/20100101 Firefox/46.0',
                                                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                                                'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
                                                'Accept-Encoding': 'gzip, deflate',
                                                'Referer': company_url,
                                                'Connection': 'keep-alive'})
        def prepareCommonInfo(html):
            tree = etree.HTML(html)
            values = tree.xpath('.//@value')
            entNo = values[1]
            entType = values[2]
            regOrg = values[3]
            return {"entNo": entNo, "entType": entType, "regOrg": regOrg}
        module.appendOutput(type=OutputType.FUNCTION, function=prepareCommonInfo)
        module.addEvent(Event(EventType.EXCEPTION_OCCURED, retry_times=5))
        self.module_manager.appendSubModule(module, True)

    def initConfigShareHolderPage(self):
        module = Module(self.crawler_master.visitGdxxJson, "股东信息")
        module.appendInput(InputType.FUNCTION, lambda company_url:re.search(r'pripid=(.*)', company_url).group(1).strip(), 'pripid')
        def getUrl(pripid):
            test_data = {
                '_': str(int(time.time() * 1000)),
                'entityVo.curPage': 1,
                'entityVo.pripid': pripid,
                'where': ' where 1=1'
            }
            return 'http://121.8.226.101:7001/search/search!investorListShow?' + urllib.urlencode(test_data)
        module.appendUrl(getUrl)
        module.appendHeaders(self.header_qyxy)
        module.appendOutput(name='pages', type=OutputType.FUNCTION, function=lambda json: range(1, int(json['baseVo']['totalPage']) + 1))
        self.module_manager.appendSubModule(module, True)

        Iterator("pages", "page_no")
        module = Module(name="股东信息翻页循环", iterator=None)
        self.module_manager.appendSubModule(module, True)

        self.initConfigShareHolderInfo(module)

    def initConfigShareHolderInfo(self, module_super):
        module = Module(self.crawler_master.visitGdxxJson, "逐页获取股东信息")
        def getUrl(pripid, page_no):
            get_data = {
                '_' : str(int(time.time() * 1000)),
                'entityVo.curPage' : page_no,
                'entityVo.pripid' : pripid,
                'where' : ' where 1=1'
            }
            return 'http://121.8.226.101:7001/search/search!investorListShow?' + urllib.urlencode(get_data)
        module.appendUrl(getUrl)
        module.appendHeaders(self.header_qyxy)
        module.addMapper({'sinvenstorname':u'股东/发起人类型', 'inv':u'股东/发起人名称', 'scertname':u'证照类型', 'cardname':u'证照类型', 'cerno':u'证照编号'})
        module_super.appendSubModule(module, True)

    def initConfigChangeInfoPage(self):
        module = Module(self.crawler_master.visitBgxxJson, "变更信息")
        def getUrl(pripid):
            test_data = {
                '_': str(int(time.time() * 1000)),
                'entityVo.curPage': 1,
                'entityVo.pripid': pripid,
                'where': ' where 1=1'
            }
            return 'http://121.8.226.101:7001/search/search!changeListShow?' + urllib.urlencode(test_data)

        module.appendUrl(getUrl)
        module.appendHeaders(self.header_qyxy)
        module.appendOutput(name='pages', type=OutputType.FUNCTION,
                            function=lambda json: range(1, int(json['baseVo']['totalPage']) + 1))
        self.module_manager.appendSubModule(module, True)

        Iterator("pages", "page_no")
        module = Module(name="变更信息翻页循环", iterator=None)
        self.module_manager.appendSubModule(module, True)

        self.initConfigChangeInfo(module)

    def initConfigChangeInfo(self, module_super):
        module = Module(self.crawler_master.visitBgxxJson, "逐页获取变更信息")
        def getUrl(pripid, page_no):
            get_data = {
                '_': str(int(time.time() * 1000)),
                'entityVo.curPage': page_no,
                'entityVo.pripid': pripid,
                'where': ' where 1=1'
            }
            return 'http://121.8.226.101:7001/search/search!changeListShow?' + urllib.urlencode(get_data)

        module.appendUrl(getUrl)
        module.appendHeaders(self.header_qyxy)
        module.addMapper({'sname':u'变更事项', 'altbe':u'变更前内容', 'altaf':u'变更后内容', 'altdate':u'变更日期'})
        module_super.appendSubModule(module, True)

    def initArchiveInfoPage(self):
        module = Module(self.crawler_master.visitBaxxJson, "备案信息")
        def getUrl(pripid):
            test_data = {
                '_': str(int(time.time() * 1000)),
                'entityVo.pageSize': 10,
                'entityVo.curPage': 1,
                'entityVo.pripid': pripid,
                'where': ' where 1=1'
            }
            return 'http://121.8.226.101:7001/search/search!staffListShow?' + urllib.urlencode(test_data)
        module.appendUrl(getUrl)
        module.appendHeaders(self.header_qyxy)
        module.appendOutput(name='pages', type=OutputType.FUNCTION,
                            function=lambda json: range(1, int(json['baseVo']['totalPage']) + 1))
        self.module_manager.appendSubModule(module, True)

        Iterator("pages", "page_no")
        module = Module(name="备案信息翻页循环", iterator=None)
        self.module_manager.appendSubModule(module, True)

        self.initArchiveInfo(module)

    def initArchiveInfo(self, module_super):
        module = Module(self.crawler_master.visitBaxxJson, "逐页获取备案信息")
        def getUrl(pripid, page_no):
            get_data = {
                '_': str(int(time.time() * 1000)),
                'entityVo.pageSize': 10,
                'entityVo.curPage': page_no,
                'entityVo.pripid': pripid,
                'where': ' where 1=1'
            }
            return 'http://121.8.226.101:7001/search/search!staffListShow?' + urllib.urlencode(get_data)
        module.appendUrl(getUrl)
        module.appendHeaders(self.header_qyxy)
        module.addMapper({'name':u'姓名', 'sdutyname':u'职务'})
        module_super.appendSubModule(module, True)

    def initBranchInfoPage(self):
        module = Module(self.crawler_master.visitFzjgJson, "分支机构信息")
        def getUrl(pripid):
            test_data = {
                '_': str(int(time.time() * 1000)),
                'entityVo.curPage': 1,
                'entityVo.pripid': pripid,
                'where': ' where 1=1'
            }
            return 'http://121.8.226.101:7001/search/search!branchListShow?' + urllib.urlencode(test_data)
        module.appendUrl(getUrl)
        module.appendHeaders(self.header_qyxy)
        module.appendOutput(name='pages', type=OutputType.FUNCTION,
                            function=lambda json: range(1, int(json['baseVo']['totalPage']) + 1))
        self.module_manager.appendSubModule(module, True)

        Iterator("pages", "page_no")
        module = Module(name="分支机构信息翻页循环", iterator=None)
        self.module_manager.appendSubModule(module, True)

        self.initBranchInfo(module)

    def initBranchInfo(self, module_super):
        module = Module(self.crawler_master.visitFzjgJson, "逐页获取分支机构信息")
        def getUrl(pripid, page_no):
            get_data = {
                '_': str(int(time.time() * 1000)),
                'entityVo.curPage': page_no,
                'entityVo.pripid': pripid,
                'where': ' where 1=1'
            }
            return 'http://121.8.226.101:7001/search/search!branchListShow?' + urllib.urlencode(get_data)
        module.appendUrl(getUrl)
        module.appendHeaders(self.header_qyxy)
        module.addMapper({'branchregno':u'注册号', 'sregorgname':u'登记机关', 'branchentname':u'名称'})
        module_super.appendSubModule(module, True)

    def initResultCollect(self):
        module = Module(self.crawler_master.resultCollect, "结果收集")
        self.module_manager.appendSubModule(module)

    def header_qyxy(self, company_url):
        header = {
            "Host": "121.8.226.101:7001",
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

