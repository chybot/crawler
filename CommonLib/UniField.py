# -*- coding: utf-8 -*-
# Created by Leo on 16/05/05
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

import copy
from TimeUtil import TimeUtil
from CalcMD5 import calcStrMD5
from Logging import Logging


class UniField(object):
    """
    用来统一字段
    """
    @staticmethod
    def updateId(src_id,upchar):
        return src_id+'|_|'+upchar
    @staticmethod
    def getId(data_dict,k_list):
        """
        把元组中的字符串用分割符连接起来
        :param key: （tuple）
        :return: (str)连接的字符串
        """
        v_list = map(lambda x: str(data_dict[x]), k_list)
        _id = "|_|".join(v_list)
        return _id

    @staticmethod
    def getRowkey(bbd_type,_id):

        name_md5 = calcStrMD5(_id)
        v_list=[]
        v_list.append(name_md5)
        v_list.append(_id)
        v_list.append(bbd_type)
        rk = "|_|".join(v_list)
        return rk

    @staticmethod
    def addDefaultField(data_dict, default_list,empty_value=""):
        for item in default_list:
            if not data_dict.has_key(item):
                data_dict[item] = empty_value
    @staticmethod
    def unifyRequestResult(data_dict, bbd_type):

        """
        同理，整理抓取后的字段
        :param company_name:  (unicode) 公司名
        :param data_dict:  (dict)  公司信息
        :return:  (bool) 是否成功存储 -> true / false
        """
        try:
            qyxx_dict = {
                "guangdong": u"广东",
                "hubei": u"湖北",
                "hunan": u"湖南",
                "henan": "河南",
                "heilongjiang": u"黑龙江",
                "hebei": u"湖北",
                "hainan": u"海南",
                "guizhou": u"贵州",
                "guangxi": u"广西",
                "fujian": u"福建",
                "chongqing": u"重庆",
                "beijing": u"北京",
                "anhui": u"安徽",
                "jiangsu": u"江苏",
                "gansu": u"甘肃",
                "xinjiang": u"新疆",
                "tianjin": u"天津",
                "sichuan": u"四川",
                "shanxixian": u"陕西",
                "shanxitaiyuan": u"山西",
                "shandong": u"山东",
                "shanghai": u"上海",
                "qinghai": u"青海",
                "ningxia": u"宁夏",
                "neimenggu": u"内蒙古",
                "liaoning": u"辽宁",
                "jilin": u"吉林",
                "jiangxi": u"江西",
                "xizang": u"西藏",
                "zhejiang": u"浙江",
                "yunnan": u"云南",
                "zongju": u"总局"
            }
            logger = Logging(name = bbd_type)
            if not data_dict.has_key("rowkey_dict"):
                raise Exception("Company data dict don't has rowkey values, wrong data")
            else:

                data_dict = copy.deepcopy(data_dict)
                rowkey_dict = copy.deepcopy(data_dict["rowkey_dict"])
                uptime = TimeUtil.timeStamp()
                dotime = TimeUtil.doTime()

                rowkey_dict["uptime"] = uptime
                rowkey_dict["dotime"] = dotime
                rowkey_dict["bbd_type"] = bbd_type

                data_dict.update(rowkey_dict)

                id_column_list = ["company_name","company_zch", "dotime"]
                _id = UniField.getId(data_dict,id_column_list)

                # 添加rowkey 和  _id
                # rk_column_list=["company_name","bbd_type","dotime"]
                rowkey = UniField.getRowkey(bbd_type,_id)
                logger.info(u"统一字段(网页原文) 产生rowkey 为：[%s]",rowkey)
                data_dict["rowkey"] = rowkey
                data_dict["_id"] = _id

                if bbd_type in qyxx_dict.keys():
                    data_dict["type"]=qyxx_dict[bbd_type]

                if data_dict.has_key(None):
                    del data_dict[None]

                return data_dict
        except Exception as e:
            logger.info(str(e))

    @staticmethod
    def cloneNeedColumns(data_dict):
        """
        源字典中拷贝除去网页原文 和 排除字段 意外的默认字段
        :param data_dict: 源文字典
        :return: 拷贝后的字典
        """

        res_dict = {}
        clone_keys = filter(lambda k: "_html" not in k and "_json" not in k ,data_dict.keys())
        ext_keys=["jbxx","baxx","bgxx","gdxx","fzjg","xzcf","values"]
        clone_keys = filter(lambda k:k not in ext_keys, clone_keys)
        ll=map(lambda key:{key:data_dict[key]}, clone_keys)
        map(lambda x:res_dict.update(x),ll)
        return res_dict

    @staticmethod
    def unifyParseResult(data_dict, bbd_type = None,**kwargs):

        if bbd_type is None:
            if data_dict.has_key("bbd_type"):
                bbd_type = data_dict["bbd_type"]
            else:
                bbd_type = "UniField"
        else:
            bbd_type = bbd_type
        logger = Logging(name = bbd_type)
        data_dict = copy.deepcopy(data_dict)
        basic_keys_list1 = ["bbd_source", "bbd_table", "version", "bbd_html", "bbd_url", "bbd_params"]
        UniField.addDefaultField(data_dict, basic_keys_list1)

        basic_keys_list2 = ["baxx", "bgxx", "gdxx", "fzjg", "xzcf"]
        UniField.addDefaultField(data_dict, basic_keys_list2, empty_value = [])
        data_dict["version"] = 3 # 兼容 数据平台字段
        data_dict.update(**kwargs)
        return data_dict
    def mapValues(self):
        pass

if __name__ == '__main__':
    d={"jbxx":1,"baxx":2,"rowkey_dict":{"company_name":u"中国石油","jbxx_html":"xxxx","company_zch":123455}}
    uni=UniField()
    uni.unifyParseResult(d)
    print uni.unifyRequestResult(d,u"北京")
    dd= uni.cloneNeedColumns(d)
    print dd
    pass