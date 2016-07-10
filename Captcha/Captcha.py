# -*- coding: utf-8 -*-
"""
企业信息网验证码模块
"""
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import os
import uuid
import urlparse
import chardet
import time
sys.path.append("../")
from CommonLib import fileutil
from CommonLib.recchar import RecChar
import logging
log = logging.getLogger(__name__)

class Captcha(object):
    """
    企业信息打码模块，
    调用时候，引用Caotch实例，然后调用yzm方法获取验证码，
    在判断验证是否时候成功的时候调用验证码连续错误计数方法yzmFlag,当连续大于100次后，判定验证码变化；休眠，发邮件
    """
    def __init__(self,name):
        self.name = name
        self.recChar = None
        self.error_lx=0
    def record_success(self, yzm, img_path, count=10000):
        """
        打码成功后记录，文件名使用yzm
        :param yzm:  验证码
        :param count: 保存验证码文件个数，默认10000个
        :return: (None)
        """
        try:
            dir_path = os.path.abspath('../')
            yzm_dir = os.path.join(dir_path, "yzm_success", self.name)
            if not fileutil.isdir(yzm_dir):
                # 建立目录
                fileutil.mkdirs(yzm_dir)
            pics = sum([len(files) for root, dirs, files in os.walk(yzm_dir)])
            log.info(u"已存放%d张验证码图片" % (pics - 1))
            if pics > count:
                log.warn(u"已存放超%d张验证码图片" % count)
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
            log.error(u"记录发生异常.错误信息:%s" % e)

    def bbd_yzm(self, img_src):
        from requests import post
        try:
            yzm_html = post('http://spider7:5678/form', files={'files': img_src}, data={'type': self.name})
            yzm_html.encoding = 'utf-8'
            yzm_html = yzm_html.content
            assert len(yzm_html.split()) == 2
            yzm, img_name = yzm_html.split()
            print yzm, img_name
            return yzm
        except Exception as e:
            log.error(u"获取验证码错误：%s" % e)


    def yzm(self, img_url, img_src,type=None,**kwargs):
        """
        :param img_url:
        :param img_src:
        :param type:
        :param kwargs:
        :return:
        """
        dir_path = os.path.abspath('.')
        urlpret = urlparse.urlparse(img_url)
        img_path = os.path.join(dir_path, "%s_%s.png" % (urlpret.hostname, self.name))
        print "img_path:", img_path, "type:", type
        fileutil.write(img_path, img_src)
        log.info(u"请求验证码")
        if type != None and len(type) > 0:
            if self.recChar == None:
                self.recChar = RecChar(type)
            ret = self.recChar.rec(img_path)
            if ret != None and len(ret) > 0:
                yzm = str(ret[0])
                if chardet.detect(yzm)['encoding'] == "utf-8":
                    yzm = yzm.decode("utf-8")
                if str(yzm).lower() == "none":
                    yzm = None
                    raise Exception(u"验证码识别错误")
                log.info(u"recChar:%s,img_path:%s"%(self.recChar,img_path))
                return yzm
            else:
                raise Exception(u"机器打码返回值为None或长度为0.")

        else:
            yzm = self.bbd_yzm(img_src)
            if not yzm:
                log.error(u"自建打码服务错误：spider7 server error!")
                if self.recChar == None:
                    self.recChar = RecChar()
                if 'typecode' in kwargs:
                    typecode = kwargs['typecode']
                    (yzm, code_id, is_report_error) = self.recChar.rec(img_path, typecode=typecode)
                else:
                    raise Exception(u'没有typecode参数')
            # 手工打码，用于测试
            # recChar=""
            # yzm=raw_input()
            # yzm= yzm.decode("UTF-8",'ignore')
            # code_id="asdfasdfasdf"
            # is_report_error=False
            # print "yzm:",yzm
            return yzm

    def yzmFlag(self,error=True):
        if error:
            self.error_lx+=1
        else:
            self.error_lx=0
        if self.error_lx>=100:
            #todo
            #send mail
            log.error(u"验证码连续错误100次，可能验证码变化，休眠3600秒")
            time.sleep(3600)