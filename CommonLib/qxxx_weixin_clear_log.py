# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding("UTF-8")
import re
import os
import time
sys.path.append("../")
from common import exceputil
root="D:\python_test"
nowtime=time.time()
def clear_log(root):
    for i in os.listdir(root):
        if re.match(r"qyxx_weixin",i):
            isfile=os.path.join(root,i)
            if os.path.isfile(isfile):
                if re.search(r"qyxx.*?log",i):
                   file_change_time=os.path.getmtime(isfile)
                   if nowtime-file_change_time>3*24*3600:
                       #os.remove(isfile)
                       print isfile
            else:
                try:
                    clear_log(isfile)
                except Exception as e:
                    exceputil.traceinfo(e)
if __name__=="__main__":
    clear_log(root)