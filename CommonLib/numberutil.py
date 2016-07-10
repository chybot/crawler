# -*- coding: utf-8 -*-
"""
数字识别工具模块
"""

__author__ = 'xww'
import re
#汉字大写0-10
chinese_number=u"零壹贰叁肆伍陆柒捌玖拾"
#汉字0-10
chinese_simple_number=u"零一二三四五六七八九十"
#加减乘除汉字
opers=u"加减乘除"
#加减乘除符号
opers_num=u"+-*/"


def match_simple(desc):
    """
    把汉字描述的加减乘除运算解析出来运算并返回结果
    :param desc: (str)  汉字描述的加减乘除运算 -> 九加十等于几
    :return: (int) 运算后的答案 -> 19
    """
    try:
        if desc.endswith(u"等于几"):
            oper=desc[1]
            if oper in opers:
                oper_num=opers_num[opers.find(oper)]
                left=desc[0]
                right=desc[2]
                if left in chinese_simple_number and right in chinese_simple_number:
                    left_num=chinese_simple_number.find(left)
                    right_num=chinese_simple_number.find(right)
                    return eval("%d%s%d" % (left_num,oper_num,right_num))


    except Exception as e:
        return False


def match(desc):
    """
     把大写汉字描述的加减乘除运算解析出来运算并返回结果
    :param desc:  (str)  大写的汉字描述的加减乘除运算 -> 陆加拾等于
    :return: （int) 运算结果 ->16
    """
    try:
        if desc.endswith(u"等于") :
            oper=desc[1]
            if oper in opers:
                oper_num=opers_num[opers.find(oper)]
                left=desc[0]
                right=desc[2]
                if left in chinese_number and right in chinese_number:
                    left_num=chinese_number.find(left)
                    right_num=chinese_number.find(right)
                    return eval("%d%s%d" % (left_num,oper_num,right_num))


    except Exception as e:
        return False

def  getInt(str):
    """
    把含有整形数字的字符串中的整形数字解析出来并返回
    :param str:  含有数字的字符串 -> a=40
    :return: (int) 字符串中的整形数字 -> 40
    """
    try:
        match=re.search(r'\d+',str)
        if match:
            intstr=match.group()
            if len(intstr)>0:
                return int(intstr)
        else:
            return 0
    except Exception as e:
        return 0

def  getfloat(str):
    """
    把含有浮点数的字符串中的浮点数解析出来并返回
    :param str:  含有浮点数的字符串 -> a=40
    :return: (int) 字符串中的浮点数 -> 40
    """
    try:
        match=re.search(r'\d+([.]\d+)?',str)
        if match:
            intstr=match.group()
            if len(intstr)>0:
                return float(intstr)
        return 0.0
    except Exception as e:
        return 0.0


if __name__=='__main__':
    # print(getInt('a=40'))
    # print (getfloat('12.3万'))
    print match(u"陆加拾等于")
    # print match(u"零加零等于")
    # print match(u"零减零等于")
    # print match(u"零除零等于")
    print match_simple(u"九加十等于几")