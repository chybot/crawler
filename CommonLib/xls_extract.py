# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding("UTF-8")

import glob
import os
import functions
def get_all_filename_from_dir(dir):
    filename_list = []
    for dirpath, dirnames, filenames in os.walk(dir):
        #print 'Directory', dirpath
        for filename in filenames:
            #print ' File', filename, os.path.join(dirpath,filename)
            filename_list.append(str(os.path.join(dirpath,filename)))
    return filename_list

from win32com.client import constants, Dispatch
xlsApp = Dispatch("Excel.Application")
# 通过赋值Visible为True或者False可以控制是否调出excle
xlsApp.Visible = False

def extract_companyname_2_file(filename, pfile):

    try:
        xlsBook = xlsApp.Workbooks.Open(unicode(filename))
        xlsSht = xlsBook.Worksheets(1)
        for i in range(10000000):
            if xlsSht.Cells(i+1, 1).Value == None:
                #print filename, i
                break;
            #print xlsSht.Cells(i+1, 1).Value, i
            line = functions.remove_all_space_char(xlsSht.Cells(i+1, 1).Value)
            if i % 1000 == 0:
                print line, i
            if line != "公司名称" and len(line) > 4 and len(line) < 128:
                pfile.write(line+"\n")

        xlsApp.Quit()
    except Exception as e:
        print "error:", filename, e

def extract_all_dirfiles_2_file(dir, outfilename):
    print len(get_all_filename_from_dir(dir))
    pfile = open(outfilename, "w")
    #pfile.close()
    #pfile = open(outfilename, "a")
    for filename in get_all_filename_from_dir(dir):
        print filename, outfilename
        extract_companyname_2_file(filename, pfile)
        pfile.flush()
    pfile.close()

allfile_2_ofilename_map = [
    u'F:\\数据\\全国精准\\浙江地区56W', u"F:\\数据\\全国精准\\zhejiang.txt",
    u'F:\\数据\\全国精准\\[辽宁7.3060W', u"F:\\数据\\全国精准\\liaoning.txt",
    u'F:\\数据\\全国精准\\安徽地区7.9388W', u"F:\\数据\\全国精准\\anhui.txt",
    u'F:\\数据\\全国精准\\北京27.9000W', u"F:\\数据\\全国精准\\beijing.txt",
    u'F:\\数据\\全国精准\\大连地区1.6708W', u"F:\\数据\\全国精准\\dalian.txt",
    u'F:\\数据\\全国精准\\福建地区18.2428W', u"F:\\数据\\全国精准\\fujian.txt",
    u'F:\\数据\\全国精准\\甘肃地区17500', u"F:\\数据\\全国精准\\gansu.txt",
    u'F:\\数据\\全国精准\\广东地区39.9W', u"F:\\数据\\全国精准\\guangdong.txt",
    u'F:\\数据\\全国精准\\广西地区54601', u"F:\\数据\\全国精准\\guangxi.txt",
    u'F:\\数据\\全国精准\\贵州地区22391', u"F:\\数据\\全国精准\\guizhou.txt",
    u'F:\\数据\\全国精准\\海南地区1.1175W', u"F:\\数据\\全国精准\\hainan.txt",
    u'F:\\数据\\全国精准\\河北地区9.4246W', u"F:\\数据\\全国精准\\hebei.txt",
    u'F:\\数据\\全国精准\\河南地区11.7500W', u"F:\\数据\\全国精准\\henan.txt",
    u'F:\\数据\\全国精准\\黑龙江地区3.7990W', u"F:\\数据\\全国精准\\heilongjiang.txt",
    u'F:\\数据\\全国精准\\湖北地区8.1W', u"F:\\数据\\全国精准\\hubei.txt",
    u'F:\\数据\\全国精准\\湖南地区10.2W', u"F:\\数据\\全国精准\\hunan.txt",
    u'F:\\数据\\全国精准\\吉林地区2.8788W', u"F:\\数据\\全国精准\\jilin.txt",
    u'F:\\数据\\全国精准\\江苏地区44W', u"F:\\数据\\全国精准\\jiangsu.txt",
    u'F:\\数据\\全国精准\\江西地区6.6489W', u"F:\\数据\\全国精准\\jiangxi.txt",
    u'F:\\数据\\全国精准\\内蒙古地区3.0129', u"F:\\数据\\全国精准\\neimenggu.txt",
    u'F:\\数据\\全国精准\\宁夏地区7200', u"F:\\数据\\全国精准\\ningxia.txt",
    u'F:\\数据\\全国精准\\青海', u"F:\\数据\\全国精准\\qinghai.txt",
    u'F:\\数据\\全国精准\\山东地区30.0646W', u"F:\\数据\\全国精准\\shandong.txt",
    u'F:\\数据\\全国精准\\山西地区4.2430W', u"F:\\数据\\全国精准\\shanxitaiyuan.txt",
    u'F:\\数据\\全国精准\\陕西地区3.1771W', u"F:\\数据\\全国精准\\shanxixian.txt",
    u'F:\\数据\\全国精准\\上海地区18，1W', u"F:\\数据\\全国精准\\shanghai.txt",
    u'F:\\数据\\全国精准\\四川地区8.7777', u"F:\\数据\\全国精准\\sichuan.txt",
    u'F:\\数据\\全国精准\\天津地区3.1680W', u"F:\\数据\\全国精准\\tianjin.txt",
    u'F:\\数据\\全国精准\\西藏', u"F:\\数据\\全国精准\\xizang.txt",
    u'F:\\数据\\全国精准\\新疆地区', u"F:\\数据\\全国精准\\xinjiang.txt",
    u'F:\\数据\\全国精准\\云南地区2.799W', u"F:\\数据\\全国精准\\yunnan.txt",

    u'F:\\数据\\全国精准\\重庆市4.2250条', u"F:\\数据\\全国精准\\chongqing.txt",
]

print len(allfile_2_ofilename_map)

for i in range(len(allfile_2_ofilename_map) / 2):
    j = 2*i
    print allfile_2_ofilename_map[j], allfile_2_ofilename_map[j+1]
    extract_all_dirfiles_2_file(allfile_2_ofilename_map[j], allfile_2_ofilename_map[j+1]);
