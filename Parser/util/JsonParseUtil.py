# -*- coding: utf-8 -*-
# Created by David on 2016/5/7.

import sys
import json
reload(sys)
sys.setdefaultencoding('utf-8')

class JsonMapType(object):
    """
    JsonMapType is used to mark the map type as an enum
    """
    OBJECT_LIST = 0

json_gdxx = '''
{"totalRecords":2,"list":[{"invNo":"c80f751d-0151-1000-e000-23180a0c0115","entNo":"f6dcaa8e-011e-1000-e000-2e860a0c0117","invType":"自然人股东","inv":"张凤茹","certName":" ","certNo":" ","subConAm":100.000000,"acConAm":0.000000,"acConDate":"Jan 21, 2009 12:00:00 AM","conForm":"货币出资","acConForm":"货币出资","respForm":""},{"invNo":"c80f751d-0151-1000-e000-23190a0c0115","entNo":"f6dcaa8e-011e-1000-e000-2e860a0c0117","invType":"自然人股东","inv":"吴浩然","certName":" ","certNo":" ","subConAm":900.000000,"acConAm":0.000000,"conForm":"货币出资","acConForm":"货币出资","respForm":""}],"pageNo":1,"pageSize":5,"url":"GSpublicity/invInfoPage.html","selList":[{"invNo":"c80f751d-0151-1000-e000-23180a0c0115","entNo":"f6dcaa8e-011e-1000-e000-2e860a0c0117","invType":"自然人股东","inv":"张凤茹","certName":" ","certNo":" ","subConAm":100.000000,"acConAm":0.000000,"acConDate":"Jan 21, 2009 12:00:00 AM","conForm":"货币出资","acConForm":"货币出资","respForm":""},{"invNo":"c80f751d-0151-1000-e000-23190a0c0115","entNo":"f6dcaa8e-011e-1000-e000-2e860a0c0117","invType":"自然人股东","inv":"吴浩然","certName":" ","certNo":" ","subConAm":900.000000,"acConAm":0.000000,"conForm":"货币出资","acConForm":"货币出资","respForm":""},null,null,null],"topPageNo":1,"totalPages":1,"previousPageNo":0,"nextPageNo":2,"bottomPageNo":1,"obj":"1"}
'''
json_gdxx2 = '''
{
  "totalRecords": 1,
  "list": [
    {
      "invNo": "a3f56f3a-0151-1000-e000-39f90a0c0115",
      "entNo": "ad14832b-012b-1000-e000-07730a0c0115",
      "invType": "企业法人",
      "inv": "东莞市邦联实业投资有限公司",
      "certName": "营业执照",
      "certNo": "441900000945253",
      "subConAm": 100.000000,
      "acConAm": 100.000000,
      "acConDate": "Oct 11, 2010 12:00:00 AM",
      "conForm": "货币出资",
      "acConForm": "货币出资",
      "respForm": "",
      "exePerson": "0"
    }
  ],
  "pageNo": 1,
  "pageSize": 5,
  "url": "GSpublicity/invInfoPage.html",
  "selList": [
    {
      "invNo": "a3f56f3a-0151-1000-e000-39f90a0c0115",
      "entNo": "ad14832b-012b-1000-e000-07730a0c0115",
      "invType": "企业法人",
      "inv": "东莞市邦联实业投资有限公司",
      "certName": "营业执照",
      "certNo": "441900000945253",
      "subConAm": 100.000000,
      "acConAm": 100.000000,
      "acConDate": "Oct 11, 2010 12:00:00 AM",
      "conForm": "货币出资",
      "acConForm": "货币出资",
      "respForm": "",
      "exePerson": "0"
    },
    null,
    null,
    null,
    null
  ],
  "topPageNo": 1,
  "totalPages": 1,
  "previousPageNo": 0,
  "nextPageNo": 2,
  "bottomPageNo": 1,
  "obj": "2"
}
'''
json_jilin_bgxx = '''
[{"altaf":"水表、塑料管材、塑料管件、保温材料的销售及水表安装（法律、法规和国务院决定禁止的项目不得经营，依法须经批准的项目，经相关部门批准后方可开展经营活动）**","altbe":"水表，塑料管，安装水表*","altdate":{"date":11,"day":4,"hours":0,"minutes":0,"month":5,"seconds":0,"time":1433952000000,"timezoneOffset":-480,"year":115},"altitem":"经营范围变更","openo":"4576753e-014d-1000-e0da-d4e8c0a80043","pripid":"88ad3d3b-7d83-43e4-8df6-cf785473bdfd","xzqh":"3700"},{"altaf":"李瑞华","altbe":"宋大成","altdate":{"date":15,"day":2,"hours":0,"minutes":0,"month":3,"seconds":0,"time":1397491200000,"timezoneOffset":-480,"year":114},"altitem":"法定代表人变更","openo":"c423e1a1-0147-1000-e02e-eddcc0a80043","pripid":"88ad3d3b-7d83-43e4-8df6-cf785473bdfd","xzqh":"3700"},{"altaf":"400.0000","altbe":"21.0000","altdate":{"date":21,"day":1,"hours":0,"minutes":0,"month":9,"seconds":0,"time":1382284800000,"timezoneOffset":-480,"year":113},"altitem":"注册资本(金)变更","openo":"c423e1a1-0147-1000-e02e-edd8c0a80043","pripid":"88ad3d3b-7d83-43e4-8df6-cf785473bdfd","xzqh":"3700"},{"altaf":"***********0026939","altbe":"***********06141","altdate":{"date":24,"day":2,"hours":0,"minutes":0,"month":8,"seconds":0,"time":1379952000000,"timezoneOffset":-480,"year":113},"altitem":"注册号升位","openo":"c423e1a1-0147-1000-e02e-edd7c0a80043","pripid":"88ad3d3b-7d83-43e4-8df6-cf785473bdfd","xzqh":"3700"},{"altaf":"水表，塑料管，安装水表*","altbe":"水表，塑料管","altdate":{"date":24,"day":2,"hours":0,"minutes":0,"month":8,"seconds":0,"time":1379952000000,"timezoneOffset":-480,"year":113},"altitem":"经营范围变更","openo":"c423e1a1-0147-1000-e02e-edd5c0a80043","pripid":"88ad3d3b-7d83-43e4-8df6-cf785473bdfd","xzqh":"3700"},{"altaf":"南关区亚泰大街7398号","altbe":"南关区南岭大街96号","altdate":{"date":12,"day":3,"hours":0,"minutes":0,"month":2,"seconds":0,"time":1047398400000,"timezoneOffset":-480,"year":103},"altitem":"住所变更","openo":"c423e1a1-0147-1000-e02e-edcec0a80043","pripid":"88ad3d3b-7d83-43e4-8df6-cf785473bdfd","xzqh":"3700"},{"altaf":"宋大成","altbe":"曲汉毅","altdate":{"date":17,"day":3,"hours":0,"minutes":0,"month":11,"seconds":0,"time":882288000000,"timezoneOffset":-480,"year":97},"altitem":"法定代表人变更","openo":"c423e1a1-0147-1000-e02e-edc9c0a80043","pripid":"88ad3d3b-7d83-43e4-8df6-cf785473bdfd","xzqh":"3700"},{"altaf":"曲汉毅","altbe":"王卫东","altdate":{"date":12,"day":1,"hours":0,"minutes":0,"month":4,"seconds":0,"time":863366400000,"timezoneOffset":-480,"year":97},"altitem":"法定代表人变更","openo":"c423e1a1-0147-1000-e02e-edc5c0a80043","pripid":"88ad3d3b-7d83-43e4-8df6-cf785473bdfd","xzqh":"3700"},{"altaf":"王卫东","altbe":"李洪增","altdate":{"date":14,"day":5,"hours":0,"minutes":0,"month":6,"seconds":0,"time":805651200000,"timezoneOffset":-480,"year":95},"altitem":"法定代表人变更","openo":"c423e1a1-0147-1000-e02e-edc1c0a80043","pripid":"88ad3d3b-7d83-43e4-8df6-cf785473bdfd","xzqh":"3700"},{"altaf":"李洪增","altbe":"宋大成","altdate":{"date":7,"day":3,"hours":0,"minutes":0,"month":3,"seconds":0,"time":734112000000,"timezoneOffset":-480,"year":93},"altitem":"法定代表人变更","openo":"c423e1a1-0147-1000-e02e-edbdc0a80043","pripid":"88ad3d3b-7d83-43e4-8df6-cf785473bdfd","xzqh":"3700"},{"altaf":"21.0000","altbe":"19.0000","altdate":{"date":3,"day":1,"hours":0,"minutes":0,"month":6,"seconds":0,"time":615394800000,"timezoneOffset":-540,"year":89},"altitem":"注册资本(金)变更","openo":"c423e1a1-0147-1000-e02e-edb9c0a80043","pripid":"88ad3d3b-7d83-43e4-8df6-cf785473bdfd","xzqh":"3700"},{"altaf":"宋大成","altbe":"陈喜林","altdate":{"date":3,"day":1,"hours":0,"minutes":0,"month":6,"seconds":0,"time":615394800000,"timezoneOffset":-540,"year":89},"altitem":"法定代表人变更","openo":"c423e1a1-0147-1000-e02e-edb8c0a80043","pripid":"88ad3d3b-7d83-43e4-8df6-cf785473bdfd","xzqh":"3700"}]
'''
map_config_gdxx = {'invType': u'股东类型', 'inv': u'股东', 'certName': u'证照/证件类型', 'certNo': u'证照/证件号码', 'invNo': 'invNo', 'primary_key':'inv,certNo'}

