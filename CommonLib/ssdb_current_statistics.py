# -*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding("UTF-8")
import ssdb
import re
import time

def main():
    tt=True
    sleep_time=0
    all_time=0
    while True:
        try:
            con1=ssdb.SSDB(host="118.123.9.75",port=57888)
            con2=ssdb.SSDB(host="118.123.9.75",port=57878)
            list1=con1.qlist(u"",u"",999)
            list2=con2.qlist(u"",u"",999)
            if len(sys.argv)>1:
                queue_names=sys.argv[1:]
                if tt:
                    sleep_time=filter(lambda x:re.search("\d{%d}"%len(x),x),queue_names)
                    if sleep_time:
                        sleep_time=int(sleep_time[0])
                tt=False
                for queue_name in filter(lambda x:re.search("\D{%d}"%len(x),x),queue_names):
                    if queue_name in list1:
                        print u"《%s》列当前长度为：%d"%(queue_name,con1.qsize(queue_name))
                    elif queue_name in list2:
                        print u"《%s》队列当前长度为：%d"%(queue_name,con2.qsize(queue_name))
                    else:
                        print u"《%s》队列当前长度为：0"%queue_name
                        print u"《%s》在当前SSDB队列里没有数据，或者队列名输入错误，请检查"%queue_name
            else:
                print u"SSDB1的当前活动队列名为："
                print "\t"+"\n\t".join(list1)
                print u"SSDB2的当前活动队列名为："
                print "\t"+"\n\t".join(list2)
                print u"如果需要查看某个队列的长度："
                print u"\teg: python ssdb_current_statistics.py queue_names 可以输入多个"
                print u"\teg: python ssdb_current_statistics.py beijing shanghai_2 sichuan"
                print u"可以在后面加上时间间隔，表示每隔几秒执行一次,时间可以放在任何位置"
                print u"\teg: python ssdb_current_statistics.py beijing shanghai_2 sichuan 5"
                print u"\teg: python ssdb_current_statistics.py beijing 5"
            if sleep_time:
                print u"wait time:%d"%sleep_time
                time.sleep(sleep_time)
            all_time+=1
            if all_time>=20 or not sleep_time:
                break
        except Exception as e:
            print e
if __name__ == '__main__':
    main()