# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding("UTF-8")
import time
import cookielib
import json
import datetime
import multiprocessing
import os
import xlrd
import re

sys.path.append("../")
from common import webutil
from common import proxyutils
from common import functions
from common import mongoutil
from common import exceputil
if not os.path.exists("./txt"):
    os.makedirs("./txt")
#遍历文件
logging=functions.get_logger("log_excel.log")
file_dir=u"E:\高新技术企业资质"
for root,dirs,files in os.walk(file_dir):
    for f in files:
        logging.info(u"%s开始导入"%f[:2])
        #打开文件
        f1=open(u"./txt/%s.txt"%f[:2],"w+")
        #文件路径
        xlsfile=root+"\\"+f
        #打开该excel
        book = xlrd.open_workbook(xlsfile)
        #获取每个excel里的sheet名
        sheet_names=book.sheet_names()
        #打开单个的sheet
        for sheet_ in sheet_names:
            try:
                if re.search(u"更名",sheet_):
                    m=2
                else:m=1
                sheet=book.sheet_by_name(sheet_)
                if len(sheet.row_values(0))>2 and len(sheet.col_values(m))>2:
                    col_data=sheet.col_values(m)
                else:continue
                if re.search(u"(企业)?(更名后名称)?",col_data[0]):
                    begin_num=1
                else:begin_num=0
                for col in range(begin_num,len(col_data)):
                    f1.write(col_data[col].strip().replace("•","").encode("GBK")+"\n")
            except Exception as e:
                logging.error(exceputil.traceinfo(e))
                continue
                time.sleep(2)
        f1.close()




# # encoding : utf-8       #设置编码方式
#
# import xlrd                    #导入xlrd模块
#
# #打开指定文件路径的excel文件
#
# xlsfile = r'D:\AutoPlan\apisnew.xls'
# book = xlrd.open_workbook(xlsfile)     #获得excel的book对象
#
# #获取sheet对象，方法有2种：
# sheet_name=book.sheet_names()[0]          #获得指定索引的sheet名字
# print sheet_name
# sheet1=book.sheet_by_name(sheet_name)  #通过sheet名字来获取，当然如果你知道sheet名字了可以直接指定
# sheet0=book.sheet_by_index(0)     #通过sheet索引获得sheet对象
#
# #获取行数和列数：
#
# nrows = sheet.nrows    #行总数
# ncols = sheet.ncols   #列总数
#
# #获得指定行、列的值，返回对象为一个值列表
#
# row_data = sheet.row_values(0)   #获得第1行的数据列表
# col_data = sheet.col_values(0)  #获得第一列的数据列表，然后就可以迭代里面的数据了
#
# #通过cell的位置坐标获得指定cell的值
# cell_value1 = sheet.cell_value(0,1)  ##只有cell的值内容，如：http://xxx.xxx.xxx.xxx:8850/2/photos/square/
# print cell_value1
# cell_value2 = sheet.cell(0,1) ##除了cell值内容外还有附加属性，如：text:u'http://xxx.xxx.xxx.xxx:8850/2/photos/square/'
# print cell_value2