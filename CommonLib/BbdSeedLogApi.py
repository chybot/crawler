# -*- coding: utf-8 -*-
# ---------------------------------------
#   程序：BbdSeedLogApi.py
#   版本：0.1
#   作者：diven
#   日期：2016-05-14
#   语言：Python 2.7
#
#   版本列表：种子标准化日志输出API
# ---------------------------------------
import sys
reload(sys)
sys.setdefaultencoding("UTF-8")

import json
import time

BBD_SEED_THIS_VERSION = 1.0

def get_logs(state_code, seed=None, data=None, table_name=None, isnew=False, remark=u"", **keys):
    """
        获取种子抓取, 可能返回：None
        :param state_code   种子抓取的状态        【必选】
        :param seed   种子                        【data数据不存在时，参数必选，其他可选】
        :param data   种子抓取的数据              【爬虫端，参数可选，其他必选】
        :param table_name   当前种子存储的表名    【data数据不存在时，必选】
        :param isnew        当前数据是否为新增    【入库模块必选，其他可选】
        :param remark       备注信息              【备注信息】
        :return 标准化日志
    """
    data = __get_data(data)
    seed = __get_seed(seed, data)
    if not seed:
        return None
    else:
        seed_log = dict()
        seed_log[u"seed"] = seed
        seed_log[u"state_code"] = state_code
        seed_log[u"uptime"] = int(time.time())
        seed_log[u"remark"] = remark
        seed_log[u"version"] = BBD_SEED_THIS_VERSION
        try:
            seed_log[u"table_name"] = __get_table_name(table_name=table_name, data=data)
            seed_log[u"data_uptime"] = __get_data_uptime(data=data)
            seed_log[u"error_info"] = __get_error_info(data=data)
            seed_log[u"res"] =__get_data_res(data=data, isnew=isnew)
        except Exception as e:
            if not seed_log.has_key(u"table_name"):
                seed_log[u"table_name"] = u""
            if not seed_log.has_key(u"data_uptime"):
                seed_log[u"data_uptime"] = None
            if not seed_log.has_key(u"error_info"):
                seed_log[u"error_info"] = [{u"code": 100001, u"message": u"python log api error"}]
            if not seed_log.has_key(u"res"):
                seed_log[u"res"] = {}
            pass
        return json.dumps(seed_log)
    pass

def __get_data(data=None):
    """获取data值"""
    if data:
        if isinstance(data, dict):
            return data
        else:
            try:
                return json.loads(data)
            except Exception as e:
                return None
            pass
        pass
    else:
        return None

def __get_seed(seed=None, data=None):
    """获取种子"""
    if (not seed) and data:
        seed = data.get(u"bbd_seed", None)
    if not seed:
        return None
    elif isinstance(seed, dict):
        return seed
    else:
        try:
            return json.loads(seed)
        except Exception as e:
            return None
        pass
    pass

def __get_table_name(table_name=None, data=None):
    """获取表名"""
    if data:
        tmp_table_name = data.get(u"bbd_table", None)
        if tmp_table_name:
            return tmp_table_name
        else:
            return table_name
    else:
        return table_name
    pass

def __get_data_uptime(data=None):
    """获取数据最后抓取的时间"""
    if data:
        uptime = data.get(u"bbd_uptime", None)
        if not uptime:
            uptime = data.get(u"uptime", None)
            if uptime:
                return int(uptime)
        else:
            return None
    else:
        return None
    pass

def __get_error_info(data=None):
    """获取错误日志"""
    if data:
        error_log = data.get(u"bbd_error_log", None)
        if error_log:
            if isinstance(error_log, list):
                return error_log
            else:
                try:
                    return json.loads(error_log)
                except Exception as e:
                    return list()
                pass
            pass
        else:
            return list()
    else:
        return list()
    pass

def __get_data_res(data=None, isnew=False):
    """获取抓取的值"""
    res = dict()
    if data:
        res[u"_id"] = data.get(u"bbd_qyxx_id", u"")
        res[u"company_name"] = __get_company_name(data=data)
        res[u"company_regno"] = __get_company_regno(data=data)
        res[u"company_creditcode"] = __get_company_creditcode(data=data)
        res[u"company_url"] = data.get(u"bbd_url", u"")
        res[u"company_param"] = data.get(u"bbd_params", u"")
        res[u"company_esdate"] = __get_company_esdate(data=data)
        res[u"company_isnew"] = isnew
        res[u"company_type"] = __get_company_type(data=data)
        pass
    return res

def __get_company_name(data=None):
    """获取公司名"""
    keys = [u"company_name", u"companyName", u"名称", u"企业中文名称", u"机构名称", u"单位名称", u"企业（机构）名称", u"企业名称", u"个体名称", u"基金会名称"]
    if data:
        for key in keys:
            if data.has_key(key):
                value = data.get(key, "")
                if value:
                    return value
                pass
            pass
        pass
    return u""

