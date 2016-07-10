# -*- coding: utf-8 -*-
# Created by David on 2016/5/9.

import sys
import random
import time
import re
import PyV8
import urllib
reload(sys)
from qyxx_all.CrawlerBase import CrawlerBase
from lxml import etree
from qyxx_all.util.common_util import substring
from qyxx_all.ModuleManager import Module,Event,Iterator,Adapter
from qyxx_all.util.crawler_util import CrawlerRunMode, InputType, OutputType, EventType, OutputParameterShowUpType

class CrawlerGdQyxx(CrawlerBase):
    def __init__(self, pinyin, crawler_master):
        self.crawler_master = crawler_master
        config_dict = dict()
        config_dict[CrawlerRunMode.COMPANY_ADAPTER] = [self.initConfigBaseInfo, self.initConfigShareHolderInfo,self.initShareHolderDetail, self.initConfigChangeInfo,
                                                       self.initArchiveInfo, self.initBranchInfo, self.initXzcf, self.initNbList, self.initNb, self.initResultCollect]
        #config_dict[CrawlerRunMode.COMPANY_ADAPTER] = [self.initConfigBaseInfo, self.initXzcf, self.initNbList, self.initNb, self.initResultCollect]
        CrawlerBase.__init__(self, pinyin, config_dict, None, None)
        self.initConfig()
        # 打开解析开关
        self.parse_on = True
        pass

    def initConfigBaseInfo(self):
        module = Module(self.crawler_master.visitJbxx, "基本信息")
        adapter = Adapter({"source": u"企业信息网"}, u"企业信息网")
        module.addAdapter(adapter)

        module.appendUrl("company_url")
        header_dict = {'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
                       'Accept-Encoding': 'gzip, deflate',
                       'Connection': 'keep-alive',
                       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                       'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:37.0) Gecko/20100101 Firefox/37.0',
                       'Host': 'gsxt.gdgs.gov.cn',
                       'Referer': 'http://gsxt.gdgs.gov.cn/aiccips/CheckEntContext/showInfo.html'}
        module.appendHeaders(header_dict)
        module.appendEncoding("UTF-8")
        module.appendAcceptCode(521)
        def prepareCommonInfo(web):
            tree = etree.HTML(web.body)
            values = tree.xpath('.//@value')
            if not values or len(values) < 3:
                return None
            entNo = values[1]
            entType = values[2]
            regOrg = values[3]
            return {"entNo": entNo, "entType": entType, "regOrg": regOrg}
        def assert_fun(entNo=None):
            if not entNo:
                return False
            return True
        module.appendOutput(type=OutputType.FUNCTION, function=prepareCommonInfo, show_up=OutputParameterShowUpType.OPTIONAL)
        module.addEvent(Event(EventType.ASSERT_FAILED, retry_times=2, assert_function=assert_fun))
        self.module_manager.appendSubModule(module, True)

    def initConfigShareHolderInfo(self):
        module = Module(self.crawler_master.visitGdxxJson, "股东信息")
        module.appendUrl('http://gsxt.gdgs.gov.cn/aiccips/GSpublicity/invInfoPage.html')
        module.appendHeaders(lambda company_url: {
                                    "Host": "gsxt.gdgs.gov.cn",
                                    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; rv:37.0) Gecko/20100101 Firefox/37.0",
                                    "Accept": "application/json, text/javascript, */*; q=0.01",
                                    "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
                                    "Accept-Encoding": "gzip, deflate",
                                    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                                    "X-Requested-With": "XMLHttpRequest",
                                    "Referer": company_url,
                                    "Connection": "keep-alive",
                                    "Pragma": "no-cache",
                                    "Cache-Control": "no-cache"
                                })
        module.appendWebMethod("post")
        module.appendPostData(lambda entNo,regOrg:{
                                    'pageNo': 1,
                                    'entNo': entNo,
                                    'regOrg': regOrg
                                })
        module.addMapper({'invType': u'股东信息.股东类型', 'inv': u'股东信息.股东', 'certName': u'股东信息.证照/证件类型', 'certNo': u'股东信息.证照/证件号码',
                          'invNo': 'invNo', 'primary_key':'inv,certNo'})
        self.module_manager.appendSubModule(module, True)

    def initShareHolderDetail(self):
        iterator = Iterator("gdxx_list", "gdxx_rcd")
        module = Module(None, "进入股东详情", iterator)
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
            return 'http://gsxt.gdgs.gov.cn/aiccips/GSpublicity/invInfoDetails.html?' + urllib.urlencode(get_data)
        sub_module.appendUrl(getGdxqUrl)
        sub_module.appendHeaders(lambda company_url:{
                                        "Host" : "gsxt.gdgs.gov.cn",
                                        "User-Agent" : "Mozilla/5.0 (Windows NT 6.1; rv:37.0) Gecko/20100101 Firefox/37.0",
                                        "Accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                                        "Accept-Language" : "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
                                        "Accept-Encoding" : "gzip, deflate",
                                        "Referer" : company_url,
                                        "Connection" : "keep-alive"
                                    })
        sub_module.appendEncoding("UTF-8")
        module.appendSubModule(sub_module, True)

    def initConfigChangeInfo(self):
        module = Module(self.crawler_master.visitBgxxJson, "变更信息")
        module.appendUrl('http://gsxt.gdgs.gov.cn/aiccips/GSpublicity/entChaPage')
        module.appendHeaders(lambda company_url: {
                                    "Host": "gsxt.gdgs.gov.cn",
                                    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; rv:37.0) Gecko/20100101 Firefox/37.0",
                                    "Accept": "application/json, text/javascript, */*; q=0.01",
                                    "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
                                    "Accept-Encoding": "gzip, deflate",
                                    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                                    "X-Requested-With": "XMLHttpRequest",
                                    "Referer": company_url,
                                    "Connection": "keep-alive",
                                    "Pragma": "no-cache",
                                    "Cache-Control": "no-cache"
                                })
        module.appendWebMethod("post")
        module.appendPostData(lambda entNo,entType,regOrg:{
                                    'pageNo': 1,
                                    'entNo': entNo,
                                    'regOrg': regOrg,
                                    'entType': entType
                                })
        module.addMapper({'altFiledName':u'变更信息.变更事项', 'altBe':u'变更信息.变更前内容', 'altAf':u'变更信息.变更后内容', 'altDate':u'变更信息.变更日期',
                          'primary_key':'altFiledName,altDate'})
        self.module_manager.appendSubModule(module, True)

    def initArchiveInfo(self):
        module = Module(self.crawler_master.visitBaxxJson, "获取备案信息")
        module.appendUrl('http://gsxt.gdgs.gov.cn/aiccips/GSpublicity/vipInfoPage')
        module.appendHeaders(CrawlerGdQyxx.baxx_and_fzjg_qyxx_header)
        module.appendWebMethod("post")
        module.appendPostData(lambda entNo,regOrg:{
                                                    'pageNo' : 1,
                                                    'entNo' : entNo,
                                                    'regOrg' : regOrg
                                                })
        module.addMapper({'name':u'主要人员信息.姓名', 'position':u'主要人员信息.职务', 'primary_key':'name,position'})
        self.module_manager.appendSubModule(module, True)

    def initBranchInfo(self):
        module = Module(self.crawler_master.visitFzjgJson, "获取分支机构信息")
        module.appendUrl('http://gsxt.gdgs.gov.cn/aiccips/GSpublicity/braInfoPage')
        module.appendHeaders(CrawlerGdQyxx.baxx_and_fzjg_qyxx_header)
        module.appendWebMethod("post")
        module.appendPostData(lambda entNo,regOrg:{
                                                    'pageNo' : 1,
                                                    'entNo' : entNo,
                                                    'regOrg' : regOrg
                                                })
        module.addMapper({'regNO':u'分支机构信息.注册号', 'regOrg':u'分支机构信息.登记机关', 'brName':u'分支机构信息.名称', 'primary_key':'regNO,brName'})
        self.module_manager.appendSubModule(module, True)

    def initXzcf(self):
        module = Module(self.crawler_master.visitXzcf, u"抓取行政处罚信息")
        module.appendUrl("http://gsxt.gdgs.gov.cn/aiccips/GSpublicity/GSpublicityList.html?service=cipPenaltyInfo")
        module.appendHeaders(self.headers_post)
        module.appendWebMethod("post")
        module.appendPostData(lambda entNo,entType,regOrg: {"entNo":entNo, "entType":entType, "regOrg":regOrg})
        self.module_manager.appendSubModule(module, True)
        pass

    def initNbList(self):
        module = Module(self.crawler_master.visitQynbList, u"抓取年报列表")
        module.appendUrl("http://gsxt.gdgs.gov.cn/aiccips/BusinessAnnals/BusinessAnnalsList.html")
        module.appendHeaders(self.headers_post)
        module.appendWebMethod("post")
        module.appendPostData(lambda entNo,entType,regOrg: {"entNo":entNo, "entType":entType, "regOrg":regOrg})
        module.appendOutput("nb_list", ".//table//td/a", OutputType.LIST, show_up=OutputParameterShowUpType.OPTIONAL)
        self.module_manager.appendSubModule(module)

    def initNb(self):
        iterator = Iterator(seeds="nb_list", param_name="nb")
        module = Module(iterator=iterator, name=u"遍历年报列表")
        self.module_manager.appendSubModule(module, True)

        self.initNbOne(module)

    def initNbOne(self, module_super):
        module = Module(self.crawler_master.visitQynb, u"抓取企业年报信息")
        def prepare(nb, nb_url=None):
            mv_dict = dict()
            mv_dict['nb_url'] = nb_url or ''.join(nb.xpath('@href'))
            mv_dict['nb_name'] = ''.join(nb.xpath('text()')).replace(u'年度报告','').strip()
            return mv_dict
        module.appendInput(input_type=InputType.FUNCTION, input_value=prepare)
        module.appendUrl("nb_url")
        module.appendHeaders({
                            "Host": "gsxt.gdgs.gov.cn",
                            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; rv:37.0) Gecko/20100101 Firefox/37.0",
                            "Accept": "application/json, text/javascript, */*",
                            "Accept-Language": "zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3",
                            "Accept-Encoding": "gzip, deflate",
                            "Content-Type": "application/x-www-form-urlencoded",
                            "X-Requested-With": "XMLHttpRequest",
                            "Connection": "keep-alive"
                        })
        def assert_fun(html=None):
            if not html:
                return False
            if html.startswith("<script>") and 'window.location.href' in html:
                str = substring(html, "window.location.href='", "';</script>")
                nb_url = "http://gsxt.gdgs.gov.cn" + str
                self.crawler_master.value_dict['nb_url'] = nb_url
                return False
            return True
        module.addEvent(Event(EventType.ASSERT_FAILED, assert_function=assert_fun))
        module_super.appendSubModule(module)

    def initResultCollect(self):
        module = Module(self.crawler_master.resultCollect, "结果收集")
        self.module_manager.appendSubModule(module)

    def headers_post(self, company_url):
        return {'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
                       'Accept-Encoding': 'gzip, deflate',
                       'Connection': 'keep-alive',
                       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                       'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:37.0) Gecko/20100101 Firefox/37.0',
                       'Host': 'gsxt.gdgs.gov.cn',
                       'Referer': company_url}

    # 获取企业信息备案信息，分支机构请求头
    baxx_and_fzjg_qyxx_header = {
        "Host": "gsxt.gdgs.gov.cn",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; rv:37.0) Gecko/20100101 Firefox/37.0",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
        "Accept-Encoding": "gzip, deflate",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "X-Requested-With": "XMLHttpRequest",
        "Referer": "http://gsxt.gdgs.gov.cn/aiccips/GSpublicity/GSpublicityList.html?service=entCheckInfo",
        "Connection": "keep-alive",
        "Pragma": "no-cache",
        "Cache-Control": "no-cache"
    }

