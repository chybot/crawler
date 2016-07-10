# -*- coding: utf-8 -*-
# Created on 2015/3/11 16:56.

import os
import re
import sys
import time
import json
import traceback
from requests import get
from requests import post

reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.append('../')

from lxml import etree
from CommonLib.exceptutil import traceinfo
from CommonLib.xpathutil import gettexts
from CommonLib.xpathutil import get_all_text

def xpath_parse(conf_dict, global_dict, results):
    # global_dict支持直接传log进来
    if not isinstance(global_dict, dict):
        global_dict = {'log': global_dict}

    log = global_dict['log']
    if 'get_global_params' in conf_dict:
        key = conf_dict['get_global_params']
        results = global_dict[key]

    returns_list = []
    xpath_parse = conf_dict['xpath']
    index = conf_dict['indexes']
    returns_list = xpath_parse_single(results, xpath_parse, index, log)

    return returns_list

def xpath_parse_single(results, xpath, index, log):
    print xpath
    print index
    returns = None
    if isinstance(results, unicode) or isinstance(results, str):
        tree = etree.HTML(results)
    else:
        tree = results

    if isinstance(xpath, list) and isinstance(tree, list):
        returns = []
        for i in range(0, len(xpath)):
            returns.append(xpath_parse_single(tree[i], xpath[i], index[i], log))
    elif isinstance(xpath, list):
        returns = []
        for i in range(0, len(xpath)):
            returns.append(xpath_parse_single(tree, xpath[i], index[i], log))
    elif isinstance(tree, list):
        returns = []
        for i in range(0, len(tree)):
            returns.append(xpath_parse_single(tree[i], xpath, index, log))
    else:
        try:
            log.debug(u'xpath is %s'%(xpath))
            if index == None:
                if xpath.endswith('/text()') and xpath != './/script/text()':
                    raw = [''.join(x.xpath('.//text()')) for x in tree.xpath(xpath.replace('/text()',''))]
                else:
                    raw = tree.xpath(xpath)
                returns = []
                log.debug(u'result of xpath is:')
                for r in raw:
                    log.debug(u'%s', r)
                    returns.append(r)
            elif isinstance(index, str) and ':' in index:
                if xpath.endswith('/text()') and xpath != './/script/text()':
                    raw = [''.join(x.xpath('.//text()')) for x in tree.xpath(xpath.replace('/text()',''))]
                else:
                    raw = tree.xpath(xpath)
                returns = []
                log.debug(u'result of xpath is:')
                temp_int = index.split(':')
                strIndex = int(temp_int[0])
                endIndex = int(temp_int[1])
                if endIndex < 0:
                    end_temp = len(raw)+endIndex
                    endIndex = end_temp+1
                for i in range(strIndex, endIndex):
                    log.debug(u'%s', raw[i])
                    returns.append(raw[i])
            elif index == 'texts':
                raw = gettexts(tree, xpath)
                log.debug(u'result of xpath is:%s', raw)
                returns = raw
            elif index == 'all_texts':
                raw = get_all_text(tree, xpath)
                log.debug(u'result of xpath is:%s', raw)
                returns = raw
            elif index == 'raw':
                raw = tree.xpath(xpath)[0]
                string = etree.tostring(raw, encoding=unicode)
                log.debug(u'result of xpath is:%s', string)
                returns = string
            elif index < 0:
                raw = tree.xpath(xpath)
                log.debug(u'result of xpath is:')
                if len(raw) < 1:
                    returns = ''
                else:
                    returns = raw[len(raw)+index]
                    log.debug(returns)
            else:
                raw = tree.xpath(xpath)
                if raw:
                    log.debug(u'result of xpath is:%s', raw[index])
                    returns = raw[index]
                else:
                    returns=""
        except Exception as e:
            log.error(u'xpath路径%s错误\n%s', xpath, traceinfo(e))
            time.sleep(1)
            returns = ''

    return returns

