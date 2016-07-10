# -*- coding: utf-8 -*-
# Created by David on 2016/4/18.

import sys
reload(sys)
sys.path.append("../")
sys.setdefaultencoding('utf-8')
import os
import time
import random
from CommonLib import exceptutil
from CommonLib.WebContent import WebContent,WebAccessType
from HttpRequst.DownLoader import DownLoaderException


class CrawlerRunMode(object):
    '''
    爬虫运行模式：通过哪种方式抓取
    '''
    COMPANY_KEY = 0
    COMPANY_URL = 1
    COMPANY_ADAPTER = 2


class InputType(object):
    '''
    模块输入类型，用作枚举
    '''
    URL = 0
    UA = 1
    HEADERS = 2
    FUNCTION = 3
    POST_DATA = 4
    METHOD = 5
    ENCODING = 6
    MAP_CONFIG = 7
    COOKIE = 8
    WEB_CONTENT = 9
    STATUS_CODE = 10


class OutputType(object):
    '''
    模块输出类型，枚举
    '''
    UA = 0
    FUNCTION = 1
    LIST = 2
    NONE_TYPE = 3   # 用于区分None，表示该输出有值，仅在某些情况为空，便于判断处理，例如深圳信用网gdxx的url


class OutputParameterShowUpType(object):
    '''
    指示某个输出结果是否必须出现
    '''
    OPTIONAL = 0
    MUST = 1


class EventType(object):
    '''
    事件类型，表示模块执行情况
    '''
    EXCEPTION_OCCURED = 0
    OUTPUT_NOT_SATISFIED = 1
    NORMAL = 2
    COMPLETED = 3
    FAILED = 4
    DO_NOTHING = 5
    ASSERT_FAILED = 6
    WEB_CONTENT_FAILED = 7          # 获取web内容失败

    @staticmethod
    def description(status):
        '''
        将对应事件类型翻译为文字，便于log输出
        :param status: 事件类型
        :return: 事件类型的文字描述
        '''
        if status == EventType.EXCEPTION_OCCURED:
            return 'ExceptionOccured'
        if status == EventType.OUTPUT_NOT_SATISFIED:
            return 'OutputNotSatisfied'
        if status == EventType.NORMAL:
            return 'Normal'
        if status == EventType.COMPLETED:
            return 'Completed'
        if status == EventType.FAILED:
            return 'Failed'
        if status == EventType.DO_NOTHING:
            return 'DoNothing'
        if status == EventType.ASSERT_FAILED:
            return 'AssertFailed'
        if status == EventType.WEB_CONTENT_FAILED:
            return 'WebContentFailed'
        return '未知事件状态！！！！！！！'


class RetryFailedStrategy(object):
    '''
    重试失败时的策略
    '''
    EXIT = -1
    IGNORE = 0

def getConfigValueByFile(input_list, input_type):
    if not input_list:
        return None
    value = None
    for input_dict in input_list:
        if 'type' in input_dict and input_dict['type'] == input_type:
            if 'path' in input_dict and 'value' in input_dict:
                path, name = os.path.split(input_dict['path'])
                sys.path.append(path)
                exec 'from ' + name + " import " + input_dict['value']
                return eval(input_dict['value'])
    return value

def moduleSleep(module, holder):
    '''
    睡眠模块
    :param module:需要休眠的模块
    :return:
    '''
    if not module.sleep or module.sleep.seconds <= 0:
        return
    seconds = module.sleep.seconds
    holder.logging.info("休眠%s秒" % seconds)
    time.sleep(int(seconds))


def request(downloader, **kwargs):
    """
    为获取网络内容封装HttpReque.Downloader
    :param downloader: 下载器
    :param url:
    :param headers:
    :param method:
    :param data:
    :param encoding:
    :param ua:
    :param is_pic: 是否获取图片内容
    :param use_proxy: 是否使用代理
    :param holder: 代持非业务对象
    :return:
    """
    start_time = time.time()
    url = kwargs.get('url', None)
    headers = kwargs.get('headers', None)
    method = kwargs.get('method', None)
    data = kwargs.get('data', None)
    encoding = kwargs.get('encoding', None)
    ua = kwargs.get('ua', None)
    is_pic = kwargs.get('is_pic', None)
    use_proxy = kwargs.get('use_proxy', None)
    holder = kwargs.get('holder', None)
    accept_code = kwargs.get('accept_code', None)

    web = WebContent(url=url, headers=headers, method=method, data=data, encoding=encoding, use_proxy=use_proxy)
    try:
        #设置User-Agent
        if ua and len(ua) > 0:
            if not headers:
                headers = dict()
            if "User-Agent" not in headers:
                headers["User-Agent"] = ua
        if accept_code:
            downloader.setNotRaise(accept_code)
        if holder: holder.logging.info(u"开始调用download获取页面内容")
        response = downloader.request(url=url, headers=headers, method=method, data=data, use_proxy=use_proxy)
        if holder: holder.logging.info(u"通过download获取页面内容结束")
        if is_pic:
            web.body = response.content
        elif encoding:
            response.encoding = encoding
            web.body = response.content
        else:
            web.body = response.text
        web.status_code = response.status_code
        # 若出错，记录原因
        web.reason = response.reason
        # 记录耗时
        web.elapsed = response.elapsed.microseconds/1000/1000
        return web
    except DownLoaderException as e:
        holder.logging.error(exceptutil.traceinfo(e))
        # 添加web状态及是否超时
        if e.res:
            web.status_code = e.res.status_code
            web.reason = e.res.reason
            web.elapsed = e.res.elapsed.microseconds/1000/1000
        elif '403' in e.exception:
            web.status_code = 403
        else:
            web.status_code = 800
        web.time_out = e.time_out
        web.access_type = WebAccessType.EXCEPTION
        if not web.elapsed:
            web.elapsed = time.time()-start_time
        return web


#user-agent集合
USER_AGENT_LIST=[
    u"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 2.0.50727)",
    u"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET4.0E; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET4.0C)",
    u"Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.2; Trident/4.0; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET4.0E; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET4.0C)",
    u"Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
    u"Mozilla/5.0 (Windows NT 5.1; rv:5.0) Gecko/20100101 Firefox/5.0",
    u"Mozilla/5.0 (Windows NT 5.2) AppleWebKit/534.30 (KHTML, like Gecko) Chrome/12.0.742.122 Safari/534.300",
    u"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1)",
    u"Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.04506.648; .NET CLR 3.5.21022; .NET4.0E; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET4.0C)",
    u"Opera/9.80 (Windows NT 5.1; U; zh-cn) Presto/2.9.168 Version/11.50",
    u"Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/533.21.1 (KHTML, like Gecko) Version/5.0.5 Safari/533.21.1",
    u"Mozilla/5.0 (Windows; U; Windows NT 5.1; ) AppleWebKit/534.12 (KHTML, like Gecko) Maxthon/3.0 Safari/534.12",
    u"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)",
    u"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)"
]

def get_user_agent():
    """
    在USER_AGENT_LIST列表随机选取一个Uset-Agent
    :return: (unicode) User_Agent
    """
    return random.choice(USER_AGENT_LIST).strip()