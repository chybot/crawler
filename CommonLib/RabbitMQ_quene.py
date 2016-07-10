# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding("UTF-8")
import pika
import hashlib
import time

def md5(word):
    m=hashlib.md5()
    m.update(str(word))
    return m.hexdigest()

class rabbitmqQueue():
    def __init__(self,queue_name,exchange_name="",rab_host="localhost",rab_port=5672):
        self.queue_name=queue_name
        self.exchange_name=exchange_name
        #建立连接
        self.connection=pika.BlockingConnection(pika.ConnectionParameters(host=rab_host,port=rab_port))
        #创建channel
        self.channel = self.connection.channel()
        #创建队列名
        self.channel.queue_declare(queue=self.queue_name, durable=True)
        #queue的持久化需要在声明时指定durable=True
        #sudo rabbitmqctl list_queues 查看当前的所有队列名
        #使用命令sudo rabbitmqctl list_bindings你可以看我们创建的queue
        #在发生和接收消息之前必须先建立链接，创建队列名和信道
        self.channel.basic_qos(prefetch_count=1) #Fair dispatch 设置消费者公平分发
        #设置交换的分发方式Exchange：direct, topic 和fanout
        # self.channel.exchange_declare(exchange=self.exchange_name,
        #                  type="direct")
    def sending(self,message):
        #exchange为交换，数据先发给exchange，然后才发生给队列，默认的exchange为空
        self.channel.basic_publish(exchange=self.exchange_name,
                        routing_key=self.queue_name,
                        body=message,
                        properties=pika.BasicProperties(
                        delivery_mode = 2   #确定消息持久化
                        ))

    def callback(self,ch, method, properties, body):
        #回调函数，处理接收到的body
        print " [x] Received %r" % (body,)

    def receiving(self,):
        #接收
        self.channel.basic_consume(self.callback,
                      queue=self.queue_name,
                      )
        #no_ack = True 关闭消息确认机制，默认为打开
        self.consuming()

    def consuming(self):
        #监听
        self.channel.start_consuming()

    def rab_close(self):
        #关闭链接
        self.connection.close()

if __name__ == '__main__':
    t1=time.time()
    for i in range(100001):
        r=rabbitmqQueue("str_md5")
        r.sending("%s"%md5(i))
    t2=time.time()
    print t2-t1
    #取数据，不需要while
    # r=rabbitmqQueue("hello")
    # r.receiving()


