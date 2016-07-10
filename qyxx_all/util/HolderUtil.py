# -*- coding: utf-8 -*-
# Created by David on 2016/4/18.

import sys
from Config.ConfigGet import ConfigGet
import crawler_util as cu
from CommonLib.Logging import Logging
reload(sys)


class HolderUtil(object):
    """
    util class, used for hold non-business objects for crawler
    """
    def __init__(self, pinyin, version=None):
        self.pinyin = pinyin
        self.ua = cu.get_user_agent()
        self.version = version
        self.logging = Logging(name=pinyin)
        self.recChar = None
        self.yzm_count = 0
        cg = ConfigGet('Config.ini')
        opt = cg.get("setting", "debug", "false")
        self.debug = 1 if opt.lower() == "true" else 0
        pass

    def init(self):
        """
        清理需每次清理的变量
        :return:
        """
        self.ua = cu.get_user_agent()

if __name__ == "__main__":
    holder = HolderUtil('beijing')
    log3 = holder.logging
    pass