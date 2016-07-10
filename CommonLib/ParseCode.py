# -*- coding: utf-8 -*-
__author__ = 'Lvv'

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import os
import chardet
from common import fileutil
from recchar import RecChar
import uuid


class ParseCode:

    def __init__(self):
        self.recChar = None
        self.yzm = None
        self.img_path = None

    def parse_yzm(self, img_src, typecode, yzm_filename='vcode', yzm_max_len=4, type=None):
        """
        对验证码进行人工打码验证
        :param img_src:  验证码图片内容
        :param typecode: 验证码类型
        :param yzm_filename: 验证码图片文件名
        :param yzm_max_len:  验证码最大长度
        :param type:  打码类型
        :return: （unicode,unicode,bool,RecChar,unicode）(验证码内容, 打码系统id, 是否正常,打码对象,验证码图片地址)
        """
        try:
            dir_path = os.path.abspath('.')
            img_path = os.path.join(dir_path, yzm_filename + '.png')
            fileutil.write(img_path, img_src)
            # 发送给打码公司打码 或 机器打码
            if type != None and len(type) > 0:
                if self.recChar == None:
                    self.recChar = RecChar(type)
                ret = self.recChar.rec(img_path)
                if ret != None and len(ret) > 0:
                    yzm = str(ret[0])
                    print 'yzm: ', yzm
                    if chardet.detect(yzm)['encoding'] == 'utf-8':
                        yzm = yzm.decode('utf-8')
                    if yzm != None and yzm.lower() == 'none':
                        yzm = None
                    return yzm, '0', False, self.recChar, img_path
                else:
                    raise Exception(u'机器打码返回值为None或长度为0！')
            else:
                if self.recChar == None:
                    self.recChar = RecChar()
                (yzm, code_id, is_report_error) = self.recChar.rec(img_path, typecode=typecode)
                print 'yzm: ', yzm
                if len(str(code_id)) < 4:
                    raise Exception(u'验证码识别错误，errorType=1, coid_id为空！')
                # 验证码内容为空
                if len(yzm) < 1 or len(yzm) > yzm_max_len:
                    raise Exception(u'验证码识别错误，errorType=2, 验证码长度不在正确范围！')
                self.yzm = yzm
                self.img_path = img_path
                return yzm, code_id, is_report_error, self.recChar, img_path
        except Exception as e:
            raise Exception(u'验证码处理异常：%s' % str(e))


    def record_success(self, dir_name, count=10000):
        """
        打码成功后记录
        :param dir_name: 保存验证码图片目录名
        :param count: 保存验证码文件个数，默认10000个
        :return: (None)
        """
        if not self.yzm or not self.img_path:
            return
        try:
            dir_path = os.path.abspath('../')
            yzm_dir = os.path.join(dir_path, 'yzm_success', dir_name)
            if not fileutil.isdir(yzm_dir):
                # 建立目录
                fileutil.mkdirs(yzm_dir)
            pics = sum([len(files) for root, dirs, files in os.walk(yzm_dir)])
            print u'已存放%d张验证码图片' % (pics - 1)
            if pics > count:
                print u'已存放超%d张验证码图片' % count
                return
            # 唯一的验证码图片文件名
            img = "%s.jpg" % str(uuid.uuid1())
            # 记录图片与验证码对应关系
            text_file_name = os.path.join(yzm_dir, 'ans.txt')
            file = open(text_file_name, 'a')
            file.write(img + ' ' + self.yzm + '\n')
            file.close()
            # 保存验证码图片
            img_name = os.path.join(yzm_dir, img)
            fileutil.copyfile(self.img_path, img_name)
        except Exception as e:
            print u'记录发生异常，错误信息：%s' % str(e)
            return