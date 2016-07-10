# -*- coding: utf-8 -*-
"""
发送邮件模块
"""
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import smtplib
from email.mime.text import MIMEText
import time

# 邮件列表
mail_list = [u"yangwen@bdservice.com",u'hehongjing@bbdservice.com', u'lvsijun@bbdservice.com', u'fumenglin@bbdservice.com',
            u'wangyao@bbdservice.com',u'wudewen@bbdservice.com', u'shuaiguangying@bbdservice.com',
             u'hejun@bbdservice.com', u'xingjie@bbdservice.com', u'dingminghui@bbdservice.com',
             u'dingyongqiang@bbdservice.com',u'qiudaoying@bbdservice.com', u'xubin@bbdservice.com']
# mail_list=[u'fumenglin@bbdservice.com',]
# 设置服务器
mail_host = 'smtp.bbdservice.com'
mail_user = 'bbdmail@bbdservice.com'
mail_pass = 'bbd12345'


class SendMail(object):
    def __init__(self):
        pass


    def sendMail(self,title, content):
        while True:
            try:
                print u"开始发送邮件"
                # 这里的hello可以任意设置，收到信后，将按照设置显示
                me = u"%s:%s"%(title,time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+'<' + mail_user + '>')
                # 创建一个实例，这里设置为html格式邮件
                msg = MIMEText(content, _subtype='html', _charset='utf-8')
                # 设置主题
                msg['Subject'] = title
                msg['From'] = me
                msg['To'] = ";".join(mail_list)
                s = smtplib.SMTP()
                s.connect(mail_host)
                s.login(mail_user, mail_pass)
                s.sendmail(me, mail_list, msg.as_string())
                s.close()
                print u"邮件发送完成"
                break
            except Exception as e:
                time.sleep(10)
                print e
    def getContent(self,titles,lists):
        html_1=u'<table width="100%" border="1" cellpadding="2" cellspacing="0"><tr>'
        for tt in titles:
            html_1+=u"<td>%s</td>"%tt
        html_1+=u"</tr>"
        for ll in lists:
            html_1+=u'<tr>'
            for l in ll:
                html_1+=u"<td>%s</td>"%l
            html_1+=u"</tr>"
        html_1+=u"</table>"
        return html_1


if __name__ == '__main__':
    tt=SendMail()
    ttt=tt.getContent(['a','b'],[[1,2],[3,4]])
    tt.sendMail('afdasdf',ttt)