# -*- coding: utf-8 -*-
"""
读取配置文件类,配置文件为filename.ini
"""

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

import ConfigParser
import os
import warnings
import hashlib

class ConfigGet(object):
    """
    读取配置文件模块
    """
    def __init__(self,path):
        """
        :param path: 配置文件的路径str
        eg:
        cc = ConfigGet('../ProxyServer/ProxyConfig.ini')
        cc.set('db1','host11','web2800')
        """
        cwd = os.path.split(os.path.realpath(__file__))[0]
        self.path = os.path.join(cwd,path)
        self.cf = ConfigParser.ConfigParser()
        self.cf.read(self.path)

    def cfMd5(self):
        '''
        对配置文件进行MD5加密
        :return:
        '''
        with open(self.path,'rb') as f:
            return hashlib.md5(f.read()).hexdigest()

    def sections(self):
        """
        获取最配置最高级的section列表
        eg:[db]  [networklock]
        :return:LIST
        """
        return self.cf.sections()

    def itemsToDict(self,section,vars={}):
        '''
        获取某个section下的key value
        :param section:
        :param vars: update dict
        :return: dict
        '''
        return dict(self.cf.items(section,vars=vars))

    def options(self,section):
        """
        获取单个section下key的列表
        :param section:
        :return: LIST
        """
        return self.cf.options(section)

    def get(self, section, option, default = None):
        """
        获取某个section下option的值,如果section, option不存在，则添加，且默认值为default
        :param section:
        :param option:
        :param default:
        :return: str
        """
        if self.cf.has_option(section,option):
            value = self.cf.get(section, option)
            if value and ((value[0] == "[") and (value[-1] == "]")) or ((value[0] == "{") and (value[-1] == "}")):
                return eval(value)
            return int(value) if value.isdigit() else value

        elif default:
            self.set(section, option, default)
            return default

        else:
            warnings.warn('No section = %s or option = %s AND not default!'%(section,option))

    def has_option(self,section,option):
        """
        判断在section下是否存在option
        :param section:
        :param option:
        :return:
        """
        if not self.cf.has_section(section):
            warnings.warn('No section : %s' % section)
            return False
        if self.cf.has_option(section,option):
            return True
        warnings.warn('No option : %s' % option)
        return False

    def set(self,section, option, value):
        """
        修改某个section下option的值为value,如果section不存则添加
        :param section:
        :param option:
        :param value:
        :return:
        """
        if not  self.cf.has_section(section):
            self.cf.add_section(section)
        self.cf.set(section, option, value)
        self.cf.write(open(self.path, 'w'))
    def reload(self):
        self.cf = ConfigParser.ConfigParser()
        self.cf.read(self.path)
confGetterFunc = lambda x,y,z:ConfigGet(x).get(y,z)

if __name__ == '__main__':
    cc = ConfigGet('ConfigLog.ini')
    print cc.items('level')
