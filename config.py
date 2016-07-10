# -*- coding: utf-8 -*-
__author__ = 'Lvv'

# 调试开关
# dubug     日志文件输出级别     是否输出html    打码方式
#   0            ERROR            否           机器打码
#   1            DEBUG            是           人工打码
debug = 1

#   type值      队列类型
#    rdb        Redis
#    ssdb       SSDB
#    mongodb    MongoDB
#    kafka      Kafka

# 种子队列
type0 = 'ssdb'
host0 = 'web29'
port0 = 9092

# 内容队列
if debug:
    type1 = 'mongodb'
    host1 = 'localhost'
    port1 = 27017
else:
    type1 = 'ssdb'
    host1 = 'web29'
    port1 = 9090

# 代理配置
proxy_host = 'master1'
proxy_port = 8880
