# -*- coding: utf-8 -*-
"""
正则工具模块
"""
__author__ = 'xww'
import re

def get_single_quote_list(str):
    """
    解析半角单引号包裹的字符串
    :param str: (str) 字符串  -> asdf'2342adef34'asdf
    :return: 单引号包裹的字符串 ->2342adef34
    """
    reObj1 = re.compile(r"['](.+?)[']")
    match=reObj1.findall(str)
    result=list()
    for m in match:
        result.append(m)
    return result


def get_quote_list(str):
    """
    解析半角双引号包裹的字符串
    :param str: (str) 字符串  -> asdf”2342adef34"asdf
    :return: 单引号包裹的字符串 ->2342adef34
    """
    reObj1 = re.compile(r'["](.+?)["]')
    match=reObj1.findall(str)
    result=list()
    for m in match:
        result.append(m)
    return result

def get_value(regex,content,group=0):
    pattern=re.compile(regex)
    match=pattern.search(content)
    if match:
        return match.group(group)
    else:
        return ""


def get_value_list(regex,content,group=0):
    result=list()
    pattern=re.compile(regex)
    if pattern!=None:
        for match in pattern.finditer(content):
            curr=match.group(group)
            result.append(curr)
    return result

def main():
    for i in get_quote_list('dwr.engine.remote.handleCallback("1","0","MjQyNTAwMDAwMTI3MTcwMzM=");'):
        print i


if __name__=="__main__":
    main()



