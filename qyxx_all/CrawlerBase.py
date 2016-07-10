# -*- coding: utf-8 -*-
# Created by David on 2016/5/4.

import sys
reload(sys)
sys.path.append('../')
sys.setdefaultencoding("UTF-8")
from lxml import etree
import inspect
import json
import copy
import re
from HttpRequst.DownLoader import DownLoader
from CrawlerControl import CrawlerControl
from util.HolderUtil import HolderUtil
from util import crawler_util
from util import yzm_util
from util.crawler_util import CrawlerRunMode
from util.crawler_util import InputType,OutputType
from ModuleManager import ModuleManager
from Parser.util.TableParseUtil import TableParseUtil
from Parser.util.JsonParseUtil import JsonParseUtil
from util.yzm_util import record_success
import Parser.parser_map_config as mapper
from Parser.ParserMapper import ParserMapper
from CrawlerStatistic import CrawlerStatic
from CommonLib.WebContent import WebContent,WebAccessType,WebContentType
from CommonLib.WebContent import CompanyAccessType, SeedAccessType, SeedAccessReport
from CommonLib.NbxxApiControler import NbxxApiControler
from CommonLib.Decorator import LogMetaclass

class CrawlerBase:
    """
    爬虫基类，提供通用模块方法的实现，供子类复用
    """

# region 初始化方法
    # __metaclass__ = LogMetaclass

    def __init__(self, pinyin, config_dict, check_dict, callback):
        """
        初始化对象参数
        :param pinyin: 省份拼音
        :param config_dict: 模块配置字典
        :param callback: 外部回调方法
        """
        # 持有核心业务无关的通用功能对象
        self.holder = HolderUtil(pinyin)
        self.pinyin = pinyin
        # 爬虫调度委托
        self.crawl_delegate = CrawlerControl(self)
        # 模块配置字典
        self.config_dict = config_dict
        # web内容下载器
        self.downloader = DownLoader(pinyin, self.holder.logging)
        # html内容检查
        self.html_check_dict = check_dict['html_check_dict'] if check_dict and 'html_check_dict' in check_dict else None
        # json内容检查
        self.json_check_dict = check_dict['json_check_dict'] if check_dict and 'json_check_dict' in check_dict else None
        # 初始化搜索列表页是否搜索到公司的判断配置
        self.non_company_set = {"无查询结果","未查询到相关记录"}
        # 外部回调方法，每爬取完一个公司的信息会被调用一次
        self.callback = callback
        # 解析器开关
        self.parse_on = False           # 除jbxx、gdxx之外的开关，False表示不做解析
        self.parse_jbxx_on = True      # jbxx开关
        self.parse_gdxx_on = True       # gdxx开关
        # 抓取情况统计
        self.statistic = CrawlerStatic(self.holder.logging)
        # 年报是否需要抓取判断
        self.nb_judge = NbxxApiControler()
        pass

    def setNonCompanyConfig(self, non_company_set):
        '''
        设置无此公司判断
        :param non_company_set:
        :return:
        '''
        self.non_company_set = non_company_set

    def initConfig(self):
        '''
        初始化模块配置, 模块配置通常包括关键字和url两种方式
        '''
        if not self.config_dict:
            raise Exception("配置列表为空，请检查！")
        # 模块管理类
        self.module_manager = ModuleManager()
        self.holder.logging.info("加载模块配置信息")
        for mode in self.config_dict:
            self.module_manager.switchToMode(mode)
            for init_function in self.config_dict[mode]:
                varnames = inspect.getargspec(init_function).args
                if len(varnames) == 2:
                    init_function(self.module_manager)
                else:
                    init_function()
        pass

    def init(self):
        '''
        爬行初始化，每次爬行会被初始化一次
        :return:
        '''
        self.holder.init()
        # value dictionary: used for passing value between functions
        self.value_dict = {'ua':self.holder.ua}
        # all company results
        self.result_list = list()
        # company dictionary: used for storing one company value between functions
        self.result_dict = dict()
        # all company pages
        self.page_list = list()
        # one company html page
        self.page_dict = dict()
        # snapshot the middle values for sub modules
        self.value_dict_snap = dict()
        # 每次爬行开始初始化downloader
        self.downloader.firstInit()
        # 每次爬行的种子report
        self.report = SeedAccessReport(0, 0, SeedAccessType.ERROR)
        # 每次爬行前需要恢复初始模块状态
        self.initConfig()

# endregion