def regex_parse(conf_dict, global_dict, results):
    # global_dict支持直接传log进来
    if not isinstance(global_dict, dict):
        global_dict = {'log': global_dict}

    log = global_dict['log']
    if 'get_global_params' in conf_dict:
        key = conf_dict['get_global_params']
        dict_list = global_dict[key]

    regex_parse = conf_dict['regex']

    returns_list = regex_parse_single(regex_parse, results, log)
    return returns_list

def regex_parse_single(regex, results, log):
    if isinstance(regex, list) and isinstance(results, list):
        temp_list = []
        for j in range(0, len(regex)):
            temp = regex_parse_single(regex[j], results[j], log)
            temp_list.append(temp)
    elif isinstance(results, list):
        temp_list = []
        for j in range(0, len(results)):
            temp = regex_parse_single(regex, results[j], log)
            temp_list.append(temp)
    elif (isinstance(regex, list)):
        temp_list = []
        for j in range(0, len(regex)):
            temp = regex_parse_single(regex[j], results, log)
            temp_list.append(temp)
    else:
        log.debug(u'regex is %s'%(regex))
        if regex == None:
            temp_list = results
        else:
            pattern = re.compile(regex)
            res = re.search(pattern, results)
            if not res:
                log.warning(u'正则表达式%s未匹配到期望的结果！', regex)
                # raise Exception() # 此处不应抛出异常，页面中内容错位或缺少信息导致无有效匹配，但属正常
                return None
            temp_list = res.group(1)

    return temp_list

def json_parse(conf_dict, global_dict, html):
    log = global_dict['log']

    content_json = None
    try:
        content_json = json.loads(html)
    except Exception as e:
        log.error(u'页数text转json失败 \n%s', traceinfo(e))
        time.sleep(1)
        raise Exception()

    return recursive_keys(content_json, conf_dict['key'], log)

def recursive_keys(json, keys, log):
    data_list = []
    json_keys = keys.keys()
    json_keys.sort()
    for jk in json_keys:
        if not json.has_key(jk):
            log.error(u'没有键%s', jk)
            data_list.append(u'不公示')
        elif isinstance(keys[jk], dict):
            temp = recursive_keys(json[jk], keys[jk], log)
            data_list.extend(temp)
        elif isinstance(keys[jk], list):
            temp_list = []
            for k in json[jk]:
                temp = recursive_keys(k, keys[jk][0], log)
                temp_list.append(temp)
            data_list.append(temp_list)
        else:
            log.debug(u'key:value %s:%s'%(jk, json[jk]))
            temp = json[jk]
            data_list.append(temp)

    return data_list

def page_url_generator(conf_dict, global_dict, results):
    log = global_dict['log']

    page_dict = results[0]
    page_urls = []
    params = None
    if 'static_params' in conf_dict:
        params = conf_dict['static_params']

    count_temp = page_dict[conf_dict['count_key']]
    try:
        count = int(count_temp)
    except Exception as e:
        log.error(u'页数转int错误\n%s', traceinfo(e))
        time.sleep(1)
        raise Exception()

    del page_dict[conf_dict['count_key']]
    if params != None:
        params_temp = dict(params, **page_dict)
    else:
        params_temp = page_dict

    for i in range(conf_dict['start_page'], count/conf_dict['page_count']+1):
        page = {conf_dict['count_key'] : i * conf_dict['index_count']}
        params_all = dict(params_temp, **page)
        url_dict = json.dumps({'url':conf_dict['url'], 'params':params_all})
        page_urls.append(url_dict)
        log.debug(url_dict)

    return page_urls

def strip_texts(conf_dict, global_dict, results):
    log = global_dict['log']
    log.debug('strip_texts:%s', results)
    returns = []
    for res in results:
        if isinstance(res, list):
            returns.append(strip_texts(conf_dict, global_dict, res))
        else:
            returns.append(res.strip())

    return returns

def delete_empty_strings(conf_dict, global_dict, results):
    log = global_dict['log']
    log.debug('delete_empty_strings:%s', results)
    returns = []
    for res in results:
        if isinstance(res, list):
            returns.append(delete_empty_strings(conf_dict, global_dict, res))
        else:
            if res != '':
                returns.append(res)

    return returns
