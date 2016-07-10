# -*- coding: utf-8 -*-
__author__ = 'Lvv'

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time


# 成功返回浏览器对象，否则一直重试
def get_browser(executable_path='phantomjs',
                service_args=None, port=0,
                desired_capabilities=DesiredCapabilities.PHANTOMJS,
                service_log_path=None, sleep_time=30):
    while True:
        try:
            browser = webdriver.PhantomJS(executable_path=executable_path, port=port,
                                          service_log_path=service_log_path,
                                          desired_capabilities=desired_capabilities,
                                          service_args=service_args)
            print 'Get browser success'
            return browser
        except Exception as e:
            print 'Get browser error: %s' % str(e)
            time.sleep(sleep_time)


# 成功返回网页原文，失败返回None
def get_page_source(browser, url, condition, encoding='utf-8', wait_time=60):
    try:
        browser.get(url)
        browser.implicitly_wait(wait_time)
        try:
            browser.find_element_by_xpath(condition)
        except Exception as e:
            print 'find_element_by_xpath() Error: %s' % str(e)
        return browser.page_source.encode(encoding)
    except Exception as e:
        print 'GetPageSourceError: %s' % str(e)
        return None