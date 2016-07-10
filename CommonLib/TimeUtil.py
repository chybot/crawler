# -*- coding: utf-8 -*-
# Created by Leo on 16/05/04
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
import time


class TimeUtil(object):
    """
    Tool for get time with diff kinds of formats
    """
    @staticmethod
    def convert(_time, format=None):
        if format:
            # print time.strftime(format, time)
            return time.strftime(format, _time)
        else:
            return time.strftime(u"%Y-%m-%d %H:%M:%S", _time)

    @staticmethod
    def currentTime(format=None):
        """
        return current time with given format default is %Y-%m-%d %H:%M:%S
        :param format: case sentive
        :return:
        """
        return TimeUtil.convert(time.localtime(), format)

    @staticmethod
    def doTime():
        """
        return time with date format
        :return:
        """
        return time.strftime(u"%Y-%m-%d", time.localtime())

    @staticmethod
    def timeStamp():
        return time.time()

    @staticmethod
    def stampFromString(date_str, format):
        """
        create timestamp from given string and format
        :param format:
        :return:
        """
        return time.mktime(time.strptime(date_str, format))

    @staticmethod
    def convertDateFromat(date_str, fromFormat, toFormat):
        """
        convert the date string from one format to the other format
        :param date_str:
        :param fromFormat:
        :param toFormat:
        :return:
        """
        tm = TimeUtil.stampFromString(date_str, fromFormat)
        return TimeUtil.stamp2Date(int(tm), toFormat)

    @staticmethod
    def stamp2Date(stamp, format=None):
        """
        convert timestamp with given format
        :param stamp: timestamp
        :param format: convert format ,case sentive
        :return:
        """
        # deal with the too long stamp
        if isinstance(stamp, long):
            stamp_str = str(stamp)
            if len(stamp_str) > 10:
                stamp_str = stamp_str[:10]+'.'+stamp_str[10:]
                stamp = float(stamp_str)
        l_time = time.localtime(stamp)
        return TimeUtil.convert(l_time,format)


if __name__ == '__main__':
    print TimeUtil.currentTime("%Y%m%d")
    print TimeUtil.doTime()
    print TimeUtil.timeStamp()
    print TimeUtil.stamp2Date(time.time())
    print TimeUtil.stamp2Date(1370534400000)
    date_str = "May 10, 2016 4:39:50 PM"
    date_formated = TimeUtil.convertDateFromat(date_str, u"%b %d, %Y %H:%M:%S PM", u"%Y年%m月%d日")
    pass
