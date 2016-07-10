# -*- coding: utf-8 -*-
# Created by David on 2016/5/9.

import sys
import random
import time
import re
import urlparse
import PyV8
reload(sys)
from qyxx_all.CrawlerBase import CrawlerBase
from lxml import etree
from qyxx_all.ModuleManager import Module,Event,Iterator,Adapter,Bypass,Sleep
from qyxx_all.util.crawler_util import CrawlerRunMode, InputType, OutputType, EventType, OutputParameterShowUpType

class CrawlerSzxy(CrawlerBase):
    def __init__(self, pinyin, crawler_master):
        self.crawler_master = crawler_master
        config_dict = dict()
        config_dict[CrawlerRunMode.COMPANY_ADAPTER] = [self.initConfigBaseInfo, self.initDetailList, self.initNbList, self.initNb, self.initResultCollect]
        CrawlerBase.__init__(self, pinyin, config_dict, None, None)
        self.initConfig()
        pass

    def initConfigBaseInfo(self):
        module = Module(self.crawler_master.visitJbxx, u"基本信息")
        adapter = Adapter({"source": u"深圳信用网"}, u"深圳信用网")
        module.addAdapter(adapter)

        module.appendUrl("company_url")
        module.appendHeaders({'Host': 'www.szcredit.com.cn',
                                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:46.0) Gecko/20100101 Firefox/46.0',
                                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                                'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
                                'Accept-Encoding': 'gzip, deflate',
                                'Referer': 'http://gsxt.gdgs.gov.cn/aiccips/CheckEntContext/showInfo.html',
                                'Connection': 'keep-alive'})
        def getRid(company_url):
            para_dict = urlparse.parse_qs(company_url)
            val_list = para_dict.values()
            if not val_list or not val_list[0]:
                return None
            return val_list[0][0]
        module.appendOutput(name="rid", type=OutputType.FUNCTION, function=getRid)
        module.appendOutput(name="detail_list", xpath=".//table//tr/td/a/@href", type=OutputType.LIST, show_up=OutputParameterShowUpType.OPTIONAL)
        module.addSleep(Sleep(10))
        self.module_manager.appendSubModule(module, True)

    def initDetailList(self):
        iterator = Iterator(seeds="detail_list", param_name="url")
        module = Module(iterator=iterator, name=u"遍历详情列表")
        self.module_manager.appendSubModule(module, True)
        module.addSleep(Sleep(10))
        self.initDetail(module)

    def initDetail(self, module_super):
        module = Module(self.crawler_master.visitGdxq, u"抓取详情")
        module.appendUrl(lambda url: "http://www.szcredit.com.cn/web/GSZJGSPT/%s" % url.lstrip('/'))
        module.addSleep(Sleep(10))
        module_super.appendSubModule(module)

    def initNbList(self):
        module = Module(self.crawler_master.visitQynbList, u"抓取年报列表")
        module.appendUrl(lambda rid: "http://www.szcredit.com.cn/web/GSZJGSPT/QynbDetail.aspx?rid=%s" % rid)
        module.appendOutput("nb_list", ".//table//td/a", OutputType.LIST, show_up=OutputParameterShowUpType.OPTIONAL)
        module.addSleep(Sleep(10))
        self.module_manager.appendSubModule(module)

    def initNb(self):
        iterator = Iterator(seeds="nb_list", param_name="nb")
        module = Module(iterator=iterator, name=u"遍历年报列表")
        self.module_manager.appendSubModule(module, True)

        self.initNbOne(module)
        self.initNbBasx(module)

    def initNbOne(self, module_super):
        module = Module(self.crawler_master.visitQynb, u"抓取企业年报信息")
        def prepare(nb):
            mv_dict = dict()
            mv_dict['nb_url'] = ''.join(nb.xpath('@href')).replace(' ','').replace('\t','')
            mv_dict['nb_name'] = ''.join(nb.xpath('text()')).replace(u'年度报告','').strip()
            return mv_dict
        module.appendInput(input_type=InputType.FUNCTION, input_value=prepare)
        module.appendUrl("nb_url")
        def bypassFun(html):
            if not html or u'深圳市市场监督管理局' not in html:
                return True
            return False
        module.appendOutput(name="nb_post_data", type=OutputType.FUNCTION, function=self.getPostData, show_up=OutputParameterShowUpType.OPTIONAL)
        module.addSleep(Sleep(10))
        module_super.appendSubModule(module, True)
        module.appendBypass(Bypass(condition_fuc=bypassFun, module_id="module_nb_basx", range_global=True))

    def initNbBasx(self, module_super):
        module = Module(self.crawler_master.visitQynb, u'抓取企业年报-备案事项')
        module.module_id = "module_nb_basx"
        module.appendUrl(lambda rid: "http://app02.szaic.gov.cn/NB.WebUI/WebPages/Publicity/NBInfo.aspx?rid=%s" % rid)
        module.appendPostData("nb_post_data")
        module.appendOutput(name="nb_post_data", type=OutputType.FUNCTION, function=self.getPostData, show_up=OutputParameterShowUpType.OPTIONAL)
        module.addSleep(Sleep(10))
        module_super.appendSubModule(module, True)

    def initResultCollect(self):
        module = Module(self.crawler_master.resultCollect, u"结果收集")
        self.module_manager.appendSubModule(module)

    def getPostData(self, html):
        if not html:
            return None
        data_dict = dict()
        tree = etree.HTML(html)
        ih_list = tree.xpath('.//input[@type="hidden"]')
        if not ih_list:
            return None
        for ih in ih_list:
            key = ''.join(ih.xpath('@id'))
            val = ''.join(ih.xpath('@value'))
            data_dict[key] = val
        return data_dict

if __name__ == "__main__":
    pass