map_config_bgxx = {'altaf': u'变更后内容', 'altbe': u'变更前内容', 'altitem': u'变更事项', 'altdate.time': u'变更日期'}

class JsonParseUtil:
    """
    JsonParseUtil is used for map the json content to the target structure
    @version:1.0
    @author:david ding
    @modify:
    """

    def __init__(self):
        """
        Initiate the parameters.
        """
        self.parsed_list = None
        self.parsed_distinct_set = None
        self.primary_key_list = None

    def parseList(self, json_list, config):
        """
        map the json list to the target result
        :param json_list: the json list
        :param config: the map config
        :return:
        """
        if not json_list: return
        for json_obj in json_list:
            if not json_obj:
                continue
            if isinstance(json_obj, list):
                self.parseList(json_obj, config)
            elif isinstance(json_obj, dict):
                self.parseDict(json_obj, config)

    def parseDict(self, json_dict, config):
        """
        map the json dictionary to the target result
        :param json_dict: the json dictionary
        :param config: the map config
        :return:
        """
        if not json_dict: return
        parsed_dict = dict()
        for key in json_dict:
            value = json_dict[key]
            if not value:
                continue
            if isinstance(value, list):
                self.parseList(value, config)
            elif isinstance(value, dict):
                zip_dict = self.tryToZipDict(key, value)
                if zip_dict:
                    for zip_key in zip_dict:
                        if zip_key in config:
                            parsed_dict[config[zip_key]] = zip_dict[zip_key]
                else:
                    self.parseDict(value, config)
            elif key in config:
                parsed_dict[config[key]] = value
        # 去重
        if parsed_dict:
            if self.primary_key_list:
                pk_value = ''
                for pk in self.primary_key_list:
                    if pk not in json_dict:
                        return
                    pk_value += str(json_dict[pk])+","
                if pk_value in self.parsed_distinct_set:
                    return
                if pk_value:
                    self.parsed_distinct_set.add(pk_value)
            self.parsed_list.append(parsed_dict)

    def tryToZipDict(self, key, val_dict):
        """
        try to zip the keys into a new dict
        :param key: the first key
        :param val_dict: the dict to provide second key and value
        :return:
        """
        res_dict = dict()
        for val_key in val_dict:
            val = val_dict[val_key]
            if isinstance(val, list) or isinstance(val, dict):
                return None
            res_dict["%s.%s" % (key, val_key)] = val
        return res_dict

    def showParsedInfo(self):
        """
        show the mapped result in console
        :return:
        """
        if self.parsed_list:
            for info_dict in self.parsed_list:
                print '----------------------------------'
                for key in info_dict:
                    print key + " = " + str(info_dict[key])

    def parse(self, json_obj, config, map_type=JsonMapType.OBJECT_LIST):
        """
        parse a json body into target collection
        :param json_obj: the json body
        :param config: the map config
        :param map_type: the type of map
        :return:
        """
        if not json_obj or not config:
            return None
        if map_type == JsonMapType.OBJECT_LIST:
            self.parseJsonObjectList(json_obj, config)
        self.showParsedInfo()
        return self.parsed_list

    def parseJsonObjectList(self, json_obj, config):
        """
        parse the json body into a list collection
        :param json_obj:
        :param config:
        :return:
        """
        self.parsed_list = list()
        self.parsed_distinct_set = set()
        self.primary_key_list = list()

        if 'primary_key' in config:
            for pk in config['primary_key'].split(','):
                if pk:
                    self.primary_key_list.append(pk.strip())
            self.primary_key_list.sort()
        if not json_obj: return None
        if isinstance(json_obj, basestring):
            json_obj = json.loads(json_obj)
        if isinstance(json_obj, list):
            self.parseList(json_obj, config)
        elif isinstance(json_obj, dict):
            self.parseDict(json_obj, config)
        return self.parsed_list

'''
约定：
1.用于排重、验证数据合法性：primary_key
'''

if __name__ == "__main__":
    parser = JsonParseUtil()
    dic_list = parser.parse(json_gdxx2, map_config_gdxx)
    # dic_list = parser.parse(json_jilin_bgxx, map_config_bgxx)
    pass
