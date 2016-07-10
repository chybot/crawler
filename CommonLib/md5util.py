# -*- coding: utf-8 -*-
# Created by David on 2016/5/12.

import sys
import hashlib
import json
reload(sys)
sys.setdefaultencoding('utf-8')


def getMd5WithDict(dic_):
    """获取md5值"""
    try:
        return getMd5WithString(json.dumps(dic_))
    except Exception as e:
        return None


def getMd5WithString(str_):
    """获取md5值"""
    try:
        md5 = hashlib.md5()
        md5.update(str_)
        return md5.hexdigest()
    except Exception as e:
        return None


