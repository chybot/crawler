# -*- coding: utf-8 -*-
# Created by Leo on 16/05/12
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
from Singleton import Singleton
class  SingleLog:
    __metaclass__ = Singleton
    def __init__(self,type):
        self.type=type
        print type
if __name__ == '__main__':
    inst = SingleLog.getInstance("bj")
    print inst
    inst2 = SingleLog.getInstance("bj")
    print inst2
    inst3 = SingleLog.getInstance()
    print inst3