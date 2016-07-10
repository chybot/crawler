# -*- coding: utf-8 -*-
__author__ = 'xww'

import re
import time
import datetime

def turn(do_time):
    """
    根据时间字符串和当前时间转换为时间戳
    :param do_time:  (unicode)  时间字符串 -> 3小时前
    :return:   (float)时间戳
    """
    number1 = int(re.search(r'\d+', do_time).group())
    second = 0
    if do_time.find(u'年前') != -1:
        second = number1 * 60 * 60 * 24 * 360
    elif do_time.find(u'月前')!= -1:
        second = number1 * 60 * 60 * 24 * 30
    elif do_time.find(u'星期前')!= -1:
        second = number1 * 60 * 60 * 24 * 7
    elif do_time.find(u'天前')!= -1 or do_time.find(u'日前')!= -1:
        second = number1 * 60 * 60 * 24
    elif do_time.find(u'小时前')!= -1 or do_time.find(u'时前')!= -1:
        second = number1 * 60 * 60
    elif do_time.find(u'分钟前')!= -1 or do_time.find(u'分前')!= -1:
        second = number1 * 60
    else:
        raise Exception(u"无效的时间%s" % do_time)
    timeArray = time.localtime(time.time() - second)
    do_time1 = time.strftime(u"%Y-%m-%d", timeArray)
    return do_time1

date_pattern=re.compile(u"([0-9]{4})[^0-9]+?([0-9]{1,2})[^0-9]+?([0-9]{1,2})")

def parse(date_str,format="%Y-%m-%d"):
    """
    解析日期字符串中的日期信息，返回指定日期格式的日期
    :param date_str: (unicode) 含有日期的字符串
    :param format:  (str) 日期格式
    :return: (str) format格式的日期字符串
    """
    try:
        match=date_pattern.search(date_str)
        if match:
            date_curr=datetime.date(int(match.group(1)),int(match.group(2)),int(match.group(3)))
            return time.strftime(format,date_curr.timetuple())
    except Exception as e:
        pass
    return date_str

def middle(start,end):
    middle=(time.mktime(start)+time.mktime(end))/2
    return time.localtime(middle)

def is_leap(year):
   return  year % 100 == 0 and year % 400 == 0 or  year % 100 != 0 and year % 4 == 0

def getdays(year,month):
    if month in (1,3,5,7,8,10,12):
        return 31
    elif month in (4,6,9,11):
        return 30
    elif is_leap(year):
        return 29
    else:
        return 28

if __name__ == '__main__':
    try:
        print(turn(u'3小时前'))
        print(turn(u'1分钟前'))
        print(turn(u'46天前'))
    except Exception:
        pass
    print  parse(u"2012年12月23日")
