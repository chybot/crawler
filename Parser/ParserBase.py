# -*- coding: utf-8 -*-
# Created by David on 2016/5/19.

import sys
import json
from util.TableParseUtil import TableParseUtil
from util.JsonParseUtil import JsonParseUtil
from ParserMapper import ParserMapper
from parser_map_config import transform
from CommonLib.Logging import Logging
from CommonLib.WebContent import WebContent, WebContentType
reload(sys)
sys.setdefaultencoding('utf-8')


class ParserBase:
    """
    ParserBase is the base parser to provide common implements for parsers
    @version:1.0
    @author:david ding
    @modify:
    """
    def __init__(self, pinyin):
        """
        Initiate the parameters.
        """
        self.pinyin = pinyin
        self.log = Logging(name=pinyin)
        self.result_collection = None
        self.json_mapper_config = dict()
        self.ignore_key_list = list()
        self.jbxx_web = None                # 存放基本信息WebContent
        pass

    def appendJsonMapperConfig(self, key, value):
        if not key or not value or not isinstance(value, dict):
            return
        self.json_mapper_config[key] = value

    def parseCommon(self, result, rslt_mapper_config=None):
        if not result:
            return None
        self.result_collection = list()
        self.rslt_mapper_config = rslt_mapper_config
        self.current_key = None
        if isinstance(result, dict):
            self.parseDict(result)
        elif isinstance(result, list):
            self.parseList(result)
        mapper_config = rslt_mapper_config if rslt_mapper_config else transform
        company = self.resultMap(self.result_collection, mapper_config)
        company_cleaned = self.cleanUp(company)
        # 提取并加入基本信息url
        if self.jbxx_web:
            company_cleaned['bbd_url'] = self.jbxx_web.url
        return company_cleaned

    def parseDict(self, result):
        if not result:
            return None
        if self.current_key:
            web = WebContent.getInstanceFromDictionary(result)
            if web:
                if self.current_key.startswith("jbxx_"):
                    self.jbxx_web = web
                return self.parseWebContentByKey(web)
        for key in result:
            if key in self.ignore_key_list:
                continue
            if key.endswith('_html') or key.endswith('_json'):
                self.current_key = key
            else:
                self.current_key = None
            value = result[key]
            if isinstance(value, dict):
                self.parseDict(value)
            elif isinstance(value, list):
                self.parseList(value)

    def parseList(self, result):
        if not result:
            return None
        for value in result:
            if isinstance(value, dict):
                self.parseDict(value)
            elif isinstance(value, list):
                self.parseList(value)

    def parseWebContentByKey(self, web):
        if not web or not isinstance(web, WebContent):
            return
        if web.status_code != 200 or web.time_out or not web.body:
            return
        result_list = None
        if self.current_key.endswith('_html'):
            result_list = self.parseHtmlTable(web.body)
        elif self.current_key.endswith('_json'):
            if not self.current_key:
                self.log.error(u"解析json内容 %s 时使无对应的key,请检查结果集结构！" % web.body)
            if not self.json_mapper_config:
                self.log.error(u"解析json内容 %s 时使用key=%s无对应的config" % (web.body, self.current_key))
            elif self.current_key and self.current_key in self.json_mapper_config:
                result_list = self.parseJson(web.body, self.json_mapper_config[self.current_key])
            else:
                self.log.error(u"解析json内容 %s 时使用key=%s无对应的config" % (web.body, self.current_key))
        if result_list:
            self.result_collection.extend(result_list)

    def parseWebContentByType(self, web):
        if not web or not isinstance(web, WebContent):
            return
        if web.status_code != 200 or web.time_out or not web.body:
            return
        result_list = None
        if web.content_type == WebContentType.HTML:
            result_list = self.parseHtmlTable(web.body)
        elif web.content_type == WebContentType.JSON:
            if not self.current_key:
                self.log.error(u"解析json内容 %s 时使无对应的key,请检查结果集结构！" % web.body)
            if not self.json_mapper_config:
                self.log.error(u"解析json内容 %s 时使用key=%s无对应的config" % (web.body, self.current_key))
            elif self.current_key and self.current_key in self.json_mapper_config:
                result_list = self.parseJson(web.body, self.json_mapper_config[self.current_key])
            else:
                self.log.error("解析json内容 %s 时使用key=%s无对应的config" % (web.body, self.current_key))
        if result_list:
            self.result_collection.extend(result_list)

    def parseHtmlTable(self, html):
        """
        解析html table型的数据，解析为键值对的标准形式
        :param html: 待解析的html table页面
        :return:
        """
        parser = TableParseUtil(html)
        info_list = parser.parse()
        self.log.info("本次模块解析结果：\n %s", json.dumps(info_list))
        return info_list

    def parseJson(self, json_obj, mapper_config):
        """
        解析json页面内容
        :param json_obj:json字符串或json对象
        :param mapper_config:映射字典
        :return:
        """
        if not json_obj:
            return None
        if isinstance(json_obj, basestring):
            json_obj = json.loads(json_obj)
        parser = JsonParseUtil()
        info_list = parser.parse(json_obj, mapper_config)
        if not info_list:
            return None
        self.log.info("本次模块解析结果：\n %s", json.dumps(info_list))
        return info_list

    def resultMap(self, result_list, mapper_config):
        """
        抓取结果收集，调用CrawlerMapper实现映射
        :param result_list:结果集
        :param mapper_config:映射文件
        :return:
        """
        company_mapped = ParserMapper.doMap(mapper_config, result_list)
        result_json = json.dumps(company_mapped, ensure_ascii=False)
        self.log.info(u"企业信息映射结果：\n" + result_json)
        return company_mapped

    def cleanUp(self, company):
        if not company or not isinstance(company, dict):
            return None
        company_clean = dict()
        for key,value in company.items():
            if key in self.ignore_key_list:
                continue
            if isinstance(value, dict):
                v_list = list()
                v_list.append(value)
                company_clean[key] = v_list
            else:
                company_clean[key] = value
        # 清理复合key中需要忽略的，例如gdxx.u'详情'
        for key in self.ignore_key_list:
            if '.' not in key:
                continue
            keys = key.split('.')
            recr_dict = company_clean
            for k in keys:
                if k not in recr_dict:
                    if isinstance(recr_dict, list):
                        for dc in recr_dict:
                            if k in dc:
                                del dc[k]
                    break
                if isinstance(recr_dict[k], basestring):
                    if k == keys[-1]:
                        del recr_dict[k]
                    break
                else:
                    recr_dict = recr_dict[k]
        result_json = json.dumps(company_clean, ensure_ascii=False)
        self.log.info(u"企业信息初步清理后结果：\n" + result_json)
        # 检查输出结果中是否有应该映射但未映射成功的key
        for key,value in company_clean.items():
            if isinstance(value, list):
                if key not in ['gdxx','bgxx','baxx','fzjg','xzcf']:
                    self.log.warning("[%s] 可能需要映射，请检查parser_map_config！" % key)
        return company_clean

if __name__ == "__main__":
    pass
