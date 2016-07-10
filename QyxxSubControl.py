# -*- coding: utf-8 -*-
# Created by Leo on 16/04/20
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

from QyxxReqWorker import work
from ProcessControl import ProcessControl


class QyxxSubControl(ProcessControl):
    """
    Class for control the processes under different types
    """

    def __init__(self, log_name = "QyxxProcess", conf_file = "ItemConfig.ini", conf_key="qyxx"):
        super(QyxxSubControl, self).__init__(work, log_name = log_name, conf_file = conf_file, conf_key=conf_key)

if __name__ == "__main__":

    sub = QyxxSubControl()
    sub.run()