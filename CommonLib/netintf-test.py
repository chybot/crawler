# -*- coding: gb18030 -*-

#!/usr/bin/python
from netintf import NetIntf
from ctypes import *

#tpl只有上海、广东、陕西有用
#山东新加模型文件hmm_shandong.txt, shandong.net

def main():
    
    #江苏
    netf=NetIntf("./jiangsu.prototxt", "./jiangsu.caffemodel", "./jiangsu.map", -1)
    print netf.ComputeJiangsu("./jiangsu_test.jpg")
    
    #广东
    netf=NetIntf("./guangdong4.prototxt", "./guangdong4.caffemodel", "./guangdong4.map", -1, "./guangdong4.tpl")
    print netf.ComputeGuangdong4("./guangdong4_test.jpg")

    #内蒙古
    netf=NetIntf("./guangdong4.prototxt", "./guangdong4.caffemodel", "./guangdong4.map", -1, "./guangdong4.tpl")
    print netf.ComputeGuangdong4("./neimenggu.png")
    
    #重庆2
    netf=NetIntf("./chongqing2.prototxt", "./chongqing2.caffemodel", "./chongqing2.map", -1)
    print netf.ComputeChongqing2("./chongqing2_test.jpg")

    #河南
    netf=NetIntf("./hn2.prototxt", "./hn2.caffemodel", "./hn2.map", -1)
    print netf.ComputeHenan2("./hn2_test.jpg")

    #黑龙江
    netf=NetIntf("./hn2.prototxt", "./hn2.caffemodel", "./hn2.map", -1)
    print netf.ComputeHenan2("./heilongjiang.jpg")
    
    #上海
    netf=NetIntf("./shanghai1.prototxt", "./shanghai1.caffemodel", "./shanghai1.map", -1, "./shanghai1.tpl")
    print netf.ComputeShanghai1("./shanghai1_test.jpg")

    #湖南
    netf=NetIntf("./shanghai1.prototxt", "./shanghai1.caffemodel", "./shanghai1.map", -1, "./shanghai1.tpl")
    print netf.ComputeShanghai1("./hunan.jpg")

    #甘肃
    netf=NetIntf("./gansu.prototxt", "./gansu.caffemodel", "./gansu.map", -1)
    print netf.ComputeGansu("./gansu_test.jpg")

    #宁夏
    netf=NetIntf("./nx.prototxt", "./nx.caffemodel", "./nx.map", -1)
    print netf.ComputeNingxia("./nx_test.jpg")

    #江西
    netf=NetIntf("./nx.prototxt", "./nx.caffemodel", "./nx.map", -1)
    print netf.ComputeNingxia("./jiangxi.jpg")

    #山西
    netf=NetIntf("./shan1xi.prototxt", "./shan1xi.caffemodel", "./shan1xi.map", -1)
    print netf.ComputeShan1xi("./shan1xi_test.gif")

    #山西2
    netf=NetIntf("./hn2.prototxt", "./hn2.caffemodel", "./hn2.map", -1)
    print netf.ComputeHenan2("./shan1xi2.jpg")

    #深圳 不上了
    #netf=NetIntf("./shenzhen.prototxt", "./shenzhen.caffemodel", "./shenzhen.map", -1)
    #print netf.ComputeShenzhen("./shenzhen_test.gif")

    #天津
    netf=NetIntf("./tianjin.prototxt", "./tianjin.caffemodel", "./tianjin.map", -1)
    print netf.ComputeTianjin("./tianjin_test.jpg")

    #新疆
    netf=NetIntf("./xj2.prototxt", "./xj2.caffemodel", "./xj2.map", -1)
    print netf.ComputeXinjiang2("./xj2_test.jpg")

    #浙江
    netf=NetIntf("./zhejiang.prototxt", "./zhejiang.caffemodel", "./zhejiang.map", -1)
    print netf.ComputeZhejiang("./zhejiang_test.jpg")

    #浙江2
    netf=NetIntf("./zhejiang2.prototxt", "./zhejiang2.caffemodel", "./zhejiang2.map", -1)
    print netf.ComputeZhejiang("./zhejiang2_test.jpg")

    #贵州
    netf=NetIntf("./guizhou.prototxt", "./guizhou.caffemodel", "./guizhou.map", -1)
    print netf.ComputeGuizhou("./guizhou_test.jpg")

    #贵州2
    netf=NetIntf("./guizhou2.prototxt", "./guizhou2.caffemodel", "./guizhou2.map", -1)
    print netf.ComputeGuizhou2("./guizhou2_test.jpg")

    #贵州3
    netf=NetIntf("./guizhou3.prototxt", "./guizhou3.caffemodel", "./guizhou3.map", -1)
    print netf.ComputeGuizhou3("./guizhou3_test.jpg")

    #湖北
    netf=NetIntf("./hubei.prototxt", "./hubei.caffemodel", "./hubei.map", -1) 
    print netf.ComputeHubei("./hubei_test.jpg")

    #湖北2
    netf=NetIntf("./hubei2.prototxt", "./hubei2.caffemodel", "./hubei2.map", -1) 
    print netf.ComputeHubei2("./hubei2_test.jpg")
   
    #陕西
    netf=NetIntf("./shan3xi.prototxt", "./shan3xi.caffemodel", "./shan3xi.map", -1, "./shan3xi.tpl")
    print netf.ComputeShan3xi("./shan3xi_test.jpg")

    #陕西2
    netf=NetIntf("./shan3xi2.prototxt", "./shan3xi2.caffemodel", "./shan3xi2.map", -1)
    print netf.ComputeShan3xi2("./shan3xi2_test.jpg")

    #山东
    netf=NetIntf("./shandong.prototxt", "./shandong.caffemodel", "./shandong.map", -1, "", "./hmm_shandong.txt", "./shandong.net", 0.1)
    print netf.ComputeShandong("./shandong_test.jpg")
        
    #北京1
    netf=NetIntf("./beijing1.prototxt", "./beijing1.caffemodel", "./beijing1.map", -1)
    print netf.ComputeBeijing1("./beijing1_test.jpg")

    #中登网
    netf=NetIntf("./zhongdeng.prototxt", "./zhongdeng.caffemodel", "./zhongdeng.map", -1)
    print netf.ComputeZhongdeng("./zhongdeng_test.jpg")

    #CNCA
    netf=NetIntf("./cnca.prototxt", "./cnca.caffemodel", "./cnca.map", -1)
    print netf.ComputeCnca("./cnca_test.jpg")

    #海关总署
    netf=NetIntf("./haiguan.prototxt", "./haiguan.caffemodel", "./haiguan.map", -1)
    print netf.ComputeHaiguan("./haiguan_test.gif")


if __name__ == '__main__':
    main()
