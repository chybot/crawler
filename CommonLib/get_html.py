# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding("UTF-8")
import time
import cookielib
import urlparse
import platform

sys.path.append("../")
from common import webutil
from common import proxyutils
from common import exceputil
from common import mongoutil
def get_html(url,proxy,logging,data=None,method="get",encoding="UTF-8"):
    error_count=1
    while True:
        try:
            logging.info(u"第%d次访问%s的信息"%(error_count,url))
            ua,cookieJar=webutil.get_user_agent(),cookielib.MozillaCookieJar()
            header={
                "Host":urlparse.urlparse(url).netloc,
                #"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
            }
            html=webutil.request(url,headers=header,proxy=proxy,data=data,method=method,encoding=encoding,ua=ua,cookie=cookieJar,savefile=None)
            if len(html)<100:
                time.sleep(1)
                raise Exception(u"访问该关键字的公司列表网页长度不合法")
            break
        except Exception as e:
            error_count+=1
            proxy=proxyutils.choice_proxy(is_debug=False,area=u"电信")
            logging.error(exceputil.traceinfo(e))
            continue
    return html

def insert_mongo(_id,dict_,logging,tables,dbs="bigdata_higgs"):
        while True:
            try:
                logging.info(u"company_name:%s插入:%s库%s表"%(_id,dbs,tables))
                if "Linux" in platform.system():
                    db_table=mongoutil.getmondb("master",25017,dbs,tables).table
                else:
                    db_table=mongoutil.getmondbbyhost(dbs, tables).table
                db_table.insert(dict_)
                break
            except Exception as e:
                exceputil.traceinfo(e)
                time.sleep(10)
                continue