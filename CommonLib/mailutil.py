# -*- coding: utf-8 -*-
__author__ = 'Lvv'

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import smtplib
from email.mime.text import MIMEText
from common import storageutil
from common import timeutil
import time
import json

class mail:
    def __init__(
            self,
            to_queue=False,
            queue_type='kafka',
            queue_table='mail_warning',
            queue_host='web14',
            queue_port=51092,
            mail_host='smtp.ym.163.com',
            mail_username='monitor@brandbigdata.com',
            mail_password='brandbigdata'
    ):
        self.to_queue = to_queue
        self.mail_host = mail_host
        self.mail_username = mail_username
        self.mail_password = mail_password
        self.queue_mail = None
        if to_queue:
            self.queue_mail = storageutil.getdb_factory(table=queue_table, type=queue_type, host=queue_host, port=queue_port, async=True)


    def send_mail(self, mail_list, sub, content):
        if self.to_queue:
            mail_data = {
                'mail_list': json.dumps(mail_list),
                'sub': sub,
                'content': content,
                'date': timeutil.format('%Y-%m-%d %H:%M:%S', time.time())
            }
            self.queue_mail.save(mail_data)
        else:
            me = 'server' + '<' + self.mail_username + '>'
            msg = MIMEText(content, _subtype='html', _charset='utf-8')
            msg['Subject'] = sub
            msg['From'] = me
            msg['To'] = ';'.join(mail_list)
            server = smtplib.SMTP()
            server.connect(self.mail_host)
            server.login(self.mail_username, self.mail_password)
            server.sendmail(me, mail_list, msg.as_string())
            server.close()


if __name__ == '__main__':
    mail = mail(True)
    mail.send_mail(['lvsijun@brandbigdata.com'], u'sub-test', u'content-test')