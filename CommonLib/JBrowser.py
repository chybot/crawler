# -*- coding: utf-8 -*-
__author__ = 'Lvv'

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from selenium import webdriver
import time


# 成功返回浏览器对象，否则一直重试
def get_browser(host, port, enablejs=True, timesleep=30):
    while True:
        try:
            driver = webdriver.Remote('http://%s:%s/wd/hub' % (host, str(port)), webdriver.DesiredCapabilities.HTMLUNITWITHJS if enablejs else webdriver.DesiredCapabilities.HTMLUNIT)
            print 'connect success'
            return driver
        except Exception as e:
            print 'ConnectError: %s' % str(e)
            time.sleep(timesleep)


# 成功返回网页原文，失败返回None
def get_page_source(browser, url, condition, encoding='utf-8', timewait=60):
    try:
        browser.get(url)
        browser.implicitly_wait(timewait)
        browser.find_element_by_xpath(condition)
        return browser.page_source.encode(encoding)
    except Exception as e:
        print 'GetPageSourceError: %s' % str(e)
        return None