#region rowkey 计算

    def setRowKey(self, map_dict=None):
        if not map_dict:
            map_dict = {'名称':'company_name','注册号':'company_zch','信用代码':'company_zch'}
        return self.defaultRowKey(map_dict)

    def defaultRowKey(self, map_dict=None):
        if 'company' not in self.result_dict:
            return False
        if not map_dict:
            return False
        rowkey_dict = dict()
        for v_list in self.result_dict['company']:
            if not v_list:
                continue
            for k,v in v_list.items():
                for km in map_dict:
                    if km in k:
                        rowkey_dict[map_dict[km]] = v
            if rowkey_dict:
                break
        self.page_dict['rowkey_dict'] = rowkey_dict
        if not rowkey_dict:
            return False
        return True

#endregion

# region 爬行入口方法 crawl crawl_url
    def crawl(self, company_key):
        self.init()
        # 切换为通过关键字抓取模式
        self.module_manager.switchToMode(CrawlerRunMode.COMPANY_KEY)
        self.holder.logging.info(u"通过关键词（%s）开始抓取信息" % company_key)
        self.value_dict['company_key'] = company_key.strip()
        self.value_dict['search_company'] = company_key.strip()
        return self._delegateCrawl(CrawlerRunMode.COMPANY_KEY)

    def crawlUrl(self, company_url, company_name):
        self.init()
        # 切换为通过Url抓取模式
        self.module_manager.switchToMode(CrawlerRunMode.COMPANY_URL)
        self.holder.logging.info(u"通过公司名(%s)和url(%s)开始抓取信息" % (company_name, company_url))
        self.value_dict['company_url'] = company_url
        self.value_dict['search_company'] = company_name
        return self._delegateCrawl(CrawlerRunMode.COMPANY_URL)

    def _delegateCrawl(self, model):
        v_dict = copy.deepcopy(self.value_dict)
        retry_times = 1
        while retry_times <= 5:
            self.crawl_delegate.crawl()
            # 统计搜索列表中各公司爬取状态，生成seed抓取报告
            self.seedReport()
            self.holder.logging.info(u"本次抓取结果类型：%s" % SeedAccessType.description(self.report.access_type))
            if self.report.access_type == SeedAccessType.ERROR:
                self.holder.logging.info(u"抓取失败，开始第 %s 次重试！" % retry_times)
            else:
                break
            retry_times += 1
            self.init()
            # 切换抓取模式
            self.module_manager.switchToMode(model)
            self.value_dict = copy.deepcopy(v_dict)
        self.statistic.statistic(self.report, retry_times-1)
        self.statistic.description()
        return self.report

# endregion

