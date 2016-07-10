# -*- coding: utf-8 -*-
"""
Created by shuaiguangying on 15-10-13
"""
__author__ = 'shuaiguangying'

import sys

reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.append("../")
sys.path.append("../../")


import logging
import socket
from common.exceputil import traceinfo
from logging import Handler
from logging.handlers import TimedRotatingFileHandler

# 日志级别
ERROR = 40      # 错误信息
WARNING = 30    # 警告信息
INFO = 20       # 一般信息
DEBUG = 10      # 调试信息

from common import storageutil
import datetime

DEFAULT_CONF = {
    'level': DEBUG,
    # kafaka config
    'is_queue': False,       # 是否输出到队列
    'type': 'kafka',        # type可以是kafka ssdb redis
    'table': 'kafka_log', #  队列表名，如果是kafka则代表topic名称
    'port': 51092,
    'host': 'web14',
    'level_queue': DEBUG,
    # 'format_queue' : '%(asctime)s %(filename)s[line:%(lineno)d] %(funcName)s %(levelname)s %(message)s',  # 输出屏幕格式
    'format_queue': '%(filename)s[line:%(lineno)d] %(funcName)s %(message)s',  # 输出屏幕格式
    'datefmt_queue': '%Y-%m-%d %H:%M:%S,%f',

    # logging config
    'is_file': True,
    'level_file': DEBUG,                                # 日志文件级别
    'format_file': '%(asctime)s %(filename)s[line:%(lineno)d] %(funcName)s %(levelname)s %(message)s',         # 输出格式
    'datefmt_file': '%Y-%m-%d %H:%M:%S',                # 日期格式
    'filepath': './',                              # 日志保存目录，默认当前目录
    'filename_prefix': 'Jpider',                   # 日志文件名前缀
    'filename_suffix': '%Y%m%d.log',               # 日志文件名后缀
    'when': 'D',                                   # 默认新建日志文件单位时间为一天
    'interval': 1,                                 # 新建日志文件间隔多少个单位时间
    'backup_count': 5,                             # 保留日志文件个数

    # console config
    'is_console': True,                            # 是否输出到屏幕
    'level_console': DEBUG,                         # 输出到屏幕日志级别
    'format_console': '%(asctime)s %(filename)s[line:%(lineno)d] %(funcName)s %(levelname)s %(message)s'  # 输出屏幕格式
}

class QueueHandler(Handler):

    def __init__(self, **kwargs):
        Handler.__init__(self)
        self.dict_conf = kwargs
        type, table, port, host = kwargs["type"], kwargs['table'], kwargs['port'], kwargs['host']
        self.queue = storageutil.getdb_factory(table=table, type=type, port=port, host=host, async=True)

    def emit(self, record):
        try:
            msg = self.format(record)
            data = {
                "host": socket.gethostname(),
                "app": self.dict_conf['app'],
                "level": record.levelname,
                "time": datetime.datetime.now().strftime(self.dict_conf['datefmt_queue'])[:-3],
                "msg": msg
            }
            self.queue.save(data)
        except:
            print u'日志写入队列失败'


def get_logger(app, **kwargs):
    dict_config = DEFAULT_CONF
    dict_config['app'] = app
    dict_config.update(kwargs)
    logger = logging.getLogger(app)
    logger.setLevel(dict_config['level'])

    if dict_config['is_file']:
        # 日志文件名按时间自动更换
        filehandler = TimedRotatingFileHandler(dict_config['filepath'] + dict_config['filename_prefix'], dict_config['when'], dict_config['interval'], dict_config['backup_count'])
        # 日志后缀名
        filehandler.suffix = dict_config['filename_suffix']
        # 每行日志的前缀设置
        formatter = logging.Formatter(fmt= dict_config['format_file'], datefmt = dict_config['datefmt_file'])
        # 设置格式到日志对象
        filehandler.setFormatter(formatter)
        filehandler.setLevel(dict_config['level_file'])
        logger.addHandler(filehandler)

    # 开启输出到屏幕
    if dict_config['is_console']:
        console = logging.StreamHandler()
        console.setLevel(dict_config['level_console'])
        formatter_console = logging.Formatter(dict_config['format_console'])
        console.setFormatter(formatter_console)
        logger.addHandler(console)

    # 开启输出到屏幕
    if dict_config['is_queue']:
        try:
            qh = QueueHandler(**dict_config)
            formatter_queue = logging.Formatter(dict_config['format_queue'])
            qh.setFormatter(formatter_queue)
            qh.setLevel(dict_config['level_queue'])
            logger.addHandler(qh)
        except Exception as e:
            print u'启动kafka 出错：{}'.format(traceinfo(e))
    return logger


if __name__ == '__main__':
    log = get_logger("aa")
    log.error("aa")

    

