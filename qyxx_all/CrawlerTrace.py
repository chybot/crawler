# -*- coding: utf-8 -*-
# Created by David on 2016/4/28.

import sys
import time
from util.crawler_util import EventType
reload(sys)
sys.setdefaultencoding('utf-8')

class CrawlerModuleRunningInfo:
    """
    CrawlerModuleRunningInfo is used to store every runtime module's run status
    @version:1.0
    @author:david ding
    @modify:
    """
    def __init__(self, name, run_event_type=EventType.NORMAL, start_time=None, end_time=None):
        """
        Initiate the parameters.
        """
        self.name = name
        self.start_time = start_time if start_time else time.time()
        self.end_time = end_time if end_time else time.time()
        self.event_type = run_event_type

    def getRunningTime(self):
        return str(round(self.end_time-self.start_time,1))

class CrawlerTrace(object):
    """
    CrawlerTrace is used to trace the crawler module run status
    @version:1.0
    @author:david ding
    @modify:
    """
    def __init__(self):
        self.modules = []

    def trace(self, module=None,event_type=None, start_time=None, end_time=None, message=None):
        info = None
        if not module:
            if message:
                info = CrawlerModuleRunningInfo(message)
        else:
            info = CrawlerModuleRunningInfo(module.name, event_type, start_time, end_time)
        if info:
            self.modules.append(info)

    def description(self):
        if not self.modules or len(self.modules)<2:
            return "未获取到模块执行跟踪信息！"
        total_time = str(round(self.modules[-1].end_time-self.modules[0].start_time, 1))
        info = '本次抓取共运行了 %s 秒，模块详细执行链如下：\n' % total_time
        for running_info in self.modules:
            info += "["+running_info.name+"("
            info += EventType.description(running_info.event_type)
            info += ")(运行了"+running_info.getRunningTime()+"秒)]-->"
        return info.rstrip("-->")

if __name__ == "__main__":
    pass
