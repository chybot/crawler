# -*- coding: utf-8 -*-
"""
代理配置模块模块
"""
import sys
reload(sys)
sys.setdefaultencoding("UTF-8")


#vule为单个IP连续抓取最大次数,针对连续抓取次数
series_num={
    'guizhou':2000,
    'guangdong':1000,
    'liaoning':1000,
    'anhui':1000,
}

#针对非连续抓取次数的，非自建代理的连续抓取次数设置
none_series_num={
    'zhejiang':50,
    'gansu':100
}

#代理访问类型
#bbd:只是使用自建代理
#buy:使用非自建代理
#all:不区分代理
prxoy_type={
    'guizhou':'bbd',
    'beijing':'buy',
    'zhejiang':'buy',
    'gansu':'buy',
    'liaoning':'bbd',
    'anhui':'bbd'
}