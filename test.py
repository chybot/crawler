# -*- coding: utf-8 -*-
# Created by Leo on 16/05/06
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
import time
import QyxxSubControlConfig as config


def getUpdateProvs( pre_dict, new_dict):
    up_dict = {}
    for k, v in pre_dict.items():
        if v != new_dict[k]:
            up_dict.update({k: new_dict[k] - v})
    return up_dict

if __name__ == '__main__':
    d1 = \
        {
            "QyxxGanSu": 50,
            "QyxxShanDong": 3,

        }
    d2 = \
        {
            "QyxxGanSu": 30,
            "QyxxShanDong": 30,
            "QyxxShanDong2": 3
        }
    n_d = getUpdateProvs(d1,d2)
    print n_d

    # while 1:
    #     print config.PROVINCE_INFO_LIST
    #     reload(config)
    #     time.sleep(1)