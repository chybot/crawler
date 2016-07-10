# -*- coding: utf-8 -*-
__author__ = 'xww'

import sys
reload(sys)
sys.setdefaultencoding("UTF-8")
sys.path.append("../../")
import xlrd
from common.exceputil import  traceinfo
class sheet:
    def __init__(self,excel_sheet):
        self.excel_sheet=excel_sheet

    def cell_value(self,row,col):
        """ get value by row and col
        :param row:  row number
        :param col:  col number
        :return:
        """
        return self.excel_sheet.cell_value(row,col)

    def row_len(self,row_num):
        """ get col count
        :param row_num: row number
        :return:
        """
        return self.excel_sheet.row_len(row_num)

    def nrows(self):
        """ get row count
        :return: (int) rows
        """
        return self.excel_sheet.nrows

def getsheet(filename,sheetname):
    # 打开 Excel 文件
    try:
        device_workbook = xlrd.open_workbook(filename)
        excel_sheet=device_workbook.sheet_by_name(sheetname)
        return sheet(excel_sheet)
    except Exception as e:
        print u'文件名%s,错误信息:%s',(filename,traceinfo(e))


def main():
    sheet=getsheet("c:/code.xlsx",u"Wind资讯")
    print sheet.row_len(0)
    print sheet.cell_value(0,1)

if __name__=="__main__":
    main()