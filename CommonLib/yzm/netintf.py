#!/usr/bin/python
from ctypes import *
import os
#export LD_LIBRARY_PATH=/usr/lib:/usr/lib/x86_64-linux-gnu/:/usr/local/lib:$LD_LIBRARY_PATH

work_dir = os.path.dirname(__file__)
print "work_dir:", work_dir, os.path.join(work_dir, './libcaffe.so')
work_dir = os.path.dirname(os.path.abspath(__file__))
print "work_dir:", work_dir, os.path.join(work_dir, './libcaffe.so')
lib = cdll.LoadLibrary(os.path.join(work_dir, './libcaffe.so'))

class NetIntf(object):
    def __init__(self, model, weights, map_path='', gpu=-1, tpl_path='', hmm_path='', net_path='', pdf_scale=0.1):
        lib.NetIntf_new.argtypes=[c_char_p, c_char_p, c_char_p, c_int, c_char_p, c_char_p, c_char_p, c_double] 
        self.obj = lib.NetIntf_new(model, weights, map_path, gpu, tpl_path, hmm_path, net_path, pdf_scale)

    def ComputeChongqing(self, img_path):
        return lib.NetIntf_ComputeChongqing(self.obj, img_path)

    def ComputeCnca(self, img_path):
        return lib.NetIntf_ComputeCnca(self.obj, img_path)

    def ComputeChongqing2(self, img_path):
        return lib.NetIntf_ComputeChongqing2(self.obj, img_path)

    def ComputeXinjiang2(self, img_path):
        return lib.NetIntf_ComputeXinjiang2(self.obj, img_path)

    def ComputeGuangdong2(self, img_path):
        lib.NetIntf_ComputeGuangdong2.restype = c_char_p
        return lib.NetIntf_ComputeGuangdong2(self.obj, img_path)

    def ComputeBeijing1(self, img_path):
        lib.NetIntf_ComputeBeijing1.restype = c_char_p
        return lib.NetIntf_ComputeBeijing1(self.obj, img_path)
    
    def ComputeHenan2(self, img_path):
        res = lib.NetIntf_ComputeHenan2(self.obj, img_path)
        if res == -9999:
            return None
        else:
            return res
    def ComputeShandong(self, img_path):
        res = lib.NetIntf_ComputeShandong(self.obj, img_path)
        if res == -9999:
            return None
        else:
            return res
    def ComputeShanghai1op(self, img_path):
        res = lib.NetIntf_ComputeShanghai1op(self.obj, img_path)
        if res == -9999:
            return None
        else:
            return res

    def ComputeShanghai1bin(self, img_path):
        return lib.NetIntf_ComputeShanghai1bin(self.obj, img_path)

    def ComputeGuangdong3(self, img_path):
        res = lib.NetIntf_ComputeGuangdong3(self.obj, img_path)
        if res == -9999:
            return None
        else:
            return res

    def ComputeNingxia(self, img_path):
        res = lib.NetIntf_ComputeNingxia(self.obj, img_path)
        if res == -9999:
            return None
        else:
            return res

    def ComputeTianjin(self, img_path):
        res = lib.NetIntf_ComputeTianjin(self.obj, img_path)
        if res == -9999:
            return None
        else:
            return res

    def ComputeShan1xi(self, img_path):
        return lib.NetIntf_ComputeShan1xi(self.obj, img_path)

    def ComputeGansu(self, img_path):
        return lib.NetIntf_ComputeGansu(self.obj, img_path)
    
    def ComputeJiangsu(self, img_path): 
        lib.NetIntf_ComputeJiangsu.restype = c_char_p
        res = lib.NetIntf_ComputeJiangsu(self.obj, img_path)
        if res =='':  
            return None
        else:            
            return res
    def ComputeShenzhen(self, img_path):
        lib.NetIntf_ComputeShenzhen.restype = c_char_p
        res = lib.NetIntf_ComputeShenzhen(self.obj, img_path)
        if res =='':  
            return None
        else:            
            return res

    def ComputeHaiguan(self, img_path):
        lib.NetIntf_ComputeHaiguan.restype = c_char_p
        res = lib.NetIntf_ComputeHaiguan(self.obj, img_path)
        if res =='':  
            return None
        else:            
            return res

    def ComputeZhongdeng(self, img_path):
        lib.NetIntf_ComputeZhongdeng.restype = c_char_p
        res = lib.NetIntf_ComputeZhongdeng(self.obj, img_path)
        if res =='':  
            return None
        else:            
            return res
    def ComputeGuangdong4(self, img_path):
        lib.NetIntf_ComputeGuangdong4.restype = c_char_p
        res = lib.NetIntf_ComputeGuangdong4(self.obj, img_path)
        if res =='':  
            return None
        else:            
            return res
    def ComputeShanghai1(self, img_path):
        lib.NetIntf_ComputeShanghai1.restype = c_char_p
        res = lib.NetIntf_ComputeShanghai1(self.obj, img_path)
        if res =='':  
            return None
        else:            
            return res
    def ComputeZhejiang(self, img_path):
        lib.NetIntf_ComputeZhejiang.restype = c_char_p
        return lib.NetIntf_ComputeZhejiang(self.obj, img_path)
    def ComputeGuizhou(self, img_path):
        lib.NetIntf_ComputeGuizhou.restype = c_char_p
        return lib.NetIntf_ComputeGuizhou(self.obj, img_path)
    def ComputeGuizhou2(self, img_path):
        lib.NetIntf_ComputeGuizhou2.restype = c_char_p
        return lib.NetIntf_ComputeGuizhou2(self.obj, img_path)
    def ComputeGuizhou3(self, img_path):
        lib.NetIntf_ComputeGuizhou2.restype = c_char_p
        return lib.NetIntf_ComputeGuizhou2(self.obj, img_path)
    def ComputeHubei(self, img_path):
        lib.NetIntf_ComputeHubei.restype = c_char_p
        return lib.NetIntf_ComputeHubei(self.obj, img_path)
    def ComputeHubei2(self, img_path):
        lib.NetIntf_ComputeHubei2.restype = c_char_p
        return lib.NetIntf_ComputeHubei2(self.obj, img_path)
    def ComputeShan3xi(self, img_path):
        lib.NetIntf_ComputeShan3xi.restype = c_char_p
        return lib.NetIntf_ComputeShan3xi(self.obj, img_path)
    def ComputeShan3xi2(self, img_path):
        return lib.NetIntf_ComputeShan3xi2(self.obj, img_path)
    def ComputeJiangxi(self, img_path):
        return lib.NetIntf_ComputeJiangxi(self.obj, img_path)
