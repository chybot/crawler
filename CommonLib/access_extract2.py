# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding("UTF-8")

import pyodbc
from numpy import *

dbname_tablename_ofilename_map = [
    u"F:\\数据帝\\经济普查\\file1orig.mdb", u"基本情况", u"2004jingjipucha.csv"
]

import pyodbc
import functions
company_name_pair_map = {}

for i in range(len(dbname_tablename_ofilename_map) / 3):
    j = 3*i
    connection = pyodbc.connect('DRIVER={Microsoft Access Driver (*.mdb)};PWD=@bzdmmsds_2011!;DBQ='+dbname_tablename_ofilename_map[j])
    cur = connection.cursor()
    cur.execute(u"select * from %s" % dbname_tablename_ofilename_map[j+1])
    counter = 0
    print dbname_tablename_ofilename_map[j]

    for row in cur:
        counter += 1
        #print 'Cname:'+row.Cname
        #fout.write(row[1]+"\n")
        #fout.write(row.Cname+"\n")
        if row.company_name not in company_name_pair_map:
            company_name_pair_map[ functions.remove_all_space_char(row.company_name.strip()) ] = "%s,%s"%(functions.remove_all_space_char(row.company_name.strip()), row.youbian)
        if counter % 10000 == 0:
            print counter

    print counter
    fout = open(dbname_tablename_ofilename_map[j+2], "w")
    for key in company_name_pair_map:
        fout.write("%s\n"%(company_name_pair_map[key]))
    fout.close()


sys.exit()

dbname_tablename_ofilename_map = [
    u"F:\\数据帝\\2004census\\2004jjpc.mdb", u"601gs", u"2013_industry_company_name_prov_pair_map.csv",
    u"F:\\数据帝\\2004census\\2004jjpc.mdb", u"601gx", u"2013_industry_company_name_prov_pair_map.csv"
]

import pyodbc
import functions
company_name_pair_map = {}

for i in range(len(dbname_tablename_ofilename_map) / 3):
    j = 3*i
    connection = pyodbc.connect('DRIVER={Microsoft Access Driver (*.mdb)};PWD=@bzdmmsds_2011!;DBQ='+dbname_tablename_ofilename_map[j])
    cur = connection.cursor()
    cur.execute(u"select * from %s" % dbname_tablename_ofilename_map[j+1])
    counter = 0
    print dbname_tablename_ofilename_map[j]

    for row in cur:
        counter += 1
        #print 'Cname:'+row.Cname
        #fout.write(row[1]+"\n")
        #fout.write(row.Cname+"\n")
        if row.B02 not in company_name_pair_map:
            company_name_pair_map[ functions.remove_all_space_char(row.B02.strip()) ] = "%s,%s"%(functions.remove_all_space_char(row.B02.strip()), row.B0561)
        if counter % 10000 == 0:
            print counter

print counter
fout = open("2004jjpc_2004census.csv", "w")
for key in company_name_pair_map:
    fout.write("%s\n"%(company_name_pair_map[key]))
fout.close()


sys.exit()

dbname_tablename_ofilename_map = [
    u"F:\\数据帝\\【批量下载】2013工业等\\2013_industry.mdb", u"2013_industry", u"2013_industry_company_name_prov_pair_map.csv"
]

import pyodbc
import functions
company_name_pair_map = {}

for i in range(len(dbname_tablename_ofilename_map) / 3):
    j = 3*i
    connection = pyodbc.connect('DRIVER={Microsoft Access Driver (*.mdb)};PWD=@bzdmmsds_2011!;DBQ='+dbname_tablename_ofilename_map[j])
    cur = connection.cursor()
    cur.execute(u"select * from %s" % dbname_tablename_ofilename_map[j+1])
    counter = 0
    print dbname_tablename_ofilename_map[j]

    for row in cur:
        counter += 1
        #print 'Cname:'+row.Cname
        #fout.write(row[1]+"\n")
        #fout.write(row.Cname+"\n")
        if row.company_name not in company_name_pair_map:
            company_name_pair_map[ row.company_name ] = "%s,%s"%(functions.remove_all_space_char(row.company_name.strip()), row.sheng)
        if counter % 10000 == 0:
            print counter

    print counter
    fout = open(dbname_tablename_ofilename_map[j+2], "w")
    for key in company_name_pair_map:
        fout.write("%s\n"%(company_name_pair_map[key]))
    fout.close()



dbname_tablename_ofilename_map = [
    u"F:\\数据帝\\【批量下载】2013工业等\\2012_industry.mdb", u"2012_industry", u"2012_industry_company_name_youbian_pair_map.csv"
]

import pyodbc
import functions
company_name_pair_map = {}

for i in range(len(dbname_tablename_ofilename_map) / 3):
    j = 3*i
    connection = pyodbc.connect('DRIVER={Microsoft Access Driver (*.mdb)};PWD=@bzdmmsds_2011!;DBQ='+dbname_tablename_ofilename_map[j])
    cur = connection.cursor()
    cur.execute(u"select * from %s" % dbname_tablename_ofilename_map[j+1])
    counter = 0
    print dbname_tablename_ofilename_map[j]

    for row in cur:
        counter += 1
        #print 'Cname:'+row.Cname
        #fout.write(row[1]+"\n")
        #fout.write(row.Cname+"\n")
        if row.company_name not in company_name_pair_map:
            company_name_pair_map[ row.company_name ] = "%s,%s"%(functions.remove_all_space_char(row.company_name.strip()), row.youbian)
        if counter % 10000 == 0:
            print counter

    print counter
    fout = open(dbname_tablename_ofilename_map[j+2], "w")
    for key in company_name_pair_map:
        fout.write("%s\n"%(company_name_pair_map[key]))
    fout.close()