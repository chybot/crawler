# -*- coding: utf-8 -*-
# Created by dingminghui on 2016/04/19
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
# sys.path.append("../")
class TCall(object):
    def getName(self):
        print "getNmae"
    name="test"

if __name__ == "__main__":
    ss="name"
    method_name ="Name"
    c=TCall()
    if hasattr(c,"get"+method_name):
        method = getattr(c,"get"+method_name)
        method()
        print c.getName
        print method