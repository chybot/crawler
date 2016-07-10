# -*- coding: utf-8 -*-
"""
解析网页分页信息的工具模块
"""
__author__ = 'xww'

from lxml import etree
import urlparse
import math
import re
import math

def getpagecount(count,pagesize):
   return int(math.ceil(1.0*count/pagesize))

def geturl(html_src,path,url):
    """
    返回每一页的url地址集合。
    1.通过html源文和xpath解析出所有超链接标签的href属性
    2.通过所有超链接标签的href属性和网页url计算出此分页的绝对url地址，返回整个集合
    :param html_src:  (unicode) html源文
    :param path:  (unicode)  包含1个或多个<b>超链接</b>的xpath路径 -> .//div/a
    :param url: (str) html源文的url地址
    :return:  (set) 所有a标签的地址
    """
    tree = etree.HTML(html_src)
    pageinfo=tree.xpath(path)
    urlset=set()
    for curr in pageinfo:
         urlset.add(urlparse.urljoin(url,curr.get("href")))
    return urlset

def getpagenum(html_src,path):
    """
    获取分页超链接的最大页码
    1.通过html源文和超链接xpath获取所有超链接的text内容
    2.遍历text内容，返回内容是数字的最大值
    :param html_src: (unicode)  html 源文
    :param path:   (str) 分页超链接标签的xpath路径 -> .//div/a
    :return: （int) 最大的页码
    """
    tree = etree.HTML(html_src)
    num=0
    pageinfo=tree.xpath(path)
    for curr in pageinfo:
         pagestr=curr.text
         match=re.search(r'\d+',pagestr)
         if match:
            numpage=match.group()
            if len(numpage)>0:
                p=int(numpage)
                if p>num:
                    num=p
    return num


def get_page_list(sum,pagesize,start=1):
    """
    根据给定的总条数、每页条数和页码起始(默认第1页）计算页码序列并返回
    :param sum:  (int) 总条数  ->35
    :param pagesize: (int)  每页条数 ->10
    :param start:(int)  起始页 -> 1
    :return: (list)  页码序列 -> [1,2,3,4]
    """
    page= int(math.ceil(1.0*sum/pagesize))
    start1=0
    return range(start1+start,page+start)

def get_offset_list(sum,pagesize,start=0):
    """
    根据给定的数据总条数、每页条数和数据起始位置(默认为0）计算出起始序列并返回
    :param sum:  (int) 数据总条数  ->101
    :param pagesize: (int)  每页条数 ->20
    :param start:(int)  起始位置 -> 0
    :return: (list)  页码序列 -> [0,20,40,60,100]
    """
    page= int(math.ceil(1.0*sum/pagesize))
    start1=0
    return range(start+start1*pagesize,page*pagesize,pagesize)


if __name__ =='__main__':
   url="http://koubei.jumei.com/user/Ub1bdcb6e126a3294/fans?fans#type=fans#page=1"
   path=".//*[@id='pageSplit']/a"
   path=".//*[@id='pagerBar']/div/a"
   url="http://hi.baidu.com/cangzhige"
   import webutil
   html_src = webutil.browse(url,spynner_browser_timeout=60.0)
   for x in geturl(html_src,path,url):
        print x
   print(getpagenum(html_src,path))
   for i in get_page_list(34,5000):
       print i
   for i in get_offset_list(101,20):
       print i