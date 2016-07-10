# -*- coding: utf-8 -*-
# Created on 2014/10/22 16:59.
from logging.handlers import TimedRotatingFileHandler

import re
import socket
import random
import time
import  logging
from StringIO import StringIO
import gzip
import smtplib
import os
from email.mime.text import MIMEText

def trip(src):
    src = str(src)
    src = src.lstrip()
    src = src.rstrip( )
    src = src.strip( )
    return src;

def get_str(src_str = "", start = "^", end = "$"):
    match = re.findall(r"%s(.*?)%s"%(start, end), src_str, re.DOTALL)
    if len(match) >= 1:
        return match[0]
    else:
        return None

_dnscache={}
def use_dns_cache():
    """
    Makes a cached version of socket._getaddrinfo to avoid subsequent DNS requests.
    """
    def _getaddrinfo(*args, **kwargs):
        global _dnscache
        if args in _dnscache:
            #print str(args)+" in cache"
            return _dnscache[args]
        else:
            #print str(args)+" not in cache"
            _dnscache[args] = socket._getaddrinfo(*args, **kwargs)
            return _dnscache[args]
    if not hasattr(socket, '_getaddrinfo'):
        socket._getaddrinfo = socket.getaddrinfo
        socket.getaddrinfo = _getaddrinfo

# def get_logger(filename):
#     #引入日志模块
#     import logging
#     logging.basicConfig(level=logging.DEBUG,
#                     format='%(asctime)s %(filename)s [line:%(lineno)d] %(levelname)s %(message)s',
#                     datefmt='%a,%Y-%m-%d %H:%M:%S',
#                     #filename='%s.log'%"".join(sys.argv[0].split(".")[:-1]),
#                     filename='%s'%str(filename).decode("utf-8").encode("gb18030"),
#                     filemode='a')
#     #################################################################################################
#     #定义一个StreamHandler，将INFO级别或更高的日志信息打印到标准错误，并将其添加到当前的日志处理对象#
#     console = logging.StreamHandler()
#     console.setLevel(logging.INFO)
#     formatter = logging.Formatter('%(name)s:%(levelname)-7s %(message)s')
#     console.setFormatter(formatter)
#     logging.getLogger('').addHandler(console)
#     #################################################################################################
#     return logging

def get_logger(filename,level=logging.INFO):
    """
    获取日志对象，当日的日志存在filename里面，以前的日志存在filename.%Y-%m-%d.log 文件里面
    暂时不支持删除旧文件
    :param filename: (str) 文件名
    :return:  log日志对象
    """
    #如果filename有后缀名则删除
    pid=os.getpid()
    if filename.endswith(".log"):
        filename=filename[0:-4]
    pid=os.getpid()
    filenames=os.path.split(filename)
    filename=filename.replace(filenames[-1],str(pid)+"_"+filenames[-1])
    filename=os.path.join(os.getenv('spider_log',default='./'),filename)

    logger1 = logging.getLogger()
    logger1.setLevel(level)

    # fh = logging.FileHandler(filename.decode("utf-8").encode("gb18030"))
    fh = TimedRotatingFileHandler(filename, "D", 1,2)


    fh.suffix = "%Y-%m-%d.log"  #设置 切分后日志文件名的时间格式 默认 filename+"." + suffix 如果需要更改需要改logging 源码

    formatter = logging.Formatter(fmt="%(asctime)s %(filename)s [line:%(lineno)d] %(levelname)s %(message)s'",datefmt='%a,%Y-%m-%d %H:%M:%S')
    fh.setFormatter(formatter)
    logger1.addHandler(fh)

    console = logging.StreamHandler()
    #console.setLevel(logging.ERROR)
    console.setLevel(level)
    formatter = logging.Formatter('%(name)s:%(levelname)-7s %(message)s')
    console.setFormatter(formatter)
    logger1.addHandler(console)

    return logger1


def choice_proxy(proxy_list, proxy_shot_time, proxy_shot_time_elapse):
    #随机选取一个代理
    proxy = random.choice(list(proxy_list))
    while True:
        now_time = time.time()
        if proxy not in proxy_shot_time:
            proxy_shot_time[proxy] = (0.0, 1)
        elif now_time - proxy_shot_time[proxy][0] < proxy_shot_time_elapse:
            print u"随机选取的代理 %s 访问间隔小于%f秒 last:%f now:%f diff:%f"%(proxy, proxy_shot_time_elapse, proxy_shot_time[proxy][0], now_time, now_time-proxy_shot_time[proxy][0])
            time.sleep(0.1)
            proxy = random.choice(proxy_list)
            continue;
        else:
            proxy_shot_time[proxy] = (now_time, int(proxy_shot_time[proxy][1]+1))
            break;
    return proxy

def get_urllib2_response_html_src(response):
    """
    如果是gzip编码的网页就进行解码，返回源文
    """
    if response.info().get('Content-Encoding') == 'gzip':
        print "Content-Encoding gzip"
        buf = StringIO( response.read())
        f = gzip.GzipFile(fileobj=buf)
        html_src = f.read()
    else:
        html_src = response.read()
    return html_src


