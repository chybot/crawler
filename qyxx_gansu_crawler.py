# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding("UTF-8")
import time
import re
import cookielib
from lxml import etree

sys.path.append("../")
from common import webutil
from common import timeutil
from common import charutils
from common import xpathutil
import qyxx_gansu_crawler_data as d
from qyxx.qyxx_crawler import qyxx_crawler # 导入父类
import json
import config
from HttpRequst.DownLoader import DownLoader
from Seed.Seed import Seed


#建立自己的类
class QyxxGanSu(qyxx_crawler):

    # 变更信息
    def __init__(self):
        """
        初始化爬虫抓取环境
        """
        self.req = DownLoader("QyxxGanSu")
        self.seed = Seed("gansu")

        self.keyword = u"合作市楚湘饭庄"
        self.method_list=[]

    def setKey(self,key_word):
        """
        设置关键字，用于搜索
        :param key_word: unicode 格式
        :return:
        """
        self.keyword = key_word
    def getYzm(self):
        """
        获取验证码
        :return:
        """
        self.req.firstInit()
        # self.logging.info(u"")
        self.response = self.req.get(d.pic_url,headers = d.pic_header)
        print self.response
    def parseYzm(self):
        """
        解析验证码， 甘肃验证码在cookie内部
        :return:
        """
        key = "session_authcode"
        for cookie in self.response.cookies:
            if cookie.name == key:
                self.yzm = cookie.value
                break
    def getList(self):
        """
        获取搜索列表，利用关键字，模拟搜索，得到网页返回的搜索列表
        :return:
        """
        self.seed.get()
        self.response = self.req.post(d.post_yzm_url, headers = d.post_yzm_header, data = d.post_yzm_data(self.yzm, self.keyword))
        print self.response
    def parseList(self):
        """
        解析搜索列表，分析每一个公司的连接和信息
        :return:
        """
        tree = etree.HTML(self.response.text)
        element_list = tree.xpath('.//div[@class="list"]')
        # map(element_list)
        self.company_list=[]

        for item in element_list:
             # 获取列表页公司名
            company_dict = {}
            try:
                company_list_name = item.xpath('.//a/text()')[0].strip()
                company_dict.update({"company_name":company_list_name})
            except Exception as e:
                company_list_name = ''
                self.logging.error(u'获取列表页公司名异常：%s' % str(e))
            # 获取id和entcate
            try:
                company_id = item.xpath('.//a/@id')[0].strip()
                company_dict.update({"company_id":company_id})
            except:
                self.logging.error(u'获取company_id异常！')
            try:
                entcate = item.xpath('.//a/@ _entcate')[0].strip()
                company_dict.update({"entcate":entcate})
            except:
                self.logging.error(u'获取entcate异常！')

            self.company_list.append(company_dict)
    def getEveryDetail(self):
        for company_info in self.company_list:
            self.req_dict = company_info
            self.crawlerUrl()

    def crawlerUrl(self):
        self.getBasicInfo()

        pass
    def getBasicInfo(self):
        company_id = self.req_dict["company_id"]
        entcate = self.req_dict["entcate"]
        self.response = self.req.post(d.company_url, data=d.post_company_data(company_id, entcate),
                                                        headers = d.company_info_html_header)
    def getGdxx(self):
        pass
    def getBgxx(self):
        pass
    def getBaxx(self):
        pass

if __name__ == "__main__":
    qg = QyxxGanSu()
    qg.getYzm()
    qg.parseYzm()
    qg.getList()
    qg.parseList()
    qg.getEveryDetail()
