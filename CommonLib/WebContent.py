# -*- coding: utf-8 -*-
# Created by David on 2016/5/12.

import sys
import md5util
from BbdSeedLogApi import STATE
reload(sys)
sys.setdefaultencoding('utf-8')


class WebContentType(object):
    """
    WebContentType is used for enumerate the type of web content
    """
    HTML = 0
    JSON = 1


class WebAccessType(object):
    """
    WebAccessType is used to mark the status of one crawl
    """
    OK = 0                      # 访问正常
    TOO_OFTEN = 1               # 访问过于频繁
    EXCEPTION = 2               # 访问时发生了异常，例如timeout
    NO_CONTENT = 3              # 返回了页面，但无可用数据
    ACCESS_VIOLATION = 4        # 非法访问，常见于ua或cookies验证失败的情况
    VALIDATE_FAILED = 5         # 验证码验证失败
    NOT_EXPECTED_STRUCTURE = 6  # 返回的结构不是预期的结构
    STAMP_OUT_OF_TIME = 7       # 时间戳超时，例如广东需携带时间戳访问

    @staticmethod
    def description(status):
        '''
        将对应种子类型翻译为文字，便于log输出
        :param status: 事件类型
        :return: 事件类型的文字描述
        '''
        if status == WebAccessType.OK:
            return "OK"
        if status == WebAccessType.TOO_OFTEN:
            return "TOO_OFTEN"
        if status == WebAccessType.EXCEPTION:
            return "EXCEPTION"
        if status == WebAccessType.NO_CONTENT:
            return "NO_CONTENT"
        if status == WebAccessType.ACCESS_VIOLATION:
            return "ACCESS_VIOLATION"
        if status == WebAccessType.VALIDATE_FAILED:
            return "VALIDATE_FAILED"
        if status == WebAccessType.NOT_EXPECTED_STRUCTURE:
            return "NOT_EXPECTED_STRUCTURE"
        if status == WebAccessType.STAMP_OUT_OF_TIME:
            return "STAMP_OUT_OF_TIME"
        return "未识别的Web访问类型！！！！！"


class CompanyAccessType(object):
    """
    used for mark the crawl status of one company
    """
    OK = 0                      # 公司所有页面均抓取正常
    INCOMPLETE = 1              # 页面抓取不完整，部分页面正常，部分页面失败
    ERROR = 2                   # 未正确抓取到任何页面


class SeedAccessType(object):
    """
    used for mark the crawl status of one seed
    """
    OK = STATE.BBD_SEED_IS_CRAWL_SUC                      # 种子下搜索出的所有公司均抓取正常
    INCOMPLETE = STATE.BBD_SEED_IS_CRAWL_PAR              # 种子下搜索出的部分公司抓取正常
    NON_COMPANY = STATE.BBD_SEED_IS_CRAWL_VOI             # 种子下未搜索出任何公司
    ERROR = STATE.BBD_SEED_IS_CRAWL_ERO                   # 种子下搜索出的所有公司均抓取不正常
    NO_VALID_COMPANY = STATE.BBD_SEED_IS_CRAWL_REV        # 种子搜索到了公司，但公司已注销，无url，无法进一步抓取信息
    NO_TARGET_SOURCE = 888888                              # 种子搜索到了公司，但未命中目标数据源，例如广东不抓取深圳信用网

    @staticmethod
    def description(status):
        '''
        将对应种子类型翻译为文字，便于log输出
        :param status: 事件类型
        :return: 事件类型的文字描述
        '''
        if status == SeedAccessType.OK:
            return "OK"
        if status == SeedAccessType.INCOMPLETE:
            return "INCOMPLETE"
        if status == SeedAccessType.NON_COMPANY:
            return "NON_COMPANY"
        if status == SeedAccessType.ERROR:
            return "ERROR"
        if status == SeedAccessType.NO_VALID_COMPANY:
            return "NO_VALID_COMPANY"
        if status == SeedAccessType.NO_TARGET_SOURCE:
            return "NO_TARGET_SOURCE"
        return "未识别的种子返回类型！！！！！"


class SeedAccessReport(object):
    """
    used to report the crawl detail info of one seed
    """
    def __init__(self, success_num, failed_num, access_type=None):
        self.success_num = success_num          # 成功抓取到的公司数
        self.failed_num = failed_num            # 抓取失败的公司数
        self.access_type = access_type          # 种子抓取类型


class WebContent(object):
    """
    WebContent is used for wrap the content which is downloaded from the web
    @version:1.0
    @author:david ding
    @modify:
    """
    def __init__(self, **kwargs):
        self.url = kwargs['url'] if 'url' in kwargs else None
        self.headers = kwargs['headers'] if 'headers' in kwargs else None
        self.method = kwargs['method'] if 'method' in kwargs else u'get'
        self.data = kwargs['data'] if 'data' in kwargs else None
        self.encoding = kwargs['encoding'] if 'encoding' in kwargs else None
        self._body = kwargs['body'] if 'body' in kwargs else None
        self.content_type = kwargs['content_type'] if 'content_type' in kwargs else WebContentType.HTML
        self.access_type = kwargs['access_type'] if 'access_type' in kwargs else WebAccessType.OK
        self.status_code = kwargs['status_code'] if 'status_code' in kwargs else None
        self.reason = kwargs['reason'] if 'reason' in kwargs else None
        self.time_out = kwargs['time_out'] if 'time_out' in kwargs else False
        self.elapsed = kwargs['elapsed'] if 'elapsed' in kwargs else None
        self.req_md5 = md5util.getMd5WithDict(kwargs)
        self.body_md5 = md5util.getMd5WithDict(self.body) if self.body else None

    @property
    def body(self):
        return self._body

    @body.setter
    def body(self, value):
        self._body = value
        self.body_md5 = md5util.getMd5WithDict(self.body) if self.body else None

    def toDictionary(self):
        return self.__dict__

    @staticmethod
    def getInstanceFromDictionary(attr_dict):
        if not attr_dict or not isinstance(attr_dict, dict):
            return None
        if '_body' not in attr_dict or 'time_out' not in attr_dict or 'status_code' not in attr_dict:
            return None
        cont = WebContent()
        for k,v in attr_dict.items():
            if k in cont.__dict__:
                cont.__dict__[k] = v
        return cont