# region 模块方法

    def visitHomePage(self, module):
        """
        访问首页
        :param module:
        :return:
        """
        web = self.fetchWebContent(module, u"访问首页，期望输出参数 %s")
        if not web.body:
            self.holder.logging.warn(u"获取 (%s) 信息失败" % module.name)
            return
        self.parseOutput(module.outputs, web.body)

    def visitValidateCode(self, module):
        """
        访问验证码
        :param module:
        :return:
        """
        web = self.fetchWebContent(module, u"访问验证码，期望输出参数 %s", is_pic=True)
        yzm_type = None
        if self.holder.debug == 0:
            yzm_type = self.holder.pinyin
        if not web.body:
            self.holder.logging.error(u"获取的验证码图片为空！")
            return
        url = module.getInputByType(InputType.URL, self.value_dict, self.holder.logging)
        try:
            (yzm, code_id, is_report_error, recChar, img_path) = yzm_util.parse_yzm(url, web.body, 5000, yzm_max_len=6,
                                                                                    type=yzm_type, holder=self.holder)
        except Exception as e:
            self.downloader.changeProxy()
            raise Exception(e)
        self.value_dict['yzm'] = yzm
        self.value_dict['img_path'] = img_path

    def visitSearchList(self, module):
        """
        访问搜索列表
        :param module:
        :return:
        """
        web = self.fetchWebContent(module, u"访问公司列表，期望输出参数 %s")
        # print("搜索结果列表页：%s" % company_list_html)
        if not web.body:
            self.holder.logging.warn(u"获取公司列表信息失败")
            return
        # 无此公司判断
        for keyword in self.non_company_set:
            if keyword in web.body:
                self.holder.logging.warn(u"无此公司！")
                self.report.access_type = SeedAccessType.NON_COMPANY
                return
        if web.access_type == WebAccessType.TOO_OFTEN:
            self.holder.logging.warning(u"访问过于频繁，可能已被网站禁止访问！！！")
            self.downloader.insertBlack()
            return
        elif web.access_type == WebAccessType.ACCESS_VIOLATION:
            self.holder.logging.warning(u"非法访问！！！")
            return
        self.parseOutput(module.outputs, web.body)
        pass
            
    def visitTopInfo(self, module):
        """
        访问页面top信息
        :param module:
        :return:
        """
        web = self.fetchSpecificCompany(module, u"访问 (%s) 的Top信息，期望输出参数 %s")
        self.appendWebContent(u'top_html', web)
        if not web: return
        self.value_dict['html'] = web.body
        # 此处未做解析
        self.parseOutput(module.outputs, web.body)
        pass

    def visitJbxx(self, module):
        """
        访问基本信息页面
        :param module:
        :return:
        """
        web = self.fetchSpecificCompany(module, u"访问 (%s) 的基本信息，期望输出参数 %s")
        self.appendWebContent(u'jbxx_html', web)
        if not web: return
        if self.parse_jbxx_on:
            self.parseHtmlTable(u"解析（%s）的基本信息")
        if 'company' in self.result_dict:
            self.value_dict['company'] = self.result_dict['company']
        self.parseOutput(module.outputs, web.body)
        pass

    def visitGdxx(self, module):
        """
        访问股东信息
        :param module:
        :return:
        """
        web = self.fetchSpecificCompany(module, u"访问 (%s) 的股东信息，期望输出参数 %s")
        self.appendWebContent(u'gdxx_html', web)
        if not web: return
        self.value_dict['html'] = web.body
        gdxx_list = None
        if self.parse_gdxx_on:
            gdxx_list = self.parseHtmlTable(u"解析（%s）的股东信息")
        if not gdxx_list or len(gdxx_list) == 0:
            return
        all_gdxx_list = []
        if 'gdxx_list' in self.value_dict:
            all_gdxx_list = self.value_dict['gdxx_list']
        all_gdxx_list.extend(gdxx_list)
        self.value_dict['gdxx_list'] = all_gdxx_list

    def visitGdxq(self, module):
        """
        访问股东详情
        :param module:
        :return:
        """
        web = self.fetchSpecificCompany(module, u"访问 (%s) 的股东详细信息，期望输出参数 %s")
        self.appendWebContent(u'gdxq_html', web)
        if not web: return
        if self.parse_on:
            self.parseGdxq()

    def visitBgxx(self, module):
        """
        访问变更信息
        :param module:
        :return:
        """
        web = self.fetchSpecificCompany(module, u"访问 (%s) 的变更信息，期望输出参数 %s")
        self.appendWebContent(u'bgxx_html', web)
        if not web: return
        if self.parse_on:
            self.parseHtmlTable(u"解析（%s）的变更信息")

    def visitBaxx(self, module):
        """
        访问备案信息
        :param module:
        :return:
        """
        web = self.fetchSpecificCompany(module, u"访问 (%s) 的备案信息，期望输出参数 %s")
        self.appendWebContent(u'baxx_html', web)
        if not web: return
        if self.parse_on:
            self.parseHtmlTable(u"解析（%s）的备案信息")
    
    def visitFzjg(self, module):
        """
        访问分支机构
        :param module:
        :return:
        """
        web = self.fetchSpecificCompany(module, u"访问 (%s) 的分支机构信息，期望输出参数 %s")
        self.appendWebContent(u"fzjg_html", web)
        if not web: return
        if self.parse_on:
            self.parseHtmlTable(u"解析（%s）的分支机构信息")

    def visitXzcf(self, module):
        """
        访问行政处罚信息
        :param module:
        :return:
        """
        web = self.fetchSpecificCompany(module, u"访问 (%s) 的行政处罚信息，期望输出参数 %s")
        self.appendWebContent(u"xzcf_html", web)
        if not web: return
        if self.parse_on:
            self.parseHtmlTable(u"解析（%s）的行政处罚信息")

    def visitQynbList(self, module):
        """
        访问行政处罚信息
        :param module:
        :return:
        """
        web = self.fetchSpecificCompany(module, u"访问 (%s) 的企业年报列表，期望输出参数 %s")
        if not web: return
        self.parseOutput(module.outputs, web.body)

    def visitQynb(self, module):
        """
        访问行政处罚信息
        :param module:
        :return:
        """
        web = self.fetchSpecificCompany(module, u"访问 (%s) 的企业年报信息，期望输出参数 %s")
        key = u"qynb_%s_html" % self.value_dict['nb_name']
        self.appendWebContent(key, web)
        if not web: return
        self.parseOutput(module.outputs, web.body)
        if self.parse_on:
            self.parseHtmlTable(u"解析（%s）的企业年报信息")

    def resultCollect(self, module):
        """
        抓取结果收集，调用ParserMapper实现映射
        :param module:
        :return:
        """
        if 'company' in self.result_dict and self.parse_on:
            result_list = self.result_dict['company']
            company_mapped = ParserMapper.doMap(mapper.transform, result_list)
            self.result_dict['company_mapped'] = company_mapped
        self.resultDelivery(module)
        pass

    def resultDelivery(self, module):
        """
        1.清理中间结果集
        2.标识页面内容抓取状态类型
        3.调用callback交付结果
        :param module:
        :return:
        """
        if 'company_mapped' in self.result_dict:
            company_mapped = self.result_dict['company_mapped']
        else:
            company_mapped = None
        self.cleanWebContents()
        html_dict_wrapped = self.wrapReturnObject()
        self.page_list.append(self.page_dict)
        self.page_dict = dict()
        self.result_list.append(self.result_dict)
        self.result_dict = dict()
        self.callback(html_dict_wrapped, company_mapped)
        pass

    def visitTopInfoJson(self, module):
        """
        访问页面顶部json结果
        :param module:
        :return:
        """
        web = self.fetchJson(module, u"访问 (%s) 的Top信息，期望输出参数 %s")
        self.appendWebContent(u'top_json', web)

    def visitJbxxJson(self, module):
        """
        访问基本信息json结果
        :param module:
        :return:
        """
        web = self.fetchJson(module, u"访问 (%s) 的基本信息，期望输出参数 %s")
        self.appendWebContent(u'jbxx_json', web)
        if self.parse_jbxx_on:
            self.parseJson(module)

    def visitGdxxJson(self, module):
        """
        访问股东信息json结果
        :param module:
        :return:
        """
        if module.web_content:
            if module.web_content in self.value_dict:
                body = self.value_dict[module.web_content]
            else:
                body = module.web_content
            web = WebContent(status_code=200, body=body, content_type=WebContentType.JSON)
        else:
            web = self.fetchJson(module, u"访问 (%s) 的股东信息，期望输出参数 %s")
        self.appendWebContent(u'gdxx_json', web)
        # 当json内容是由上级模块解析生成，但body为None，说明未解析出需要的输出但不代表是异常状态，例如：长白山森工集团安图林业有限公司安林物流中心分公司
        if module.web_content and body is None:
            return
        if self.parse_gdxx_on:
            gdxx_list = self.parseJson(module, web.body)
            self.value_dict['gdxx_list'] = gdxx_list

    def visitGdxqJson(self, module):
        """
        访问股东详情信息json结果
        :param module:
        :return:
        """
        web = self.fetchJson(module, u"访问 (%s) 的股东详情信息，期望输出参数 %s")
        self.appendWebContent(u'gdxq_json', web)

    def visitBgxxJson(self, module):
        """
        访问变更信息json结果
        :param module:
        :return:
        """
        if module.web_content:
            if module.web_content in self.value_dict:
                body = self.value_dict[module.web_content]
            else:
                body = module.web_content
            web = WebContent(status_code=200, body=body, content_type=WebContentType.JSON)
        else:
            web = self.fetchJson(module, u"访问 (%s) 的变更信息，期望输出参数 %s")
        self.appendWebContent(u'bgxx_json', web)
        if self.parse_on:
            self.parseJson(module, web.body)

    def visitBaxxJson(self, module):
        """
        访问备案信息json结果
        :param module:
        :return:
        """
        web = self.fetchJson(module, u"访问 (%s) 的备案信息，期望输出参数 %s")
        self.appendWebContent(u'baxx_json', web)
        if self.parse_on:
            self.parseJson(module)

    def visitFzjgJson(self, module):
        """
        访问分支机构json结果
        :param module:
        :return:
        """
        web = self.fetchJson(module, u"访问 (%s) 的分支机构信息，期望输出参数 %s")
        self.appendWebContent(u'fzjg_json', web)
        if self.parse_on:
            self.parseJson(module)

    def visitXzcfJson(self, module):
        """
        访问行政处罚json结果
        :param module:
        :return:
        """
        web = self.fetchJson(module, u"访问 (%s) 的行政处罚信息，期望输出参数 %s")
        self.appendWebContent(u'xzcf_json', web)
        if self.parse_on:
            self.parseJson(module)

    def visitQynbJson(self, module):
        """
        访问企业年报json结果
        :param module:
        :return:
        """
        web = self.fetchJson(module, u"访问 (%s) 的企业年报信息，期望输出参数 %s")
        key = u"qynb_%s_json" % self.value_dict['nb_name']
        self.appendWebContent(key, web)
        if self.parse_on:
            self.parseJson(module)

    def getWebHtml(self, module):
        """
        访问获取html页面内容通用模块方法
        :param module:
        :return:
        """
        self.value_dict['html'] = None
        self.value_dict['web'] = None
        url, headers, method, post_data = module.getHttpInput(self.value_dict, self.holder.logging)
        if not url:
            self.holder.logging.warn(u"缺少url参数")
            return None
        encoding = module.getInputByType(InputType.ENCODING, self.value_dict, self.holder.logging)
        accept_code = module.getInputByType(InputType.STATUS_CODE, self.value_dict, self.holder.logging)
        self.holder.logging.info(u"访问%s，获取输出参数 %s" % (url, module.outputsDescription()))
        self.setCookie(module)
        web = crawler_util.request(downloader=self.downloader,
                                   url=url,
                                   method=method,
                                   headers=headers,
                                   data=post_data,
                                   encoding=encoding,
                                   ua=self.holder.ua,
                                   use_proxy=module.use_proxy,
                                   holder=self.holder,
                                   accept_code=accept_code)
        # 模块休眠
        crawler_util.moduleSleep(module, self.holder)
        self.htmlContentCheck(web)
        module.detectWebContent(web=web, log=self.holder.logging)
        self.value_dict['html'] = web.body if web else None
        self.value_dict['web'] = web
        if web and web.body:
            self.parseOutput(module.outputs, web.body)
        self.htmlContentCheck(web)

    def getJson(self, module):
        """
        访问获取json页面内容通用模块方法
        :param module:
        :return:
        """
        self.value_dict['json'] = None
        self.value_dict['web'] = None
        search_company = self.value_dict.get('search_company', '')
        self.holder.logging.info(u"访问json信息[company_key=%s]，获取输出参数 %s" % (search_company, module.outputsDescription()))
        url, headers, method, post_data = module.getHttpInput(self.value_dict, self.holder.logging)
        if not url:
            self.holder.logging.warn(u"缺少url参数")
            return None
        encoding = module.getInputByType(InputType.ENCODING, self.value_dict, self.holder.logging)
        accept_code = module.getInputByType(InputType.STATUS_CODE, self.value_dict, self.holder.logging)
        self.setCookie(module)
        web = crawler_util.request(downloader=self.downloader,
                                   url=url,
                                   method=method,
                                   headers=headers,
                                   data=post_data,
                                   encoding=encoding,
                                   ua=self.holder.ua,
                                   use_proxy=module.use_proxy,
                                   holder=self.holder,
                                   accept_code=accept_code)
        # 模块休眠
        crawler_util.moduleSleep(module, self.holder)
        web.content_type = WebContentType.JSON
        self.jsonContentCheck(web)
        module.detectWebContent(web=web, log=self.holder.logging)
        body = web.body if web.body else ''
        self.holder.logging.info(u"本次json抓取结果：\n"+body)
        if body:
            json_data = json.loads(web.body)
            self.value_dict['json'] = json_data
        self.value_dict['web'] = web
        return web

