# -*- coding: utf-8 -*-
"""
logging模块
"""

import sys
reload(sys)
sys.setdefaultencoding("utf-8")
sys.path.append("../")
import os

import logging
from logging.handlers import TimedRotatingFileHandler
from logging import Handler

from DB.DBManager import DBManager
from Singleton import Singleton
from Config.ConfigGet import ConfigGet

CRITICAL = 50
FATAL = CRITICAL
ERROR = 40
WARNING = 30
WARN = WARNING
INFO = 20
DEBUG = 10
NOTSET = 0

fmt = '%(asctime)s (%(process)d) [%(filename)s-%(module)s-%(funcName)s %(lineno)d] %(levelname)s: %(message)s'
#输出格式  时间 （进程号） [文件名-模块名-函数名-行号] 日志等级:日志

level_config = {
    'CRITICAL' : logging.CRITICAL,
    'ERROR' : logging.ERROR,
    'WARN' : logging.WARNING,
    'WARNING' : logging.WARNING,
    'INFO' : logging.INFO,
    'DEBUG' : logging.DEBUG,
    'NOTSET' : logging.NOTSET,
}


f = lambda x,y,z:ConfigGet(x).get(y,z)

path1 = 'Config.ini'
path2 = 'ConfigLog.ini'

config = {
    'debug':f(path1,'setting','debug').lower(),
    'logger_level' :f(path2,'level','logger_level').upper(),
    'file_level':f(path2,'level','file_level').upper(),
    'stream_level': f(path2,'level','stream_level').upper(),
    'db_level':f(path2,'level','db_level').upper(),
    'type':f(path2,'db','type').lower(),
    'host':f(path2,'db','host').lower(),
    'port':int(f(path2,'db','port'))
}
qyxx_dict = {
    "guangdong": u"广东",
    "hubei": u"湖北",
    "hunan": u"湖南",
    "henan": "河南",
    "heilongjiang": u"黑龙江",
    "hebei": u"湖北",
    "hainan": u"海南",
    "guizhou": u"贵州",
    "guangxi": u"广西",
    "fujian": u"福建",
    "chongqing": u"重庆",
    "beijing": u"北京",
    "anhui": u"安徽",
    "jiangsu": u"江苏",
    "gansu": u"甘肃",
    "xinjiang": u"新疆",
    "tianjin": u"天津",
    "sichuan": u"四川",
    "shanxixian": u"陕西",
    "shanxitaiyuan": u"山西",
    "shandong": u"山东",
    "shanghai": u"上海",
    "qinghai": u"青海",
    "ningxia": u"宁夏",
    "neimenggu": u"内蒙古",
    "liaoning": u"辽宁",
    "jilin": u"吉林",
    "jiangxi": u"江西",
    "xizang": u"西藏",
    "zhejiang": u"浙江",
    "yunnan": u"云南",
    "zongju": u"总局"
}

class Logging1(object):
    """
    logging日志类
    use eg:
    log = Logging(name = 'anhui,level = logging.INFO).getLogger
    log.info(u'安徽爬虫抓取开始')
    """
    __metaclass__ = Singleton

    def __init__(self,name =None, file_flag=None,db_flag=None, stream_flag=True ):
        assert name != None ,'name == None'
        self.name = name.lower()

        self.pid = os.getpid()
        if stream_flag:
            self.stream_flag = stream_flag
        else:
            self.stream_flag = None
        if file_flag:
            self.file_flag = file_flag
        else:
            self.file_flag = True if  f(path2,'save','file_flag').lower() == 'true' else False
        if db_flag:
            self.db_flag = db_flag
        else:
            self.db_flag =True if f(path2,'save','db_flag').lower() == 'true' else False
        self.logger = logging.getLogger(self.name)
        self.cf = config
        #初始化logger
        self.logger.setLevel(level_config[self.cf['logger_level']])
        #设置logger等级
        self.getLogger()
        self.logger.propagate = False

    def getLogger(self):
        if self.logger.handlers:
            return self.logger
        if self.stream_flag:
            sl = self.streamLogger()
            self.logger.addHandler(sl)
        # if self.cf['debug'] == 'true':
        #     return self.logger
        if self.file_flag  == True:
            fl = self.fileLogger()
            self.logger.addHandler(fl)
        if self.db_flag  == True:
            dl = self.DbLogger()
            self.logger.addHandler(dl)
        return self.logger

    def fileLogger(self):
        """
        日志输出到文件
        :return:
        """
        log_env = os.getenv('spider_log',default=None)
        if log_env:
            filename = os.path.join(log_env,self.name + '_' + str(self.pid))
        else:
            filename = self.name
        filehandler = TimedRotatingFileHandler(filename,'D',1,2)
        filehandler.suffix = '%Y-%m-%d.log'
        filehandler.setLevel(level_config[self.cf['file_level']])
        fmtr = logging.Formatter(fmt = fmt)
        filehandler.setFormatter(fmtr)
        return filehandler


    def streamLogger(self):
        """
        日志输出到屏幕
        :return:
        """

        sl = logging.StreamHandler()
        sl.setLevel(level_config[self.cf['stream_level']])
        fmtr = logging.Formatter(fmt=fmt)
        sl.setFormatter(fmtr)
        return sl


    def DbLogger(self):
        """
        日志输出到DB
        :return:
        """
        db = DbHandler(name = self.name)
        formatter_queue = logging.Formatter(fmt=fmt)
        db.setLevel(level_config[self.cf['db_level']])
        db.setFormatter(formatter_queue)
        return db

class DbHandler(Handler):
    """
    自建DBHandler
    """
    def __init__(self,**kwargs):
        Handler.__init__(self)
        name = kwargs['name'] if 'name' in kwargs else 'xgxx_log'
        if name in qyxx_dict:
            self.db_name = "qyxx_log"
        else:
            self.db_name = "xgxx_log"
        types ,queue,port ,host = config['type'],self.db_name,config['port'],config['host']
        try:
            self.__db = DBManager.getInstance(types,queue,host=host,port=port)
        except Exception as e1:
            pass

    def emit(self, record):
        """
        重写emit
        :param record:
        :return:
        """
        try:
            msg = self.format(record)
            self.__db.put(msg)
        except Exception:
            print u"日志写入存储DB队列失败"

class Logging2(Logging1):
    pass

def Logging(name = None,**kw):
    log = Logging1(name, **kw)
    return log.logger
def LogingMain(name = None,**kw):
    log = Logging2(name, **kw)
    return log.logger
if __name__ == '__main__':
    # log1 = Logging(name='test1')
    # print log1
    # log.getLogger.info('eg msg')
    # logger11 = logging.getLogger("11")
    # logger12 = logging.getLogger("12")
    log2 = Logging(name = 'test2',file_flag = True, stream_flag = False)
    print log2
    log2.info('adddress =%s ', str(log2))
    logger13 = logging.getLogger("13")
    log3 = LogingMain(name = 'test2', file_flag = True, stream_flag = False)
    print log3
    log3.info('adddress =%s ', str(log2))



