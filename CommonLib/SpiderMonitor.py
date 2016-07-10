# -*- coding: utf-8 -*-
__author__ = 'Lvv'

import os
import sys
import threading
import time
import requests
import json


g_threadLock = threading.Lock()


class SpiderMonitor(threading.Thread):
    def __init__(self, project, seconds=60):
        threading.Thread.__init__(self)
        # Project Name
        self.__project = project
        # Time interval
        self.__seconds = seconds
        # Counter
        self.__count = 0
        # Start mark
        self.__flag = False

    def run(self):
        self.__monitor()

    def __monitor(self):
        if self.__flag:
            self.__send()
        else:
            self.__flag = True
        threading.Timer(self.__seconds, self.__monitor).start()

    def __send(self):
        post_data = self.__make_post_data()
        print post_data
        try:
            req = requests.post('http://monitor.bbdservice.bbd', data=json.dumps(post_data), timeout=10.0)
            print req.status_code
            if req.status_code != 200:
                raise Exception('failure to submit data')
        except Exception as e:
            print str(e)


    def __make_post_data(self):
        dirname, filename = os.path.split(os.path.abspath(sys.argv[0]))
        return [
            {
                'headers': {
                    'spiderProject': self.__project.encode('utf-8') if \
                                     isinstance(self.__project, unicode) else self.__project,
                    'timestamp': int(time.time() * 1000)
                },
                'body': {
                    'spiderProcessId': os.getpid(),
                    'spiderProcessName': filename,
                    'spiderPath': dirname,
                    'crawlingAmount': self.add(isIncr=False)
                }
            }
        ]

    def add(self, isIncr=True):
        g_threadLock.acquire()
        count = self.__count
        if isIncr:
            self.__count += 1
        else:
            self.__count = 0
        g_threadLock.release()
        return count


if __name__ == '__main__':
    sm = SpiderMonitor(u'旅游局', seconds=5)
    sm.start()

    while True:
        sm.add()
        time.sleep(1)


