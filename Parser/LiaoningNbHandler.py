# -*- coding: utf-8 -*-
# Created by fml on 2016/6/22.

import sys
import os
import re
import json
import copy
import chardet
from lxml import etree
from ParserNbBase import ParserNbBase
import html4test as test
reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

class LiaoningNbHandler(ParserNbBase):
    """
    ParserShanghai is used to parse the enterprise info from Shanghai
    @version:1.0
    @author:david ding
    @modify:
    """
    def __init__(self, pinyin):
        """
        Initiate the parameters.
        """
        ParserNbBase.__init__(self, pinyin)

    def parse(self, html_dict, reslt_dict=None):
        if not html_dict or not isinstance(html_dict, dict):
            return None
        if 'company_name' in html_dict:
            self.log.info(u"开始解析 %s" % html_dict['company_name'])
        self.log.info(u"开始解析通用信息")
        company = self.parseCommon(html_dict)
        self.log.info(u"通用信息解析完成")
        qynb = company.get('qynb',{})
        body = self.getWeb(html_dict)
        network = self.getTsw(body)
        qynb[u'网站或网店信息'] = network
        tzPaging = self.tzPaging(body)
        qynb[u'对外投资信息'] = tzPaging
        dbPaging = self.getdbPaging(body)
        qynb[u'对外提供保证担保信息'] = dbPaging
        xgPaging = self.getxgPaging(body)
        qynb[u'修改记录'] = xgPaging
        company['qynb'] = qynb
        company_copied = copy.deepcopy(company)
        if reslt_dict and isinstance(reslt_dict, dict):
            reslt_dict.update(company_copied)
        result_json = json.dumps(reslt_dict, ensure_ascii=False)
        self.log.info(u"LiaoningNbHandler解析结果：\n" + result_json)
        return reslt_dict
    def getxgPaging(self,body):
        '''
        修改记录
        :param body:
        :return:
        '''
        xg_list = []
        compile_str = re.compile('tzPaging\((\[.*?\])\)', re.S)
        tz = re.search(compile_str, body)
        if not tz:
            return xg_list
        tsw = tz.group(1)
        tz = json.loads(tsw)
        _dict = {
                u'修改事项':'alt',
                u'修改前':'altbe',
                u'修改后':'altaf',
                u'修改日期':'getAltdatevalue'}
        xg_list_temp = self.changeList(tz, _dict)
        index = 1
        for dd in xg_list_temp:
            dd[u'序号'] = index
            xg_list.append(dd)
            index+=1
        return xg_list
    def getdbPaging(self,body):
        '''
        对外提供保证担保信息
        :param body:
        :return:
        '''
        db_list = []
        #dbPaging([])
        compile_str = re.compile('dbPaging\((\[.*?\])\)', re.S)
        tz = re.search(compile_str, body)
        if not tz:
            return db_list
        tsw = tz.group(1)
        tz = json.loads(tsw)
        _dict = {u'债权人':'more',
                u'债务人':'mortgagor',
                u'主债权种类':'priclaseckindvalue',
                u'主债权数额':'priclasecam',
                u'履行债务的期限':'pefperformandto',
                u'保证的期间':'guaranperiodvalue',
                u'保证的方式':'gatypevalue',
                u'保证担保的范围':'ragevalue'}
        db_list = self.changeList(tz, _dict)
        return db_list
    def tzPaging(self,body):
        '''
        获取对外投资信息
        :param body:
        :return:
        '''
        tz_list = []
        compile_str = re.compile('tzPaging\((\[.*?\])\)', re.S)
        tz = re.search(compile_str, body)
        if not tz:
            return tz_list
        tsw = tz.group(1)
        tz = json.loads(tsw)
        _dict = {u'投资设立企业或购买股权企业名称':'inventname',u'统一社会信用代码/注册号':'regno'}
        tz_list = self.changeList(tz,_dict)
        return tz_list
    def getTsw(self,body):
        '''
        网站或网店信息
        :param html_dict:
        :return:
        '''
        tsw_list =[]
        compile_str = re.compile('swPaging\((\[.*?\])\)',re.S)
        tsw = re.search(compile_str,body)
        if not tsw:
            return tsw_list
        tsw = tsw.group(1)
        tsw = json.loads(tsw)
        _dict = {u'类型':'typofwebName',u"名称":'websitname',u'网址':'domain'}
        tsw_list = self.changeList(tsw,_dict)
        return tsw_list

    def changeList(self,_list,_dict):
        '''
        根据_dict修改网页list为我们自己的list
        :param _list:
        :param _dict:
        :return:
        '''
        __list=[]
        for ll in _list:
            dd = dict()
            for x,y in _dict.items():
                dd[x] = ll.get(y,'')
            __list.append(dd)
        return __list

    def getWeb(self, html_dict):
        '''
        获取web对象指定的年报body
        :param html_dict:
        :return:
        '''
        web = None
        keys_filter = filter(lambda x:'qynb' in x, html_dict.keys())
        if not keys_filter:
            return web
        web = html_dict[keys_filter[0]]
        if not web :
            return web
        web = web[0]
        web = web.get('_body')
        if keys_filter[0].endswith('json') and isinstance(web,basestring):
            web = json.loads(web)
        return web



if __name__ == "__main__":
    pass


