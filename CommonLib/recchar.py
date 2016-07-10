#!/usr/bin/python
#  -*- coding: gb2312 -*-

import sys
import os
import hashlib
import httplib
import urllib
import string
from hashlib import md5
import requests
from ctypes import *
from exceptutil import traceinfo

work_dir = os.path.dirname(__file__)
print "recchar work_dir:", work_dir
work_dir = os.path.dirname(os.path.abspath(__file__))
print "recchar work_dir:", work_dir

# ��ֵ��
threshold = 125
table = []
for i in range(256):
    if i < threshold:
        table.append(0)
    else:
        table.append(1)

#���ڶ�������
#����ʶ�����ĸ�� ���øñ��������
rep={'O':'0',
     'Q':'0',
    'I':'1','L':'1',
    'Z':'2',
    'S':'8'
    };


class RClient(object):

    def __init__(self, username, password, soft_id, soft_key):
        self.username = username
        self.password = md5(password).hexdigest()
        self.soft_id = soft_id
        self.soft_key = soft_key
        self.base_params = {
            'username': self.username,
            'password': self.password,
            'softid': self.soft_id,
            'softkey': self.soft_key,
        }
        self.headers = {
            'Connection': 'Keep-Alive',
            'Expect': '100-continue',
            'User-Agent': 'ben',
        }

    def rk_create(self, im, im_type, timeout=60):
        """
        im: ͼƬ�ֽ�
        im_type: ��Ŀ����
        """
        params = {
            'typeid': im_type,
            'timeout': timeout,
        }
        params.update(self.base_params)
        files = {'image': ('a.jpg', im)}
        r = requests.post('http://api.ruokuai.com/create.json', data=params, files=files, headers=self.headers, timeout=timeout*1.2)
        return r.json()

    def rk_report_error(self, im_id):
        """
        im_id:������Ŀ��ID
        """
        params = {
            'id': im_id,
        }
        r = requests.post('http://api.ruokuai.com/reporterror.json', data=params, headers=self.headers)
        return r.json()


