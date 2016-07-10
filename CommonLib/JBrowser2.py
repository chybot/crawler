# -*- coding: utf-8 -*-
__author__ = 'Lvv'

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from splinter import Browser
import time


# 成功返回浏览器对象，否则一直重试
def get_browser(user_agent=None, load_images=False, desired_capabilities=None,
                wait_time=2, sleep_time=30, **kwargs):
    while True:
        try:
            browser = Browser('phantomjs', user_agent=user_agent, load_images=load_images,
                              desired_capabilities=desired_capabilities, wait_time=wait_time, **kwargs)
            print 'Get browser success'
            return browser
        except Exception as e:
            print 'Get browser error: %s' % str(e)
            time.sleep(sleep_time)


# 成功返回网页原文，失败返回None
def get_page_source(browser, url, xpath_condition, encoding='utf-8', wait_time=60):
    try:
        browser.visit(url)
        browser.is_element_present_by_xpath(xpath_condition, wait_time=wait_time)
        return browser.html.encode(encoding)
    except Exception as e:
        print 'GetPageSourceError: %s' % str(e)
        return None