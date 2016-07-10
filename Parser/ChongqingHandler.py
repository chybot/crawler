# -*- coding: utf-8 -*-
# Created by fml on 2016/5/19.

import sys
import os
import json
import chardet
import copy
from lxml import etree
from ParserBase import ParserBase
import html4test as test
from CommonLib.TimeUtil import TimeUtil
reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import re
import json
import warnings
class ChongqingHandler(ParserBase):
    """
    ParserShanghai is used to parse the enterprise info from Shanghai
    @version:1.0
    @author:david ding
    @modify:
    """
    def __init__(self, pinyin):
        """
        Initiate the parameters.
        """
        ParserBase.__init__(self, pinyin)
        #self.initMapper()
        self.log.info(u"ChongqingHandler构造开始")

    def initMapper(self):
        pass
        # self.appendJsonMapperConfig("gdxx_json", {'C2': u'gdxx.股东/发起人', 'C1': u'gdxx.股东/发起人类型', 'C3': u'gdxx.证照/证件类型', 'C4': u'gdxx.证照/证件号码'})
        # self.appendJsonMapperConfig("bgxx_json", {'C1': u'bgxx.变更事项', 'C2': u'bgxx.变更前内容', 'C3': u'bgxx.变更后内容', 'C4': u'bgxx.变更日期'})
        # self.appendJsonMapperConfig('fzjg_json',{'RN':u'fzjg.序号','C1':u'fzjg.注册号','C2':u'fzjg.名称','C3':u'fzjg.登记机关',})

    def parse(self, html_dict, all_reslt_dict=None):
        if not all_reslt_dict:
            all_reslt_dict = dict()
        if not html_dict or not isinstance(html_dict, dict):
            return None
        if u'company_name' in html_dict:
            self.log.info(u"开始解析 %s" % html_dict['company_name'])
        self.log.info(u"开始解析通用信息")

        self.log.info(u"通用信息解析完成")
        self.log.info(u"开始解析top信息")
        top_html = html_dict['top_html']
        top_dict = self.parseTop(top_html)
        all_reslt_dict.update(top_dict)
        jsons = html_dict['jbxx_html']
        jbxx_json = jsons[0]['_body']
        jbxx_json = self.getjsonstr(jbxx_json)
        self.log.info(u"top信息解析完成，开始解析分支机构信息")
        all_reslt_dict.update({'fzjg':self.fzjgxx_information(jbxx_json)})
        table_html = html_dict['table_html'][0]['_body']
        jbxx = self.jbxx_data_result(jbxx_json,table_html)
        all_reslt_dict.update(jbxx)
        bgxx = self.bgxx_information(jbxx_json)
        all_reslt_dict.update({'bgxx':bgxx})
        if all_reslt_dict.get(u"类型") in [u"集体经济", u"国有经济", u"股份合作制"]:
            all_reslt_dict["gdxx"] = self.baxx_information( jbxx_json, bz=2)
        else:
            # 获取股东信息
            all_reslt_dict["gdxx"] = self.gdxx_information(jbxx_json)
            # 获取备案信息
            all_reslt_dict["baxx"] = self.baxx_information(jbxx_json)
        return all_reslt_dict
        # 股东信息


    def baxx_information(self, company_infomation, bz=1):
        try:
            baxx = company_infomation.setdefault("members", [])
            # dict_["baxx"]=[]
            ba = []
            if len(baxx) > 0:
                self.log.info(u"备案信息获取开始" )
                for inf in baxx:
                    d_ = {}

                    # 原结构
                    if bz == 1:
                        d_[u"姓名"] = inf.setdefault("name", "")
                        d_[u"职务"] = inf.setdefault("position", "")
                    elif bz == 2:
                        d_[u"出资人"] = inf.setdefault("name", "")
                        d_[u"出资人类型"] = inf.setdefault("invtype", "")
                        d_[u"证照/证件类型"] = inf.setdefault("blictype", "") or inf.setdefault("certype", "")
                        d_[u"证照/证件号码"] = inf.setdefault("blicno", "") or inf.setdefault("cerno", "")
                    else:
                        pass
                    if filter(lambda x: len(x) > 1, d_.values()):
                        ba.append(d_)

            # 设置编号
            num = 0
            for item in ba:
                num += 1
                item[u"序号"] = str(num)
                pass
            return ba
        except Exception as e:
            self.log.error(u"备案信息获取出错%s" % e)

    def gdxx_information(self,company_infomation):
        try:
            gdxx = company_infomation.setdefault("investors", [])
            gd = []
            if len(gdxx) > 0:
                self.log.info(u"股东信息获取开始")
                for f_gd in gdxx:
                    f_gdxx = {}
                    f_gdxx[u"股东类型"] = f_gd.setdefault("invtype", "")
                    f_gdxx[u"股东"] = f_gd.setdefault("inv", "")
                    f_gdxx[u"证照/证件类型"] = f_gd.setdefault("certype", "") + f_gd.setdefault("blictype", "")
                    f_gdxx[u"证照/证件号码"] = f_gd.setdefault("blicno", "") + f_gd.setdefault("cerno", "")
                    f_gdxx[u"详情"] = f_gd.setdefault("gInvaccon", "")
                    if filter(lambda x: len(x) > 1, f_gdxx.values()):
                        gd.append(f_gdxx)
                    else:
                        f_gdxx = {}
                        f_gdxx[u"姓名"] = f_gd.setdefault("name", "")
                        f_gdxx[u"投资方式"] = f_gd.setdefault("sconform", "")
                        if filter(lambda x: len(x) > 1, f_gdxx.values()):
                            gd.append(f_gdxx)
            else:
                gdxx = company_infomation.setdefault("gNzgshhrqyTzrczrinfos", [])
                for f_gd in gdxx:
                    f_gdxx = {}
                    f_gdxx[u"合伙人类型"] = f_gd.setdefault("invtype", "")
                    f_gdxx[u"合伙人"] = f_gd.setdefault("inv", "")
                    f_gdxx[u"证照/证件类型"] = f_gd.setdefault("certype", "") + f_gd.setdefault("blictype", "")
                    f_gdxx[u"证照/证件号码"] = f_gd.setdefault("blicno", "") + f_gd.setdefault("cerno", "")
                    gd.append(f_gdxx)
                    pass
                pass
            return gd
        except Exception as e:
            self.log.error(u"股东信息获取出错%s" % e)
    # 变更信息
    def bgxx_information(self, company_infomation):
            try:
                bgxx = company_infomation.setdefault("alters", [])
                bg = []
                if len(bgxx) > 0:
                    self.log.info(u"变更信息获取开始" )
                    for f_bg in bgxx:
                        d_bg = {}
                        d_bg[u"变更后内容"] = f_bg.setdefault("altaf", "")
                        d_bg[u"变更前内容"] = f_bg.setdefault("altbe", "")
                        d_bg[u"变更时间"] = f_bg.setdefault("altdate", "")
                        d_bg[u"变更事项"] = f_bg.setdefault("altitem", "")
                        if filter(lambda x: len(x) > 1, d_bg.values()):
                            bg.append(d_bg)
                return bg
            except Exception as e:
                self.log.error(u"变更信息获取出错%s" % e)
                # 股东信息
    # 基本信息解析模板
    def jbxx_data_result(self, jbxx, jbxx_data_html):
        result = {}
        if len(jbxx) < 1:
            self.log.error('no jbxx,')
            return result
        raw_json = None
        # 处理json
        try:
            raw_json = jbxx
            if raw_json == None:
                raise Exception()
        except Exception as e:
            self.log.error('json error,')
            return result

        if raw_json.has_key('base'):
            base = raw_json['base']
        else:
            self.log.error('json has no base key,')
            return result

        try:
            jbxx_tree = etree.HTML(jbxx_data_html)
            # 基本信息多个模板xpath，没有找到就查询下一个
            jbxx_table = jbxx_tree.xpath(".//*[@id='register']/div[1]/table[1]")
            if not jbxx_table:
                jbxx_table = jbxx_tree.xpath(".//*[@id='register']/div/table[1]")
            if not jbxx_table:
                jbxx_table = jbxx_tree.xpath(".//*[@id='register']/div[2]/table[1]")
            if not jbxx_table:
                jbxx_table = jbxx_tree.xpath(".//*[@id='ng_fgsqyfr']/div[1]/table[1]")
            if not jbxx_table:
                jbxx_table = jbxx_tree.xpath(".//*[@id='nz_fgsqyfrfzjg']/div[1]/table[1]")
            if not jbxx_table:
                jbxx_table = jbxx_tree.xpath(".//*[@id='ng-hhqyfzjg']/div[1]/table[1]")
            if not jbxx_table:
                jbxx_table = jbxx_tree.xpath(".//*[@id='ng_fgs']/div[1]/table[1]")
            if not jbxx_table:
                jbxx_table = jbxx_tree.xpath(".//*[@id='ng_hhqy']/div[1]/table[1]")

            jbxx_table = jbxx_table[0]
            jbxx_trs = jbxx_table.xpath(".//tr")
            if ''.join(jbxx_trs[0].xpath('./th/text()')).strip() == u'基本信息':
                jbxx_trs = jbxx_trs[1:]
            for tr in jbxx_trs:
                try:
                    td_xp = tr.xpath(".//td")
                    td_len = len(td_xp)
                    try:
                        # 原理：查找td的attrib值，找不到则查询td下的span,span有值则拼起attrib和text的值，因为这些值有base的key,所以通过这种方式自动获取
                        # base中的键值对应模板中的名称,使字段自动化匹配，分析模板有2列和4列的情况，所以有if td_len == 4的判断
                        atrr = td_xp[1].attrib
                        if not atrr:
                            atrr = ""
                            td_xp_span = td_xp[1].xpath(".//span")
                            if td_xp_span:
                                for tds in range(0, len(td_xp_span)):
                                    atrr += str(td_xp_span[tds].attrib)
                                    if not atrr:
                                        if td_xp_span[tds].text:
                                            atrr += str(td_xp_span[tds].text.encode("utf-8"))
                            else:
                                if td_xp[1].text:
                                    atrr = str(td_xp[1].text.encode("utf-8"))
                        else:
                            atrr = str(atrr)
                        # print atrr
                        td_val = ""
                        for key in base.keys():
                            # 防止name(负责人等)与entname(公司名)存在时取值name就退出
                            if u"entname" in atrr:
                                td_val = base["entname"]
                                break

                            if key in atrr:
                                td_val = base[key]
                                if td_val:
                                    break
                        # 没有值，查找td中的span
                        if not td_val:
                            atrr = ""
                            td_xp_span = td_xp[1].xpath(".//span")
                            if td_xp_span:
                                for tds in range(0, len(td_xp_span)):
                                    atrr += str(td_xp_span[tds].attrib)
                                    if not atrr:
                                        if td_xp_span[tds].text:
                                            atrr += str(td_xp_span[tds].text.encode("utf-8"))
                            else:
                                if td_xp[1].text:
                                    atrr = str(td_xp[1].text.encode("utf-8"))

                            td_val = ""
                            for key in base.keys():
                                # 防止name(负责人等)与entname(公司名)存在时取值name就退出
                                if u"entname" in atrr:
                                    td_val = base["entname"]
                                    break

                                if key in atrr:
                                    td_val = base[key]
                                    if td_val:
                                        break
                        td_key = td_xp[0].text
                        if td_key:
                            td_key = td_key.strip()
                        if not td_key:
                            td_key_span = td_xp[0].xpath(".//span")
                            if td_key_span[1].text:
                                td_key = td_key_span[1].text.strip()
                        result[td_key.replace(u"{", "").replace(u"}", "")] = td_val
                    except Exception as e:
                        self.log.error(u'解析基本信息出错，原因：' % str(e))

                    try:
                        if td_len == 4:
                            attrt = td_xp[3].attrib
                            if not attrt:
                                attrt = ""
                                td_xp_span = td_xp[3].xpath(".//span")
                                if td_xp_span:
                                    for tds in range(0, len(td_xp_span)):
                                        attrt += str(td_xp_span[tds].attrib)
                                        if not attrt:
                                            if td_xp_span[tds].text:
                                                attrt += str(td_xp_span[tds].text.encode("utf-8"))
                                else:
                                    if td_xp[3].text:
                                        attrt = str(td_xp[3].text.encode("utf-8"))
                            else:
                                attrt = str(attrt)

                            # print attrt
                            td_val = ""
                            for key in base.keys():
                                # 防止name(负责人等)与entname(公司名)存在时取值name就退出
                                if u"entname" in attrt:
                                    td_val = base["entname"]
                                    break
                                if key in attrt:
                                    td_val = base[key]
                                    if td_val:
                                        break

                            if not td_val:
                                attrt = ""
                                td_xp_span = td_xp[3].xpath(".//span")
                                if td_xp_span:
                                    for tds in range(0, len(td_xp_span)):
                                        attrt += str(td_xp_span[tds].attrib)
                                        if not attrt:
                                            if td_xp_span[tds].text:
                                                attrt += str(td_xp_span[tds].text.encode("utf-8"))
                                else:
                                    if td_xp[3].text:
                                        attrt = str(td_xp[3].text.encode("utf-8"))

                                td_val = ""
                                for key in base.keys():
                                    # 防止name(负责人等)与entname(公司名)存在时取值name就退出
                                    if u"entname" in attrt:
                                        td_val = base["entname"]
                                        break
                                    if key in attrt:
                                        td_val = base[key]
                                        if td_val:
                                            break

                            td_key = td_xp[2].text
                            if td_key:
                                td_key = td_key.strip()
                            if not td_key:
                                td_key_span = td_xp[2].xpath(".//span")
                                if len(td_key_span)<2:
                                    continue
                                if td_key_span[1].text:
                                    td_key = td_key_span[1].text.strip()
                            result[td_key.replace(u"{", "").replace(u"}", "")] = td_val
                    except Exception as e:
                        self.log.error(u'解析基本信息出错，原因：%s' % str(e))

                except Exception as e:
                    self.log.error(u'解析基本信息出错，原因：%s' % str(e))
                    continue

        except Exception as e:
            self.log.error(u'访问基本信息网页模板失败，原因：%s' % str(e))
            return result

        # 根据网站判断条件赋值，完善数据
        try:
            if base.has_key('opto'):
                pass
            else:
                result[u'营业期限至'] = u'永久'
            if base.has_key('regorg'):
                regorg = base['regorg']
                if regorg == u'高新区分局':
                    result[u'登记机关'] = u'九龙坡区分局'
                elif regorg == u'九龙坡局高新区局':
                    result[u'登记机关'] = u'九龙坡局'
                elif regorg == u'经开区分局':
                    result[u'登记机关'] = u'南岸区分局'
                elif regorg == u'南岸局经开区局':
                    result[u'登记机关'] = u'南岸局'
                else:
                    result[u'登记机关'] = base['regorg']
            if base.has_key('opstateno'):
                opstateno = base['opstateno']
                if opstateno == "2":
                    result[u'登记状态'] = u"已吊销"
                    if base.has_key('revdate'):
                        result[u'吊销日期'] = base['revdate']
                else:
                    if base.has_key('opstate'):
                        result[u'登记状态'] = base['opstate']
                    del result[u'吊销日期']
            if base.has_key('regcap'):
                result[u'注册资本'] = str(result[u'注册资本']) + u'万元人民币'
            if u"creditcode" in base:
                result[u"统一社会信用代码/注册号"] = base.get("creditcode")
                result[u"top_统一社会信用代码/注册号"] = base.get("creditcode")
            else:
                result[u"统一社会信用代码/注册号"] = base.get("regno")
                result[u"top_统一社会信用代码/注册号"] = base.get("regno")
        except Exception as e:
            self.log.error(u'转换部分基本信息判断数据失败，原因：%s' % str(e))

        return result

    def fzjgxx_information(self,company_infomation):
        try:

            fzjgxx = company_infomation.setdefault("brunchs", [])
            fz = []
            if len(fzjgxx) > 0:
                self.log.info(u"分支机构信息获取开始")
                for f_fz in fzjgxx:
                    f_fzxx = {}
                    f_fzxx[u"统一社会信用代码/注册号"] = f_fz.setdefault("regno", "")
                    f_fzxx[u"名称"] = f_fz.setdefault("brname", "")
                    f_fzxx[u"登记机关"] = f_fz.setdefault("regorgname", "")
                    if filter(lambda x: len(x) > 1, f_fzxx.values()):
                        fz.append(f_fzxx)
            return fz
        except Exception as e:
            self.log.error(u"分支机构信息获取出错%s" % e)


    def parseTop(self,top_json):
        top = {}
        if not isinstance(top_json,dict) and  not isinstance(top_json,list):
            top_json = json.loads(top_json)
        if not top_json:
            return top
        topjson = top_json[0]['_body']
        tree = etree.HTML(topjson)
        tops = tree.xpath(".//*[@id='user-info']/span/text()")
        if not tops:
            return top
        top[u"top_企业名称"] = str(tops[0])
        for tt in tops[1:]:
            if re.search(u"{{.*?}}",tt):
                continue
            ky = tt.split("：")
            if len(ky)==2:
                top[u"top_"+ky[0]] = ky[1]
        return top

    def getjsonstr(self,htmls):
        """
        解析字符串，返回里面的json字符串
        :param  (str):  可能含有json字符串的字符串  -> abc{xxx}
        :return:  (str) json字符串 ->{xxx}
        """
        str = htmls.strip()
        start = str.find('{')
        fstart = str.find('[')

        if fstart >= 0 and (fstart < start or start < 0):
            start = fstart
            end = str.rfind("]")
        else:
            end = str.rfind('}')
        if start > -1 and end > start:
            return json.loads(str[start:end + 1])






if __name__ == "__main__":
    handler = ChongqingHandler("Chongqing")
