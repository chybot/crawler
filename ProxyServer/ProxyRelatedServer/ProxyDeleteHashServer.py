# -*- coding:utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding("UTF-8")

import smtplib
from email.mime.text import MIMEText
import time
from apscheduler.schedulers.background import BlockingScheduler

sys.path.append('../../')
from CommonLib.DB.DBManager import DBManager
from Config.ConfigGet import ConfigGet as C

proxy_cf = 'ConfigProxyServer.ini'
f = lambda y,z:C(proxy_cf).get(y,z)

_type = f('db','type')
_host = f('db','host')
_port = f('db','port')

class ProxyDeleteHashServer(object):
    def __init__(self):
        self.dict_={}
        self.__db = DBManager.getInstance(_type,'name',host = _host,port = _port)
    def time_othersty(self,tt):
        timeStamp = int(float(tt))
        timeArray = time.localtime(timeStamp)
        return time.strftime("%Y-%m-%d", timeArray)
    def get_count(self,kk,value):
        ll=kk.split("_")
        if len(ll)<3:
            return
        queue="_".join(ll[1:-1])
        uptime=value.get("uptime",0)
        str_tt=str(self.time_othersty(uptime))
        num=int(value.get("now_num",0))
        self.dict_.setdefault(str_tt,{}).setdefault("bbd",{})[queue]=self.dict_.setdefault(str_tt,{}).setdefault("bbd",{}).setdefault(queue,0)+num
    def verify(self):
        tt=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        for key in self.__db.hlistHash("",""):
            map_value=self.__db.hgetallHash(key)
            self.get_count(key,map_value)
            uptime=map_value.get("uptime",0)
            #num=map_value.get("now_num",0)
            if self.time_othersty(uptime)!=self.time_othersty(time.time()):
                self.__db.hclearHash(key)
                #log.msg(u"代理%s过期，过期时间%s,当天访问次数%d"%(key,self.time_othersty(uptime),int(num)))
        html=u"<li><a>代理统计截止时间：%s</a></li>"%tt
        for time_str in self.dict_:
            dict_buy={}
            dict_bbd={}
            dict_all={}
            dict_={}
            for type_str,dict_queue in self.dict_.get(time_str).items():
                for dd in dict_queue.items():
                    queue,num=dd
                    dict_all[queue]=dict_all.get(queue,0)+int(num)
                    if type_str=="bbd":
                        dict_bbd[queue]=dict_bbd.get(queue,0)+int(num)
                    else:
                        dict_buy[queue]=dict_buy.get(queue,0)+int(num)
            for kk,vv in dict_all.items():
                dict_[kk]=[vv,dict_bbd.get(kk,0),dict_buy.get(kk,0)]

            #html1=u"<html1>代理统计截止时间：%s<html>%s代理访问统计</html><html1>"%(tt,time_str)+self.mail_content(dict_)
            html1=u"<li><a>%s代理访问统计</a></li>"%time_str+self.mail_content(dict_)
            html+=html1
        to_list=("fumenglin@brandbigdata.com","hehongjing@brandbigdata.com","hejun@brandbigdata.com","liqian@brandbigdata.com","zouqinlin@brandbigdata.com",
                 "lvsijun@brandbigdata.com","wangyao@brandbigdata.com","wudewen@brandbigdata.com",
                 "shuaiguangying@brandbigdata.com","xubin@brandbigdata.com","dingminghui@brandbigdata.com","yangwen@brandbigdata.com",
                 "dingyongqiang@brandbigdata.com")

        sub = u"[代理访问量统计]：" +u";send mail time:"+ time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.send_mail(to_list,sub,html)

    def mail_content(self,dict_):
        html_1 = u'<table width="100%" border="1" cellpadding="2" cellspacing="0"><tr><td>获取代理的队列名</td><td>总的访问次数</td><td>自建代理的访问次数</td><td>非自建代理</td></tr>'
        for kk,vv in dict_.items():
            html_1+=u"<tr><td>" + str(kk) +  u"</td><td>"+str(vv[0])+u"</td><td>"+str(vv[1])+u"</td><td>"+str(vv[2])+u"</td></tr>"
        html_1+=u"</table>"
        return html_1


    def send_mail(self,to_list, sub, content):
        while True:
            try:
                mail_host = "smtp.ym.163.com"
                mail_user = "fumenglin@brandbigdata.com"
                mail_pass = "fumenglin"
                print u"开始发送邮件"
                # 这里的hello可以任意设置，收到信后，将按照设置显示
                me = u"代理访问次数统计邮件:%s"%time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+'<' + mail_user + '>'
                # 创建一个实例，这里设置为html格式邮件
                msg = MIMEText(content, _subtype='html', _charset='utf-8')
                # 设置主题
                msg['Subject'] = sub
                msg['From'] = me
                msg['To'] = ";".join(to_list)
                s = smtplib.SMTP()
                s.connect(mail_host)
                s.login(mail_user, mail_pass)
                s.sendmail(me, to_list, msg.as_string())
                s.close()
                print u"邮件发送完成"
                break
            except Exception as e:
                time.sleep(10)
                print e

def main():
    dele_proxy = ProxyDeleteHashServer()
    dele_proxy.verify()
    dele_proxy.dict_ = {}

if __name__ == '__main__':
    scheduler = BlockingScheduler()
    scheduler.add_job(main(), 'cron', second='0', minute='0', hour='6')
    scheduler.start()