class RecChar:
    def __init__(self, type = "ruokuai", s_id = 2349, s_key = "d5dd3969cc134d8ba90096eafcad983d", user = "qpzm1234qpzm", passwd = "brandbigdata1234", log=None):
        """ʹ��Ĭ�ϵ�����id�����룬�˻��������롣���û������"""
        self.type = type
        self.log = log
        if self.type == "mimidama":
            s_id = 2349
            s_key = "d5dd3969cc134d8ba90096eafcad983d"
            user = "qpzm1234qpzm"
            passwd = "brandbigdata1234"
            mimiDLL=os.path.join(work_dir, 'mimidama', 'Mimidama.dll')                   #��ǰĿ¼�µ��������API�ӿ��ļ�
            self.s_id  = s_id
            self.s_key = s_key
            self.user = user
            self.passwd = passwd
            #print mimiDLL
            mimi = windll.LoadLibrary(mimiDLL)

            # ��ʼ����������
            self.RecPath = mimi.RecPath
            self.getRecResult = mimi.getRecResult
            self.upload = mimi.upload
            self.getScore = mimi.getScore
            self.reportError = mimi.reportError
        elif self.type == "ruokuai":
            s_id=29509
            s_key="762118a521e64d369ac9c0dc6dde135c"
            user="qpzm1234qpzm"
            passwd="brandbigdata1234"
            self.rc = RClient(user, passwd, s_id, s_key)
        #ml
        elif self.type == "jiangsu":#����
            from yzm.netintf import NetIntf

            self.handleLog("jiangsu.prototxt:",os.path.join(work_dir, "jiangsu.prototxt"))
            self.handleLog("jiangsu.caffemodel:",os.path.join(work_dir, "jiangsu.caffemodel"))
            self.handleLog("jiangsu.jiangsu.map:",os.path.join(work_dir, "jiangsu.map"))
            self.netf=NetIntf(os.path.join(work_dir, "jiangsu.prototxt"), os.path.join(work_dir, "jiangsu.caffemodel"), os.path.join(work_dir, "jiangsu.map"), -1)
            #print self.netf.ComputeXinjiang2("./jiangsu_test.jpg")

        elif self.type == "xinjiang":#�½�
            from yzm.netintf import NetIntf

            self.handleLog(os.path.join(work_dir, "./xj2.prototxt"))
            self.netf=NetIntf(os.path.join(work_dir, "./xj2.prototxt"), os.path.join(work_dir, "./xj2.caffemodel"), os.path.join(work_dir, "./xj2.map"), -1)
        elif self.type == "sichuan":#�Ĵ�ͬ�½�2
            from yzm.netintf import NetIntf

            self.handleLog(os.path.join(work_dir, "./xj2.prototxt"))
            self.netf=NetIntf(os.path.join(work_dir, "./xj2.prototxt"), os.path.join(work_dir, "./xj2.caffemodel"), os.path.join(work_dir, "./xj2.map"), -1)

        elif self.type == "chongqing":#����
            from yzm.netintf import NetIntf
            
            self.netf=NetIntf(os.path.join(work_dir, "./chongqing2.prototxt"), os.path.join(work_dir, "./chongqing2.caffemodel"), os.path.join(work_dir, "./chongqing2.map"), -1)
            #print self.netf.ComputeChongqing("./cq_test.jpg")

        elif self.type == "guangdong":#�㶫
            from yzm.netintf import NetIntf
            
            self.netf=NetIntf(os.path.join(work_dir, "./guangdong4.prototxt"), os.path.join(work_dir, "./guangdong4.caffemodel"), os.path.join(work_dir, "./guangdong4.map"),  -1, os.path.join(work_dir, "./guangdong4.tpl"))
        elif self.type == "hainan":#�����õ��ϵĹ㶫
            from yzm.netintf import NetIntf
            
            self.netf=NetIntf(os.path.join(work_dir, "./gd3.prototxt"), os.path.join(work_dir, "./gd3.caffemodel"), os.path.join(work_dir, "./gd3.map"), -1)
        elif self.type == "neimenggu":#���ɹ��ù㶫4
            from yzm.netintf import NetIntf
            
            self.netf=NetIntf(os.path.join(work_dir, "./guangdong4.prototxt"), os.path.join(work_dir, "./guangdong4.caffemodel"), os.path.join(work_dir, "./guangdong4.map"),  -1, os.path.join(work_dir, "./guangdong4.tpl"))
        elif self.type == "gansu":#����
            from yzm.netintf import NetIntf
            
            self.netf=NetIntf(os.path.join(work_dir, "./gansu.prototxt"), os.path.join(work_dir, "./gansu.caffemodel"), os.path.join(work_dir, "./gansu.map"), -1)

        elif self.type == "henan":#����
            from yzm.netintf import NetIntf
            
            self.netf=NetIntf(os.path.join(work_dir, "./hn2.prototxt"), os.path.join(work_dir, "./hn2.caffemodel"), os.path.join(work_dir, "./hn2.map"), -1)
        elif self.type == "anhui":#�����õĺ���2
            from yzm.netintf import NetIntf
            
            self.netf=NetIntf(os.path.join(work_dir, "./hn2.prototxt"), os.path.join(work_dir, "./hn2.caffemodel"), os.path.join(work_dir, "./hn2.map"), -1)
        elif self.type == "guangxi":#�����õĺ���2
            from yzm.netintf import NetIntf
            
            self.netf=NetIntf(os.path.join(work_dir, "./hn2.prototxt"), os.path.join(work_dir, "./hn2.caffemodel"), os.path.join(work_dir, "./hn2.map"), -1)
        elif self.type == "xizang":#�����õĺ���2
            from yzm.netintf import NetIntf
            
            self.netf=NetIntf(os.path.join(work_dir, "./hn2.prototxt"), os.path.join(work_dir, "./hn2.caffemodel"), os.path.join(work_dir, "./hn2.map"), -1)
        elif self.type == "qinghai":#�ຣ�õĺ���2
            from yzm.netintf import NetIntf
            
            self.netf=NetIntf(os.path.join(work_dir, "./hn2.prototxt"), os.path.join(work_dir, "./hn2.caffemodel"), os.path.join(work_dir, "./hn2.map"), -1)
        elif self.type == "shanxitaiyuan":#ɽ��̫ԭ�õĺ���2
            from yzm.netintf import NetIntf
            
            self.netf=NetIntf(os.path.join(work_dir, "./hn2.prototxt"), os.path.join(work_dir, "./hn2.caffemodel"), os.path.join(work_dir, "./hn2.map"), -1)
        elif self.type == "heilongjiang":#�������õĺ���2
            from yzm.netintf import NetIntf
            
            self.netf=NetIntf(os.path.join(work_dir, "./hn2.prototxt"), os.path.join(work_dir, "./hn2.caffemodel"), os.path.join(work_dir, "./hn2.map"), -1)

        elif self.type == "shanghai":#�Ϻ�
            from yzm.netintf import NetIntf
            
            self.netf=NetIntf(os.path.join(work_dir, "./shanghai1.prototxt"), os.path.join(work_dir, "./shanghai1.caffemodel"), os.path.join(work_dir, "./shanghai1.map"), -1, os.path.join(work_dir, "./shanghai1.tpl"))
        elif self.type == "fujian":#�����õ��Ϻ�1
            from yzm.netintf import NetIntf
            
            self.netf=NetIntf(os.path.join(work_dir, "./shanghai1.prototxt"), os.path.join(work_dir, "./shanghai1.caffemodel"), os.path.join(work_dir, "./shanghai1.map"), -1, os.path.join(work_dir, "./shanghai1.tpl"))
        elif self.type == "hebei":#�ӱ��õ��Ϻ�1
            from yzm.netintf import NetIntf
            
            self.netf=NetIntf(os.path.join(work_dir, "./shanghai1.prototxt"), os.path.join(work_dir, "./shanghai1.caffemodel"), os.path.join(work_dir, "./shanghai1.map"), -1, os.path.join(work_dir, "./shanghai1.tpl"))

        elif self.type == "yunnan":#�����õ��Ϻ�1
            from yzm.netintf import NetIntf
            
            self.netf=NetIntf(os.path.join(work_dir, "./shanghai1.prototxt"), os.path.join(work_dir, "./shanghai1.caffemodel"), os.path.join(work_dir, "./shanghai1.map"), -1, os.path.join(work_dir, "./shanghai1.tpl"))
        elif self.type == "zongju":#�ܾ��õ��Ϻ�1
            from yzm.netintf import NetIntf
            
            self.netf=NetIntf(os.path.join(work_dir, "./shanghai1.prototxt"), os.path.join(work_dir, "./shanghai1.caffemodel"), os.path.join(work_dir, "./shanghai1.map"), -1, os.path.join(work_dir, "./shanghai1.tpl"))
        elif self.type == "hunan":#�����õ��Ϻ�1
            from yzm.netintf import NetIntf
            
            self.netf=NetIntf(os.path.join(work_dir, "./shanghai1.prototxt"), os.path.join(work_dir, "./shanghai1.caffemodel"), os.path.join(work_dir, "./shanghai1.map"), -1, os.path.join(work_dir, "./shanghai1.tpl"))

        elif self.type == "ningxia":#����
            from yzm.netintf import NetIntf
            
            self.netf=NetIntf(os.path.join(work_dir, "./nx.prototxt"), os.path.join(work_dir, "./nx.caffemodel"), os.path.join(work_dir, "./nx.map"), -1)
        elif self.type == "jiangxi":#����
            from yzm.netintf import NetIntf
            
            self.netf=NetIntf(os.path.join(work_dir, "./jiangxi.prototxt"), os.path.join(work_dir, "./jiangxi.caffemodel"), os.path.join(work_dir, "./jiangxi.map"), -1)

        elif self.type == "tianjin":#���
            from yzm.netintf import NetIntf
            
            self.netf=NetIntf(os.path.join(work_dir, "./tj.prototxt"), os.path.join(work_dir, "./tj.caffemodel"), os.path.join(work_dir, "./tj.map"), -1)

        elif self.type == "zhejiang":#�㽭
            from yzm.netintf import NetIntf
            
            #self.netf=NetIntf(os.path.join(work_dir, "./zhejiang.prototxt"), os.path.join(work_dir, "./zhejiang.caffemodel"), os.path.join(work_dir, "./zhejiang.map"), -1)
            self.netf=NetIntf(os.path.join(work_dir, "./zhejiang2.prototxt"), os.path.join(work_dir, "./zhejiang2.caffemodel"), os.path.join(work_dir, "./zhejiang2.map"), -1)

        elif self.type == "guizhou":#����
            from yzm.netintf import NetIntf
            
            self.netf=NetIntf(os.path.join(work_dir, "./guizhou3.prototxt"), os.path.join(work_dir, "./guizhou3.caffemodel"), os.path.join(work_dir, "./guizhou3.map"), -1)

        elif self.type == "hubei":#����
            from yzm.netintf import NetIntf
            
            self.netf=NetIntf(os.path.join(work_dir, "./hubei.prototxt"), os.path.join(work_dir, "./hubei.caffemodel"), os.path.join(work_dir, "./hubei.map"), -1)
        elif self.type == "hubei2":#����
            from yzm.netintf import NetIntf
            
            self.netf=NetIntf(os.path.join(work_dir, "./hubei2.prototxt"), os.path.join(work_dir, "./hubei2.caffemodel"), os.path.join(work_dir, "./hubei2.map"), -1)
        elif self.type == "shan3xi":#����
            from yzm.netintf import NetIntf
            
            self.netf=NetIntf(os.path.join(work_dir, "./shan3xi.prototxt"), os.path.join(work_dir, "./shan3xi.caffemodel"), os.path.join(work_dir, "./shan3xi.map"), -1, os.path.join(work_dir, "./shan3xi.tpl"))
        elif self.type == "shan3xi2":#����
            from yzm.netintf import NetIntf
            
            self.netf=NetIntf(os.path.join(work_dir, "./shan3xi2.prototxt"), os.path.join(work_dir, "./shan3xi2.caffemodel"), os.path.join(work_dir, "./shan3xi2.map"), -1)
        elif self.type == "shandong":#ɽ��
            from yzm.netintf import NetIntf
            
            self.netf=NetIntf(os.path.join(work_dir, "./shandong.prototxt"), os.path.join(work_dir, "./shandong.caffemodel"), os.path.join(work_dir, "./shandong.map"), -1, "", os.path.join(work_dir, "./hmm_shandong.txt"), os.path.join(work_dir, "./shandong.net"), 0.1)
        elif self.type == "beijing":#����
            from yzm.netintf import NetIntf
            
            self.netf=NetIntf(os.path.join(work_dir, "./beijing1.prototxt"), os.path.join(work_dir, "./beijing1.caffemodel"), os.path.join(work_dir, "./beijing1.map"), -1)

        elif self.type == "zhongdeng":#�е���
            from yzm.netintf import NetIntf
            
            self.netf=NetIntf(os.path.join(work_dir, "./zhongdeng.prototxt"), os.path.join(work_dir, "./zhongdeng.caffemodel"), os.path.join(work_dir, "./zhongdeng.map"), -1)

        elif self.type == "cnca":#������ϵ��֤
            from yzm.netintf import NetIntf
            
            self.netf=NetIntf(os.path.join(work_dir, "./cnca.prototxt"), os.path.join(work_dir, "./cnca.caffemodel"), os.path.join(work_dir, "./cnca.map"), -1)

        elif self.type == "haiguan":#������ϵ��֤
            from yzm.netintf import NetIntf
            
            self.netf=NetIntf(os.path.join(work_dir, "./haiguan.prototxt"), os.path.join(work_dir, "./haiguan.caffemodel"), os.path.join(work_dir, "./haiguan.map"), -1)

        elif self.type == "jilin":#����
            from yzm.tesintf import TesIntf
            self.netf=TesIntf()
        elif self.type == "liaoning":#����
            from yzm.tesintf import TesIntf
            self.netf=TesIntf()

        else:
            self.handleLog("unkown type:", self.type)
            sys.exit(-1)

    def handleException(self, e):
        if self.log:
            self.log.error(traceinfo(e))

    def handleLog(self, *msgs, **log_level):
        if not self.log:
            return
        if not msgs:
            return
        try:
            level = "info"
            if level and 'level' in level:
                level = log_level['level']
            func = eval('self.log.%s' % level)
            if not callable(func):
                return
            for msg in msgs:
                func(str(msg))
        except:
            return

    def getScore(self):
        """��ȡ��ǰ�Ļ��֣�����-1�������ӿ��д�"""
        ret = -1;
        if self.type == "mimidama":
            ret = self.getScore(self.user, self.passwd, c_int(self.s_id), c_char_p(self.s_key)) #��ȡ�û���ǰʣ�����
            #print('The Score of User : %s  is :%d' % (user.value, ret))
        return ret

    def rec(self, pic_file_path = os.path.join(work_dir, 'mimidama', 'test_pics', 'test1.jpg'), typecode = 60001, timeout=120):
        """
        :param pic_file_path:ͼƬ·��
        :param typecode:��֤������
        :return:(str(ret), code_id, is_report_error) ��֤��,��֤���id,�Ƿ��ύ�Ĵ��󱨸�

        ��retΪ�ջ�ʵ��ʶ�����ʱ�����ж�is_report_error�Ƿ�ΪFalse�����ΪFalse��Ҫ�ύһ����֤����󱨸�(self.reportError(code_id))
        """
        self.handleLog(u"����recchar�Ĵ��뷽����", pic_file_path, typecode, timeout, self.type)
        ret = ""
        code_id = 0
        is_report_error = False
        if self.type == "mimidama":
            result = c_char_p("")
            #self.log.info("type=%s,pic_file_path=%s" % (self.type, pic_file_path))
            code_id = self.RecPath(c_int(self.s_id), c_char_p(self.s_key), self.user, self.passwd, c_char_p(pic_file_path), c_int(60001), result)
            self.handleLog("result", result)
            if code_id <= 0:
                print('get result error ,ErrorCode:%d do reportError!' % code_id)
                report_ret = self.reportErrorID(code_id)
                self.handleLog("report_ret:", report_ret)
                if report_ret != 0:
                    self.handleLog("��֤��ʶ�����ʱ�ύ������� report_ret:%d pic_file_path:%s"%(report_ret, pic_file_path))
                else:
                    self.handleLog("reportError ok!")
                    is_report_error = True
            else:
                self.handleLog("the code_id is:%d result is:%s" % (code_id, result.value))
                ret = result.value
                pass
        elif self.type == "ruokuai":
            self.log.info("type=%s,pic_file_path=%s" % (self.type, pic_file_path))
            im = open(pic_file_path, 'rb').read()
            try:
                rk_create_ret = self.rc.rk_create(im, typecode, timeout)
                self.handleLog("%s, %s" % (str(rk_create_ret), rk_create_ret.get('Error',"NO Error")))
                ret = rk_create_ret["Result"]
                code_id = rk_create_ret["Id"]
                self.handleLog("%s, %s" % (rk_create_ret["Result"], rk_create_ret["Id"]))
            except Exception as e:
                self.handleException(e)
        elif self.type == "zhongdengwang":
            import Image
            import sys
            import ImageEnhance
            import ImageFilter
            from pyocr import pyocr
            #self.log.info("type=%s,pic_file_path=%s" % (self.type, pic_file_path))
            try:
                tools = pyocr.get_available_tools()[:]
                if len(tools) == 0:
                    print("No OCR tool found")
                    sys.exit(1)
                #print("Using '%s'" % (tools[0].get_name()))

                #��ͼƬ
                im = Image.open(pic_file_path)
                #ת��������
                imgry = im.convert('L')
                #imgry.save('g'+pic_file_path)

                #��ֵ��
                out = imgry.point(table,'1')
                #out.save('b'+pic_file_path)

                #ret = tools[0].image_to_string(Image.open(pic_file_path), lang='fra')
                #print ret
                ret = tools[0].image_to_string(out, lang='fra')

                #ʶ�����
                ret = ret.strip()
                #ret = ret.upper();

                for r in rep:
                    ret = ret.replace(r,rep[r])
                #print ret
            except Exception as e:
                self.handleException(e)
        elif self.type == "jiangsu":
            #print "pic_file_path:", pic_file_path, " strlen:", len(pic_file_path), " type", type(pic_file_path), " id:", id(pic_file_path)
            #print "pic_file_path:", pic_file_path, " strlen:", len(pic_file_path), " type", type(str(pic_file_path)), "id:", id(str(pic_file_path))
            try:
                ret = self.netf.ComputeJiangsu(str(pic_file_path))
            except Exception as e:
                self.handleException(e)
        elif self.type == "xinjiang":
            self.log.info("type=%s,pic_file_path=%s" % (self.type, pic_file_path))
            try:
                ret = self.netf.ComputeXinjiang2(str(pic_file_path))
            except Exception as e:
                self.handleException(e)
        elif self.type == "chongqing":
            self.log.info("type=%s,pic_file_path=%s" % (self.type, pic_file_path))
            try:
                ret = self.netf.ComputeChongqing2(str(pic_file_path))
            except Exception as e:
                self.handleException(e)
        elif self.type == "guangdong":
            self.log.info("type=%s,pic_file_path=%s" % (self.type, pic_file_path))
            try:
                ret = self.netf.ComputeGuangdong4(str(pic_file_path))
            except Exception as e:
                self.handleException(e)
        elif self.type == "neimenggu":
            self.log.info("type=%s,pic_file_path=%s" % (self.type, pic_file_path))
            try:
                ret = self.netf.ComputeGuangdong4(str(pic_file_path))
            except Exception as e:
                self.handleException(e)
        elif self.type == "gansu":
            self.log.info("type=%s,pic_file_path=%s" % (self.type, pic_file_path))
            try:
                ret = self.netf.ComputeGansu(str(pic_file_path))
            except Exception as e:
                self.handleException(e)
        elif self.type == "hainan":
            self.log.info("type=%s,pic_file_path=%s" % (self.type, pic_file_path))
            try:
                ret = self.netf.ComputeGuangdong3(str(pic_file_path))
            except Exception as e:
                self.handleException(e)
        elif self.type == "henan":
            self.log.info("type=%s,pic_file_path=%s" % (self.type, pic_file_path))
            try:
                ret = self.netf.ComputeHenan2(str(pic_file_path))
            except Exception as e:
                self.handleException(e)
        elif self.type == "shanghai":
            self.log.info("type=%s,pic_file_path=%s" % (self.type, pic_file_path))
            try:
                ret = self.netf.ComputeShanghai1(str(pic_file_path))
            except Exception as e:
                self.handleException(e)
        elif self.type == "hunan":
            self.log.info("type=%s,pic_file_path=%s" % (self.type, pic_file_path))
            try:
                ret = self.netf.ComputeShanghai1(str(pic_file_path))
            except Exception as e:
                self.handleException(e)
        elif self.type == "ningxia":
            self.log.info("type=%s,pic_file_path=%s" % (self.type, pic_file_path))
            try:
                ret = self.netf.ComputeNingxia(str(pic_file_path))
            except Exception as e:
                self.handleException(e)
        elif self.type == "jiangxi":
            self.log.info("type=%s,pic_file_path=%s" % (self.type, pic_file_path))
            try:
                ret = self.netf.ComputeJiangxi(str(pic_file_path))
            except Exception as e:
                self.handleException(e)
        elif self.type == "tianjin":
            self.log.info("type=%s,pic_file_path=%s" % (self.type, pic_file_path))
            try:
                ret = self.netf.ComputeTianjin(str(pic_file_path))
            except Exception as e:
                self.handleException(e)
        elif self.type == "fujian":
            self.log.info("type=%s,pic_file_path=%s" % (self.type, pic_file_path))
            try:
                ret = self.netf.ComputeShanghai1(str(pic_file_path))
            except Exception as e:
                self.handleException(e)
        elif self.type == "hebei":
            self.log.info("type=%s,pic_file_path=%s" % (self.type, pic_file_path))
            try:
                ret = self.netf.ComputeShanghai1(str(pic_file_path))
            except Exception as e:
                self.handleException(e)
        elif self.type == "anhui":
            self.log.info("type=%s,pic_file_path=%s" % (self.type, pic_file_path))
            try:
                ret = self.netf.ComputeHenan2(str(pic_file_path))
            except Exception as e:
                self.handleException(e)
        elif self.type == "guangxi":
            self.log.info("type=%s,pic_file_path=%s" % (self.type, pic_file_path))
            try:
                ret = self.netf.ComputeHenan2(str(pic_file_path))
            except Exception as e:
                self.handleException(e)
        elif self.type == "heilongjiang":
            self.log.info("type=%s,pic_file_path=%s" % (self.type, pic_file_path))
            try:
                ret = self.netf.ComputeHenan2(str(pic_file_path))
            except Exception as e:
                self.handleException(e)
        elif self.type == "yunnan":
            self.log.info("type=%s,pic_file_path=%s" % (self.type, pic_file_path))
            try:
                ret = self.netf.ComputeShanghai1(str(pic_file_path))
            except Exception as e:
                self.handleException(e)
        elif self.type == "xizang":
            self.log.info("type=%s,pic_file_path=%s" % (self.type, pic_file_path))
            try:
                ret = self.netf.ComputeHenan2(str(pic_file_path))
            except Exception as e:
                self.handleException(e)
        elif self.type == "qinghai":
            self.log.info("type=%s,pic_file_path=%s" % (self.type, pic_file_path))
            try:
                ret = self.netf.ComputeHenan2(str(pic_file_path))
            except Exception as e:
                self.handleException(e)
        elif self.type == "sichuan":
            self.log.info("type=%s,pic_file_path=%s" % (self.type, pic_file_path))
            try:
                ret = self.netf.ComputeXinjiang2(str(pic_file_path))
            except Exception as e:
                self.handleException(e)
        elif self.type == "zongju":
            self.log.info("type=%s,pic_file_path=%s" % (self.type, pic_file_path))
            try:
                ret = self.netf.ComputeShanghai1(str(pic_file_path))
            except Exception as e:
                self.handleException(e)
        elif self.type == "zhejiang":
            self.log.info("type=%s,pic_file_path=%s" % (self.type, pic_file_path))
            try:
                ret = self.netf.ComputeZhejiang(str(pic_file_path))
            except Exception as e:
                self.handleException(e)
        elif self.type == "shanxitaiyuan":
            self.log.info("type=%s,pic_file_path=%s" % (self.type, pic_file_path))
            try:
                ret = self.netf.ComputeHenan2(str(pic_file_path))
            except Exception as e:
                self.handleException(e)
        elif self.type == "guizhou":
            self.log.info("type=%s,pic_file_path=%s" % (self.type, pic_file_path))
            try:
                ret = self.netf.ComputeGuizhou3(str(pic_file_path))
            except Exception as e:
                self.handleException(e)
        elif self.type == "hubei":
            self.log.info("type=%s,pic_file_path=%s" % (self.type, pic_file_path))
            try:
                ret = self.netf.ComputeHubei(str(pic_file_path))
            except Exception as e:
                self.handleException(e)
        elif self.type == "hubei2":
            self.log.info("type=%s,pic_file_path=%s" % (self.type, pic_file_path))
            try:
                ret = self.netf.ComputeHubei2(str(pic_file_path))
            except Exception as e:
                self.handleException(e)
        elif self.type == "shan3xi":
            self.log.info("type=%s,pic_file_path=%s" % (self.type, pic_file_path))
            try:
                ret = self.netf.ComputeShan3xi(str(pic_file_path))
            except Exception as e:
                self.handleException(e)
        elif self.type == "shan3xi2":
            self.log.info("type=%s,pic_file_path=%s" % (self.type, pic_file_path))
            try:
                ret = self.netf.ComputeShan3xi2(str(pic_file_path))
            except Exception as e:
                self.handleException(e)
        elif self.type == "shandong":
            self.log.info("type=%s,pic_file_path=%s" % (self.type, pic_file_path))
            try:
                ret = self.netf.ComputeShandong(str(pic_file_path))
            except Exception as e:
                self.handleException(e)
        elif self.type == "beijing":
            self.log.info("type=%s,pic_file_path=%s" % (self.type, pic_file_path))
            try:
                ret = self.netf.ComputeBeijing1(str(pic_file_path))
            except Exception as e:
                self.handleException(e)

        elif self.type == "zhongdeng":#�е���
            self.log.info("type=%s,pic_file_path=%s" % (self.type, pic_file_path))
            try:
                ret = self.netf.ComputeZhongdeng(str(pic_file_path))
            except Exception as e:
                self.handleException(e)

        elif self.type == "cnca":#������ϵ��֤
            self.log.info("type=%s,pic_file_path=%s" % (self.type, pic_file_path))
            try:
                ret = self.netf.ComputeCnca(str(pic_file_path))
            except Exception as e:
                self.handleException(e)

        elif self.type == "haiguan":#������ϵ��֤
            self.log.info("type=%s,pic_file_path=%s" % (self.type, pic_file_path))
            try:
                ret = self.netf.ComputeHaiguan(str(pic_file_path))
            except Exception as e:
                self.handleException(e)

        elif self.type == "jilin":
            self.log.info("type=%s,pic_file_path=%s" % (self.type, pic_file_path))
            try:
                ret = self.netf.ComputeShandong(str(pic_file_path))
            except Exception as e:
                self.handleException(e)
        elif self.type == "liaoning":
            self.log.info("type=%s,pic_file_path=%s" % (self.type, pic_file_path))
            try:
                ret = self.netf.ComputeLiaoning3(str(pic_file_path))
            except Exception as e:
                self.handleException(e)

        else:
            self.handleLog("unkown type:", self.type)
            sys.exit(-1)

        return (ret, code_id, is_report_error)

    def reportErrorID(self, code_id):
        """
        ���ִ���ʱ�ύ��֤id��������
        :param code_id:
        :return:
        """
        if self.type == "mimidama":
            return self.reportError(code_id)
        elif self.type == "ruokuai":
            return self.rc.rk_report_error(code_id)

