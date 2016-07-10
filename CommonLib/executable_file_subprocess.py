# -*- coding: utf-8 -*-
"""
批量启动可执行文件
"""
import sys
reload(sys)
sys.setdefaultencoding("UTF-8")
import subprocess
import os
import re
import time
import datetime
sys.path.append("../")
from common import exceputil
from common import functions

#dir_path=sys.argv[1]
dir_path="D:\\fumenglin\\python_program"
python_path="D:\WinPython-64bit-2.7.6.4\python-2.7.6.amd64\python.exe"

#存储pid的文件夹，当前进程号的pid保存文件名为dir_path的“\”后面部分，如"E:\svn"为svn
if not os.path.exists(u"./pid"):
    os.makedirs(u"./pid")
#存储log文件的文件夹
if not os.path.exists(u"./log"):
    os.makedirs(u"./log")


dir_last_file=dir_path[dir_path.rfind("\\"):]
fil_tuples=[]
do_time=datetime.datetime.now().strftime("%Y-%m-%d-%H")
logging=functions.get_logger("./log/subproces_%s.log"%do_time)

#黑名单，不需要执行的程序文件，如__init__.py，或者data文件
not_tuples=[u"__init__.py"]

#获取执行可执行文件保存pid的文件夹命名，以"\"或"/"最后一位以后的字符串命名
def  path_last_f(dir_path):
    if dir_path.rfind("\\"):
        return dir_path[dir_path.rfind("\\"):]
    elif dir_path.rfind("/"):
        return dir_path[dir_path.rfind("/"):]
    else:
        print u"不能获取保存pid的文件名，默认为现在的YYYY-MM-DD-HH格式的文件:%s"%do_time
        return do_time
#执行可执行文件，并把pid写在
def exce_file_subprocess(exce_file):
    try:
        if exce_file.endswith("py"):
            #启动的py文件
            child_sub=subprocess.Popen("%s %s"%(python_path,exce_file),shell=True)#,stderr=subprocess.STDOUT)
        elif exce_file.endswith("bat"):
            #启动windows的批处理
            child_sub=subprocess.Popen(exce_file,shell=True)
        else:
            logging.info(u"启动的文件既不是py,也不是py,启动文件错误：%s"%exce_file)
            return
        c=str(child_sub.pid)
        write_file(u"./pid/%s_pid.txt"%dir_last_file,c+"|"+exce_file,"a+")
        child_sub.wait()
        time.sleep(1)
    except Exception as e:
        exceputil.traceinfo(e)
        print u"执行%s时候出错"%exce_file
        #杀死该进程
        child_sub.kill()
        write_file(u"./pid/%s_error.txt"%dir_last_file,c+"|"+exce_file,"a+")
        time.sleep(3)
#以追加方式写入内容
def write_file(open_file,write_str,pattern):
    while True:
        try:
            f=open(open_file,pattern)
            f.write(str(write_str)+"\n")
            f.close()
            break
        except Exception as e:
            exceputil.traceinfo(e)
            time.sleep(1)

#获取当前文件下面所有的以.py或者bat结尾的py文件
#style为bat(批处理)，或者py(py文件)
def get_exec_files(style,dir_path):
    global fil_tuples
    for i in os.listdir(dir_path):
        file=os.path.join(dir_path,i)
        if os.path.isfile(file):
            if str(file).endswith(style) and not str(file).endswith("pyc"):
                if i not in not_tuples:
                    fil_tuples.append(file)
        else:
            try:
                get_exec_files(style,file)
            except Exception as e:
                exceputil.traceinfo(e)
    return fil_tuples


def run():
    for ss in get_exec_files(style,dir_path):
        print ss
        exce_file_subprocess(ss)
if __name__=="__main__":
    style="bat"
    run()