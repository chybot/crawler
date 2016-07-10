# -*- coding: utf-8 -*-
__author__ = 'xww'
import os
import shutil
import chardet

def clear(file_name):
    """
    清除文件内容
    :param file_name:  文件名
    :return:
    """
    f=None
    try:
        f=open(file_name,"wb")
        f.write("")
        return True
    except Exception as e1:
        return False
    finally:
        if f !=None:
            try:
                f.close()
            except Exception as e :
                pass


def write(filename,content,mode="wb"):
    """
    写入文件
    :param filename:  文件名
    :param content:  文件内容
    :param mode: 打开文件模式
    :return: 写入是否成功
    """
    f=None
    try:
        f = open(filename, mode)
        f.write(content)
        return True
    except Exception as e:
        return False
    finally:
        if f!=None:
            try:
                f.close()
            except Exception as  e2:
                pass

def isdir(path):
    """
    判断path是否是路径
    :param path:  路径名
    :return: 是否是路径
    """
    return os.path.isdir(path)

def isfile(path):
    """
    判断path是否是文件
    :param path: 路径名
    :return: 是否是文件
    """
    return os.path.isfile(path)

def exists(path):
    """
    判断文件是否存在
    :param path:  (str) 文件路径 -> D:/123
    :return: (bool) 文件是否存在
    """
    return os.path.exists(path)

def mkdir(path):
    """
    建立单级目录，返回是否成功
    1、如果存在且是目录则返回True
    2、如果存在，但是文件不是目录则返回False
    3、如果不存在则建立目录，返回成功与否
    :param path:  (str) 目录路径 -> D:/123
    :return: 建立单级目录是否成功
    """
    if isdir(path):
        return True
    if isfile(path):
        return False
    try:
        os.mkdir(path)
        return True
    except Exception as e:
        return False

def mkdirs(path):
    """
    建立多级目录，返回是否成功
    1、如果存在且是目录则返回True
    2、如果存在，但是文件不是目录则返回False
    3、如果不存在则建立多级目录，返回成功与否
    :param path:  (str) 目录路径 -> D:/123
    :return: 建立目录是否成功
    """
    if isdir(path):
        return True
    if isfile(path):
        return False
    try:
        os.makedirs(path)
        return True
    except Exception as e:
        return False

def copyfile(src,aim):
    """
    复制单个文件，返回是否成功
    :param src: (unicode) 源文件名
    :param aim: (unicode) 目标文件名
    :return: (bool) ->True：复制成功,False:复制失败
    """
    try:
        shutil.copyfile(src,aim)
        return True
    except Exception as e:
        return False

def copytree(src,aim):
    """
    复制目录树，返回是否成功
    :param src: (unicode) 源文件名
    :param aim: (unicode) 目标文件名
    :return: (bool) ->True：复制成功,False:复制失败
    """
    try:
        shutil.copytree(src,aim)
        return True
    except Exception as e:
        return False

def rename(old,new):
    """
    重命名
    :param old: （unicode) 源文件名
    :param new:  (unicode) 目标文件名
    :return: (bool) 是否成功 -> True:成功,False:失败
    """
    try:
        os.rename(old,new)
        return True
    except Exception as e:
        return False


def remove(file):
    """
    删除文件
    :param file:  (str) 文件名
    :return: （bool) 是否成功 -> True：成功 False:失败
    """
    if exists(file):
        try:
            os.remove(file)
            return True
        except Exception as e:
            return False
    else:
        return True

def rmdir(dir):
    """
    删除目录或文件
    :param dir: (str)  目录名
    :return: (bool) 是否成功 -> True:成功 False:失败
    """
    try:
        shutil.rmtree(dir)
        return True
    except Exception as e:
        return False

def read(filename,encoding=None):
    """
    读取文件，返回内容
    :param filename:  (unicode) 文件名
    :param encoding:  (unicode) 编码
    :return: （unicode) 文件内容
    """
    f=None
    try:
        f=open(filename,"r")
        content=f.read()
        if encoding ==None or len(encoding)<1:
            info = chardet.detect(content)
            encoding= info['encoding']
        return content.decode(encoding,"ignore")
    except Exception as e:
        print e
        return u""
    finally:
        if f !=None:
            try:
                f.close()
            except Exception as e:
                print e

def join(dirname,filename):
    """
    拼接文件绝对路劲
    :param dirname: (str) 目录名
    :param filename: （str) 文件名
    :return: 文件绝对路径
    """
    return os.path.join(dirname,filename)

def size(filename):
    """
    获取文件大小字节数
    :param filename: (str) 文件名
    :return: （long)  字节数
    """
    return os.path.getsize(filename)

if __name__=="__main__":
    html_src= read("c:/a.html",encoding="UTF-8")
    print html_src
    print size("D:\\crawler\\common\\charutils.py")

