# -*- coding: utf-8 -*-
# Created by David on 2016/6/3.
import re
import sys
import os
import time
import json
import copy
import chardet
from lxml import etree
from ParserNbBase import ParserNbBase
from lxml import etree

import html4test as test
reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

class ShandongNbHandler(ParserNbBase):
    """
    ShandongNbHandler is used to parse the annual report
    @version:1.0
    @author:wuyong
    @modify:
    """
    def __init__(self, pinyin):
        """
        Initiate the parameters.
        """
        ParserNbBase.__init__(self, pinyin)
        self.log.info(u"ShandongNbHandler 构造完成")

    def parse(self, html_dict, reslt_dict=None):
        if not html_dict or not isinstance(html_dict, dict):
            return None
        if 'company_name' in html_dict:
            self.log.info(u"开始解析 %s" % html_dict['company_name'])
        self.log.info(u"开始解析通用信息")
        company = self.parseCommon(html_dict)
        self.log.info(u"通用信息解析完成")
        key = filter(lambda x:x.endswith("_html") , html_dict.keys())
        body = html_dict[key[0]][0]["_body"] if key else ''
        map_dict = self.parseNbInfo(body)
        company['qynb'].update(map_dict)
        company_copied = copy.deepcopy(company)
        if reslt_dict and isinstance(reslt_dict, dict):
            reslt_dict.update(company_copied)
        result_json = json.dumps(reslt_dict, ensure_ascii=False)
        print 'company: ', company
        #self.log.info(u"SichuanNbHandler解析结果：\n" + result_json)
        return reslt_dict

    def parseNbInfo(self, body):
        map_key = ['wdxxliststr', 'czxxliststr', 'dwtzliststr', 'nbdwdbstr', 'nbgqbgsstr', 'nbalthisstr']
        map_dict = {}
        for key in map_key:
            rs = re.findall(r'var\s+%s\s*=\s*\'\s*(\[.*?\])\s*\'\s*;' % key, body, re.S)
            map_dict[key] = rs[0] if rs else u'[]'
        rs = self.parseJsonInfo(map_dict)
        return rs
        #return map_dict


        #print 'map_dict ' , map_dict
    def parseJsonInfo(self, map_dict):
        qynb = {}
        qynb[u'网站或网店信息'] = self.parseWebSites(json.loads(map_dict['wdxxliststr']))
        qynb[u'股东及出资信息'] = self.pasreGdczxx(json.loads(map_dict['czxxliststr']))
        qynb[u'对外投资信息'] = self.parseDwtzlxx(json.loads(map_dict['dwtzliststr']))
        qynb[u'对外提供保证担保信息'] = self.parseDwbgxx(json.loads(map_dict['nbdwdbstr'])) #
        qynb[u'股权变更信息'] = self.parseGqbgxx(json.loads(map_dict['nbgqbgsstr']))
        qynb[u'修改记录'] = self.parseXgjl(json.loads(map_dict['nbalthisstr']))
        for k, v  in qynb.items():
            if not v:
                del qynb[k]
        return qynb

    #TODO 对照js修改完毕
    def parseWebSites(self, wbxx_list):
        #print 'web_lsit ', wbxx_list
        web_site_list = []
        for wbxx in  wbxx_list:
            type_id = wbxx.get('webtype')
            if not type_id:
                type_ch = ''
            else:
                type_ch = u'网站' if type_id == u'1' else u'网店'
            web_site_list.append({u'类型':type_ch, u'名称':wbxx.get('websitname', ''), u'网址':wbxx.get('domain', '')})
        return web_site_list

    #股东出资信息
    def pasreGdczxx(self, czxx_list):
        #print 'czxx_list ', czxx_list
        czxx_rlist = []
        for czxx in czxx_list:
            czxx_rlist.append({
                u'股东（发起人）': czxx.get('inv', ''),
                u'认缴出资额': self.getRelMoney(czxx.get('lisubconam', ''), czxx.get('subconcurrency')),
                u'认缴出资时间': self.secToTime(czxx['subcondate'].get('time') if czxx.get('subcondate') else None),
                u'认缴出资方式': czxx.get('subconform').split('|')[-1] if czxx.get('subconform') else '',
                u'实缴出资额': self.getRelMoney(czxx.get('liacconam', ''), czxx.get('acconcurrency')),
                u'实缴出资时间': self.secToTime(czxx['subcondate'].get('time') if czxx.get('subcondate') else None),
                u'实缴出资方式': czxx['acconform'].split('|')[1] if czxx.get('acconform') else '',
            })
       # print 'czxx_rlist',  czxx_rlist
        return czxx_rlist

    #对外投资信息
    def parseDwtzlxx(self, dwtz_list):
        print 'dwtz_list ',  dwtz_list
        dwtz_rlist = []
        for dwtz in dwtz_list:
            dwtz_rlist.append({
                u"投资设立企业或购买股权企业名称": dwtz.get('entname', ''),
                u"注册号":  dwtz.get('regno', '')
            })
        print 'dwtz_rlist', dwtz_rlist
        return   dwtz_rlist

    #ok
    def parseGqbgxx(self, gqbg_list):
        print 'gqbg_list ' , gqbg_list
        gqbg_rlist = []
        for gdxx in gqbg_list:
            gqbg_rlist.append({
                u"股东（发起人）": gdxx.get('inv', ''),
                u"变更前股权比例": str(gdxx['transamprpre'])+'%' if gdxx.get('transamprpre') else '',
                u"变更后股权比例": str(gdxx['transampraf'])+'%' if gdxx.get('transampraf') else '',
                u"股权变更日期": self.secToTime(gdxx['altdate']['time'] if gdxx.get('altdate') else None),
            })
        print gqbg_rlist
        return gqbg_rlist

    #修改事项
    def parseXgjl(self, xgjl_list):
        print 'xgjl_list' , xgjl_list
        xgjl_rlist = []
        index  = 1
        for xgjl in xgjl_list:
            xgjl_rlist.append({
                u'序号': index,
                u'修改事项': xgjl.get('altfield', ''),
                u'修改前': xgjl.get('altbefore', ''),
                u'修改后': xgjl.get('altafter', ''),
                u'修改日期': self.secToTime(xgjl['altdate']['time'] if xgjl.get('altdate') else None)
            })
            index += 1
        print xgjl_rlist
        return xgjl_rlist

    #测试完：日期改成了　年－月－日格式
    def parseDwbgxx(self, dwdb_list):
        #print 'dwdb_list', dwdb_list
        dwdb_rlist = []
        for dwdb in dwdb_list:
            gatype = ''
            if dwdb.get('gatype')=='1':
                gatype = u'一般保证'
            elif dwdb.get('gatype')=='2':
                gatype = u'连带保证'
            else:
                gatype = u'未约定'
            if dwdb.get('pefperfrom') and dwdb.get('pefperto'):
                lxqx = self.secToTime(dwdb["pefperfrom"]['time']) + ' - ' + self.secToTime(dwdb['pefperto']['time'])
            dwdb_rlist.append({
                u"债权人":dwdb.get("more", ''),
                u"债务人":dwdb.get("mortgagor", ''),
                u"主债权种类": u'合同' if dwdb.get("gatype")==u'1' else u'其他',
                u"主债权数额":str(dwdb["priclasecam"])+u'万元' if dwdb.get("priclasecam") else '',
                u"履行债务的期限":lxqx,
                u"保证的期间": u"期限" if dwdb.get('guaranperiod') == u'1' else u'未约定',
                u"保证的方式": gatype
            })
        #print 'dwdb_rlist', dwdb_rlist
        return dwdb_rlist

    def secToTime(self, sec):
        str_time =  time.strftime(u"%Y年%m月%d日", time.localtime(sec/1000)) if sec else ''
        return unicode(str_time) if isinstance(str_time, str) else str_time

    def convertMoney(self, cur):
        strcur = u'元'
        if cur == '156':
            strcur = u'元'
        elif cur == '840':
            strcur == u'美元'
        elif cur == '392':
            strcur == u'日元'
        elif cur == '954':
            strcur == u'欧元'
        elif cur == '344':
            strcur == u'港元'
        elif cur == '826':
            strcur == u'英镑'
        elif cur == '280':
            strcur == u'德国马克'
        elif cur == '124':
            strcur == u'加拿大元'
        elif cur == '250':
            strcur == u'法国法郎'
        elif cur == '528':
            strcur == u'荷兰'
        elif cur == '756':
            strcur == u'瑞士法郎'
        elif cur == '702':
            strcur == u'新加坡元'
        elif cur == '036':
            strcur == u'澳大利亚元'
        elif cur == '208':
            strcur == u'丹麦克郎'
        return strcur

    def getRelMoney(self, money, money_id):
        if not money:
            return ''
        if isinstance(money, (int, float)):
            money = str(money)
        return money + u'万' + self.convertMoney(money_id)

        # if 'webSites' in json_nbinfo:
        #     for item in json_nbinfo['webSites']:
        #         website.append(dict(zip([u'类型',u'名称',u'网址'],[item.get('webtypename',''),item.get('websitname',''),item.get('domain','')])))
        # return website):

        #print 'wdxxliststr  ',  re.findall(r'var\s+wdxxliststr\s*=\s*\'\s*(\[.*?\])\s*\'\s*;', body, re.S)  #网站及网店信息
        #print  'czxxliststr ',  re.findall(r'var\s+czxxliststr\s*=\s*\'\s*(\[.*?\])\s*\'\s*;', body, re.S)  # 股东及出资信息
       # print  'dwtzliststr  ', re.findall(r'var\s+dwtzliststr\s*=\s*\'\s*(\[.*?\])\s*\'\s*;', body, re.S) #对外投资信息

       # print 'nbgqbgsstr', re.findall(r'var\s+nbgqbgsstr\s*=\s*\'\s*(\[.*?\])\s*\'\s*;', body, re.S)  # 股权变更信息
        # print  'nbalthisstr  ', re.findall(r'var\s+nbalthisstr\s*=\s*\'\s*(\[.*?\])\s*\'\s*;', body, re.S)  # 修改信息
        # print  'nbdwdbstr  ', re.findall(r'var\s+nbdwdbstr\s*=\s*\'\s*(\[.*?\])\s*\'\s*;', body, re.S)  # 对外投资担保信息

        # #单独解析股东及出资信息
      #  print 'xian :::  ', company
      #   if body and nb_year:
      #       rs_dic = self.parseGdczxx(body)
      #       if rs_dic:
      #               if  company['qynb'] and  company['qynb'].get(rs_dic.keys()[0]):#(company['qynb'].get(u'股东及出资信息') or ):
      #                   company['qynb'].update(rs_dic)
      #       rs_list =self.parseBgxx(body)
      #       if rs_list:
      #           head  = rs_list[0]
      #           bgxx_list = rs_list[1]
      #           if bgxx_list:
      #               if company['qynb'] and company['qynb'].get(head):
      #                   company['qynb'].update({head:bgxx_list})

       # print 'hou :::  ', company


    # #股东及出资信息
    # def parseGdczxx(self, body):
    #     rs_dict = {}
    #     if not body:
    #         return rs_dict
    #     et = etree.HTML(body.replace("<br>", "").replace("</br>", ""))
    #     # print et.xpath('.//table[@id="table_tzrxx"]/tr[1]/th[1]/text()')
    #     gdcz_list = []
    #     t_tab = et.xpath('.//table[@id="table_tzrxx"]')
    #     if t_tab:
    #         head = t_tab[0].xpath("./tr[1]/th/text()")
    #         if head and head[0].strip():
    #             l_col = t_tab[0].xpath("./tr[2]/th/text()")
    #             if len(l_col) >= 7:
    #                 cols = t_tab[0].xpath('./tr[@name="tzrxx"]')
    #                 for col in cols:
    #                     per_dict = {}
    #                     col_0 = col.xpath('./td[1]/div/text()')
    #                     per_dict[l_col[0]] = col_0[0].strip() if col_0 and col_0[0].strip() else ''
    #                     for i in range(2, 8, 1):
    #                         col_i = col.xpath('./td[%d]/ul/li/text()' % i)
    #                         per_dict[l_col[i - 1].strip()] = col_i[0].strip() if col_i and col_i[0].strip() else ''
    #                     gdcz_list.append(per_dict)
    #                 rs_dict = {head[0].strip(): gdcz_list}
    #     return rs_dict
    #
    # def parseBgxx(self, body):
    #     if not body:
    #         return None
    #     et = etree.HTML(body.replace("<br>", "").replace("</br>", ""))
    #     tab_bg = et.xpath('.//table[@id="table_bgxx"]')
    #     if not tab_bg:
    #         return None
    #     tab_bg = tab_bg[0]
    #     head = tab_bg.xpath('.//tr[1]/th/text()')
    #     if not head or not head[0].strip():
    #         return None
    #     head = head[0].strip()
    #     bgrow = tab_bg.xpath('.//tr[2]/th/text()')
    #     rs_list = []
    #     if bgrow and len(bgrow) >= 5:
    #         bgrow = map(lambda x : x.strip(), bgrow)
    #         if  bgrow[0] and bgrow[1] and bgrow[2] and bgrow[3] and bgrow[4]:
    #             rows = tab_bg.xpath('.//tr[@name="bgxx"]')
    #             for row in rows:
    #                 tmp_dict = {}
    #                 row_1 = row.xpath('.//td[1]/text()')
    #                 tmp_dict[bgrow[0]] = row_1[0] if row_1 else ''
    #                 row_2 = row.xpath('.//td[2]/text()')
    #                 tmp_dict[bgrow[1]] = row_2[0] if row_2 else ''
    #                 row_3_xpah = row.xpath('.//td[3]/span')
    #                 if row_3_xpah:
    #                     row_3 = row_3_xpah[0].xpath('.//text()') if len(row_3_xpah) == 1 else row_3_xpah[1].xpath(
    #                         './/text()')
    #                     tmp_dict[bgrow[2]] = row_3[0].strip() if row_3 else ''
    #                 else:
    #                     tmp_dict[bgrow[2]] = ''
    #                 row_4_xpah = row.xpath('.//td[4]/span')
    #                 if row_4_xpah:
    #                     row_4 = row_4_xpah[0].xpath('.//text()') if len(row_4_xpah) == 1 else row_4_xpah[1].xpath(
    #                         './/text()')
    #                     tmp_dict[bgrow[3]] = row_4[0].strip() if row_4 else ''
    #                 else:
    #                     tmp_dict[bgrow[3]] = ''
    #                 row_5 = row.xpath('.//td[5]/text()')
    #                 tmp_dict[bgrow[4]] = row_5[0].strip() if row_5 else ''
    #                 rs_list.append(tmp_dict)
    #     return head ,rs_list


def secToTime(sec):
    return time.strftime(u"%Y年%m月%d日", time.localtime(sec / 1000)) if sec else ''

if __name__ == "__main__":
    #pass

    print secToTime(1358265600000)
