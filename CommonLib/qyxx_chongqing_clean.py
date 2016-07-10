# -*- coding: utf-8 -*-
import sys

reload(sys)
sys.setdefaultencoding("UTF-8")
import re
import json
sys.path.append("../")
from common import exceputil
from common import mongoutil

def chongqing_company_get():
    f=open("E:\\bad_key.txt")
    txt=f.read()
    p=re.compile(r"1\n重庆\n(.+?)\n")
    company_=p.findall(txt)
    for ss in company_:
        print ss
        db_table=mongoutil.getmondbbyhost("bigdata_higgs", "wowotuan")#.table
        _table=db_table.find_one({"company_name":ss,"version":1})
        print _table
        #db_table.update({"_id":_id},{"$set":dict_},True)
p = re.compile(r"\<span\>(.*)")
def clean():
    f=open(u"E:\cq.txt","r")
    liness=f.readlines()
    for line in liness:
        if line:
            company_name=line.strip()
           # print company_name
            db_table=mongoutil.getmondbbyhost("bigdata_higgs", "qyxx").table
            company_=db_table.find_one({"version":1, "company_name" : company_name})
            if not company_:
                print "no_company",company_name
            if company_:
                print "company",company_name
                #company_=json.loads(company_)
                dict_={}
                for com in company_:
                    _id=company_["_id"]
                    pp=p.findall(str(com))
                    _idd=company_name+"|_|"+company_["do_time"]
                    dict_["_id"]=_idd
                    if pp:
                        #print  company_name
                        value=company_[com]
                        keyss=u"%s"%pp[len(pp)-1]
                        dict_[keyss]=value
                    else:
                        dict_[com]=company_[com]
                        #print com
                #print  dict_
                db_table.remove({"_id":_id})
                db_table.insert(dict_)
                #db_table.update({"_id":_id},{"$set":dict_},upsert=True)
                #raw_input()


if __name__=="__main__":
    clean()