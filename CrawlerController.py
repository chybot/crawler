# -*- coding: utf-8 -*-
# Created by leo on 2016/04/19
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
# sys.path.append("../")
import logging
from CommandParameter import CommandParameter
from CommonLib.ClassFactory import ClassFactory
from CommonLib.Logging import Logging
class CrawlerController(object):
    """
    class for control different type of subcontrol
    such as qyxx, xgxx
    paramater is the outer input
    get subcontrol instance dynamically
    """
    def __init__(self,paras):
        """
        init property use the para instance
        :param paras:
        :return:
        """
        self.subcontrol = paras.getProperty("subcontrol")
        self.inst_name = paras.getProperty("inst_name")
        self.process_num = paras.getProperty("process_num")

        self.logger = Logging("qyxx_process_info", stream_flag = False)
        self.logger.info("logger address")
    def loadSubControl(self):
        sub_ctrl_inst = ClassFactory.getClassInst(self.subcontrol)
        return sub_ctrl_inst


def parseCommands(argv):
    '''
    Change the commandline to CMDParameter instance.
    @param:args str the command line from other process.
    subcontrol is the type of subcontrol ,such as qyxx, xgxx, tb
    inst_name is the province name
    process_num is process num which for
    '''

    paras = CommandParameter()
    subcontrol = None
    inst_name = None
    process_num = None
    if len(argv) == 1:
        subcontrol = "QyxxSubControl"
    elif len(argv) == 2:
        subcontrol = argv[1]
    elif len(argv) == 4:
        subcontrol = argv[1]
        inst_name = argv[2]
        process_num = argv[3]
    else:
        logging.warning("Too much parameters, please check.")
    if subcontrol:
        paras.setProperty("subcontrol",subcontrol)
    if inst_name:
        paras.setProperty("inst_name", inst_name)
    if process_num:
        paras.setProperty("process_num", process_num)
    return paras;
# end def parseCommands(args):
if __name__ == "__main__":
    para = parseCommands(sys.argv)
    control = CrawlerController(para)
    sub_control = control.loadSubControl()
    sub_control.run()