mail_user="monitor@brandbigdata.com"
mail_host = "smtp.ym.163.com"
mail_pass = "brandbigdata"
mailto_list_ourselves = ("hehongjing@brandbigdata.com", "wangzhenyu@brandbigdata.com", "fumenglin@brandbigdata.com", "wangyao@brandbigdata.com", "lvsijun@brandbigdata.com", "shuaiguangying@brandbigdata.com", "guomao@brandbigdata.com", "duchengfei@brandbigdata.com", "wudewen@brandbigdata.com")

def send_mail_old(to_list, sub, content):
    """
    发送邮件
    :param to_list: 收件人
    :param sub: 主题
    :param content: 邮件内容
    :return:
    """
    # 这里的hello可以任意设置，收到信后，将按照设置显示
    me = "server"+"<"+mail_user+">"
    # 创建一个实例，这里设置为html格式邮件
    msg = MIMEText(content, _subtype='html', _charset='utf-8')
    # 设置主题
    msg['Subject'] = sub
    msg['From'] = me
    msg['To'] = ";".join(to_list)
    try:
        s = smtplib.SMTP()
        # 连接smtp服务器
        s.connect(mail_host)
        # 登陆服务器
        s.login(mail_user, mail_pass)
        # 发送邮件
        s.sendmail(me, to_list, msg.as_string())
        s.close()
        return "Sent successfully!"
    except Exception as e:
        print str(e)





def test():
    logging=get_logger("d:/test")
    for j in range(3):
        logging.info("123")

from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText

# python 2.3.*: email.Utils email.Encoders
from email.utils import COMMASPACE,formatdate
from email import encoders
#server['name'], server['user'], server['passwd']
def send_mail(server, fro, to, subject, text, files=[]):
    assert type(server) == dict
    assert type(to) == list
    assert type(files) == list

    msg = MIMEMultipart()
    msg['From'] = fro
    msg['Subject'] = subject
    msg['To'] = COMMASPACE.join(to) #COMMASPACE==', '
    msg['Date'] = formatdate(localtime=True)
    msg.attach(MIMEText(text))

    for file in files:
        part = MIMEBase('application', 'octet-stream') #'octet-stream': binary data
        part.set_payload(open(file, 'rb').read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(file))
        msg.attach(part)

    import smtplib
    smtp = smtplib.SMTP(server['name'], '25')
    smtp.login(server['user'], server['passwd'])
    smtp.sendmail(fro, to, msg.as_string())
    smtp.close()

def send_mail_to_someone(subject="",text="",files=[],to=[]):
    server = {}
    server['name'] = "smtp.ym.163.com"
    server['user'] = "hehongjing@brandbigdata.com"
    server['passwd'] = "qpzm1234"
    mail_postfix="brandbigdata.com"
    fro = server['user']+"<"+server['user']+"@"+mail_postfix+">"

    import datetime
    subject = subject + " time:" + str(datetime.datetime.now())
    #text = "内容"
    #files = ["testdata.txt"]
    #files.append("testdata1.txt");
    try:
        send_mail(server, fro, to, subject, text, files)
        print u"发送成功"
    except Exception, e:
        print u"发送失败",str(e)

import smtplib

mail_server="smtp.ym.163.com"
mail_user1="hehongjing@brandbigdata.com"
mail_psw="qpzm1234"
mail_port='25'#'465'
def sendMail(content,subject="subject",send_to="hehongjing@brandbigdata.com"):
    #server = smtplib.SMTP_SSL()
    server = smtplib.SMTP()
    server.connect(mail_server, mail_port)
    #server.ehlo()
    #server.starttls()
    #server.ehlo()
    server.set_debuglevel(1)
    server.login(mail_user1,mail_psw)
    msg = ("From: %s\r\nTo: %s\r\nSubject: %s\r\n\r\n%s"% (mail_user1, send_to,subject,content))
    server.sendmail(mail_user1, send_to, msg)

def remove_all_space_char(ss):
    """
    去掉所有的不可见字符，包括空格，换行等等
    :param ss:
    :return:
    """
    temp = re.sub(ur'[\x00-\x20]', '', unicode(ss))
    return temp

# if __name__=="__main__":
#     import sys
#     print remove_all_space_char("\r\n                            长期\r\n              ")
#     print remove_all_space_char("123\t \n\r123asddsafasd\n  \r  a   ")
#     sys.exit()
#     #test_ssl_mail()
#     #sendMail("test send mail 123123")
#     send_mail_to_someone(subject="subject test",text="text test",to=["hehongjing@brandbigdata.com"])
#     #test()=======
#     # test()
#     send_mail(["xuweiwei@brandbigdata.com"],"hello","hi")

def get_all_filename_from_dir(dir):
    __doc__ = "获取某个目录中 目录和子目录下所有的文件的绝对路径名"
    filename_list = []
    for dirpath, dirnames, filenames in os.walk(dir):
        #print 'Directory', dirpath
        for filename in filenames:
            #print ' File', filename, os.path.join(dirpath,filename)
            filename_list.append(str(os.path.join(dirpath,filename)))
    return filename_list
if __name__ == '__main__':
    print os.getenv('spider_log',default='')