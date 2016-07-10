# -*- coding: utf-8 -*-
"""
系统信息公共类
"""
__author__ = 'xww'

import sys
reload(sys)
sys.setdefaultencoding("UTF-8")
sys.path.append("../")

import socket
import re

import psutil

from common import webutil


def hostname():
    """
    获取机器名
    :return: (str) 机器名
    """
    return socket.gethostname()

def intr_ip():
    """
    获取内网IP地址
    :return: (str) 内网ip地址
    """
    hostname=socket.gethostname()
    # ip_adds= socket.gethostbyname_ex(hostname)
    # for ip in ip_adds:
    #     if isinstance(ip,basestring):
    #         if ip!=hostname:
    #             return ip
    #     elif isinstance(ip,list):
    #         if len(ip)<1:
    #             continue
    #         for sub_ip in ip:
    #             if ip!=hostname:
    #                 return sub_ip
    return socket.gethostbyname(hostname)

def inter_ip():
    """
    获取外网IP地址
    1.访问 http://www.whereismyip.com 网站
    2。解析页面内容，抽取ip地址
    :return: （str)外网IP地址
    """

    html_src=webutil.request("http://www.whereismyip.com",timeout=30,retry=2,encoding="iso8859-1")
    return  re.search(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}',html_src).group(0)



def cpu_count():
    """
    获取cpu核数
    :return: (int) cpu核数
    """
    return psutil.cpu_count()

def cpu_used_rate():
    """
    获取cpu使用率
    :return:(float) cpu使用率
    """
    return psutil.cpu_percent()


def memory_total():
    """
    获取内存总量
    :return:(long) 内存总量字节数
    """
    mem_info= psutil.virtual_memory()
    return mem_info.total

def memory_used_rage():
    """
    获取内存使用率
    :return: (float)内存使用率
    """
    mem_info= psutil.virtual_memory()
    return  mem_info.percent

def memory_swap_total():
    """
    获取虚拟内存大小
    :return: (long) 虚拟内存总量字节数
    """
    swap= psutil.swap_memory()
    return swap.total


def  disk_info():
    """
    获取磁盘信息
    :return:(long,long,long,float) 硬盘总量字节数,已使用字节数,未使用字节数,使用百分比(保留两位小数) ->80023224320,34031636480,42.52
    """
    total=0
    used=0
    free=0
    pattern_list=psutil.disk_partitions()
    for patt in pattern_list:
        mountpoint=patt.mountpoint
        fstype=patt.fstype
        if fstype!=None and len(fstype)>0:
            try:
                pattern_info=psutil.disk_usage(mountpoint)
                total+=pattern_info.total
                used+=pattern_info.used
                free+=pattern_info.free
            except Exception as e:
                print e
    percent=int(1.0*used/total*10000)/100.0
    return total,used,free,percent



def main():
    print "hostname:%s"%hostname()
    print "intranet ip address:%s"%intr_ip()
    print "internet ip address:%s"%inter_ip()
    print "cpu count:%s"%cpu_count()
    print "cpu used rate:%s"%cpu_used_rate()
    print "memory total:%s"%memory_total()
    print "memory used rate :%s"%memory_used_rage()
    total,used,free,used_percent,=disk_info()
    print "total disk:%s"%total
    print "used disk:%s"%used
    print "free disk:%s"%free
    print "used percent:%s%%"%used_percent






if __name__=="__main__":
    main()