import time
import random
if __name__ == "__main__":

    recChar = RecChar(type="jiangxi");
    pic_filename = "./jiangxi_test.jpg"
    ret = recChar.rec(pic_filename)
    print(pic_filename, ret[0])

    sys.exit()

    recChar = RecChar();#����
    pic_filename = "./vcode.png"
    ret = recChar.rec(pic_filename, typecode=2040)
    print pic_filename, ret[0]

    recChar = RecChar(type="beijing");#����
    pic_filename = "./beijing1_test.jpg"
    ret = recChar.rec(pic_filename)
    print pic_filename, ret[0]



    recChar = RecChar(type="haiguan");#����
    pic_filename = "./haiguan_test.gif"
    ret = recChar.rec(pic_filename)
    print pic_filename, ret[0]

    recChar = RecChar(type="hubei2");#����2
    pic_filename = "./hubei2_test.jpg"
    ret = recChar.rec(pic_filename)
    print pic_filename, ret[0]

    recChar = RecChar(type="cnca");#������ϵ��֤
    pic_filename = "./cnca_test.jpg"
    ret = recChar.rec(pic_filename)
    print pic_filename, ret[0]

    recChar = RecChar(type="shan3xi2");
    pic_filename = "./shan3xi2_test.jpg"
    ret = recChar.rec(pic_filename)
    print pic_filename, ret[0]

    """while True:
        #print random.random()
        #time.sleep(random.random())
        recChar = RecChar();
        pic_filename = "./shanghai1_test.jpg"
        ret = recChar.rec(pic_filename, typecode=5000)
        print pic_filename, ret[0]
    """
    sys.exit()

    #����ml�Ŀ�
    recChar = RecChar(type="jiangsu");
    pic_filename = "./jiangsu_test.jpg"
    ret = recChar.rec(pic_filename)
    print pic_filename, ret[0]

    recChar = RecChar(type="guangdong");
    pic_filename = "./guangdong4_test.jpg"
    ret = recChar.rec(pic_filename)
    print pic_filename, ret[0]

    recChar = RecChar(type="chongqing");
    pic_filename = "./chongqing2_test.jpg"
    ret = recChar.rec(pic_filename)
    print pic_filename, ret[0]

    recChar = RecChar(type="henan");
    pic_filename = "./hn2_test.jpg"
    ret = recChar.rec(pic_filename)
    print pic_filename, ret[0]

    recChar = RecChar(type="shanghai");
    pic_filename = "./shanghai1_test.jpg"
    ret = recChar.rec(pic_filename)
    print pic_filename, ret[0]

    recChar = RecChar(type="gansu");
    pic_filename = "./gansu_test.jpg"
    ret = recChar.rec(pic_filename)
    print pic_filename, ret[0]

    recChar = RecChar(type="hainan");
    pic_filename = "./hainan_test.jpg"
    ret = recChar.rec(pic_filename)
    print pic_filename, ret[0]

    recChar = RecChar(type="ningxia");
    pic_filename = "./nx_test.jpg"
    ret = recChar.rec(pic_filename)
    print pic_filename, ret[0]

    recChar = RecChar(type="shanxitaiyuan");
    pic_filename = "./shan1xi2.jpg"
    ret = recChar.rec(pic_filename)
    print pic_filename, ret[0]

    recChar = RecChar(type="tianjin");
    pic_filename = "./tj_test.jpg"
    ret = recChar.rec(pic_filename)
    print pic_filename, ret[0]

    recChar = RecChar(type="xinjiang");
    pic_filename = "./xj2_test.jpg"
    ret = recChar.rec(pic_filename)
    print pic_filename, ret[0]

    recChar = RecChar(type="fujian");
    pic_filename = "./fujian.png"
    ret = recChar.rec(pic_filename)
    print pic_filename, ret[0]

    recChar = RecChar(type="hebei");
    pic_filename = "./hebei.jpg"
    ret = recChar.rec(pic_filename)
    print pic_filename, ret[0]

    recChar = RecChar(type="anhui");
    pic_filename = "./anhui.jpg"
    ret = recChar.rec(pic_filename)
    print pic_filename, ret[0]

    recChar = RecChar(type="guangxi");
    pic_filename = "./guangxi.jpg"
    ret = recChar.rec(pic_filename)
    print pic_filename, ret[0]

    recChar = RecChar(type="yunnan");
    pic_filename = "./yunnan.jpg"
    ret = recChar.rec(pic_filename)
    print pic_filename, ret[0]

    recChar = RecChar(type="xizang");
    pic_filename = "./xizang.png"
    ret = recChar.rec(pic_filename)
    print pic_filename, ret[0]

    recChar = RecChar(type="sichuan");
    pic_filename = "./sichuan.jpg"
    ret = recChar.rec(pic_filename)
    print pic_filename, ret[0]

    recChar = RecChar(type="zongju");
    pic_filename = "./zongju.jpg"
    ret = recChar.rec(pic_filename)
    print pic_filename, ret[0]

    recChar = RecChar(type="zhejiang");
    pic_filename = "./zhejiang2_test.jpg"
    ret = recChar.rec(pic_filename)
    print pic_filename, ret[0]

    recChar = RecChar(type="heilongjiang");
    pic_filename = "./heilongjiang.jpg"
    ret = recChar.rec(pic_filename)
    print pic_filename, ret[0]

    recChar = RecChar(type="guizhou");
    pic_filename = "./guizhou3_test.jpg"
    ret = recChar.rec(pic_filename)
    print pic_filename, ret[0]

    recChar = RecChar(type="neimenggu");
    pic_filename = "./neimenggu.png"
    ret = recChar.rec(pic_filename)
    print pic_filename, ret[0]

    recChar = RecChar(type="hunan");
    pic_filename = "./hunan.jpg"
    ret = recChar.rec(pic_filename)
    print pic_filename, ret[0]

    recChar = RecChar(type="jiangxi");
    pic_filename = "./jiangxi.jpg"
    ret = recChar.rec(pic_filename)
    print pic_filename, ret[0]

    recChar = RecChar(type="hubei");
    pic_filename = "./hubei_test.jpg"
    ret = recChar.rec(pic_filename)
    print pic_filename, ret[0]

    recChar = RecChar(type="shan3xi");
    pic_filename = "./shan3xi_test.jpg"
    ret = recChar.rec(pic_filename)
    print pic_filename, ret[0]

    recChar = RecChar(type="jilin");
    pic_filename = "./jilin_test.jpg"
    ret = recChar.rec(pic_filename)
    print pic_filename, ret[0]

    recChar = RecChar(type="liaoning");
    pic_filename = "./liaoning3_test.jpg"
    ret = recChar.rec(pic_filename)
    print pic_filename, ret[0]

    recChar = RecChar(type="shandong");
    pic_filename = "./shandong_test.jpg"
    ret = recChar.rec(pic_filename)
    print pic_filename, ret[0]

    recChar = RecChar(type="beijing");
    pic_filename = "./beijing1_test.jpg"
    ret = recChar.rec(pic_filename)
    print pic_filename, ret[0]

    recChar = RecChar(type="zhongdeng");
    pic_filename = "./zhongdeng_test.jpg"
    ret = recChar.rec(pic_filename)
    print pic_filename, ret[0]

    sys.exit()

    recChar = RecChar(type="zhongdengwang");
    for i in range(0, 10):
        #ret = recChar.rec(ur"valid%d.bmp"%i)
        ret = recChar.rec(ur"valid%d.png"%i)
        print ret[0]

    sys.exit()
    """

    #����һ
    recChar = RecChar();
    #print recChar.rec();
    #print recChar.rec(ur"D:\python_test\ruokuai-python2\shanghai1.bmp");
    #(ret, code_id, is_report_error) = recChar.rec(ur"D:\python_test\ruokuai-python2\shanghai2.bmp");
    #print ret, code_id, is_report_error
    #if ret != u"��ɲ����":
    #    print recChar.reportErrorID(code_id)
    (ret, code_id, is_report_error) = recChar.rec(ur"D:\python_test\ruokuai-python2\shanghai3.bmp", typecode=5000);
    print ret, code_id, is_report_error
    if ret != u"����۸�":
        print recChar.reportErrorID(code_id)
    (ret, code_id, is_report_error) = recChar.rec(ur"D:\python_test\ruokuai-python2\shanghai4.bmp");
    print ret, code_id, is_report_error
    if ret != u"����ͺ�":
        print recChar.reportErrorID(code_id)
    (ret, code_id, is_report_error) = recChar.rec(ur"D:\python_test\ruokuai-python2\shanghai5.bmp");
    print ret, code_id, is_report_error
    if ret != u"0":
        print recChar.reportErrorID(code_id)    """
"""
    #����2
    print recChar.rec(ur"D:\python_test\ruokuai-python2\shanghai1.bmp");
    print recChar.rec(ur"D:\python_test\ruokuai-python2\shanghai2.bmp");
    print recChar.rec(ur"D:\python_test\ruokuai-python2\shanghai3.bmp");
    print recChar.rec(ur"D:\python_test\ruokuai-python2\shanghai4.bmp");
    print recChar.rec(ur"D:\python_test\ruokuai-python2\shanghai5.bmp");"""
