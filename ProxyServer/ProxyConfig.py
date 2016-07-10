# -*- coding: utf-8 -*-
"""
代理配置模块
"""
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

host = 'web29'
port = 9091

lockoutproxysegment =['jilin','jiangsu']

configs={
    u'qyxy_shenzhen':[1000,200],
    u'guangdong':[1000,3600*2],
    u'hubei':[200,120],
    u'hunan':[800,2],
    u'henan':[800,2],
    u'heilongjiang':[900,120],
    u'hebei':[800,120],
    u'hainan':[800,120],
    u'guizhou':[1000,3600*2],
    u'guangxi':[800,120],
    u'fujian':[800,120],
    u'chongqing':[800,120],
    u'beijing':[30,1200],
    u'anhui':[1000,3600*2],
    u'jiangsu':[50,600],
    u'gansu':[200,120],
    u'xinjiang':[400,120],
    u'tianjin':[800,120],
    u'sichuan':[800,120],
    u'shanxixian':[800,120],
    u'shanxitaiyuan':[800,120],
    u'shanghai_2':[800,120],
    u'shandong':[50,120],
    u'qinghai':[800,120],
    u'ningxia':[30,120],
    u'neimenggu':[800,120],
    u'liaoning':[1000,120],
    u'jilin':[1000,200],
    u'jiangxi':[100,180],
    u'xizang':[800,120],
    u'zhejiang':[100,120],
    u'yunnan':[800,120],
    u'zongju':[800,120],
    u"bjxy_beijing":[30,120],
    u"wusong":[200,120],
    u"common":[1000,120],
    u"qyxy_chengdu":[1000,120],
    u"tdsy":[1000,120],
    u'12306':[1000,120]
}

balck_config={
    'beijing':3600*24,
}