# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding("UTF-8")
import re
import os
import json
sys.path.append("../")
from common import mongoutil
from common import exceputil

if not os.path.exists("D:/hehongjing"):
    os.makedirs("D:/hehongjing")
p=re.compile('\\"(.*?)\\"')
def main_():
    dict_={u"北京":30000,u"上海":30000,u"江苏":20000,u"浙江":20000}
    f=open("D:/hehongjing/xxxx.json","w")
    for dd in dict_:
        print dd
        table=mongoutil.getmondbbyhost("bigdata_higgs","qyxx").table
        tables=table.find({"type":dd}).limit(dict_[dd])
        for tt in tables:
            try:
                if dd==u"上海":
                    for _html in ["other_html","company_html"]:
                        if _html in tt:
                            del tt[_html]
                if dd==u"浙江":
                     for _html in ["baxx_html"]:
                        if _html in tt:
                            del tt[_html]
                jj=json.dumps(tt)
                jj=jj.replace(u"xa0","").replace("ue001","").replace("ue00b","").replace("\\\\","\\")
                #js= jj.decode('raw_unicode_escape').encode("UTF-8")
                js= jj.decode('raw_unicode_escape').decode("UTF-8").encode("GBK")
                f.write(js+"\n")
            except Exception as e:
                exceputil.traceinfo(e)
    f.close()
    print "end"

if __name__=="__main__":
    main_()