# endregion

# region 抓取页面内容

    def fetchWebContent(self, module, prompt_info, is_pic=False):
        """
        抓取搜索列表之前页面
        :param module:
        :param prompt_info: 提示信息
        :param is_pic: 是否是获取图片
        :return:
        """
        self.value_dict["html"] = None
        self.value_dict['web'] = None
        self.holder.logging.info(prompt_info % module.outputsDescription())
        url, headers, method, post_data = module.getHttpInput(self.value_dict, self.holder.logging)
        if not url:
            self.holder.logging.warn(u"缺少url参数")
            return None
        elif url == OutputType.NONE_TYPE:
            return None
        encoding = module.getInputByType(InputType.ENCODING, self.value_dict, self.holder.logging)
        accept_code = module.getInputByType(InputType.STATUS_CODE, self.value_dict, self.holder.logging)
        self.setCookie(module)
        web = crawler_util.request(downloader=self.downloader,
                                   url=url,
                                   method=method,
                                   headers=headers,
                                   data=post_data,
                                   encoding=encoding,
                                   ua=self.holder.ua,
                                   is_pic=is_pic,
                                   use_proxy=module.use_proxy,
                                   holder=self.holder,
                                   accept_code=accept_code)
        # 模块休眠
        crawler_util.moduleSleep(module, self.holder)
        self.htmlContentCheck(web)
        redo_module = self.module_manager.getFirstModule()
        module.detectWebContent(web=web, redo_module=redo_module.module_id, log=self.holder.logging)
        self.value_dict['html'] = web.body if web else None
        self.value_dict['web'] = web
        return web

    def fetchSpecificCompany(self, module, prompt_info):
        """
        抓取具体公司信息页面
        :param module:
        :param prompt_info: 提示信息
        :return:
        """
        self.value_dict["html"] = None
        self.value_dict['web'] = None
        search_company = self.value_dict.get('search_company', '')
        self.holder.logging.info(prompt_info % (search_company, module.outputsDescription()))
        url, headers, method, post_data = module.getHttpInput(self.value_dict, self.holder.logging)
        if not url:
            self.holder.logging.warn(u"缺少url参数")
            return None
        # 存在输入url在某种情况下为空的情况(广东-深圳信用)
        elif url == OutputType.NONE_TYPE:
            return None
        encoding = module.getInputByType(InputType.ENCODING, self.value_dict, self.holder.logging)
        accept_code = module.getInputByType(InputType.STATUS_CODE, self.value_dict, self.holder.logging)
        self.setCookie(module)
        web = crawler_util.request(downloader=self.downloader,
                                   url=url,
                                   method=method,
                                   headers=headers,
                                   data=post_data,
                                   encoding=encoding,
                                   ua=self.holder.ua,
                                   use_proxy=module.use_proxy,
                                   holder=self.holder,
                                   accept_code=accept_code)
        # 模块休眠
        crawler_util.moduleSleep(module, self.holder)
        self.htmlContentCheck(web)
        module.detectWebContent(web=web, log=self.holder.logging)
        self.value_dict['html'] = web.body if web else None
        self.value_dict['web'] = web
        return web

    def fetchJson(self, module, prompt_info):
        """
        抓取json页面
        :param module:
        :param prompt_info:
        :return:
        """
        self.value_dict['json'] = None
        search_company = self.value_dict.get('search_company', '')
        self.holder.logging.info(prompt_info % (search_company, module.outputsDescription()))
        web = self.getJson(module)
        return web

    def setCookie(self, module):
        cookie = module.getInputByType(InputType.COOKIE, self.value_dict, self.holder.logging)
        if cookie:
            self.downloader.cookieUpdate(cookie)

