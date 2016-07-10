# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding("UTF-8")

import glob
import os
from functions import *
from jsonutil import *
from exceputil import *

fout1 = open("qiyeplus_all_company_name_20150601_not_end_gongsi.txt", "w")
fout2 = open("qiyeplus_all_company_name_20150601_end_gongsi.txt", "w")
i = 0
company_name_gongsi_count = 0
for filename in get_all_filename_from_dir(ur"D:\devtemp\qiplus_v1.3.3_20150601\data"):
    #print str(filename)
    try:
        myfile = open(str(filename).decode())
        line = myfile.readline()
        while True:
            if line:
                ret = decode(getjsonstr(line))
                for info in ret["data"]["list"]:
                    i += 1
                    if info["fei_entname"].endswith("公司"):
                        company_name_gongsi_count += 1
                        fout2.write("%s\n"%info["fei_entname"])
                    else:
                        fout1.write("%s\n"%info["fei_entname"])
                    if i % 100000 == 0:
                        print(info["fei_entname"], company_name_gongsi_count)
                ret = None
                line = myfile.readline()
            else:
                break
        myfile.close()
    except Exception as e:
        print "error file:", str(filename), traceinfo(e)
        if myfile:
            myfile.close()
            continue
fout1.close()
fout2.close()