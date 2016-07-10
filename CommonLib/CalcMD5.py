# -*- coding: utf-8 -*-
# Created by Leo on 16/05/06
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
import hashlib
import os
# import time

def calcSha1(filepath):
    """
    get Shaa for a file, file size is limit
    :param filepath:
    :return:
    """
    with open(filepath,'rb') as f:
        sha1_obj = hashlib.sha1()
        sha1_obj.update(f.read())
        hash = sha1_obj.hexdigest()
        return hash

def calcFileMD5(filepath):
    with open(filepath,'rb') as f:
        md5_obj = hashlib.md5()
        md5_obj.update(f.read())
        md5_str = md5_obj.hexdigest()
        return md5_str
def calcStrMD5(str):
    md5_obj = hashlib.md5()
    md5_obj.update(str)
    md5_str = md5_obj.hexdigest()
    return md5_str

if __name__ == "__main__":

    hashfile = u"股东信息错位名单.txt"
    md5 = calcStrMD5("xxxx")
    print "md5:", md5
    if not os.path.exists(hashfile):
        dir_name = os.path.dirname(__file__)
        hashfile = dir_name + "/"+hashfile
        if not os.path.exists(hashfile):
            print("cannot found file")
        else:
            calcFileMD5(hashfile)
    else:
        while 1:
            # md5 = calcFileMD5(hashfile)
            # print "md5:",md5
            # time.sleep(1)
            md5 = calcStrMD5("xxxx")
            print "md5:", md5
