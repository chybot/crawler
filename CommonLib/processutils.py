# -*- coding: utf-8 -*-
"""
进程管理工具模块
"""
__author__ = 'xww'
import sys
reload(sys)
sys.setdefaultencoding("UTF-8")
sys.path.append("../")

import os
import psutil

def pid():
    """
     获取当前进程号
    :return: (int) 进程号
    """
    return os.getpid()

def cpu_percent(pid):
    """
    获取进程cpu占用率
    :param pid: (int) 进程号
    :return: (float) cpu占用率
    """
    p=psutil.Process(pid)
    return p.cpu_percent()

def mem_percent(pid):
    """
    获取内存占用率
    :param pid:  (int) 进程号
    :return:float) 内存占用率
    """
    p=psutil.Process(pid)
    return p.memory_percent()

def get_bin_path(pid):
    """
    获取进程bin绝对路径
    :param pid:  (int) 进程号
    :return: (str) 进程bin绝对路径
    """
    p=psutil.Process(pid)
    return p.exe()

def get_cwd_path(pid):
    """
    获取进程工作目录绝对路径
    :param pid:  (int) 进程号
    :return: (str) 进程工作目录绝对路径
    """
    p=psutil.Process(pid)
    return p.cwd()

def  create_time(pid):
    """
    获取进程创建时间戳
    :param pid: (int) 进程号
    :return: (long) 进程创建时间戳
    """
    p=psutil.Process(pid)
    return p.create_time()

def  kill(pid):
    """
    杀死进程
    :param pid: (int) 进程号
    """
    p=psutil.Process(pid)
    p.kill()


def main():
    kill(9288)
    # print create_time(os.getpid())

if __name__=="__main__":
    main()
