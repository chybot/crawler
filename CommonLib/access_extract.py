# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding("UTF-8")

import pyodbc
from numpy import *

dbname_tablename_ofilename_map = [
    #u"F:\\数据帝\\08年经济普查全样本\\浙江省.mdb", u"浙江省", u"zhejiang.txt",
    #u"F:\\数据帝\\08年经济普查全样本\\安徽省.mdb", u"安徽省", u"anhui.txt",
    #u"F:\\数据帝\\08年经济普查全样本\\北京.mdb", u"北京", u"beijing.txt",
    #u"F:\\数据帝\\08年经济普查全样本\\福建省.mdb", u"福建", u"fujian.txt",
    #u"F:\\数据帝\\08年经济普查全样本\\甘肃省.mdb", u"甘肃", u"gansu.txt",
    #u"F:\\数据帝\\08年经济普查全样本\\广东省.mdb", u"广东", u"guangdong.txt",
    #u"F:\\数据帝\\08年经济普查全样本\\广西.mdb", u"广西", u"guangxi.txt",
    #u"F:\\数据帝\\08年经济普查全样本\\贵州省.mdb", u"贵州省", u"guizhou.txt",
    #u"F:\\数据帝\\08年经济普查全样本\\海南省.mdb", u"海南", u"hainan.txt",
    #u"F:\\数据帝\\08年经济普查全样本\\河北省.mdb", u"河北省", u"hebei.txt",
    #u"F:\\数据帝\\08年经济普查全样本\\河南省.mdb", u"河南省", u"henan.txt",
    u"F:\\数据帝\\08年经济普查全样本\\黑龙江省.mdb", u"黑龙江", u"heilongjiang.txt",
    u"F:\\数据帝\\08年经济普查全样本\\湖北省.mdb", u"湖北", u"hubei.txt",
    u"F:\\数据帝\\08年经济普查全样本\\湖南省.mdb", u"湖南省", u"hunan.txt",
    #u"F:\\数据帝\\08年经济普查全样本\\吉林省.mdb", u"吉林省", u"jining.txt",
    u"F:\\数据帝\\08年经济普查全样本\\江苏省.mdb", u"江苏", u"jiangsu.txt",
    u"F:\\数据帝\\08年经济普查全样本\\江西省.mdb", u"江西省", u"jiangxi.txt",
    #u"F:\\数据帝\\08年经济普查全样本\\辽宁省.mdb", u"辽宁省", u"liaoning.txt",
    u"F:\\数据帝\\08年经济普查全样本\\内蒙古.mdb", u"内蒙", u"neimenggu.txt",
    u"F:\\数据帝\\08年经济普查全样本\\宁夏.mdb", u"宁夏", u"ningxia.txt",
    u"F:\\数据帝\\08年经济普查全样本\\青海省.mdb", u"青海", u"qinghai.txt",
    u"F:\\数据帝\\08年经济普查全样本\\山东省.mdb", u"山东", u"shandong.txt",
    #u"F:\\数据帝\\08年经济普查全样本\\山西省.mdb", u"山西省", u"shanxitaiyuan.txt",
    #u"F:\\数据帝\\08年经济普查全样本\\陕西省.mdb", u"陕西省", u"shanxixian.txt",
    #u"F:\\数据帝\\08年经济普查全样本\\上海市.mdb", u"上海市", u"shanghai.txt",
    u"F:\\数据帝\\08年经济普查全样本\\四川.mdb", u"四川", u"sichuan.txt",
    u"F:\\数据帝\\08年经济普查全样本\\天津.mdb", u"天津", u"tianjin.txt",
    u"F:\\数据帝\\08年经济普查全样本\\西藏.mdb", u"西藏", u"xizang.txt",
    u"F:\\数据帝\\08年经济普查全样本\\新疆.mdb", u"新疆", u"xinjiang.txt",
    u"F:\\数据帝\\08年经济普查全样本\\云南省.mdb", u"云南省", u"yunnan.txt",
    #u"F:\\数据帝\\08年经济普查全样本\\浙江省.mdb", u"浙江省", u"zhejiang.txt",
    u"F:\\数据帝\\08年经济普查全样本\\重庆.mdb", u"重庆", u"chongqing.txt",
]

print len(dbname_tablename_ofilename_map)

import pyodbc

for i in range(len(dbname_tablename_ofilename_map) / 3):
    j = 3*i
    connection = pyodbc.connect('DRIVER={Microsoft Access Driver (*.mdb)};PWD=@bzdmmsds_2011!;DBQ='+dbname_tablename_ofilename_map[j])
    cur = connection.cursor()
    cur.execute(u"select * from %s" % dbname_tablename_ofilename_map[j+1])
    counter = 0
    print dbname_tablename_ofilename_map[j+2],
    fout = open(dbname_tablename_ofilename_map[j+2], "w");
    for row in cur:
        counter += 1
        #print 'Cname:'+row.Cname
        #fout.write(row[1]+"\n")
        fout.write(row.Cname+"\n")
    fout.close()
    print counter

