# -*- coding: utf-8 -*-
"""
企业信息网下载模块
"""

import sys
reload(sys)
sys.setdefaultencoding("UTF-8")
sys.path.append("../")
import time
import re
import urllib
from DownLoader import DownLoader
class qyxx(object):
    def __init__(self, *args,**kwargs):
        self.ss= DownLoader('liaoning')


    def crawler(self):
        self.ss.firstInit()
        res=self.ss.request('http://gsxt.lngs.gov.cn/saicpub/commonsSC/loginDC/securityCode.action?tdate=0')
        from requests import post
        yzm_html=post('http://spider7:5678/form',files={'files':res.content},data={'type':'liaoning'})
        yzm_html.encoding='utf-8'
        yzm_html=yzm_html.content
        assert len (yzm_html.split())==2
        yzm,img_name=yzm_html.split()
        print yzm
        headers={
    "Host": "gsxt.lngs.gov.cn",
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
    "Accept-Encoding": "gzip, deflate",
    "Referer": "http://gsxt.lngs.gov.cn/saicpub/entPublicitySC/entPublicityDC/entPublicity/search/searchmain.jsp",
    "Connection": "keep-alive",
    "Content-Type": "application/x-www-form-urlencoded"
}
        list_ser=self.ss.request('http://gsxt.lngs.gov.cn/saicpub/entPublicitySC/entPublicityDC/lngsSearchFpc.action',method='post',headers=headers,data={
        "authCode":urllib.quote(yzm.encode("UTF-8")),
        "solrCondition":u"铁岭市薄香花"#urllib.quote(company_key.encode("UTF-8"))
    })
        html=list_ser.text
        if re.search(u"您搜索的条件无查询结果",unicode(html)):
            print u"您搜索的条件无查询结果"
            time.sleep(2)
            return (0,False)
        if re.search(u'var\s*?codevalidator\\=\s*?\\"fail\\"\\;',unicode(html)):
            time.sleep(0.5)
            print 'codevalidator'

        company_re=re.compile(r"searchList_paging(.*?)var\s*?codevalidator",re.S)
        company_js=re.search(company_re,str(html))
        if company_js:
            print company_js.group()


if __name__ == '__main__':
    crawler=qyxx()
    while True:
        crawler.crawler()