# -*- coding: utf-8 -*-
# Created by John on 2016/5/27.

import sys
import random
import time
import re
import urlparse
reload(sys)
sys.path.append('../')
sys.setdefaultencoding("UTF-8")
sys.path.append('./util')
from CrawlerBase import CrawlerBase
from lxml import etree
from ModuleManager import Module,Event,Iterator,Sleep,Bypass
from util.crawler_util import CrawlerRunMode, InputType, OutputType, EventType, OutputParameterShowUpType
from CommonLib.WebContent import WebAccessType, SeedAccessType

class CrawlerGuizhou(CrawlerBase):
    def __init__(self, pinyin, callbackFromOuterControl):
        config_dict = dict()
        config_dict[CrawlerRunMode.COMPANY_KEY] = [self.initPVCheck, self.initValidateCode, self.getSereachList,
                                                   self.fetchCompanyInfo]

        check_dict = dict()
        # check_dict的中文不能使用unicode,否则WebKeywordCheck检查会抛异常
        check_dict["html_check_dict"] = {"过于频繁": WebAccessType.TOO_OFTEN, "非正常访问": WebAccessType.ACCESS_VIOLATION}
        # check_dict['json_check_dict'] = {'验证码输入不正确': WebAccessType.VALIDATE_FAILED }
        CrawlerBase.__init__(self, pinyin, config_dict, check_dict, callbackFromOuterControl)

        # 打开基本信息解析开关
        self.parse_jbxx_on = True
        # 临时打开其他解析开关，便于观察抓取情况
        self.parse_on = True
        pass

    # Module initPVCheck Start
    # PV验证不是必须步骤,但如果PV验证都没有通过,则后续步骤的抓取也会失败,所以保留
    def initPVCheck(self):
        module = Module(self.getJson, u"PV验证")
        module.module_id = "positive_vetting_check"

        module.appendUrl("http://gsxt.gzgs.gov.cn/search!pv.shtml")
        module.appendHeaders({
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:33.0) Gecko/20100101 Firefox/33.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3",
            "Accept-Encoding": "gzip, deflate",
            "Host": "gsxt.gzgs.gov.cn",
            "Origin": "http://gsxt.saic.gov.cn/",
            "Connection": "keep-alive"
        })
        module.appendWebMethod("post")
        module.appendPostData({"sys": 1,
                               "pg": "http://gsxt.gzgs.gov.cn/",
                               "rf": "http://gsxt.gzgs.gov.cn/"
                               })

        # 检查PV验证的返回结果
        # 返回数据格式: {"successed":true}
        # loads之后的数据为:{u'successed': True}
        def checkPV(json = None):
            if not json:
                return False
            else:
                if not json["successed"]:
                    self.holder.logging.warning(u'PV验证失败,更换代理')
                    self.downloader.insertBlack()
                return json["successed"]

        module.addSleep(Sleep(2))
        module.addEvent(Event(EventType.ASSERT_FAILED, assert_function=checkPV, retry_times=100))

        self.module_manager.appendSubModule(module, supportDefaultEvent=True)
    # Module initPVCheck End

    # Module initValidateCode Start
    def initValidateCode(self):
        module = Module(self.visitValidateCode, u"获取验证码")
        module.module_id = "init_validate_code"

        module.appendUrl("http://gsxt.gzgs.gov.cn/search!generateCode.shtml?validTag=searchImageCode&" + str(random.random()))
        module.appendHeaders({
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:33.0) Gecko/20100101 Firefox/33.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3",
            "Accept-Encoding": "gzip, deflate",
            "Host": "gsxt.gzgs.gov.cn",
            "Origin": "http://gsxt.saic.gov.cn/",
            "Connection": "keep-alive"
        })
        module.addSleep(Sleep(2))

        module.addEvent(Event(EventType.EXCEPTION_OCCURED, retry_times=100))

        self.module_manager.appendSubModule(module)
    # Module initValidateCode End

    # Module getSereachList Start
    def getSereachList(self):
        module = Module(self.getJson, u"抓取公司列表")
        module.module_id = "get_search_list"

        module.appendUrl("http://gsxt.gzgs.gov.cn/search!searchSczt.shtml?random=" + str(int(time.time()) * 100))
        module.appendHeaders({
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:33.0) Gecko/20100101 Firefox/33.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
            "Accept-Language": "zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3",
            "Accept-Encoding": "gzip, deflate",
            "Host": "gsxt.gzgs.gov.cn",
            "Origin": "http://gsxt.gzgs.gov.cn/list.jsp",
            "Connection": "keep-alive"
        })
        module.appendWebMethod("post")
        module.appendEncoding("utf-8")
        module.appendPostData(lambda yzm, company_key: {"q": company_key, "validCode": yzm})
        module.addSleep(Sleep(2))

        # 从返回的JSON数据中获取结果:1. 验证码验证结果; 2. 验证码错误提示; 3. 搜索列表
        def getReturnedValue(json = None, web = None):
            query_dict = {}

            # 检查代理有效性
            if u'数据查询中' in web.body:
                query_dict["proxy_err"] = True
                return query_dict

            # 把以下参数置为None,防止REDO时影响正确执行
            key_name = ['yzm_err', 'yzm_msg', 'no_company', 'company_list']
            key_value = map(lambda key: {key: None}, key_name)
            map(lambda x: query_dict.update(x), key_value)

            if json:
                if json["successed"]:
                    if not json["count"]:
                        query_dict["no_company"] = True
                    else:
                        query_dict["company_list"] = json["data"]

                else:
                    query_dict["yzm_err"] = True
                    query_dict["yzm_msg"] = json["message"]

            return query_dict

        # 检查是否需要更换代理
        def checkProxy(proxy_err = None):
            if proxy_err:
                self.holder.logging.warning(u'代理不可用,被封锁,更换代理')
                self.downloader.insertBlack()
                return False
            else:
                return True

        # 检查验证码正确性
        def checkValidateCode(yzm_err = None, yzm_msg = None):
            if yzm_err and yzm_msg:
                self.holder.logging.warning(yzm_msg)
                return False
            else:
                return True

        # 检查公司列表
        def checkCompanyList(no_company = None, company_list = None):
            if no_company or not company_list:
                self.report.access_type = SeedAccessType.NON_COMPANY
                self.holder.logging.warning(u"抓取公司列表->无此公司")
                return False
            return True

        module.appendOutput(type=OutputType.FUNCTION, function=getReturnedValue)

        # 检查是否需要更换代理,如果需要则从新执行验证码模块
        module.addEvent(Event(EventType.ASSERT_FAILED, retry_times=50, assert_function=checkProxy, redo_module="init_validate_code"))
        # 如果验证码输入不正确,断言失败,重新执行获取验证码模块(默认重试五次)
        module.addEvent(Event(EventType.ASSERT_FAILED, retry_times=50, assert_function=checkValidateCode, redo_module="init_validate_code"))
        module.addEvent(Event(EventType.EXCEPTION_OCCURED, retry_times=100, redo_module="init_validate_code"))
        module.addEvent(Event(EventType.OUTPUT_NOT_SATISFIED, retry_times=100, redo_module="init_validate_code"))
        # 验证码输入正确,如果公司列表还是为空,重试一次后结束当前搜索链(不能重试当前模块,验证码可能已经失效,会导致checkValidateCode必然返回False)
        module.addEvent(Event(EventType.ASSERT_FAILED, retry_times=50, assert_function=checkCompanyList, redo_module="init_validate_code"))

        self.module_manager.appendSubModule(module)
    # Module getSereachList End

    # Module fetchCompanyInfo Start
    # 创建迭代器,依次抓取每个公司对应信息
    def fetchCompanyInfo(self):
        iterator = Iterator("company_list", "com")
        module = Module(None, u"抓取公司", iterator)

        self.module_manager.appendSubModule(module, True)

        self.prepareCompanyParms(module)
        self.getCompanyTopInfo(module)
        self.getCompanyBaseInfo(module)
        self.fetchStockHolderInfo(module)
        self.getCompanyChangeInfo(module)
        self.getCompanyRecordInfo(module)
        self.getCompanyBranchInfo(module)
        self.getCompanyPunishInfo(module)
        self.fetchCompanyAnnalsInfo(module)
        self.collectResult(module)
    # Module fetchCompanyInfo End

    # Module prepareCompanyParms Start
    def prepareCompanyParms(self, module_super):
        module = Module(None, u"抓取公司-预处理")

        # 准备后续模块需要的必要参数
        def prepareParms(com = None):
            query_dict = {}

            key_name = ['post_type', 'nbxh', 'qymc', 'zch', 'company_name', 'company_zch', 'search_company']
            key_value = map(lambda key: {key: None}, key_name)
            map(lambda x: query_dict.update(x), key_value)

            try:
                if com and len(com) >= 10:
                    query_dict["post_type"] = self.getPostType(com["ztlx"], com["qylx"])
                    query_dict["nbxh"] = com["nbxh"]
                    query_dict["qymc"] = com["qymc"]
                    query_dict["zch"] = com["zch"]
                    query_dict["company_name"] = com["qymc"]
                    query_dict["company_zch"] = com["zch"]
                    query_dict["search_company"] = com["qymc"]
            except Exception as e:
                map(lambda x: query_dict.update(x), key_value)

            return query_dict

        # 如果函数prepareParms执行异常,则只需要检查第一个参数即可
        def checkPreparedInfo(post_type = None):
            if not post_type:
                self.holder.logging.warning(u"抓取公司-预处理: 参数准备出错")
                return False
            else:
                return True

        module.appendOutput(type=OutputType.FUNCTION, function=prepareParms)
        # 如果获取公司列表失败,则只需要从校验验证码模块开始,PV验证不需要重复执行
        module.addEvent(Event(EventType.ASSERT_FAILED, retry_times=50, assert_function=checkPreparedInfo, redo_module="init_validate_code"))

        module_super.appendSubModule(module, True)
    # Module prepareCompanyParms End

    # Module getCompanyTopInfo Start
    def getCompanyTopInfo(self, module_super):
        module = Module(self.visitTopInfo, u"抓取公司-首页信息")

        module.appendUrl(lambda post_type: "http://gsxt.gzgs.gov.cn/%s/index.jsp" % post_type)
        module.appendHeaders({
            'Host': 'gsxt.gzgs.gov.cn',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
            'Referer': 'http://gsxt.gzgs.gov.cn/list.jsp',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded'
        })
        module.appendWebMethod("post")
        module.appendPostData(lambda nbxh, qymc, zch: {"nbxh": nbxh, "qymc": qymc, "zch": zch})
        module.addSleep(Sleep(2))

        def checkReturnedHTML(html = None):
            if not html:
                return False
            if len(html) < 10:
                self.holder.logging.warning(u"抓取公司-首页信息: 抓取HTML失败")
                return False
            return True

        module.addEvent(Event(EventType.ASSERT_FAILED, retry_times=100, assert_function=checkReturnedHTML))

        # 从公司首页获取后续模块需要的参数信息
        module.appendOutput(type=OutputType.FUNCTION, function=self.getCompanyJbxxParms)
        module.appendOutput(type=OutputType.FUNCTION, function=self.getCompanyGdxxParms)
        module.appendOutput(type=OutputType.FUNCTION, function=self.getCompanyBgxxParms)
        module.appendOutput(type=OutputType.FUNCTION, function=self.getCompanyBaxxParms)
        module.appendOutput(type=OutputType.FUNCTION, function=self.getCompanyXzcfParms)
        module.appendOutput(type=OutputType.FUNCTION, function=self.getCompanyAnnalsIterator)

        module_super.appendSubModule(module, True)

        # 判断后续模块是否需要略过
        module.appendBypass(Bypass(condition_fuc=self.checkJbxxParms, module_id="fetch_base_info", range_global=True))
        module.appendBypass(Bypass(condition_fuc=self.checkGdxxParms, module_id="fetch_stock_holder_info", range_global=True))
        module.appendBypass(Bypass(condition_fuc=self.checkBgxxParms, module_id="get_company_change_info", range_global=True))
        module.appendBypass(Bypass(condition_fuc=self.checkBaxxParms, module_id="get_company_record_info", range_global=True))
        module.appendBypass(Bypass(condition_fuc=self.checkFzjgxxParms, module_id="get_company_branch_info", range_global=True))
        module.appendBypass(Bypass(condition_fuc=self.checkXzcfxxParms, module_id="get_company_punish_info", range_global=True))

        # module_super.appendSubModule(module, True)
        # Module getCompanyTopInfo End

    # Module getCompanyBaseInfo Start
    def getCompanyBaseInfo(self, module_super):
        module = Module(self.visitJbxxJson, u"抓取公司-基本信息")
        module.module_id = "fetch_base_info"

        module.appendUrl(lambda post_type: "http://gsxt.gzgs.gov.cn/%s/search!searchData.shtml" % post_type)
        module.appendHeaders(lambda post_type: {
            'Host': 'gsxt.gzgs.gov.cn',
            'Accept': 'application/json, text/javascript, */*',
            'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'X-Requested-With': 'XMLHttpRequest',
            'Referer': 'http://gsxt.gzgs.gov.cn/%s/index.jsp' % post_type,
            'Connection': 'keep-alive',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache'
        })
        module.appendWebMethod('post')
        module.appendEncoding('utf-8')
        module.appendPostData(lambda jbxxc, jbxxt, nbxh: {"c": jbxxc, "t": jbxxt, "nbxh": nbxh})
        module.addSleep(Sleep(2))

        module.addEvent(Event(EventType.ASSERT_FAILED, retry_times=50, assert_function=self.checkReturnedResults))

        module_super.appendSubModule(module, True)
    # Module getCompanyBaseInfo End

    # Module fetchStockHolderInfo Start
    def fetchStockHolderInfo(self, module_super):
        # 此处的gd_parms只用作迭代标志,为了让可能存在的股东信息以及股东详情作为一个整体模块,可以被上一个模块bypass
        iterator = Iterator("gd_parms", "com")
        module = Module(None, u"抓取公司-股东信息", iterator)
        module.module_id = "fetch_stock_holder_info"

        module_super.appendSubModule(module, True)

        self.getStockholderInfoAndList(module)
        self.getStockholderTopPage(module)
        self.fetchStockholderDetail(module)
    # Module fetchStockHolderInfo End

    # Module getStockholderInfo Start
    def getStockholderInfoAndList(self, module_super):
        module = Module(self.visitGdxxJson, u"股东信息-股东信息和详情列表")
        module.module_id = "get_stock_holder_list"

        module.appendUrl(lambda post_type: "http://gsxt.gzgs.gov.cn/%s/search!searchData.shtml" % post_type)
        module.appendHeaders(lambda post_type: {
            'Host': 'gsxt.gzgs.gov.cn',
            'Accept': 'application/json, text/javascript, */*',
            'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'X-Requested-With': 'XMLHttpRequest',
            'Referer': 'http://gsxt.gzgs.gov.cn/%s/index.jsp' % post_type,
            'Connection': 'keep-alive',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache'
        })
        module.appendWebMethod("post")
        module.appendEncoding("utf-8")
        module.appendPostData(lambda gdxxc, gdxxt, gdxxnbxh: {"c": gdxxc, "t": gdxxt, "nbxh": gdxxnbxh})
        module.addSleep(Sleep(2))

        def getGdxqList(json = None):
            if not json or "data" not in json:
                return None
            return json["data"]

        def checkGdxqParms(gdxq_list = None):
            if not gdxq_list:
                return True
            return False

        module.appendOutput(name="gdxq_list", type=OutputType.FUNCTION, function=getGdxqList)

        # 检查返回值中successed的状态
        module.addEvent(Event(EventType.ASSERT_FAILED, retry_times=50, assert_function=self.checkReturnedResults))
        module.addEvent(Event(EventType.EXCEPTION_OCCURED, retry_times=50))

        module_super.appendSubModule(module, True)

        module.appendBypass(Bypass(condition_fuc=checkGdxqParms, module_id="get_stock_holder_top_page", range_global=True))
        module.appendBypass(Bypass(condition_fuc=checkGdxqParms, module_id="fetch_stock_holder_detail", range_global=True))
    # Module getStockholderInfo End

    # Module getStockholderTopPage Start
    def getStockholderTopPage(self, module_super):
        module = Module(self.getWebHtml, u"抓取股东详情-首页")
        module.module_id = "get_stock_holder_top_page"

        module.appendUrl(lambda post_type: "http://gsxt.gzgs.gov.cn/%s/tzrxx.jsp" % post_type)
        module.appendHeaders(lambda post_type: {
            'Host': 'gsxt.gzgs.gov.cn',
            'Accept': 'application/json, text/javascript, */*',
            'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'X-Requested-With': 'XMLHttpRequest',
            'Referer': 'http://gsxt.gzgs.gov.cn/%s/index.jsp' % post_type,
            'Connection': 'keep-alive',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache'
        })
        module.appendWebMethod('post')
        module.appendEncoding('utf-8')
        module.appendPostData(lambda nbxh, qymc, zch:
                              {"tzr_nbxh": nbxh, "tzr_czmc": '', "nbxh": nbxh, "qymc": qymc, "zch": zch})
        module.addSleep(Sleep(2))

        def checkReturnedHTML(html = None):
            if not html:
                return False
            if len(html) < 10:
                self.holder.logging.warning(u"抓取股东详情-首页: 抓取HTML失败")
                return False
            return True

        module.addEvent(Event(EventType.ASSERT_FAILED, retry_times=50, assert_function=checkReturnedHTML))

        module.appendOutput(type=OutputType.FUNCTION, function=self.getGdxqParms)
        module.addEvent(Event(EventType.EXCEPTION_OCCURED, retry_times=50))

        module_super.appendSubModule(module, True)

        module.appendBypass(Bypass(condition_fuc=self.checkGdxqParms, module_id="fetch_stock_holder_detail", range_global=True))
    # Module getStockholderTopPage End

    # Module fetchStockholderDetail Start
    def fetchStockholderDetail(self, module_super):
        iterator = Iterator("gdxq_list", "gdxq")
        module = Module(None, u"抓取股东详情", iterator)
        module.module_id = "fetch_stock_holder_detail"

        module_super.appendSubModule(module, True)

        self.prepareStockholderDetail(module)
        # self.getStockholderTopPage(module)
        self.getStockholderDetaiInfo(module)
    # Module fetchStockholderDetail End

    # Module prepareStockholderDetail Start
    def prepareStockholderDetail(self, module_super):
        module = Module(None, u"抓取股东详情-预处理")
        module.module_id = "prepare_stock_holder_detail"

        def prepareParms(gdxq = None):
            query_dict = {}

            try:
                query_dict['czmc'] = None
                if gdxq:
                    query_dict['czmc'] = gdxq['czmc']
            except Exception as e:
                pass

            return query_dict

        # 如果函数prepareParms执行异常,则只需要检查第一个参数即可
        def checkPreparedInfo(czmc = None):
            if not czmc:
                self.holder.logging.warning(u"抓取股东详情-预处理: 无抓取股东详情的必要参数")
                return True
            else:
                return False

        module.appendOutput(type=OutputType.FUNCTION, function=prepareParms)

        module_super.appendSubModule(module, True)

        module.appendBypass(Bypass(condition_fuc=checkPreparedInfo, module_id="get_stock_holder_detail_info", range_global=True))
    # Module prepareStockholderDetail End

    # Module getStockholderDetaiInfo Start
    def getStockholderDetaiInfo(self, module_super):
        module = Module(self.visitGdxqJson, u"抓取股东详情-详情信息")
        module.module_id = "get_stock_holder_detail_info"

        module.appendUrl(lambda post_type: "http://gsxt.gzgs.gov.cn/%s/search!searchTzr.shtml" % post_type)
        module.appendHeaders(lambda post_type: {
            'Host': 'gsxt.gzgs.gov.cn',
            'Accept': 'application/json, text/javascript, */*',
            'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'X-Requested-With': 'XMLHttpRequest',
            'Referer': 'http://gsxt.gzgs.gov.cn/%s/tzrxx.jsp' % post_type,
            'Connection': 'keep-alive',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache'
        })

        module.appendWebMethod('post')
        module.appendEncoding('utf-8')
        module.appendPostData(lambda gdxqc, gdxqt, gdxqnbxh, czmc:
                              {"c": gdxqc, "t": gdxqt, "nbxh": gdxqnbxh, "czmc": czmc})
        module.addSleep(Sleep(2))

        # 检查返回值中successed的状态
        module.addEvent(Event(EventType.ASSERT_FAILED, retry_times=50, assert_function=self.checkReturnedResults))
        module.addEvent(Event(EventType.EXCEPTION_OCCURED, retry_times=50))

        module_super.appendSubModule(module, True)
    # Module getStockholderDetaiInfo End

    # Module getCompanyChangeInfo Start
    def getCompanyChangeInfo(self, module_super):
        module = Module(self.visitBgxxJson, u"抓取公司-变更信息")
        module.module_id = "get_company_change_info"

        module.appendUrl(lambda post_type: "http://gsxt.gzgs.gov.cn/%s/search!searchData.shtml" % post_type)
        module.appendHeaders(lambda post_type: {
            'Host': 'gsxt.gzgs.gov.cn',
            'Accept': 'application/json, text/javascript, */*',
            'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'X-Requested-With': 'XMLHttpRequest',
            'Referer': 'http://gsxt.gzgs.gov.cn/%s/index.jsp' % post_type,
            'Connection': 'keep-alive',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache'
        })
        module.appendWebMethod('post')
        module.appendEncoding('utf-8')

        module.appendPostData(lambda bgxxc=None, bgxxt=None, bgxxnbxh=None:
                              {"c": bgxxc, "t": bgxxt, "nbxh": bgxxnbxh})
        module.addSleep(Sleep(2))

        # 检查返回值中successed的状态
        module.addEvent(Event(EventType.ASSERT_FAILED, retry_times=50, assert_function=self.checkReturnedResults))
        module.addEvent(Event(EventType.EXCEPTION_OCCURED, retry_times=50))

        module_super.appendSubModule(module, True)
    # Module getCompanyChangeInfo End

    # Module getCompanyRecordInfo Start
    def getCompanyRecordInfo(self, module_super):
        module = Module(self.visitBaxxJson, u"抓取公司-备案信息")
        module.module_id = "get_company_record_info"

        module.appendUrl(lambda post_type: "http://gsxt.gzgs.gov.cn/%s/search!searchData.shtml" % post_type)
        module.appendHeaders(lambda post_type: {
            'Host': 'gsxt.gzgs.gov.cn',
            'Accept': 'application/json, text/javascript, */*',
            'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'X-Requested-With': 'XMLHttpRequest',
            'Referer': 'http://gsxt.gzgs.gov.cn/%s/index.jsp' % post_type,
            'Connection': 'keep-alive',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache'
        })
        module.appendWebMethod('post')
        module.appendEncoding('utf-8')

        module.appendPostData(lambda baxxc=None, baxxt=None, baxxnbxh=None:
                              {"c": baxxc, "t": baxxt, "nbxh": baxxnbxh})
        module.addSleep(Sleep(2))

        # 检查备案信息中的内容,如果是全名所有制类型的公司,需要把抓取到的内容加到股东信息中去
        module.appendOutput(type=OutputType.FUNCTION, function=self.checkRecordInfo)
        # 检查返回值中successed的状态
        module.addEvent(Event(EventType.ASSERT_FAILED, retry_times=50, assert_function=self.checkReturnedResults))
        module.addEvent(Event(EventType.EXCEPTION_OCCURED, retry_times=50))

        module_super.appendSubModule(module, True)
    # Module getCompanyRecordInfo End

    # Module getCompanyBranchInfo Start
    def getCompanyBranchInfo(self, module_super):
        module = Module(self.visitFzjgJson, u"抓取公司-分支机构信息")
        module.module_id = "get_company_branch_info"

        module.appendUrl(lambda post_type: "http://gsxt.gzgs.gov.cn/%s/search!searchData.shtml" % post_type)
        module.appendHeaders(lambda post_type: {
            'Host': 'gsxt.gzgs.gov.cn',
            'Accept': 'application/json, text/javascript, */*',
            'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'X-Requested-With': 'XMLHttpRequest',
            'Referer': 'http://gsxt.gzgs.gov.cn/%s/index.jsp' % post_type,
            'Connection': 'keep-alive',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache'
        })
        module.appendWebMethod('post')
        module.appendEncoding('utf-8')
        module.appendPostData(lambda fzjgc=None, fzjgt=None, fzjgnbxh=None:
                              {"c": fzjgc, "t": fzjgt, "nbxh": fzjgnbxh})
        module.addSleep(Sleep(2))

        # 检查返回值中successed的状态
        module.addEvent(Event(EventType.ASSERT_FAILED, retry_times=50, assert_function=self.checkReturnedResults))
        module.addEvent(Event(EventType.EXCEPTION_OCCURED, retry_times=50))

        module_super.appendSubModule(module, True)
    # Module getCompanyBranchInfo End

    # Module getCompanyPunishInfo Start
    def getCompanyPunishInfo(self, module_super):
        module = Module(self.visitXzcfJson, u"抓取公司-行政处罚信息")
        module.module_id = "get_company_punish_info"

        module.appendUrl(lambda post_type: "http://gsxt.gzgs.gov.cn/%s/search!searchData.shtml" % post_type)
        module.appendHeaders(lambda post_type: {
            'Host': 'gsxt.gzgs.gov.cn',
            'Accept': 'application/json, text/javascript, */*',
            'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'X-Requested-With': 'XMLHttpRequest',
            'Referer': 'http://gsxt.gzgs.gov.cn/%s/index.jsp' % post_type,
            'Connection': 'keep-alive',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache'
        })
        module.appendWebMethod('post')
        module.appendEncoding('utf-8')
        module.appendPostData(lambda xzcfc=None, xzcft=None, xzcfnbxh=None:
                              {"c": xzcfc, "t": xzcft, "nbxh": xzcfnbxh})
        module.addSleep(Sleep(2))

        # 检查返回值中successed的状态
        module.addEvent(Event(EventType.ASSERT_FAILED, retry_times=50, assert_function=self.checkReturnedResults))
        module.addEvent(Event(EventType.EXCEPTION_OCCURED, retry_times=50))

        module_super.appendSubModule(module, True)
    # Module getCompanyPunishInfo End

    # Module fetchCompanyAnnalsInfo Start
    def fetchCompanyAnnalsInfo(self, module_super):
        iterator = Iterator("nb_parms", "com")
        module = Module(None, u"抓取公司-抓取年报", iterator)
        module.module_id = "fetch_company_annals_info"

        module_super.appendSubModule(module, True)

        self.getAnnalsListTopPage(module)
        self.getAnnalsList(module)
        self.fetchAnnalsInfo(module)
    # Module fetchCompanyAnnalsInfo End

    # Module getAnnalsTopPage Start
    def getAnnalsListTopPage(self, module_super):
        module = Module(self.getWebHtml, u"抓取年报-列表首页")
        module.module_id = "get_annals_list_top_page"

        module.appendUrl(lambda post_type: "http://gsxt.gzgs.gov.cn/%s/qygs.jsp" % post_type)
        module.appendHeaders(lambda post_type: {
            'Host': 'gsxt.gzgs.gov.cn',
            'Accept': 'application/json, text/javascript, */*',
            'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'X-Requested-With': 'XMLHttpRequest',
            'Referer': 'http://gsxt.gzgs.gov.cn/%s/index.jsp' % post_type,
            'Connection': 'keep-alive',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache'
        })
        module.appendWebMethod('post')
        module.appendEncoding('utf-8')
        module.appendPostData(lambda nbxh=None, qymc=None, zch=None: {"nbxh": nbxh, "qymc": qymc, "zch": zch})
        module.addSleep(Sleep(2))

        # 从年报首页获取访问年报列表需要的参数信息
        module.appendOutput(type=OutputType.FUNCTION, function=self.getAnnalsListParms)

        def checkReturnedHTML(html = None):
            if not html:
                return False
            if len(html) < 10:
                self.holder.logging.warning(u"抓取年报-列表首页失败")
                return False
            return True

        module.addEvent(Event(EventType.ASSERT_FAILED, retry_times=50, assert_function=checkReturnedHTML))

        module_super.appendSubModule(module, True)
    # Module getAnnalsTopPage End

    # Module getAnnalsList Start
    def getAnnalsList(self, module_super):
        module = Module(self.getJson, u"抓取年报-年报列表")
        module.module_id = "get_annals_list"

        module.appendUrl(lambda post_type: "http://gsxt.gzgs.gov.cn/%s/search!searchData.shtml" % post_type)
        module.appendHeaders(lambda post_type: {
            'Host': 'gsxt.gzgs.gov.cn',
            'Accept': 'application/json, text/javascript, */*',
            'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'X-Requested-With': 'XMLHttpRequest',
            'Referer': 'http://gsxt.gzgs.gov.cn/%s/qygs.jsp' % post_type,
            'Connection': 'keep-alive',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache'
        })
        module.appendWebMethod('post')
        module.appendEncoding('utf-8')
        module.appendPostData(lambda nbxxc=None, nbxxt=None, nbxxnbxh=None: {"c": nbxxc, "t": nbxxt, "nbxh": nbxxnbxh})
        module.addSleep(Sleep(2))

        def getReturnedValue(json = None):
            query_dict = {}

            query_dict["annals_list"] = None
            if json and json["successed"]:
                query_dict["annals_list"] = json["data"]

            return query_dict

        def checkAnnalsList(annals_list = None):
            if not annals_list:
                self.holder.logging.warning(u"年报列表为空")
                return True
            else:
                return False

        module.appendOutput(type=OutputType.FUNCTION, function=getReturnedValue)

        # 检查返回值中successed的状态
        module.addEvent(Event(EventType.ASSERT_FAILED, retry_times=50, assert_function=self.checkReturnedResults))
        module.addEvent(Event(EventType.EXCEPTION_OCCURED, retry_times=50))

        module_super.appendSubModule(module, True)

        module.appendBypass(Bypass(condition_fuc=checkAnnalsList, module_id="fetch_annals_info", range_global=True))

    # Module getAnnalsList Start

    # Module fetchAnnalsInfo Start
    def fetchAnnalsInfo(self, module_super):
        iterator = Iterator("annals_list", "annals")
        module = Module(None, u"抓取年报信息", iterator)
        module.module_id = "fetch_annals_info"

        module_super.appendSubModule(module, True)

        self.prepareAnnalsParms(module)
        self.getAnnalsTopPage(module)
        self.getAnnalsBaseInfo(module)
        self.getAnnalsWebsiteInfo(module)
        self.getAnnalsFinancialInfo(module)
        self.getAnnalsInvestmentInfo(module)
        self.getAnnalsContributeInfo(module)
        self.getAnnalsAssuranceInfo(module)
        self.getAnnalEequityUpdateInfo(module)
        self.getAnnalsUpdateInfo(module)
    # Module fetchAnnalsInfo End

    # Module prepareAnnalsParms Start
    def prepareAnnalsParms(self, module_super):
        module = Module(None, u"抓取年报-预处理")

        # 准备后续模块需要的必要参数
        def prepareParms(annals = None):
            query_dict = {}

            key_name = ['nbtopnbxh', 'nbtopnd', 'nbtoplsh', 'nb_name']
            key_value = map(lambda key: {key: None}, key_name)
            map(lambda x: query_dict.update(x), key_value)

            try:
                if annals and len(annals) >= 5:
                    query_dict["nbtopnbxh"] = annals["nbxh"]
                    query_dict["nbtopnd"] = annals["nd"]
                    query_dict["nbtoplsh"] = annals["lsh"]
                    query_dict["nb_name"] = annals["nd"]
            except Exception as e:
                map(lambda x: query_dict.update(x), key_value)

            return query_dict

        module.appendOutput(type=OutputType.FUNCTION, function=prepareParms)

        module_super.appendSubModule(module, True)
    # Module prepareAnnalsParms End

    # Module getAnnalsTopPage Start
    def getAnnalsTopPage(self, module_super):
        module = Module(self.getWebHtml, u"抓取年报-年报首页信息")

        module.appendUrl(lambda post_type: "http://gsxt.gzgs.gov.cn/%s/nbxq.jsp" % post_type)
        module.appendHeaders(lambda post_type: {
            'Host': 'gsxt.gzgs.gov.cn',
            'Accept': 'application/json, text/javascript, */*',
            'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'X-Requested-With': 'XMLHttpRequest',
            'Referer': 'http://gsxt.gzgs.gov.cn/%s/qygs.jsp' % post_type,
            'Connection': 'keep-alive',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache'
        })
        module.appendWebMethod('post')
        module.appendEncoding('utf-8')
        # 此处nbxh必须使用nbxh而不是topnbxh
        module.appendPostData(lambda nbxh=None, qymc=None, zch=None, nbtopnd=None, nbtoplsh=None:
                              {"nbxh": nbxh, "qymc": qymc, "zch": zch, "nd": nbtopnd, "lsh": nbtoplsh})
        module.addSleep(Sleep(2))

        def checkReturnedHTML(html = None):
            if not html:
                return False
            if len(html) < 10:
                self.holder.logging.warning(u"抓取失败: 抓取年报-年报首页信息")
                return False
            return True

        module.addEvent(Event(EventType.ASSERT_FAILED, retry_times=50, assert_function=checkReturnedHTML))

        # 从公司首页获取后续模块需要的参数信息
        module.appendOutput(type=OutputType.FUNCTION, function=self.getAnnalsJbxxParms)#t=14
        module.appendOutput(type=OutputType.FUNCTION, function=self.getAnnalsWzwdParms)#t=15
        module.appendOutput(type=OutputType.FUNCTION, function=self.getAnnalsZczkParms)#t=16
        module.appendOutput(type=OutputType.FUNCTION, function=self.getAnnalsDwtzParms)#t=18
        module.appendOutput(type=OutputType.FUNCTION, function=self.getAnnalsGdczParms)#t=19
        module.appendOutput(type=OutputType.FUNCTION, function=self.getAnnalsDwtgdbParms)#t=24
        module.appendOutput(type=OutputType.FUNCTION, function=self.getAnnalsGqbgParms)#t=39
        module.appendOutput(type=OutputType.FUNCTION, function=self.getAnnalsXgjlParms)#t=41

        module_super.appendSubModule(module, True)

        # 判断后续模块是否需要略过
        module.appendBypass(Bypass(condition_fuc=self.checkAnnalsJbxxParms, module_id="get_annals_base_info", range_global=True))
        module.appendBypass(Bypass(condition_fuc=self.checkAnnalsWzwdParms, module_id="get_annals_website_info", range_global=True))
        module.appendBypass(Bypass(condition_fuc=self.checkAnnalsZczkParms, module_id="get_annals_financial_info", range_global=True))
        module.appendBypass(Bypass(condition_fuc=self.checkAnnalsDwtzParms, module_id="get_annals_investment_info", range_global=True))
        module.appendBypass(Bypass(condition_fuc=self.checkAnnalsGdczParms, module_id="get_annals_contribute_info", range_global=True))
        module.appendBypass(Bypass(condition_fuc=self.checkAnnalsDwtgdbParms, module_id="get_annals_assurance_info", range_global=True))
        module.appendBypass(Bypass(condition_fuc=self.checkAnnalsGqbgParms, module_id="get_annals_equity_update_info", range_global=True))
        module.appendBypass(Bypass(condition_fuc=self.checkAnnalsXgjlParms, module_id="get_annals_update_info", range_global=True))
    # Module getAnnalsTopPage End

    # Module getAnnalsBaseInfo Start
    def getAnnalsBaseInfo(self, module_super):
        module = Module(self.visitQynbJson, u"获取年报-基本信息")
        module.module_id = "get_annals_base_info"

        module.appendUrl(lambda post_type: "http://gsxt.gzgs.gov.cn/%s/search!searchNbxx.shtml" % post_type)
        module.appendHeaders(lambda post_type: {
            'Host': 'gsxt.gzgs.gov.cn',
            'Accept': 'application/json, text/javascript, */*',
            'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'X-Requested-With': 'XMLHttpRequest',
            'Referer': 'http://gsxt.gzgs.gov.cn/%s/nbxq.jsp' % post_type,
            'Connection': 'keep-alive',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache'
        })
        module.appendWebMethod('post')
        module.appendEncoding('utf-8')
        # 此处nbxh必须使用nbxh而不是topnbxh
        module.appendPostData(lambda nbjbxxc=None, nbjbxxt=None, nbxh=None, nbtoplsh=None:
                              {"c": nbjbxxc, "t": nbjbxxt, "nbxh": nbxh, "lsh": nbtoplsh})
        module.addSleep(Sleep(2))

        # 检查返回值中successed的状态
        module.addEvent(Event(EventType.ASSERT_FAILED, retry_times=50, assert_function=self.checkReturnedResults))
        module.addEvent(Event(EventType.EXCEPTION_OCCURED, retry_times=50))

        module_super.appendSubModule(module, True)
    # Module getAnnalsBaseInfo End

    # Module getAnnalsWebsiteInfo Start
    def getAnnalsWebsiteInfo(self, module_super):
        module = Module(self.visitQynbJson, u"获取年报-网站网店信息")
        module.module_id = "get_annals_website_info"

        module.appendUrl(lambda post_type: "http://gsxt.gzgs.gov.cn/%s/search!searchNbxx.shtml" % post_type)
        module.appendHeaders(lambda post_type: {
            'Host': 'gsxt.gzgs.gov.cn',
            'Accept': 'application/json, text/javascript, */*',
            'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'X-Requested-With': 'XMLHttpRequest',
            'Referer': 'http://gsxt.gzgs.gov.cn/%s/nbxq.jsp' % post_type,
            'Connection': 'keep-alive',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache'
        })
        module.appendWebMethod('post')
        module.appendEncoding('utf-8')
        # 此处nbxh必须使用nbxh而不是topnbxh
        module.appendPostData(lambda nbwzwdc=None, nbwzwdt=None, nbxh=None, nbtoplsh=None:
                              {"c": nbwzwdc, "t": nbwzwdt, "nbxh": nbxh, "lsh": nbtoplsh})
        module.addSleep(Sleep(2))

        # 检查返回值中successed的状态
        module.addEvent(Event(EventType.ASSERT_FAILED, retry_times=50, assert_function=self.checkReturnedResults))
        module.addEvent(Event(EventType.EXCEPTION_OCCURED, retry_times=50))

        module_super.appendSubModule(module, True)
    # Module getAnnalsWebsiteInfo End

    # Module getAnnalsFinancialInfo Start
    def getAnnalsFinancialInfo(self, module_super):
        module = Module(self.visitQynbJson, u"获取年报-资产状况信息")
        module.module_id = "get_annals_financial_info"

        module.appendUrl(lambda post_type: "http://gsxt.gzgs.gov.cn/%s/search!searchNbxx.shtml" % post_type)
        module.appendHeaders(lambda post_type: {
            'Host': 'gsxt.gzgs.gov.cn',
            'Accept': 'application/json, text/javascript, */*',
            'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'X-Requested-With': 'XMLHttpRequest',
            'Referer': 'http://gsxt.gzgs.gov.cn/%s/nbxq.jsp' % post_type,
            'Connection': 'keep-alive',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache'
        })
        module.appendWebMethod('post')
        module.appendEncoding('utf-8')
        # 此处nbxh必须使用nbxh而不是topnbxh
        module.appendPostData(lambda nbzczkc=None, nbzczkt=None, nbxh=None, nbtoplsh=None:
                              {"c": nbzczkc, "t": nbzczkt, "nbxh": nbxh, "lsh": nbtoplsh})
        module.addSleep(Sleep(2))

        # 检查返回值中successed的状态
        module.addEvent(Event(EventType.ASSERT_FAILED, retry_times=50, assert_function=self.checkReturnedResults))
        module.addEvent(Event(EventType.EXCEPTION_OCCURED, retry_times=50))

        module_super.appendSubModule(module, True)
    # Module getAnnalsFinancialInfo End

    # Module getAnnalsInvestmentInfo Start
    def getAnnalsInvestmentInfo(self, module_super):
        module = Module(self.visitQynbJson, u"获取年报-对外投资信息")
        module.module_id = "get_annals_investment_info"

        module.appendUrl(lambda post_type: "http://gsxt.gzgs.gov.cn/%s/search!searchNbxx.shtml" % post_type)
        module.appendHeaders(lambda post_type: {
            'Host': 'gsxt.gzgs.gov.cn',
            'Accept': 'application/json, text/javascript, */*',
            'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'X-Requested-With': 'XMLHttpRequest',
            'Referer': 'http://gsxt.gzgs.gov.cn/%s/nbxq.jsp' % post_type,
            'Connection': 'keep-alive',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache'
        })
        module.appendWebMethod('post')
        module.appendEncoding('utf-8')
        # 此处nbxh必须使用nbxh而不是topnbxh
        module.appendPostData(lambda nbdwtzc=None, nbdwtzt=None, nbxh=None, nbtoplsh=None:
                              {"c": nbdwtzc, "t": nbdwtzt, "nbxh": nbxh, "lsh": nbtoplsh})
        module.addSleep(Sleep(2))

        # 检查返回值中successed的状态
        module.addEvent(Event(EventType.ASSERT_FAILED, retry_times=50, assert_function=self.checkReturnedResults))
        module.addEvent(Event(EventType.EXCEPTION_OCCURED, retry_times=50))

        module_super.appendSubModule(module, True)
    # Module getAnnalsInvestmentInfo End

    # Module getAnnalsContributeInfo Start
    def getAnnalsContributeInfo(self, module_super):
        module = Module(self.visitQynbJson, u"获取年报-股东出资信息")
        module.module_id = "get_annals_contribute_info"

        module.appendUrl(lambda post_type: "http://gsxt.gzgs.gov.cn/%s/search!searchNbxx.shtml" % post_type)
        module.appendHeaders(lambda post_type: {
            'Host': 'gsxt.gzgs.gov.cn',
            'Accept': 'application/json, text/javascript, */*',
            'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'X-Requested-With': 'XMLHttpRequest',
            'Referer': 'http://gsxt.gzgs.gov.cn/%s/nbxq.jsp' % post_type,
            'Connection': 'keep-alive',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache'
        })
        module.appendWebMethod('post')
        module.appendEncoding('utf-8')
        # 此处nbxh必须使用nbxh而不是topnbxh
        module.appendPostData(lambda nbgdczc=None, nbgdczt=None, nbxh=None, nbtoplsh=None:
                              {"c": nbgdczc, "t": nbgdczt, "nbxh": nbxh, "lsh": nbtoplsh})
        module.addSleep(Sleep(2))

        # 检查返回值中successed的状态
        module.addEvent(Event(EventType.ASSERT_FAILED, retry_times=50, assert_function=self.checkReturnedResults))
        module.addEvent(Event(EventType.EXCEPTION_OCCURED, retry_times=50))

        module_super.appendSubModule(module, True)
    # Module getAnnalsContributeInfo End

    # Module getAnnalsAssuranceInfo Start
    def getAnnalsAssuranceInfo(self, module_super):
        module = Module(self.visitQynbJson, u"获取年报-对外提供担保信息")
        module.module_id = "get_annals_assurance_info"

        module.appendUrl(lambda post_type: "http://gsxt.gzgs.gov.cn/%s/search!searchNbxx.shtml" % post_type)
        module.appendHeaders(lambda post_type: {
            'Host': 'gsxt.gzgs.gov.cn',
            'Accept': 'application/json, text/javascript, */*',
            'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'X-Requested-With': 'XMLHttpRequest',
            'Referer': 'http://gsxt.gzgs.gov.cn/%s/nbxq.jsp' % post_type,
            'Connection': 'keep-alive',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache'
        })
        module.appendWebMethod('post')
        module.appendEncoding('utf-8')
        # 此处nbxh必须使用nbxh而不是topnbxh
        module.appendPostData(lambda nbdwtgdbc=None, nbdwtgdbt=None, nbxh=None, nbtoplsh=None:
                              {"c": nbdwtgdbc, "t": nbdwtgdbt, "nbxh": nbxh, "lsh": nbtoplsh})
        module.addSleep(Sleep(2))

        # 检查返回值中successed的状态
        module.addEvent(Event(EventType.ASSERT_FAILED, retry_times=50, assert_function=self.checkReturnedResults))
        module.addEvent(Event(EventType.EXCEPTION_OCCURED, retry_times=50))

        module_super.appendSubModule(module, True)
    # Module getAnnalsAssuranceInfo End

    # Module getAnnalEequityUpdateInfo Start
    def getAnnalEequityUpdateInfo(self, module_super):
        module = Module(self.visitQynbJson, u"获取年报-股权变更信息")
        module.module_id = "get_annals_equity_update_info"

        module.appendUrl(lambda post_type: "http://gsxt.gzgs.gov.cn/%s/search!searchNbxx.shtml" % post_type)
        module.appendHeaders(lambda post_type: {
            'Host': 'gsxt.gzgs.gov.cn',
            'Accept': 'application/json, text/javascript, */*',
            'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'X-Requested-With': 'XMLHttpRequest',
            'Referer': 'http://gsxt.gzgs.gov.cn/%s/nbxq.jsp' % post_type,
            'Connection': 'keep-alive',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache'
        })
        module.appendWebMethod('post')
        module.appendEncoding('utf-8')
        # 此处nbxh必须使用nbxh而不是topnbxh
        module.appendPostData(lambda nbgqbgc=None, nbgqbgt=None, nbxh=None, nbtoplsh=None:
                              {"c": nbgqbgc, "t": nbgqbgt, "nbxh": nbxh, "lsh": nbtoplsh})
        module.addSleep(Sleep(2))

        # 检查返回值中successed的状态
        module.addEvent(Event(EventType.ASSERT_FAILED, retry_times=50, assert_function=self.checkReturnedResults))
        module.addEvent(Event(EventType.EXCEPTION_OCCURED, retry_times=50))

        module_super.appendSubModule(module, True)
    # Module getAnnalEequityUpdateInfo End

    # Module getAnnalsUpdateInfo Start
    def getAnnalsUpdateInfo(self, module_super):
        module = Module(self.visitQynbJson, u"获取年报-修改记录信息")
        module.module_id = "get_annals_update_info"

        module.appendUrl(lambda post_type: "http://gsxt.gzgs.gov.cn/%s/search!searchNbxx.shtml" % post_type)
        module.appendHeaders(lambda post_type: {
            'Host': 'gsxt.gzgs.gov.cn',
            'Accept': 'application/json, text/javascript, */*',
            'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'X-Requested-With': 'XMLHttpRequest',
            'Referer': 'http://gsxt.gzgs.gov.cn/%s/nbxq.jsp' % post_type,
            'Connection': 'keep-alive',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache'
        })
        module.appendWebMethod('post')
        module.appendEncoding('utf-8')
        # 此处nbxh必须使用nbxh而不是topnbxh
        module.appendPostData(lambda nbxgjlc=None, nbxgjlt=None, nbxh=None, nbtoplsh=None:
                              {"c": nbxgjlc, "t": nbxgjlt, "nbxh": nbxh, "lsh": nbtoplsh})
        module.addSleep(Sleep(2))

        # 检查返回值中successed的状态
        module.addEvent(Event(EventType.ASSERT_FAILED, retry_times=50, assert_function=self.checkReturnedResults))
        module.addEvent(Event(EventType.EXCEPTION_OCCURED, retry_times=50))

        module_super.appendSubModule(module, True)
    # Module getAnnalsUpdateInfo End

    # Module collectResult Start
    def collectResult(self, module_super):
        module = Module(self.resultCollect, "结果收集")
        module_super.appendSubModule(module)
    # Module collectResult End

    #
    # 模块子函数
    #

    # Func checkReturnedResults Start
    # 对返回的JSON状态码进行检查(因为每次返回的数据会保存在中间变量json中,所以各个模块可以通用)
    def checkReturnedResults(self, json = None):
        if not json:
            self.holder.logging.warning(u"抓取JSON失败")
            self.report.access_type = SeedAccessType.ERROR
            return False
        else:
            return json["successed"]
    # Func checkReturnedResults End

    # Func checkJbxxParms Start
    def checkJbxxParms(self, jbxxc = None, jbxxt = None, jbxxnbxh = None):
        return not jbxxc or not jbxxt or not jbxxnbxh
    # Func checkJbxxParms End

    # Func checkGdxxParms Start
    def checkGdxxParms(self, gdxxc = None, gdxxt = None, gdxxnbxh = None):
        return not gdxxc or not gdxxt or not gdxxnbxh
    # Func checkGdxxParms End

    # Func checkGdxqParms Start
    def checkGdxqParms(self, gdxqc = None, gdxqt = None, gdxqnbxh = None):
        return not gdxqc or not gdxqt or not gdxqnbxh
    # Func checkGdxqParms End

    # Func checkBgxxParms Start
    def checkBgxxParms(self, bgxxc = None, bgxxt = None, bgxxnbxh = None):
        return not bgxxc or not bgxxt or not bgxxnbxh
    # Func checkBgxxParms End

    # Func checkBaxxParms Start
    def checkBaxxParms(self, baxxc = None, baxxt = None, baxxnbxh = None):
        return not baxxc or not baxxt or not baxxnbxh
    # Func checkBaxxParms End

    # Func checkFzjgxxParms Start
    def checkFzjgxxParms(self, fzjgc = None, fzjgt = None, fzjgnbxh = None):
        return not fzjgc or not fzjgt or not fzjgnbxh
    # Func checkFzjgxxParms End

    # Func checkXzcfxxParms Start
    def checkXzcfxxParms(self, xzcfc = None, xzcft = None, xzcfnbxh = None):
        return not xzcfc or not xzcft or not xzcfnbxh
    # Func checkXzcfxxParms End

    # Func checkAnnalsParms Start
    def checkAnnalsParms(self, nbc = None, nbt = None, nbnbxh = None):
        return not nbc or not nbt or not nbnbxh
    # Func checkAnnalsParms End

    # Func checkAnnalsJbxxParms Start
    def checkAnnalsJbxxParms(self, nbjbxxc = None, nbjbxxt = None, nbtoplsh = None, nbxh = None):
        return not nbjbxxc or not nbjbxxt or not nbtoplsh or not nbxh
    # Func checkAnnalsJbxxParms End

    # Func checkAnnalsWzwdParms Start
    def checkAnnalsWzwdParms(self, nbwzwdc = None, nbwzwdt = None, nbtoplsh = None, nbxh = None):
        return not nbwzwdc or not nbwzwdt or not nbtoplsh or not nbxh
    # Func checkAnnalsWzwdParms End

    # Func checkAnnalsZczkParms Start
    def checkAnnalsZczkParms(self, nbzczkc = None, nbzczkt = None, nbtoplsh = None, nbxh = None):
        return not nbzczkc or not nbzczkt or not nbtoplsh or not nbxh
    # Func checkAnnalsZczkParms End

    # Func checkAnnalsDwtzParms Start
    def checkAnnalsDwtzParms(self, nbdwtzc = None, nbdwtzt = None, nbtoplsh = None, nbxh = None):
        return not nbdwtzc or not nbdwtzt or not nbtoplsh or not nbxh
    # Func checkAnnalsDwtzParms End

    # Func checkAnnalsGdczParms Start
    def checkAnnalsGdczParms(self, nbgdczc = None, nbgdczt = None, nbtoplsh = None, nbxh = None):
        return not nbgdczc or not nbgdczt or not nbtoplsh or not nbxh
    # Func checkAnnalsGdczParms End

    # Func checkAnnalsDwtgdbParms Start
    def checkAnnalsDwtgdbParms(self, nbdwtgdbc = None, nbdwtgdbt = None, nbtoplsh = None, nbxh = None):
        return not nbdwtgdbc or not nbdwtgdbt or not nbtoplsh or not nbxh
    # Func checkAnnalsDwtgdbParms End

    # Func checkAnnalsGqbgParms Start
    def checkAnnalsGqbgParms(self, nbgqbgc = None, nbgqbgt = None, nbtoplsh = None, nbxh = None):
        return not nbgqbgc or not nbgqbgt or not nbtoplsh or not nbxh
    # Func checkAnnalsGqbgParms End

    # Func checkAnnalsXgjlParms Start
    def checkAnnalsXgjlParms(self, nbxgjlc = None, nbxgjlt = None, nbtoplsh = None, nbxh = None):
        return not nbxgjlc or not nbxgjlt or not nbtoplsh or not nbxh
    # Func checkAnnalsXgjlParms End

    # Func checkRecordInfo End
    # 特殊备案信息转股东信息
    def checkRecordInfo(self, web = None, json = None):
        query_dict = {}

        if not web or not json:
            return query_dict

        if json["successed"]:
            for data in json["data"]:
                if "tzrlxmc" in data and "czmc" in data and "zzlxmc" in data and "zzbh" in data:
                    if u"gdxx_json" not in self.page_dict:
                        self.page_dict[u"gdxx_json"] = list()
                    self.page_dict[u"gdxx_json"].append(web)
                    break

        return query_dict
    # Func checkRecordInfo End

    # Func trem Start
    def trem(self, data):
        if data is not None:
            if isinstance(data, basestring):
                if len(data) > 0:
                    return data.strip()
                else:
                    return data
            else:
                return data
        else:
            return ''
    # Func trem End

    # Func getParms Start
    def getParms(self, srt):
        try:
            if len(srt) == 0:
                return []
            else:
                prams = srt[0].split(",")
                prams = [self.trem(a) for a in prams]
                return prams[0:3]
        except Exception as e:
            return []
    # Func getParms End

    # Func getCompanyParms Start
    def getCompanyParms(self, plist, html):
        parms_dict = {}
        query_dict = {}
        parms_list = []

        key_name = [plist[1], plist[2], plist[3]]
        key_value = map(lambda key: {key: None}, key_name)
        map(lambda x: query_dict.update(x), key_value)

        tree = etree.HTML(html)
        parms_dict[plist[0]] = []

        try:
            jbxx = tree.xpath(".//li[@id='%s']" % plist[6])[0].get("onclick")
            jb_onclick = jbxx.replace("'", "").strip().strip('\r\t')
            search_one = re.findall(r"%s\((.*?)\)" % plist[4], jb_onclick, re.S)
            if len(search_one):
                parms_dict[plist[0]] = self.getParms(search_one)
        except Exception as e:
            pass

        try:
            if tree.xpath(".//*[@id='%s']" % plist[5]):
                if len(parms_dict[plist[0]]):
                    parms_list = parms_dict[plist[0]]
                    query_dict[plist[1]] = parms_list[0]
                    query_dict[plist[2]] = parms_list[1]
                    query_dict[plist[3]] = parms_list[2]
        except Exception as e:
            map(lambda x: query_dict.update(x), key_value)

        return query_dict
    # Func getCompanyParms End

    # Func getCompanyJbxxParms Start
    def getCompanyJbxxParms(self, html):
        plist = ["jbxx", "jbxxc", "jbxxt", "jbxxnbxh", "searchOne", "baseinfo", "jbxx"]
        return self.getCompanyParms(plist, html)
    # Func getCompanyGdxxParms Start

    def getCompanyGdxxParms(self, html):
        plist = ["gdxx", "gdxxc", "gdxxt", "gdxxnbxh", "searchTzrList", "tzxxTable", "jbxx"]
        query_dict = self.getCompanyParms(plist, html)
        # 添加股东信息迭代器
        query_dict['gd_parms'] = ["exist"]
        return query_dict
    # Func getCompanyGdxxParms End

    # Func getGdxqParms Start
    def getGdxqParms(self, html, nbtoplsh = None):
        plist = ["gdxq", "gdxqc", "gdxqt", "gdxqnbxh", "searchTzrDetail", "touziren", "4"]
        # 股东详情的参数源(html中的内嵌JavaScript)和年报参数源格式一致,所以调用getAnnalsParms来获取股东详情参数
        return self.getAnnalsParms(plist, html, nbtoplsh)
    # Func getGdxqParms End

    # Func getCompanyBgxxParms Start
    def getCompanyBgxxParms(self, html):
        plist = ["bgxx", "bgxxc", "bgxxt", "bgxxnbxh", "searchList", "bgxxTable", "jbxx"]
        return self.getCompanyParms(plist, html)
    # Func getCompanyBgxxParms End

    # Func getCompanyBaxxParms Start
    # 备案信息和分支机构相关联,所以放在一起获取
    def getCompanyBaxxParms(self, html):
        parms_dict = {}
        query_dict = {}
        baxx_parms_list = []
        fzjg_parms_list = []

        query_dict["baxxc"] = None
        query_dict["baxxt"] = None
        query_dict["baxxnbxh"] = None

        query_dict["fzjgc"] = None
        query_dict["fzjgt"] = None
        query_dict["fzjgnbxh"] = None

        try:
            tree = etree.HTML(html)
        except Exception as e:
            return query_dict

        parms_dict["baxx"] = []
        parms_dict["fzjg"] = []

        try:
            baxx = tree.xpath(".//li[@id='baxx']")[0].get("onclick")
            ba_onclick = baxx.replace("'", "").strip().strip('\r\t')
            searchQyZyryList = re.findall(r"searchQyZyryList\((.*?)\)", ba_onclick, re.S)
            searchGtJtcyList = re.findall(r"searchGtJtcyList\((.*?)\)", ba_onclick, re.S)
            searchList = re.findall(r"searchList\((.*?)\)", ba_onclick, re.S)
            searchNzcyList=re.findall(r"searchNzcyList\((.*?)\)", ba_onclick, re.S)
            searchTzrList=re.findall(r"searchTzrList\((.*?)\)", ba_onclick, re.S)

            if len(searchQyZyryList):
                parms_dict["baxx"] = self.getParms(searchQyZyryList)
            elif len(searchGtJtcyList):
                parms_dict["baxx"] = self.getParms(searchGtJtcyList)
            elif len(searchNzcyList):
                parms_dict["baxx"] = self.getParms(searchNzcyList)
            elif len(searchTzrList):
                parms_dict["baxx"] = self.getParms(searchTzrList)
            else:
                pass

            if len(searchList):
                eparms = self.getParms(searchList)
                if eparms[1] == '6':
                    parms_dict["baxx"] = eparms
                elif eparms[1] == '9':
                    parms_dict["fzjg"] = eparms
        except Exception as e:
            pass

        if tree.xpath(".//*[@id='zyryTable']") or tree.xpath(".//*[@id='beian']"):
            # 可能存在备案信息
            try:
                if len(parms_dict["baxx"]):
                    baxx_parms_list = parms_dict['baxx']
                    query_dict["baxxc"] = baxx_parms_list[0]
                    query_dict["baxxt"] = baxx_parms_list[1]
                    query_dict["baxxnbxh"] = baxx_parms_list[2]
            except Exception as e:
                query_dict["baxxc"] = None
                query_dict["baxxt"] = None
                query_dict["baxxnbxh"] = None

        if tree.xpath(".//*[@id='fzjgTable']"):
            # 可能存在分之机构信息
            try:
                if len(parms_dict["fzjg"]):
                    fzjg_parms_list = parms_dict["fzjg"]
                    query_dict["fzjgc"] = fzjg_parms_list[0]
                    query_dict["fzjgt"] = fzjg_parms_list[1]
                    query_dict["fzjgnbxh"] = fzjg_parms_list[2]
            except Exception as e:
                query_dict["fzjgc"] = None
                query_dict["fzjgt"] = None
                query_dict["fzjgnbxh"] = None

        return query_dict
    # Func getCompanyBaxxParms End

    # Func getCompanyXzcfParms Start
    def getCompanyXzcfParms(self, html):
        plist = ["bgxx", "xzcfc", "xzcft", "xzcfnbxh", "searchAjList", "xzcfTable", "xzcf"]
        return self.getCompanyParms(plist, html)
    # Func getCompanyXzcfParms End

    # Func getCompanyAnnalsIterator Start
    # 创建访问年报信息的迭代器
    def getCompanyAnnalsIterator(self):
        query_dict = {}
        query_dict["nb_parms"] = ["exist"]
        return query_dict
    # Func getCompanyAnnalsIterator End

    # Func getAnnalsParms Start
    # Annals common function
    def getAnnalsParms(self, plist, html, lsh = None):
        parms_dict = {}
        query_dict = {}
        parms_list = {}

        key_name = [plist[1], plist[2], plist[3]]
        key_value = map(lambda key: {key: None}, key_name)
        map(lambda x: query_dict.update(x), key_value)

        # plist[6]为"4"时,为股东详情和年报列表访问,没有lsh参数传过来,所以不检查
        if plist[6] != "4":
            if not lsh:
                return query_dict

        tree = etree.HTML(html)
        parms_dict[plist[0]] = []

        try:
            nb = tree.xpath(".//script[%s]/text()" % plist[6])[0]
            nb_text = nb.replace('"', "").strip().strip('\r\n')
            searchNbxqOne = re.findall(r"%s\((.*?)\)" % plist[4], nb_text, re.S)

            searchNbxq = []
            for search in searchNbxqOne:
                if plist[5] in search:
                    searchNbxq.append(search)
                    break

            if len(searchNbxq):
                parms_dict[plist[0]] = self.getParms(searchNbxq)
        except Exception as e:
            pass

        try:
            if len(parms_dict[plist[0]]):
                parms_list = parms_dict[plist[0]]
                query_dict[plist[1]] = parms_list[0]
                query_dict[plist[2]] = parms_list[1]
                query_dict[plist[3]] = parms_list[2]
        except Exception as e:
            map(lambda x: query_dict.update(x), key_value)

        return query_dict
    # Func getAnnalsParms Start

    # Func getAnnalsListParms Start
    def getAnnalsListParms(self, html):
        plist = ["nbxx", "nbxxc", "nbxxt", "nbxxnbxh", "searchNbList", "qynbTable", "4"]
        return self.getAnnalsParms(plist, html)
    # Func getAnnalsListParms End

    # Func getAnnalsJbxxParms Start
    # 年报基本信息
    def getAnnalsJbxxParms(self, html, nbtoplsh = None):
        plist = ["nbjbxx", "nbjbxxc", "nbjbxxt", "nbjbxxnbxh", "searchNbxqOne", "1_", "3"]
        return self.getAnnalsParms(plist, html, nbtoplsh)
    # Func getAnnalsJbxxParms End

    # Func getAnnalsZczkParms Start
    # 企业资产状况信息或生产经营情况
    def getAnnalsZczkParms(self, html, nbtoplsh = None):
        plist = ["nbzczk", "nbzczkc", "nbzczkt", "nbzczknbxh", "searchNbxqOne", "2_", "3"]
        return self.getAnnalsParms(plist, html, nbtoplsh)
    # Func getAnnalsZczkParms End

    # Func getAnnalsWzwdParms Start
    # 年报网站或网站信息
    def getAnnalsWzwdParms(self, html, nbtoplsh = None):
        plist = ["nbwzwd", "nbwzwdc", "nbwzwdt", "nbwzwdnbxh", "searchNbxqList", "wzwdTable", "3"]
        return self.getAnnalsParms(plist, html, nbtoplsh)
    # Func getAnnalsWzwdParms End

    # Func getAnnalsDwtzParms Start
    # 年报对外投资信息
    def getAnnalsDwtzParms(self, html, nbtoplsh = None):
        plist = ["nbdwtz", "nbdwtzc", "nbdwtzt", "nbdwtznbxh", "searchNbxqList", "dwtzTable", "3"]
        return self.getAnnalsParms(plist, html, nbtoplsh)
    # Func getAnnalsDwtzParms End

    # Func getAnnalsGdczParms Start
    # 年报股东及出资信息
    def getAnnalsGdczParms(self, html, nbtoplsh = None):
        plist = ["nbgdcz", "nbgdczc", "nbgdczt", "nbgdcznbxh", "searchNbxqList", "tzxxTable", "3"]
        return self.getAnnalsParms(plist, html, nbtoplsh)
    # Func getAnnalsGdczParms End

    # Func getAnnalsDwtgdbParms Start
    # 年报对外提供担保信息
    def getAnnalsDwtgdbParms(self, html, nbtoplsh = None):
        plist = ["nbdwtgdb", "nbdwtgdbc", "nbdwtgdbt", "nbdwtgdbnbxh", "searchNbxqList", "dwtgdbTable", "3"]
        return self.getAnnalsParms(plist, html, nbtoplsh)
    # Func getAnnalsDwtgdbParms End

    # Func getAnnalsGqbgParms Start
    # 年报股权变更信息
    def getAnnalsGqbgParms(self, html, nbtoplsh = None):
        plist = ["nbgqbg", "nbgqbgc", "nbgqbgt", "nbgqbgnbxh", "searchNbxqList", "gqbgTable", "3"]
        return self.getAnnalsParms(plist, html, nbtoplsh)
    # Func getAnnalsGqbgParms End

    # Func getAnnalsXgjlParms Start
    # 年报修改记录信息
    def getAnnalsXgjlParms(self, html, nbtoplsh = None):
        plist = ["nbxgjl", "nbxgjlc", "nbxgjlt", "nbxgjlnbxh", "searchNbBgxxList", "bgxxTable", "3"]
        return self.getAnnalsParms(plist, html, nbtoplsh)
    # Func getAnnalsXgjlParms End

    # Func getPostType Start
    # 返回具体的请求类型
    def getPostType(self, ztlx, qylx=None):
        if ztlx == '1' and qylx is not None:
            if qylx[0] == '1':
                return 'nzgs'
            elif qylx[0] == '2':
                return 'nzgsfgs'
            elif qylx[0] == '3':
                return 'nzqyfr'
            elif qylx == '4000' or (qylx[0] == '4' and qylx[1] in ['1','2','3','4','6','7']):
                return 'nzyy'
            elif qylx[0] == '4' and qylx[1] == '5' and qylx[2] == '3':
                return 'nzhh'
            elif qylx == '4540':
                return 'grdzgs'
            elif qylx[0] == '4' and qylx[1] == '5' and qylx[2] == '5':
                return 'nzhhfz'
            elif qylx == '4560':
                return 'grdzfzjg'
            elif qylx[:2] in ['50','51','52','53','60','61','62','63']:
                return 'wstz'
            elif (qylx[:2] in ['58','68','70','71'] or qylx == '7310' or qylx == '7390') and qylx != '5840' and qylx != '6840':
                return 'wstzfz'
            elif qylx[:2] in ['54','64']:
                return 'wzhh'
            elif qylx == '5840' or qylx == '6840':
                return 'wzhhfz'
            elif qylx == '7200':
                return 'czdbjg'
            elif qylx == '7300':
                return 'wgqycsjyhd'
            elif qylx == '9100':
                return 'nmzyhzs'
            elif qylx == '9200':
                return 'nmzyhzsfz'
            else:
                return None
        elif ztlx == '2':
            return 'gtgsh'
        else:
            return None
    # Func getPostType End

    # Func setRowKey Start
    # 贵州页面返回数据为json格式,需要覆写父类的setRowKey方法,将公司名称和注册号配置到page_dict["rowkey_dict"]
    def setRowKey(self, map_dict=None):
        if not map_dict:
            company_name = self.value_dict.get("company_name")
            company_zch = self.value_dict.get("company_zch")
            self.page_dict["rowkey_dict"] = {"company_name": company_name, "company_zch": company_zch}
            return True
        return False
    # Func setRowKey Start

if __name__ == "__main__":
    pass
