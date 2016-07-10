# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding("UTF-8")
import time
import re
import cookielib
import os
import json
sys.path.append("../")
from common import functions
from common import mongoutil

if not os.path.exists("D:/hehongjing"):
    os.makedirs("D:/hehongjing")
def main_():
    dict_={u"北京":30000,u"上海":30000,u"江苏":20000,u"浙江":20000}
    f=open("D:/hehongjing/xxx.json","w")
    for dd in dict_:
        table=mongoutil.getmondbbyhost("bigdata_higgs","qyxx").table
        tables=table.find({"type":dd}).limit(dict_[dd])
        for tt in tables:
            jj=json.dumps(tt)
            f.write(jj+"\n")
    f.close()

if __name__=="__main__":
    main_()