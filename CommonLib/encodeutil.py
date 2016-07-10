# -*- coding: utf-8 -*-
__author__ = 'xww'

import hashlib


def md5(str):
    """计算字符串MD5值并返回
    :param str:(str)   原文
    :return: （unicode) 密文
    """
    if isinstance(str,basestring) and len(str)>0:
        m = hashlib.md5()
        m.update(str)
        return m.hexdigest()
    else:
        return ""


if __name__=="__main__":
    print md5("张三")