# endregion

# region 解析模块输出、html页面、json页面及股东详情信息

    def parseOutput(self, outputs, html):
        """
        解析模块输出
        :param outputs:模块所需要的输出
        :param html: 页面内容
        :return:
        """
        if not html or not outputs:
            return
        tree = etree.HTML(html)
        for output in outputs:
            if tree and output.xpath:
                if output.type == OutputType.LIST:
                    result = tree.xpath(output.xpath)
                else:
                    result = "".join(tree.xpath(output.xpath))
            elif output.regex:
                if output.type == OutputType.LIST:
                    result = re.findall(output.regex, html)
                else:
                    result = "".join(re.findall(output.regex, html))
            else:
                continue
            # 自动合并同名list中间结果
            if output.name in self.value_dict and isinstance(self.value_dict[output.name], list) and isinstance(result, list):
                self.value_dict[output.name].extend(result)
            else:
                self.value_dict[output.name] = result

    def parseHtmlTable(self, prompt_info, should_collect_result=True):
        """
        解析html table型的数据，解析为键值对的标准形式
        :param prompt_info: 提示信息
        :param should_collect_result:是否需要收集本次解析结果到结果集中
        :return:
        """
        search_company = self.value_dict.get('search_company', '')
        self.holder.logging.info(prompt_info % search_company)

        if 'company' not in self.result_dict:
            self.result_dict['company'] = list()
        if 'html' not in self.value_dict or not self.value_dict['html']:
            raise Exception(u"未获取到html页面")
        html = self.value_dict['html']
        parser = TableParseUtil(html)
        info_list = parser.parse()
        self.holder.logging.info(u"本次模块解析结果：\n %s", json.dumps(info_list))
        # 获取股东详情的情况下不应该加入，而应update
        if should_collect_result:
            self.result_dict['company'].extend(info_list)
        return info_list

    def parseJson(self, module, json_obj=None):
        """
        解析json页面内容
        :param module:
        :return:
        """
        if 'json' in self.value_dict:
            json_obj = self.value_dict['json']
        # 此处判断不能简化，需要区分空list和None
        elif json_obj is None:
            # raise Exception("未获取到json页面")  # 存在网站原因缺少某些信息，例如：长白山森工集团安图林业有限公司安林物流中心分公司，页面上完全无备案信息、分支机构的展示
            self.holder.logging.error(u"未获取到json页面!!!")
            return None
        if isinstance(json_obj, basestring):
            json_obj = json.loads(json_obj)
        if not json_obj:
            if isinstance(json_obj, list):
                self.holder.logging.warn(u"成功得到了json页面内容，但json体为空！")
            else:
                self.holder.logging.error(u"未获取到json页面!!!")
            return None
        parser = JsonParseUtil()
        info_list = parser.parse(json_obj, module.mapper_config)
        if not info_list:
            return None
        if 'company' not in self.result_dict:
            self.result_dict['company'] = list()
        self.result_dict['company'].extend(info_list)
        self.holder.logging.info(u"本次模块解析结果：\n %s", json.dumps(info_list))
        return info_list

    def parseGdxq(self):
        """
        解析股东详情信息内容
        :return:
        """
        gdxq_list = self.parseHtmlTable(u"解析（%s）的股东详情信息", False)

        if not gdxq_list or len(gdxq_list) == 0:
            self.holder.logging.info(u"未获取到股东详情信息")
            return
        if 'gdxx_rcd' not in self.value_dict:
            return
        gdxx_rcd = self.value_dict['gdxx_rcd']
        if not gdxx_rcd or not isinstance(gdxx_rcd, dict):
            return
        for key in gdxx_rcd:
            try:
                if isinstance(eval(gdxx_rcd[key]), dict):
                    gdxx_rcd[key] = gdxq_list[0]
                    return
            except Exception as e:
                self.holder.logging.warn(e.message)
        key = ''
        for rcd_key in gdxx_rcd.keys():
            if '.' not in rcd_key:
                continue
            keys = rcd_key.split('.')
            key = ''
            if len(keys) >= 2:
                for i in range(0, len(keys)-1):
                    key += keys[i]+'.'
            if key:
                break
        key += u'详情'
        gdxx_rcd[key] = gdxq_list[0]

