# -*- coding: utf-8 -*-
# Created by wuyong on 2016/5/21.

import sys
import os
import re
import json
import copy
import chardet
from lxml import etree
import time
from ParserBase import ParserBase
import html4test as test
reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))



#TODO 行政处罚json不知道怎么解析(因为没有数据样式)
class ShandongHandler(ParserBase):
    """
    ParserShanghai is used to parse the enterprise info from Shanghai
    @version:1.0
    @author: wuyong
    @modify:
    """
    def __init__(self, pinyin):
        """
        Initiate the parameters.
        """
        ParserBase.__init__(self, pinyin)
        self.ignore_key_list.extend(["gdxq_html",u'gdxx.详情'])
        self.ignore_key_list.extend(["_", u'gdxx.详情'])
        self.initMapper()
        self.log.info("ShandongHandler 构造完成")


    def initMapper(self):
        self.appendJsonMapperConfig("baxx_json", {'name': u'baxx.姓名', 'position': u'baxx.职务'})
        self.appendJsonMapperConfig("fzjg_json", {'regno': u'fzjg.注册号', 'brname': u'fzjg.名称', 'regorg':u'fzjg.登记机关'})

    #TODO  {u'注册资本': u'25142.24%xa0万', 在线unicode转中文，出现%xa0字符,尝试过替换，替换不了
    def parse(self, html_dict, reslt_dict=None):
        if not html_dict or not isinstance(html_dict, dict):
            return None
        if 'company_name' in html_dict:
            self.log.info("开始解析 %s" % html_dict['company_name'])
        self.log.info("开始解析通用信息")
        company = self.parseCommon(html_dict)   #没传映射配置
        print 'company,  ',  company
        self.log.info("通用信息解析完成")
        top_dict = self.parseTop(html_dict)
        if top_dict:
            self.log.info("top信息解析成功")
            company.update(top_dict)
        else:
            self.log.info("top信息解析失败")
        jsonstr_dict = self.parseGdxxBgxx(html_dict)
        if jsonstr_dict:
            company.update(jsonstr_dict)
        company = self.standardizeField(company)

        company_copied = copy.deepcopy(company)
        if reslt_dict and isinstance(reslt_dict, dict):
            reslt_dict.update(company_copied)
        result_json = json.dumps(reslt_dict, ensure_ascii=False)
        self.log.info("ShandongHandler解析结果：\n" + result_json)
        print 'rsdict  ', company_copied#[u'fzjg']
        return reslt_dict

    def standardizeField(self, company):
        self.log.info("开始清理、修复字段")
        zb = company.get(u'注册资本')
        if zb:
            company[u'注册资本'] = self.remove_all_space_char(zb)
        return company

    def remove_all_space_char(self, ss):
        """
        去掉所有的不可见字符，包括空格，换行等等
        """
        temp = re.sub(ur'[\x00-\x20]', '', unicode(ss))
        return re.sub(ur'\xa0', '', unicode(temp))

    def parseTop(self, html_dict):
        if 'jbxx_html' not in html_dict:
            return None
        jbxx_list = html_dict['jbxx_html']
        if not jbxx_list:
            return None
        if '_body' not in jbxx_list[0]:
            return None
        return self.parseTopHtml(jbxx_list[0]['_body'])

    def parseTopHtml(self, html):
        if not html:
            return None
        # 页面编码检测
        try:
            encoding = chardet.detect(html)['encoding']  # 此处检测有时会出异常
            tree = etree.HTML(html.decode(encoding))
        except:
            tree = etree.HTML(html)
        self.log.info("开始解析top信息")
        dict_ = dict()
        try:
            top_str = tree.xpath(".//*[@id='details']/h2/text()")
            print 'topstr,  ',  top_str
            if not top_str:
                print 'topstr1,  ', top_str
                self.log.info("获取top信息失败")
                return None
            #.replace(u'\xa0', '')

            top_str = top_str[0].replace("该企业已列入经营异常名录", "").replace(u'“该企业为吊销状态”','').replace(u':', u'：')
            tops = top_str.split()
            print 'topsxxx, ', tops
            print len(tops)
            if len(tops) >= 2:
                dict_[u'top_企业名称'] = tops[0].strip()
                zch = tops[1].split(u'：')
                if len(zch) == 2:
                    dict_[u'top_' + zch[0].strip()] = zch[1].strip()
        except:
                self.log.info("获取top信息异常")
        print dict_
        return dict_

    def parseGdxxBgxx(self, html_dict):
        if 'jbxx_html' not in html_dict:
            return None
        jbxx_list = html_dict['jbxx_html']
        if not jbxx_list:
            return None
        if '_body' not in jbxx_list[0]:
            return None
        return self.parseGdxxBgxxHtml(jbxx_list[0]['_body'])


    def parseGdxxBgxxHtml(self, body):
        map_dict = {}
        for key in [u'czxxliststr', u'bgsxliststr']:
            rs = re.findall(r'var\s+%s\s*=\s*\'\s*(\[.*?\])\s*\'\s*;' % key, body, re.S)
            map_dict[key] = rs[0] if rs else u'[]'
        rs = self.parseJsonInfo(map_dict)
        print 'rs', rs
        return rs

    def parseJsonInfo(self, map_dict):
        qyxx = {}
        czxx_list = json.loads(self.toUtf8(map_dict['czxxliststr']))
        bgxx_list = json.loads(self.toUtf8(map_dict['bgsxliststr']))
        qyxx[u'gdxx'] = self.parseCzxxList(czxx_list)
        qyxx[u'bgxx'] = self.parseBgxxList(bgxx_list)
        for k, v in qyxx.items():
            if not v:
                del qyxx[k]
        return qyxx

    # TODO 详情不加进去
    def parseCzxxList(self, czxx_list):
        print 'czxx_lsit ', czxx_list
        czxx_rlist = []
        for czxx in czxx_list:
            czxx_rlist.append({
                u"股东类型": czxx.get('invtype', ''),
                u"股东": czxx.get('inv', ''),
                u"证照/证件类型": czxx.get('blictype', ''),
                u"证照/证件号码": czxx.get('blicno'),
            })
        print 'czxx_rlist ', czxx_rlist
        return czxx_rlist

    def parseBgxxList(self, bgxx_list):
        print 'bgxx_list ', bgxx_list
        bgxx_rlist = []
        for bgxx in bgxx_list:
            bgxx_rlist.append({
                u"变更事项": bgxx.get('altitem', ''),
                u"变更前内容": bgxx.get('altbe', ''),
                u"变更后内容": bgxx.get('altaf', ''),
                u"变更日期": self.secToTime(bgxx['altdate']['time'] if bgxx.get('altdate') else ''),
            # bgxx['altdate']['time'] if bgxx['altdate'] else '',
            })

        print 'bgxx_rlist ', bgxx_rlist
        return bgxx_rlist

    def toUtf8(self, s):
        if isinstance(s, unicode):
            print 'unicode',
            company_key = s.encode('utf-8')
        else:
            charcode = chardet.detect(s).get('encoding')
            print charcode, s
            if charcode:
                s = s.decode(charcode).encode('utf-8')
        return s

    def secToTime(self, sec):
        str_time = time.strftime(u"%Y年%m月%d日", time.localtime(sec / 1000)) if sec else ''
        print str_time
        return unicode(str_time) if isinstance(str_time, str) else str_time

if __name__ == "__main__":
    # top_dict = test_top()
    #handler = BeijingHandler("beijing")
    #tp_dict = handler.parseTopHtml(test.html_shanghai)
    pass


