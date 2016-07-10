# -*- coding: utf-8 -*-
# Created by Leo on 16/05/12
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


import test_single2
import test_single3
if __name__ == '__main__':
    inst1 =  test_single2.getInst()
    print inst1
    inst2 =  test_single3.getInst3()
    print inst2