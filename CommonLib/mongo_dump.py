__author__ = 'rubin'

import os
import pymongo
import time, datetime
from multiprocessing import Pool
import subprocess

db_black_list=["admin","config", "robin_test"]
table_black_list=["system.indexes","monitor","startup_log", "qyxx_monitor", "robin_test_monitor", "robin_test_qyxx_monitor"]
host = '192.168.3.100'
port = 25017
dir_path = r"E:\backup_bigdata"

def mongodump():
    cmd_list = []
    conn= pymongo.Connection(host, port, network_timeout=5.0)
    for db_name in conn.database_names():
        if db_name in  db_black_list:
            continue
        db = conn[db_name]
        for table_name in db.collection_names():
            if table_name in table_black_list:
                continue
            cmd = r'D:\mongodb-win32-x86_64-2008plus-2.4.11\bin\mongodump -h %s --port %d -d %s -c %s -o E:\backup_bigdata' %(host, port, db_name, table_name,)
            today = str(datetime.date.today())
            cmd += "\\"
            cmd += today
            cmd_list.append(cmd)
    return cmd_list

def backup_pool():
    p = Pool()
    cmd_list = mongodump()
    for cmd in cmd_list:
        cmd = str(cmd)
        print cmd
        p.apply_async(os.system, args=(cmd,))
    p.close()
    p.join()

if __name__ == "__main__":
    backup_pool()
    while(True):
        now = time.localtime()
        hour = now[3]
        if hour == 4:
            backup_pool()
            time.sleep(60*60)
        time.sleep(60*60)

