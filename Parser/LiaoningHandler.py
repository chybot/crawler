# -*- coding: utf-8 -*-
# Created by fml on 2016/6/22.

import sys
import os
import re
import json
import copy
import chardet
from lxml import etree
from ParserBase import ParserBase
import html4test as test
reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

class LiaoningHandler(ParserBase):
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
        self.ignore_key_list.extend(["gdxq_html",u'gdxx.详情'])
        self.log.info("LiaoningHandler 构造完成")


    def parse(self, html_dict, reslt_dict=None):
        if not html_dict or not isinstance(html_dict, dict):
            return None
        if 'company_name' in html_dict:
            self.log.info("开始解析 %s" % html_dict['company_name'])
        self.log.info("开始解析通用信息")
        company = self.parseCommon(html_dict)
        for k,v in company.items():
            if not v:
                del company[k]
        self.log.info("通用信息解析完成")
        top_dict = self.parseTop(html_dict)
        if top_dict:
            self.log.info("top信息解析成功")
            company.update(top_dict)
        else:
            self.log.info("top信息解析失败")
        baxx = self.getBaxx(html_dict,'baxx_html')
        company.update(baxx)
        if 'gdxx' not in company:
            company['gdxx']=self.getGdxx(html_dict,'gdxx_html')
        company['fzjg'] = self.getFzjg(html_dict,'fzjg_html')
        company['bgxx'] = self.getBgxx(html_dict,'bgxx_html')
        company_copied = copy.deepcopy(company)
        if reslt_dict and isinstance(reslt_dict, dict):
            reslt_dict.update(company_copied)
        result_json = json.dumps(reslt_dict, ensure_ascii=False)
        self.log.info("LiaoningHandler解析结果：\n" + result_json)
        print 'rsdict  ', company_copied

        return reslt_dict
    def getBgxx(self,html_dict,key):
        '''
        获取变更信息
        :param html_dict:
        :param key:
        :return:
        '''

        bgxx = []
        values = self.getWeb(html_dict, key)
        if not values:
            return bgxx
        values = values[0]
        bgxx_re = re.compile(r"paging\((.*?\}\])")
        bgxx_s = bgxx_re.search(values)
        if bgxx_s:
            bgxx_s = eval(bgxx_s.group(1))
            for bg in bgxx_s:
                dict_bg = {}
                dict_bg[u"变更事项"] = bg.setdefault("altitemName", "")
                dict_bg[u"变更前内容"] = bg.setdefault("altbe", "")
                dict_bg[u"变更后内容"] = bg.setdefault("altaf", "")
                dict_bg[u"变更日期"] = bg.setdefault("altdate", "")
                if filter(lambda x: len(x) > 1, dict_bg.values()):
                    bgxx.append(dict_bg)
        return bgxx

    def getFzjg(self,html_dict,key):
        '''
        获取分支机构信息
        :param html_dict:
        :param key:
        :return:
        '''
        fzjg = []
        values = self.getWeb(html_dict, key)
        if not values:
            return fzjg
        values = values[0]
        fzjg_re = re.compile(r"fzjgPaging\((\[\{.*?\}\])")
        fzjg_s = re.search(fzjg_re,values)
        if fzjg_s:
            fzjg = fzjg_s.group(1)
        return fzjg

    def getGdxx(self,html_dict,key):
        '''
        获取股东信息
        :param html_dict:
        :param key:
        :return:
        '''

        gdxx = []
        values = self.getWeb(html_dict, key)
        if not values:
            return gdxx
        values = values[0]
        gdxx_re = re.compile(r"tzr_paging\((\[\{.*?\}\])")
        gdxx_s = gdxx_re.search(values)
        if gdxx_s:
            gdxx_s = eval(gdxx_s.group(1))
            for gd in gdxx_s:
                gd_dict = {}
                gd_dict[u"股东类型"] = gd.setdefault("invtypeName", "")
                gd_dict[u"股东"] = gd.setdefault("inv", "")
                gd_dict[u"证照/证件类型"] = gd.setdefault("sconformName", "") or gd.setdefault(
                    "blictypeName", "")
                if re.search(u"\d", gd_dict[u"证照/证件类型"], re.S):
                    gd_dict[u"证照/证件类型"] = gd.setdefault("blictypeName", "")
                if "|" in gd_dict[u"证照/证件类型"]:
                    gd_dict[u"证照/证件类型"] = gd.setdefault("blictypeName", "")

                gd_dict[u"证照/证件号码"] = gd.setdefault("blicno", "")
                if filter(lambda x: len(x) > 1, gd_dict.values()):
                    gdxx.append(gd_dict)
        else:
            gdxx_re = re.compile(r"tzr_nzhh_paging\((\[\{.*?\}\])")
            gdxx_s = gdxx_re.search(values)
            if gdxx_s:
                gdxx_s = eval(gdxx_s.group(1))
                for gd in gdxx_s:
                    gd_dict = {}
                    gd_dict[u"合伙人类型"] = gd.setdefault("invtypeName", "")
                    gd_dict[u"合伙人"] = gd.setdefault("inv", "")
                    gd_dict[u"证照/证件类型"] = gd.setdefault("blictypeName", "")
                    gd_dict[u"证照/证件号码"] = gd.setdefault("blicno", "")
                    if filter(lambda x: len(x) > 1, gd_dict.values()):
                        gdxx.append(gd_dict)
        if not gdxx:
            gdxx_re = re.compile(r"tzr_fgsfr_paging\((\[\{.*?\}\])")
            tzrxx_s = gdxx_re.search(values)
            if tzrxx_s:
                tzrxx = eval(tzrxx_s.group(1))
                for tz in tzrxx:
                    dict_tz = {}
                    dict_tz[u"出资人类型"] = tz.setdefault("invtypeName", "")
                    dict_tz[u"出资人"] = tz.setdefault("inv", "")
                    dict_tz[u"证照/证件类型"] = tz.setdefault("blictypeName", "")
                    dict_tz[u"证照/证件号码"] = tz.setdefault("blicno", "")
                    if filter(lambda x: len(x) > 1, dict_tz.values()):
                        gdxx.append(dict_tz)

        # 个人独资企业
        if not gdxx:
            gdxx_re = re.compile(r"tzr_grdz_paging\((\[\{.*?\}\])")
            grtzxx_s = gdxx_re.search(values)
            if grtzxx_s:
                grtzxx = eval(grtzxx_s.group(1))
                for grt in grtzxx:
                    dict_tz = {}
                    dict_tz[u"姓名"] = grt.setdefault("inv", "")
                    dict_tz[u"出资方式"] = grt.setdefault("sconformName", "")
                    if filter(lambda x: len(x) > 1, dict_tz.values()):
                        gdxx.append(dict_tz)
        return gdxx

    def getBaxx(self,html_dict,key):
        '''
        获取备案信息或者股东信息
        :param html_dict:
        :param key:
        :return:
        '''
        baxx = []
        values = self.getWeb(html_dict,key)
        if not values:
            return {'baxx':baxx}
        values = values[0]
        baxx_ = re.search(r"\((\[.*?\}\])", str(values))
        if baxx_:
            for ba in json.loads(baxx_.group(1)):
                bas = {}
                bas[u"姓名"] = ba.setdefault("name", "")
                bas[u"职务"] = ba.setdefault("positionName", "")
                if filter(lambda x: len(x) > 1, bas.values()):
                    baxx.append(bas)
        else:
            tzrxx_re = re.compile(r"tzr_fgsfr_paging\((\[\{.*?\}\])")
            tzrxx_s = tzrxx_re.search(values)
            if tzrxx_s:
                tzrxx = eval(tzrxx_s.group(1))
                gdxx = []
                for tz in tzrxx:
                    dict_tz = {}
                    dict_tz[u"出资人类型"] = tz.setdefault("invtypeName", "")
                    dict_tz[u"出资人"] = tz.setdefault("inv", "")
                    dict_tz[u"证照/证件类型"] = tz.setdefault("sconformName", "")
                    dict_tz[u"证照/证件号码"] = tz.setdefault("blicno", "")
                    if filter(lambda x: len(x) > 1, dict_tz.values()):
                        gdxx.append(dict_tz)
                return {'gdxx':gdxx}
        if baxx:
            # 设置编号
            num = 0
            for item in baxx:
                num += 1
                item[u"序号"] = str(num)
            return {'baxx':baxx}

    def parseTop(self,html_dict):
        '''
        解析top_html
        :param html_dict:
        :return:
        '''
        top = dict()
        top_html = self.getWeb(html_dict,'top_html')
        if not top_html:
            return top
        top_html = top_html[0]
        top_tree = etree.HTML(top_html)
        tops = "".join(top_tree.xpath(".//*[@id='details']/h2/text()")).strip().split()
        if tops:
            top[u"top_企业名称"] = tops[0]
            for tt in tops[1:]:
                kv = tt.split("：")
                if len(kv) == 2:
                    top[u"top_" + kv[0]] = kv[1]
        return top

    def getWeb(self,html_dict,key):
        '''
        获取web对象指定的body
        :param html_dict:
        :param key:
        :return:
        '''
        values = html_dict.get(key)
        if not values:
            return None
        values = map(lambda x:x.get('_body'),values)
        if key.endswith('json'):
            values = [json.loads(x) for x in values if isinstance(x,basestring)]
        return values

    def remove_all_space_char(self, ss):
        """
        去掉所有的不可见字符，包括空格，换行等等
        :param ss:
        :return:
        """
        temp = re.sub(ur'[\x00-\x20]', '', unicode(ss))
        return re.sub(ur'\xa0', '', unicode(temp))



if __name__ == "__main__":
    pass


