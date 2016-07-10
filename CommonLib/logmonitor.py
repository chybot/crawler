# coding=utf-8
__author__ = 'rubin'

import time, datetime
import pymongo
import smtplib
import glob
from email.mime.text import MIMEText

mailto_list=[ "xuweiwei@brandbigdata.com","hehongjing@brandbigdata.com","yanrubin@brandbigdata.com","fumenglin@brandbigdata.com"]

mail_host="smtp.ym.163.com"  #设置服务器
mail_user="monitor@brandbigdata.com"    #用户名
mail_pass="brandbigdata"   #口令
keywords=[u"请求验证码",u"验证码返回结果",u"验证码识别成功",u"errorType=1",u"errorType=2",u"errorType=3",u"errorType=4",u"errorType=5",u"errorType=6",u"请求返回数据为0"]
keywords_show=[u"请求验证码",u"验证码返回结果",u"验证码识别成功",u"coid_id为空",u"验证码内容为空",u"report_error",u"验证码请求发生异常",u"退钱发生异常",u"提交服务器返回错误",u"请求返回数据为0"]

def send_mail(to_list,sub,content):  #to_list：收件人；sub：主题；content：邮件内容
    me="server"+"<"+mail_user+">"   #这里的hello可以任意设置，收到信后，将按照设置显示
    msg = MIMEText(content,_subtype='html',_charset='utf-8')    #创建一个实例，这里设置为html格式邮件
    msg['Subject'] = sub    #设置主题
    msg['From'] = me
    msg['To'] = ";".join(to_list)
    try:
        s = smtplib.SMTP()
        s.connect(mail_host)  #连接smtp服务器
        s.login(mail_user,mail_pass)  #登陆服务器
        s.sendmail(me, to_list, msg.as_string())  #发送邮件
        s.close()
        return True
    except Exception as e:
        print u"error:%s"%str(e)
        return False



def gettime(line):
    pos=line.find(",")
    if pos<1:
        return None
    line=line[pos+1:]
    time=line[0:19]
    return time

def analyzer_line(line,day):
    countlist=list()
    datestr=gettime(line)
    if datestr is None:
        return None
    ymd=datestr[0:10]
    if ymd==day:
        for keyword in keywords:
           have_word=line.find(keyword)>0
           if have_word:
               countlist.append(1)
           else:
               countlist.append(0)
        return countlist
    else :
        return None


def analyzer_file(filename,day):
    l1=list()
    for k in keywords:
        l1.append(0)
    with open(filename) as f:
        try:
            while True:
                log_line=f.readline().decode("utf-8","ignore")
                if not log_line:
                    break
                curr=analyzer_line(log_line,day)
                if curr is not None:
                    l2=list()
                    for i in range(0,len(curr)):
                        l2.append(l1[i]+curr[i])
                    l1=l2
            return l1
        except Exception as e:
            print e


def analyzer_day(day):
    """
    解析指定某一天的日期
    """

    html = u'<table  width="100%" border="1" cellpadding="2" cellspacing="0"><tr><td></td>'
    for i in range(len(keywords)):
        html+="<td>"+keywords_show[i]+"</td>"
    html+="</tr>"
    for filename in glob.glob(u"D:/python_test/qyxx_*/*.log"):
        html+="<tr><td>"+ filename +"</td>"
        l2=analyzer_file(filename,day)
        for ll2 in l2:
            html+="<td>"+str(ll2)+"</td>"
        html+="</tr>"
    html+="</table>"
    return html

def log_analyzer():
    """
    日志分析主函数
    """
    today=time.strftime("%Y-%m-%d")
    yesterday=datetime.datetime.now()-datetime.timedelta(days = 1)
    yesterday=time.strftime("%Y-%m-%d",yesterday.timetuple())
    html=""

   #解析昨天的日志内容
    html+=u"<h1>%s 企业信息日志分析结果</h1>"%yesterday
    html+=analyzer_day(yesterday)
    html+=u"<br/><br/>"

    #解析今日的日志内容
    html+=u"<h1>%s 企业信息日志分析结果</h1>"%today
    html+=analyzer_day(today)
    sub = u"全国企业信息日志监控报告,时间:" + time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
    send_mail(mailto_list,sub,html)
    print u"邮件发送成功"

def main():
    print u"开始"
    while(True):
        now = time.localtime()
        hour = now[3]
        if hour == 8 or hour==13 or hour ==17:
            log_analyzer()
            time.sleep(60*60)
        time.sleep(60*60)

if __name__ == '__main__':
    main()
    # log_analyzer()
    # curr=analyzer_line(u"Mon,2014-11-24 17:06:55 qyxx_shanghai_crawler.py [line:433] INFO 请求验证码'","2014-11-24","2014-11-25")
    # l2=analyzer_file(u"D:/个人资料/工作/数联铭品/验证码/qyxx_shanghai_yzm1.log","2014-11-24","2014-11-25")
    # for l in l2:
    #     print l