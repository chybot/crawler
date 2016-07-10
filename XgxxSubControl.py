# -*- coding: utf-8 -*-
# Created by Leo on 16/04/20
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

from XgxxReqWorker import work
from ProcessControl import ProcessControl


class XgxxSubControl(ProcessControl):
    """
    Class for control the processes under different types
    """

    def __init__(self, log_name = "XgxxProcess", conf_file = "XgxxItemConfig.ini", conf_key="xgxx"):
        super(XgxxSubControl, self).__init__(work,
                                             log_name = log_name,
                                             conf_file = conf_file,
                                             conf_key=conf_key,
                                             seed_key = "need_seed")

if __name__ == "__main__":

    sub = XgxxSubControl()
    sub.run()