def __get_company_regno(data=None):
    """获取公司注册号"""
    keys = [u"regno", u"regNo", u"注册号", u"企业注册号", u"营业执照注册号", u"新企业注册号"]
    if data:
        for key in keys:
            if data.has_key(key):
                value = data.get(key, "")
                if value:
                    return value
                pass
            pass
        pass
    return u""

def __get_company_creditcode(data=None):
    """获取公司注社会信用代码"""
    keys = [u"credit_code", u"creditCode", u"统一社会信用代码", u"社会信用代码"]
    if data:
        for key in keys:
            if data.has_key(key):
                value = data.get(key, "")
                if value:
                    return value
                pass
            pass
        pass
    return u""

def __get_company_esdate(data=None):
    """获取公司注社会信用代码"""
    keys = [u"esdate", u"esDate", u"成立日期", u"本机构设立日期", u"集团成立日期", u"成立日期：", u"注册日期{{}}", u"注册日期"]
    if data:
        for key in keys:
            if data.has_key(key):
                value = data.get(key, "")
                if value:
                    return value
                pass
            pass
        pass
    return u""

def __get_company_type_value(data=None):
    """获取公司注社会信用代码"""
    keys = [u"company_type", u"companyType", u"类型", u"公司类型", u"经营性质", u"经济性质", u"企业类型", u"法人类型", u"合伙企业类型"]
    if data:
        for key in keys:
            if data.has_key(key):
                value = data.get(key, "")
                if value:
                    return value
                pass
            pass
        pass
    return u""

def __get_company_type(data=None):
    company_type_value = __get_company_type_value(data=data)
    if company_type_value:
        company_type_value = company_type_value.replace("(", "（").replace(")", "）")
        #合伙企业
        if u"合伙" in company_type_value or u"集体" in company_type_value or u"全民" in company_type_value:
            if u"分公司" in company_type_value or u"分支机构" in company_type_value or u"办事处" in company_type_value:
                pass
            else:
                return 2
            pass
        #外国
        if u"外国（地区）企业" in company_type_value:
            return 3
        #个体
        if u"个体" in company_type_value or u"分公司" in company_type_value or u"分支机构" in company_type_value or u"个人经营" in company_type_value or u"个人独资企业" in company_type_value or u"办事处" in company_type_value or u"国有事业单位营业" in company_type_value or u"集体经济" in company_type_value:
            return 4
        pass
        #公司类型
        return 1
    else:
        return 0
    pass

class STATE(object):
    #队列状态
    BBD_SEED_IS_QUEUE_ING = 110001

    #抓取状态
    BBD_SEED_IS_CRAWL_ING = 120101  #正在抓取
    BBD_SEED_IS_CRAWL_SUC = 120102  #抓取成功
    BBD_SEED_IS_CRAWL_VOI = 120103  #抓取成功，但数据为空
    BBD_SEED_IS_CRAWL_ERO = 120104  #抓取失败
    BBD_SEED_IS_CRAWL_REV = 120105  #公司已注销
    BBD_SEED_IS_CRAWL_PAR = 120106  #部分抓取成功

    #爬虫解析状态
    BBD_SEED_IS_CRAWL_PARSE_ING = 120201  #正在解析
    BBD_SEED_IS_CRAWL_PARSE_SUC = 120202  #解析成功
    BBD_SEED_IS_CRAWL_PARSE_ERO = 120204  #解析失败

    #统一字段
    BBD_SEED_IS_UNIT_ING = 130001
    BBD_SEED_IS_UNIT_SUC = 130002
    BBD_SEED_IS_UNIT_ERO = 130004

    #清洗字段
    BBD_SEED_IS_CLEAN_ING = 140001
    BBD_SEED_IS_CLEAN_SUC = 140002
    BBD_SEED_IS_CLEAN_ERO = 140004

    #验证字段
    BBD_SEED_IS_VALIDATE_ING = 150001
    BBD_SEED_IS_VALIDATE_SUC = 150002
    BBD_SEED_IS_VALIDATE_ERO = 150004

    #数据排重
    BBD_SEED_IS_UNIQUE_ING = 160001
    BBD_SEED_IS_UNIQUE_SUC = 160002
    BBD_SEED_IS_UNIQUE_ERO = 160004

    #数据存储
    BBD_SEED_IS_SAVE_ING = 170001
    BBD_SEED_IS_SAVE_SUC = 170002
    BBD_SEED_IS_SAVE_ERO = 170004
pass

if __name__ == '__main__':
    state_code = STATE.BBD_SEED_IS_CLEAN_ERO
    seed = {u"bbd_province": u"g", u"company_creditcode": u"d", u"company_url": u"e", u"company_param": u"f", u"seed_type": 1, u"company_name": u"b", u"company_regno": u"c", u"_id": u"a"}
    data = {u"名称": u"中国石油", u"bbd_uptime": u"1463207511", u"bbd_table": u"qyxx", u"credit_code": u"91230102MA18W2HK8H"}
    print get_logs(state_code=state_code, seed=seed, data=data, table_name=None, remark=u"")