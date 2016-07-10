# -*- coding: utf-8 -*-
"""
Created by shuaiguangying on 15-10-31
"""
__author__ = 'shuaiguangying'

import sys

reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.append("../")
sys.path.append("../../")

"""
约定的队列传输数据标准, 防止字段出错。
1 内部使用key一律以"_"开头
2 外部使用的key一律不能以"_"开头

"""
import json
import time


class QueueData:

    def __init__(self, state):
        self.__qd = dict()
        self.__state = state

    def state(self):
        return self.__state

    @staticmethod
    def to_queue_data(qstr):
        kws = json.loads(qstr)
        qdata = QueueData(kws['_state'])
        qdata.update(**kws)
        del qdata['_state']
        return qdata

    def __delitem__(self, key):
        del self.__qd[key]

    def update(self, **kws):
        self.__qd.update(**kws)
        return self

    def add_url(self, url):
        self.__qd['_url_%s' % self.__state] = url
        return self

    def pop_html(self):
        key = '_html_%s' % self.__state
        return self.__qd.pop(key, None)

    def url(self):
        return self.__qd['_url_%s' % self.__state]

    def add_html(self, html):
        self.__qd['_html_%s' % self.__state] = html
        return self

    def html(self):
        key = '_html_%s' % self.__state
        return key in self.__qd and self.__qd[key]

    def add_id_uptime(self, unique_key):
        self.__qd['_id'] = unique_key + '|_|' + time.strftime('%Y-%m-%d', time.localtime(float(time.time())))
        self.__qd['_uptime'] = time.time()
        return self

    def to_state(self, state):
        return QueueData(state).update(**self.__qd)

    def __getitem__(self, item):
        return self.__qd[item]
    
    def __setitem__(self, key, value):
        self.__qd[key] = value

    def data(self):
        return self.__qd

    def __str__(self):
        self.__qd['_state'] = self.__state
        return json.dumps(self.__qd, ensure_ascii=False)


if __name__ == '__main__':
    qdata = QueueData('list').copy('detail')
    print qdata


