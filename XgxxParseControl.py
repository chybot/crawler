# -*- coding: utf-8 -*-
# Created by Leo on 16/04/20
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.append("Parser")
from ProcessControl import ProcessControl
# from QyxxParseWorker import work
from XgxxParseWorker import work
class XgxxParseControl(ProcessControl):
    """
    Class for control the processes under different types
    """

    def __init__(self, log_name =__name__, conf_file = "ParseItemConfig.ini", conf_key = "xgxx"):
        super(XgxxParseControl, self).__init__(work, log_name = log_name, conf_file = conf_file, conf_key = conf_key)


if __name__ == "__main__":

    sub = XgxxParseControl()
    sub.run()
    # print SeedAccessType.OK