# endregion

#region 中间结果状态的保存与恢复

    def snapshot(self, snap_id):
        """
        存储当前中间状态
        :param snap_id: 需保存的中间状态id
        :return:
        """
        self.value_dict_snap[snap_id] = copy.deepcopy(self.value_dict)

    def recoverFromSnapshot(self, snap_id):
        """
        从之前保存的中间状态中恢复
        :param snap_id: 待恢复的中间状态id
        :return:
        """
        if not snap_id or snap_id not in self.value_dict_snap:
            self.holder.logging.warning("snap id %s not exist!!" % snap_id)
            return
        self.value_dict = self.value_dict_snap[snap_id]

#endregion

# region Web页面内容检查

    def htmlContentCheck(self, web):
        """
        验证并封装页面
        :param web:
        :return:
        """
        self.WebKeywordCheck(web, self.html_check_dict)

    def jsonContentCheck(self, web):
        """
        验证并封装页面
        :param web:
        :return:
        """
        self.WebKeywordCheck(web, self.json_check_dict)

    def WebKeywordCheck(self, web, check_dict):
        """
        验证并封装页面
        :param web:
        :param check_dict:
        :return:
        """
        if web.access_type != WebAccessType.OK:
            return
        if not web.body:
            web.access_type = WebAccessType.NO_CONTENT
            return
        if not web.access_type:
            web.access_type = WebAccessType.OK
        if not check_dict:
            return
        for key in check_dict:
            if key in web.body:
                # 后面配置会覆盖前面配置类型
                web.access_type = check_dict[key]
                self.holder.logging.info(u"页面因包含 '%s' 被识别为类型 %s" % (key,WebAccessType.description(check_dict[key])))
        return web

