# -*- coding: utf-8 -*-
# Created by John on 2016/6/3.

import sys
import os
import json
import copy
import re
import time
import chardet
from lxml import etree
from ParserNbBase import ParserNbBase
from CommonLib.TimeUtil import TimeUtil
import html4test as test

reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


class JilinNbHandler(ParserNbBase):
    """
    JilinNbHandler is used to parse the annual report
    @version:1.0
    @author:John Liu
    @modify:
    """

    def __init__(self, pinyin):
        """
        Initiate the parameters.
        """
        ParserNbBase.__init__(self, pinyin)

    def parse(self, html_dict, reslt_dict=None):
        if not html_dict or not isinstance(html_dict, dict):
            return None
        if 'company_name' in html_dict:
            self.log.info(u"开始解析 %s" % html_dict['company_name'])
        self.log.info(u"开始解析通用信息")
        company = self.parseCommon(html_dict)
        self.log.info(u"通用信息解析完成")
        company_copied = copy.deepcopy(company)

        # Manual parsing start
        qynb = company_copied[u'qynb']
        web_html = map(lambda x:html_dict[x],filter(lambda x:x.endswith('_html'),html_dict.keys()))
        web_html = map(lambda x: json.loads(x) if not isinstance(x,(list,dict)) else x, web_html)
        web_html = map(lambda x:x.get('_body'), web_html[0])
        web_html = str(web_html[0])

        tree = etree.HTML(web_html)
        script = str(tree.xpath(".//script[3]/text()")[0])
        script = script.replace("var", "").strip().replace(" ", "")

        qynb[u"网站或网店信息"] = self.parseWebsite(script)
        qynb[u"股东及出资信息"] = self.parseStockholderContribute(script)
        qynb[u"对外投资信息"] = self.parseInvestment(script)
        qynb[u"对外提供保证担保信息"] = self.parseAssurance(script)
        qynb[u"股权变更信息"] = self.parseEquityUpdate(script)
        qynb[u"修改记录"] = self.parseChangeRecord(script)

        company_copied['qynb'] = qynb
        # Manual parsing end

        if reslt_dict and isinstance(reslt_dict, dict):
            reslt_dict.update(company_copied)
        result_json = json.dumps(reslt_dict, ensure_ascii=False)
        self.log.info(u"JilinNbHandler解析结果：\n" + result_json)
        return reslt_dict

    def parseWebsite(self, script):
        website = []
        wdxxliststr = re.findall(r"wdxxliststr='([^']+)'", script)
        if wdxxliststr:
            wdxxlist = json.loads(wdxxliststr[0])

            for wdxx in wdxxlist:
                website.append(dict(zip([u"类型", u"名称", u"网址"], [wdxx.get("webtype"), wdxx.get("websitname"), wdxx.get("domain")])))

        return website

    def parseStockholderContribute(self, script):
        sh_cntrbt = []
        czxxliststr = re.findall(r"czxxliststr='([^']+)'", script)
        if czxxliststr:
            czxxlist = json.loads(czxxliststr[0])

            for czxx in czxxlist:
                subcondate = TimeUtil.convertDateFromat(str(TimeUtil.stamp2Date(czxx.get("subcondate")["time"], u"%Y-%m-%d %H:%M:%S")), u"%Y-%m-%d %H:%M:%S", u"%Y年%m月%d日") if czxx.get("subcondate") else None
                accondate = TimeUtil.convertDateFromat(str(TimeUtil.stamp2Date(czxx.get("accondate")["time"], u"%Y-%m-%d %H:%M:%S")), u"%Y-%m-%d %H:%M:%S", u"%Y年%m月%d日") if czxx.get("accondate") else None
                sh_cntrbt.append(dict(zip([u"股东(发起人)", u"认缴出资额(万元)", u"认缴出资时间", u"认缴出资方式", u"实际出资额(万元)", u"出资时间", u"出资方式"],
                                        [czxx.get("inv"), str(czxx.get("lisubconam")) + u"万元", subcondate, czxx.get("subconform").split("|")[1],
                                         str(czxx.get("liacconam")) + u"万元", accondate, czxx.get("acconform")[1]])))

        return sh_cntrbt

    def parseAssurance(self, script):
        assurance = []
        nbdwdbstr = re.findall(r"nbdwdbstr='([^']+)'", script)
        if nbdwdbstr:
            nbdwdblist = json.loads(nbdwdbstr[0])

            for nbdwdb in nbdwdblist:
                priclaseckind = u"合同" if nbdwdb.get("priclaseckind") and nbdwdb.get("priclaseckind") == "1" else u"其他"
                pefperfrom = TimeUtil.convertDateFromat(str(TimeUtil.stamp2Date(nbdwdb.get("pefperfrom")["time"], u"%Y-%m-%d %H:%M:%S")), u"%Y-%m-%d %H:%M:%S", u"%Y年%m月%d日") if nbdwdb.get("pefperfrom") else None
                pefperto = TimeUtil.convertDateFromat(str(TimeUtil.stamp2Date(nbdwdb.get("pefperto")["time"], u"%Y-%m-%d %H:%M:%S")), u"%Y-%m-%d %H:%M:%S", u"%Y年%m月%d日") if nbdwdb.get("pefperto") else None
                guaranperiod = u"期限" if nbdwdb.get("guaranperiod") and nbdwdb.get("guaranperiod") == "1" else u"未约定"
                gatype = u""
                if nbdwdb["gatype"]:
                    if nbdwdb["gatype"] == "1":
                        gatype = u"一般保证"
                    elif nbdwdb["gatype"] == "2":
                        gatype = u"连带保证"
                    else:
                        gatype = u"未约定"

                assurance.append(dict(zip([u"债权人", u"债务人", u"主债权种类", u"主债权数额", u"履行债务的期限", u"保证的期间", u"保证的方式"],
                                          [nbdwdb.get("more"), nbdwdb.get("mortgagor"), priclaseckind, nbdwdb.get("priclasecam"),
                                           pefperfrom + "-" + pefperto, guaranperiod, gatype])))

        return assurance

    def parseInvestment(self, script):
        investment = []
        dwtzliststr = re.findall(r"dwtzliststr='([^']+)'", script)
        if dwtzliststr:
            dwtzlist = json.loads(dwtzliststr[0])

            for dwtz in dwtzlist:
                investment.append(dict(zip([u"投资设立企业或购买股权企业名称", u"注册号"], [dwtz.get("entname"), dwtz.get("regno")])))

        return investment

    def parseEquityUpdate(self, script):
        equity_update = []
        nbgqbgsstr = re.findall(r"nbgqbgsstr='([^']+)'", script)
        if nbgqbgsstr:
            gqbglist = json.loads(nbgqbgsstr[0])

            for nbgqbg in gqbglist:
                altdate = TimeUtil.convertDateFromat(str(TimeUtil.stamp2Date(nbgqbg.get("altdate")["time"], u"%Y-%m-%d %H:%M:%S")), u"%Y-%m-%d %H:%M:%S", u"%Y年%m月%d日") if nbgqbg.get("altdate") else None
                equity_update.append(dict(zip([u"股东(发起人)", u"变更前股权比例", u"变更后股权比例", u"股权变更日期"],
                                              [nbgqbg.get("inv"), str(nbgqbg.get("transamprpre")) + "%", str(nbgqbg.get("transampraf")) + "%", altdate])))

        return equity_update

    def parseChangeRecord(self, script):
        change_record = []
        nbalthisstr = re.findall(r"nbalthisstr='([^']+)'", script)
        if nbalthisstr:
            nbalthislist = json.loads(nbalthisstr[0])

            for nbalthis in nbalthislist:
                altdate = TimeUtil.convertDateFromat(str(TimeUtil.stamp2Date(nbalthis.get("altdate")["time"], u"%Y-%m-%d %H:%M:%S")), u"%Y-%m-%d %H:%M:%S", u"%Y年%m月%d日") if nbalthis.get("altdate") else None
                change_record.append(dict(zip([u"修改事项", u"修改前", u"修改后", u"修改日期"],
                                              [nbalthis.get("altfield"), nbalthis.get("altbefore"), nbalthis.get("altafter"), altdate])))

        return change_record

if __name__ == "__main__":
    pass