if __name__ == "__main__":
    body = '''<script>var x="replace@k@D@setTimeout@cd@f@1464604473@1@i@length@0@innerHTML@Yh@cookie@__phantomas@l@_phantom@captcha@var@Mon@toLowerCase@x@W@https@firstChild@__jsl_clearance@M@741@6@function@11@for@createElement@while@xd@dc@a@charAt@document@return@window@1500@Z@h@r@substr@div@May@3@join@href@match@Y@7@3F@34@30@B@challenge@16@location@2@q2@Expires@33@GMT@Path@if@try@addEventListener@catch@e@false@DOMContentLoaded@else@attachEvent@onreadystatechange".replace(/@*$/,"").split("@"),y="j g=u(){y(F.h||F.f){};j 5,A='q=7.s|b|';j 6=[u(m){E m},u(m){E m;},(u(){j I=D.x('L');I.c='<B P=\\'/\\'>m</B>';I=I.p.P;j J=I.Q(/o?:\\/\\//)[b];I=I.K(J.a).l();E u(m){w(j 9=b;9<m.a;9++){m[9]=I.C(m[9])};E m.O('')}})()];5=[[(-~~~{}|-~-~~~{})+(-~~~{}|-~-~~~{})],[-~!{}-~!{}]+[-~!{}-~!{}],[-~!{}-~!{}]+(-~~~{}+[[]][~~{}]),(-~~~{}+[[]][~~{}])+[-~!{}-~!{}],(-~~~{}+[[]][~~{}])+([(-~!{}+[(-~{}<<-~{})]>>(-~{}<<-~{}))]*((-~!{}+[(-~{}<<-~{})]>>(-~{}<<-~{})))+[[]][~~{}]),(-~~~{}+[[]][~~{}])+(-~~~{}+[[]][~~{}]),([(-~!{}+[(-~{}<<-~{})]>>(-~{}<<-~{}))]*((-~!{}+[(-~{}<<-~{})]>>(-~{}<<-~{})))+[[]][~~{}]),[-~!{}-~!{}]+((+!(+[]))+(-~!{}+[(-~{}<<-~{})]>>(-~{}<<-~{}))+[{}, []][-~!{}]),[([-~-~~~{}]+~~!{}>>-~-~~~{})],(-~~~{}+[[]][~~{}])+((+[])+[[], !-{}][~~[]]),(-~~~{}+[[]][~~{}]),(-~~~{}+[[]][~~{}])+[(-~{}<<-~{})+t],((+[])+[[], !-{}][~~[]]),(-~~~{}+[[]][~~{}])+((+!(+[]))+(-~!{}+[(-~{}<<-~{})]>>(-~{}<<-~{}))+[{}, []][-~!{}]),(-~~~{}+[[]][~~{}])+[([-~-~~~{}]+~~!{}>>-~-~~~{})],(-~~~{}+[[]][~~{}])+[(-~~~{}|-~-~~~{})+(-~~~{}|-~-~~~{})],[-~!{}-~!{}]+((+[])+[[], !-{}][~~[]]),[S],((+!(+[]))+(-~!{}+[(-~{}<<-~{})]>>(-~{}<<-~{}))+[{}, []][-~!{}]),[-~!{}-~!{}],[(-~{}<<-~{})+t],(-~~~{}+[[]][~~{}])+[S],(-~~~{}+[[]][~~{}])+(-~{}+(-~{}<<-~{})+[]+[]),(-~{}+(-~{}<<-~{})+[]+[]),[-~!{}-~!{}]+(-~{}+(-~{}<<-~{})+[]+[])];w(j 9=b;9<5.a;9++){5[9]=6[[8,b,8,b,8,b,8,b,8,b,8,b,16,b,8,b,8,b,8,b,8,b,8,b,8][9]]([[(-~~~{}+[[]][~~{}])],'12',(!(+[])+[[]][~~{}]).C(-~[(-~{}<<-~{})])+[(-~~~{}|-~-~~~{})+(-~~~{}|-~-~~~{})],(-~{}+(-~{}<<-~{})+[]+[]),'R','n%','H',[!+{}+[[]][~~{}]][b].C(16),'r','z',[-~!{}-~!{}],((-~{}+(-~{}<<-~{}))/~~{}+[[]][~~{}]).C(N+((-~{}<<-~{})<<-~{})),(!(+[])+[[]][~~{}]).C(-~[(-~{}<<-~{})]),'2%',({}+[]).C(((+!(+[]))<<(-~!{}-~!{}^(+!(+[]))))),'d',((-~{}+(-~{}<<-~{}))/~~{}+[[]][~~{}]).C(N+((-~{}<<-~{})<<-~{})),([(-~!{}+[(-~{}<<-~{})]>>(-~{}<<-~{}))]*((-~!{}+[(-~{}<<-~{})]>>(-~{}<<-~{})))+[[]][~~{}]),([(-~!{}+[(-~{}<<-~{})]>>(-~{}<<-~{}))]*((-~!{}+[(-~{}<<-~{})]>>(-~{}<<-~{})))+[[]][~~{}]),'17','T','8',(!(+[])+[[]][~~{}]).C(-~[(-~{}<<-~{})]),'3',(!(+[])+[[]][~~{}]).C(-~[(-~{}<<-~{})])][5[9]])};5=5.O('');A+=5;4('15.P=15.P.1(/[\\?|&]i-13/,\\'\\')',G);D.e=(A+';18=k, 11-M-14 v:10:19 1a;1b=/;');};1c((u(){1d{E !!F.1e;}1f(1g){E 1h;}})()){D.1e('1i',g,1h);}1j{D.1k('1l',g);}",z=0,f=function(x,y){var a=0,b=0,c=0;x=x.split("");y=y||99;while((a=x.shift())&&(b=a.charCodeAt(0)-77.5))c=(Math.abs(b)<13?(b+48.5):parseInt(a,36))+y*c;return c},g=y.match(/\b\w+\b/g).sort(function(x,y){return f(x)-f(y)}).pop();while(f(g,++z)-x.length){};eval(y.replace(/\b\w+\b/g, function(y){return x[f(y,z)-1]}));</script>'''
    str1 = 'var x="'
    str2 = '".replace(/@*$/,"").split("@")'
    idx1 = body.find(str1)
    idx2 = body.find(str2)
    x_str = body[idx1+len(str1):idx2]
    x_clr = x_str.replace("/@*$/", "").split("@")
    origin = body[idx1: idx2+len(str2)]
    replaced = ''
    for val in x_clr:
        replaced += '"%s",' % val
    replaced = replaced.rstrip(',')
    replaced = 'var x=new Array(%s)' % replaced
    body_clr = body.replace(origin, replaced)
    with PyV8.JSContext() as se:
        se.eval(body_clr)
        a = se.locals.a
        cookie = a.split('=')[1].split(';')[0]
        cookie_temp1 = dict({'ROBOTCOOKIEID': cookie})
        pass
    pass