# endregion

# region WebContent相关处理
    def appendWebContent(self, name, web):
        """
        追加页面内容到页面结果集中
        :param name:
        :param web:
        :return:
        """
        if name not in self.page_dict:
            self.page_dict[name] = list()
        self.page_dict[name].append(web)

    def cleanWebContents(self):
        """
        1.清理掉页面结果中的None及重试出错的页面
        2.生成该公司抓取情况类型
        :return:
        """
        if not self.page_dict:
            self.page_dict['status'] = CompanyAccessType.ERROR
            return
        success_num = 0
        failed_num = 0
        for key in self.page_dict:
            values = self.page_dict[key]
            if not isinstance(values, list):
                continue
            if not values:
                failed_num += 1
                continue
            req_md5_set = set()
            i = len(values)-1
            while i >= 0:
                val = values[i]
                if not val:
                    del values[i]
                elif val.req_md5 in req_md5_set:
                    del values[i]
                else:
                    req_md5_set.add(val.req_md5)
                    # 暂对股东详情不做要求
                    if val.status_code >= 400 and key != u'gdxq_html':
                        failed_num += 1
                    else:
                        success_num += 1
                i -= 1
        # 过滤掉空值
        self.page_dict = dict(filter(lambda item: item[1], self.page_dict.items()))
        if success_num > 0 and failed_num == 0:
            self.page_dict['status'] = CompanyAccessType.OK
        elif success_num > 0:
            self.page_dict['status'] = CompanyAccessType.INCOMPLETE
        else:
            self.page_dict['status'] = CompanyAccessType.ERROR

    def wrapReturnObject(self):
        """
        封装web内容结果集返回给外部callback
        :return:
        """
        # 所有子类调用existQynbList方法后，此处设置rowkey逻辑可以去掉
        if 'rowkey_dict' not in self.page_dict:
            success = self.setRowKey()
            if not success:
                self.holder.logging.error(u"提取rowkey参数出错！")
        html_dict_copy = copy.deepcopy(self.page_dict)
        for hk,hv in html_dict_copy.items():
            if isinstance(hv, list):
                v_list = filter(lambda x: isinstance(x, WebContent), hv)
                v_dict_list = map(lambda x: x.toDictionary(), v_list)
                html_dict_copy[hk] = v_dict_list
        return html_dict_copy

