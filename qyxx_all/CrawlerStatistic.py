# -*- coding: utf-8 -*-
# Created by David on 2016/5/23.

import sys
from CommonLib.WebContent import SeedAccessReport, SeedAccessType
reload(sys)
sys.setdefaultencoding('utf-8')


class CrawlerStatic:
    """
    CrawlerStatic is used to statistic the crawler
    @version:1.0
    @author:david ding
    @modify:
    """

    def __init__(self, log):
        """
        Initiate the parameters.
        """
        self.log = log
        self.run_times = 0
        self.success_num = 0
        self.failed_num = 0
        self.failed_reasons = dict()
        self.retry_times = dict()

    def statistic(self, report, retry_times):
        """
        Statistic one report
        :param report:
        :param retry_times:
        :return:
        """
        self.run_times += 1
        if report.access_type == SeedAccessType.ERROR:
            self.failed_num += 1
            if report.access_type not in self.failed_reasons:
                self.failed_reasons[report.access_type] = 1
            else:
                self.failed_reasons[report.access_type] += 1
        else:
            self.success_num += 1
        if retry_times not in self.retry_times:
            self.retry_times[retry_times] = 1
        else:
            self.retry_times[retry_times] += 1

    def description(self):
        """
        Describe the report for output
        :return:
        """
        msg = "抓取统计报告：共抓取%s次，成功%s次，失败%s次，失败原因：" % (self.run_times, self.success_num, self.failed_num)
        for key in self.failed_reasons:
            msg += "[%s]=%s次，" % (SeedAccessType.description(key), self.failed_reasons[key])
        msg += "重试情况："
        for key in self.retry_times:
            msg += "[%s]=%s次，" % (key, self.retry_times[key])
        self.log.info(msg)

if __name__ == "__main__":
    pass
