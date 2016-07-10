# -*- coding: utf-8 -*-
import urllib
import time

# 甘肃第一步，请求验证码图片
domain = "http://xyjg.egs.gov.cn"
#pic_url = "http://xygs.gsaic.gov.cn/gsxygs/securitycode.jpg?v=" + str(int(time.time() * 1000))
pic_url='http://xygs.gsaic.gov.cn/gsxygs/securitycode.jpg'
pic_header = {
    "Host" : "xygs.gsaic.gov.cn",
    "User-Agent" : "Mozilla/5.0 (Windows NT 6.1; rv:40.0) Gecko/20100101 Firefox/40.0",
    "Accept" : "image/png,image/*;q=0.8,*/*;q=0.5",
    "Accept-Language" : "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
    "Accept-Encoding" : "gzip, deflate",
    "Referer" : "http://xygs.gsaic.gov.cn/gsxygs/main.jsp"
}

# 第二步_访问企业列表
post_yzm_url = "http://xygs.gsaic.gov.cn/gsxygs/pub!list.do"
post_yzm_header = {
                    "Host": "xygs.gsaic.gov.cn",
                    "Connection": "keep-alive",
                    "Cache-Control": "max-age=0",
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                    "Origin": "http://xygs.gsaic.gov.cn",
                    "Upgrade-Insecure-Requests": "1",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36",
                    "Content-Type": "application/x-www-form-urlencoded",
                    "Referer": "http://xygs.gsaic.gov.cn/gsxygs/pub!list.do",
                    "Accept-Encoding": "gzip, deflate",
                    "Accept-Language": "zh-CN,zh;q=0.8"
}

def post_yzm_data(yzm, company_key):
    data = {
        # "browse":"",
        # "loginName":urllib.quote(u"输入注册号/统一代码点击搜索".encode("utf-8")),
        # "cerNo":"",
        # "authCode":"",
        "authCodeQuery" :yzm,
        "queryVal" : company_key
    }
    return data


# 第三步_访问企业基本详情网页数据
company_url = 'http://xygs.gsaic.gov.cn/gsxygs/pub!view.do'
company_info_html_header = {
    "Host" : "xygs.gsaic.gov.cn",
    "User-Agent" : "Mozilla/5.0 (Windows NT 6.1; rv:40.0) Gecko/20100101 Firefox/40.0",
    "Accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language" : "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
    "Accept-Encoding" : "gzip, deflate",
    "Referer" : "http://xygs.gsaic.gov.cn/gsxygs/pub!list.do",
    "Content-Type": "application/x-www-form-urlencoded"
}
def post_company_data(id, entcate):
    data = {
        'regno': id,
        'entcate': entcate
    }
    return data

# 详情页面header
detail_header = {
    "Host" : "xygs.gsaic.gov.cn",
    "User-Agent" : "Mozilla/5.0 (Windows NT 6.1; rv:40.0) Gecko/20100101 Firefox/40.0",
    "Accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language" : "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
    "Accept-Encoding" : "gzip, deflate",
    "Referer" : "http://xygs.gsaic.gov.cn/gsxygs/pub!view.do"
}