# endregion
    def bypassQynb(self):
        """
        判断年报是否需要抓取以及哪些年份已被抓取
        :return: 是否访问年报信息，True=不访问，False=访问，set()：哪些年份不需要访问
        """
        # 抓取年报信息需要依赖rowkey，放在此处设置
        success = self.setRowKey()
        if not success:
            self.holder.logging.error(u"提取rowkey参数出错！")
            should_visit,has_years = True,set()
        else:
            should_visit, has_years = self.nb_judge.visitJudgement(company_name=self.page_dict['rowkey_dict']['company_name'],
                                                                   company_zch=self.page_dict['rowkey_dict']['company_zch'])
        self.value_dict['qynb_should_visit'] = should_visit
        self.value_dict['qynb_has_years'] = has_years
        return not should_visit

    def filterQynbList(self, nb_list):
        """
        清理年报列表，将不需要抓取的年份清除出去
        :param nb_list: 年报列表，每一项必须是一个包含年份数据的标签，否则需要子类提供
        :return:
        """
        should_visit = self.value_dict.get('qynb_should_visit','')
        has_years = self.value_dict.get('qynb_has_years',set())
        if not should_visit:
            del nb_list[:]
            return
        temp_list = list(nb_list)
        for nb in temp_list:
            arr = re.findall('\d{4}', ''.join(nb.xpath('text()')))
            if not arr:
                nb_list.remove(nb)
                continue
            if arr[0] in has_years:
                nb_list.remove(nb)

    def yzmSave(self, yzm, img_path):
        """
        保存验证码，子类根据需要进行调用
        :param img_path:
        :return:
        """
        record_success(self.pinyin, yzm, img_path, self.holder)
        pass

    def getMonitorMiddleValues(self, module):
        """
        获取被监视的中间结果
        :param module:
        :return:
        """
        if not module.monitor_values:
            return None
        mm_dict = dict()
        for key in module.monitor_values:
            mm_dict[key] = self.value_dict.get(key, None)
        return mm_dict

    def seedReport(self):
        """
        生成种子抓取情况报告
        :return:
        """
        try:
            if self.report.access_type == SeedAccessType.NON_COMPANY or self.report.access_type == SeedAccessType.NO_VALID_COMPANY:
                return
            for page_dict in self.page_list:
                if not page_dict or 'status' not in page_dict:
                    self.report.failed_num += 1
                elif page_dict['status'] == CompanyAccessType.OK:
                    self.report.success_num += 1
                else:
                    self.report.failed_num += 1
            if self.report.success_num > 0 and self.report.failed_num == 0:
                self.report.access_type = SeedAccessType.OK
            elif self.report.success_num > 0:
                self.report.access_type = SeedAccessType.INCOMPLETE
            elif self.report.access_type == SeedAccessType.NO_TARGET_SOURCE:
                return
            else:
                self.report.access_type = SeedAccessType.ERROR
        except Exception as e:
            self.holder.logging.error(e.message)


if __name__ == '__main__':
    pass