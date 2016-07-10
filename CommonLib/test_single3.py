# -*- coding: utf-8 -*-
# Created by Leo on 16/05/12
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
from SingleLog import SingleLog
def getInst3():
    inst = SingleLog.getInstance()
    return inst
if __name__ == '__main__':
    print getInst3()