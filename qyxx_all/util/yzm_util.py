# -*- coding: utf-8 -*-
# Created by David on 2016/4/18.

from __future__ import division
__author__ = 'xww'

import sys
reload(sys)
sys.setdefaultencoding("UTF-8")
sys.path.append("../")
import urlparse
import os
import chardet
import uuid
from CommonLib import fileutil
from CommonLib import exceptutil
from CommonLib.recchar import RecChar
from requests import post

def parse_yzm(img_url, img_src, typecode, yzm_max_len=4, type=None, holder=None):
    """
    对验证码进行人工打码验证
    :param img_url:  验证码图片地址
    :param img_src:  验证码图片内容
    :param typecode:
    :param yzm_max_len:  验证码最大长度
    :return: （unicode,unicode,bool,RecChar,unicode）(验证码内容, 打码系统id, 是否正常,打码对象,验证码图片地址)
    """
    img_path = None
    try:
        if len(img_src) <= 50 or len(img_src) > 1024 * 1024:
            raise Exception(u'img_src len error!')
        if not os.path.exists('yzm'):
            os.mkdir('yzm')
        pid = str(os.getpid())
        dir_path = os.path.abspath('.')
        urlpret = urlparse.urlparse(img_url)
        img_path = os.path.join(dir_path, 'yzm',"%s_%s.png" % (urlpret.hostname, pid+'_'+holder.pinyin))
        print "img_path:", img_path, "type:", type
        fileutil.write(img_path, img_src)
        holder.logging.info(u"请求验证码")
        # 发送给打码公司打码 或 机器打码
        if type != None and len(type) > 0:
            if holder.recChar == None:
                holder.recChar = RecChar(type=type, log=holder.logging)
            ret = holder.recChar.rec(img_path)
            yzm = None
            if ret != None and len(ret) > 0:
                yzm = str(ret[0])
                print "yzm:", yzm
                if chardet.detect(yzm)['encoding'] == "utf-8":
                    yzm = yzm.decode("utf-8")
                if yzm != None and yzm.lower() == "none":
                    yzm = None
                holder.logging.info("机器打码结果：yzm=%s" % (yzm if yzm else ''))
            else:
                holder.logging.info("机器打码结果：yzm为None或长度为0.")
            if yzm and yzm != '-9999':
                return yzm, "0", False, holder.recChar, img_path
            if yzm == '-9999':
                raise Exception(u'yzm -9999 error...')
            else:
                return parseYzmManual(img_path, typecode, holder)
        else:
            return parseYzmManual(img_path, typecode, holder)
    except Exception as e1:
        holder.logging.error(u"验证码处理异常,error:%s" % exceptutil.traceinfo(e1))
        raise Exception(e1)


def parseYzmManual(img_path, typecode, holder):
    """
    parse the validate code manually
    :param img_path:
    :param typecode:
    :param holder:
    :return:
    """
    if holder.recChar == None:
        holder.recChar = RecChar(log=holder.logging)
    holder.yzm_count += 1
    f = open(img_path,'rb')
    img_src = f.read()
    f.close()
    yzm = None
    if holder.debug == 1:
        (yzm, code_id, is_report_error, img_path_remote) = bbd_yzm(img_src, holder)
    if not yzm:
        (yzm, code_id, is_report_error) = holder.recChar.rec(img_path, typecode=typecode)
    holder.logging.info("手工打码结果,yzm:%s,code_id:%s,is_report_error:%s" % (yzm, str(code_id), str(is_report_error)))
    return (yzm, code_id, is_report_error, holder.recChar, img_path)

def bbd_yzm(img_src, holder=None):
    """
    parse the yzm from spider7 through net work
    :param img_src:
    :param holder:
    :return:
    """
    try:
        yzm_html = post('http://spider7:5678/form', files={'files': img_src}, data={'type': holder.pinyin})
        yzm_html.encoding = 'utf-8'
        yzm_html = yzm_html.content
        assert len(yzm_html.split()) == 2
        yzm, img_name = yzm_html.split()
        print yzm, img_name
        return yzm, img_name, "no erro", img_name
    except Exception as e:
        holder.logging.error(exceptutil.traceinfo(e))
        return None,None,None,None
        #raise Exception(u"获取验证码错误：%s" % e)

def record_success(pinyin, yzm, img_path, holder, count=10000):
    """
    打码成功后记录，文件名使用yzm
    :param yzm:  验证码
    :param count: 保存验证码文件个数，默认10000个
    :return: (None)
    """
    try:
        dir_path = os.path.abspath('../')
        yzm_dir = os.path.join(dir_path, "yzm_success", pinyin)
        if not fileutil.isdir(yzm_dir):
            # 建立目录
            fileutil.mkdirs(yzm_dir)
        pics = sum([len(files) for root, dirs, files in os.walk(yzm_dir)])
        holder.logging.info("已存放%d张验证码图片" % (pics - 1))
        if pics > count:
            holder.logging.warn("已存放超%d张验证码图片,不再存储" % count)
            return
        # 唯一的验证码图片文件名
        img = "%s.jpg" % str(uuid.uuid1())
        # 记录图片与验证码对应关系
        text_file_name = os.path.join(yzm_dir, "ans.txt")
        file = open(text_file_name, "a")
        file.write(img + ' ' + yzm + '\n')
        file.close()
        # 保存验证码图片
        img_name = os.path.join(yzm_dir, img)
        fileutil.copyfile(img_path, img_name)
    except Exception as e:
        holder.logging.error(u"记录发生异常.错误信息:%s" % exceptutil.traceinfo(e))


class LogUtil(object):
    def __init__(self, log):
        self.log = log

    def handleLog(self, *msgs, **log_level):
        if not self.log:
            return
        if not msgs:
            return
        try:
            level = "info"
            if log_level and 'level' in log_level:
                level = log_level['level']
            func = eval('self.log.%s' % level)
            if not callable(func):
                return
            for msg in msgs:
                func(str(msg))
        except:
            return

if __name__ == "__main__":
    from HolderUtil import HolderUtil
    holder = HolderUtil("ppp")
    holder.init()
    util = LogUtil(holder.logging)
    util.handleLog(holder, util)
    pass