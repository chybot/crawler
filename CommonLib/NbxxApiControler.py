# -*- coding: utf-8 -*-
"""
年报信息抓取接口模块
"""
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import time
sys.path.append("../")
from CommonLib.DB.DBManager import DBManager
from Config.ConfigGet import ConfigGet
fp = 'NbxxApiControler.ini'
f = lambda x:ConfigGet(fp).get('db',x)


class NbxxApiControler(object):
    def __init__(self):
        self.__db = DBManager.getInstance(f('type'),f('table'), server=f('server'))

    def getRowkey(self,**kwargs):
        '''
        获取rowkey
        :param kwargs:mapping:company_name,company_zch or zch
        :return:
        '''

        company_name = kwargs.get('company_name','')
        zch = kwargs.get('company_zch','')
        zch = zch if zch else kwargs.get('zch','')
        pinyin = kwargs.get('pinyin', '')
        rowkey = company_name + '|_|' + zch
        rowkey = rowkey.strip('|_|')
        rowkey = rowkey + '|_|' +pinyin.lower()

        return rowkey.strip('|_|')

    def timeJudgment(self,uptime):
        '''
        判断当前和上次存储的时间间隔,360天
        :param uptime: 上次年报信息的存储时间
        :return:
        '''
        now_time = int(time.time())
        pass_day = (now_time - int(uptime))/3600*24
        if pass_day>=360:
            return True
        return False

    def visitJudgement(self,**kwargs):
        '''
        判断该rowkey是否访问
        :param kwargs: company_name,company_zch or zch
        :return: 是否访问年报信息，True=访问，False=不访问，set()：那些年份不需要访问
        '''
        rowkey = self.getRowkey(**kwargs)
        data = None
        data = self.__db.find(id = rowkey)
        if not data:
            #如果solr出现连接问题，则默认不抓取年报信息，主要是避免因为solr出现问题，影响企业信息的抓取
            return False,{}
        data = data['docs']
        if not data:
            return True,{}
        data = data[0]
        uptime = data.get('uptime',0)
        has_years = set(data.get('has_years',[]))
        if uptime:
            return True,has_years
        return False,has_years

    def nbUpdate(self,**kwargs):
        '''
        更新数据
        :param kwargs:mapping:company_name,company_zch or zch
        :return:
        '''
        rowkey = self.getRowkey(**kwargs)
        data = None
        data = self.__db.find(id = rowkey)
        if not data:
            data = {}
        data = data['docs']
        if data:
            data = data[0]
        if not data:
            data = {}
        if 'years_list' in kwargs:
            has_years = data.get('has_years',[])
            has_years.extend(kwargs['years_list'])
            data['id'] = rowkey
            company_name = kwargs['company_name'] if 'company_name' in kwargs else ''
            if company_name:
                data['company_name'] = company_name
            zch = kwargs['company_zch'] if 'company_zch' in kwargs else ''
            zch = zch if zch else kwargs['zch'] if zch in kwargs else ''
            if zch:
                data['company_zch'] = zch
            pinyin = kwargs.get('pinyin', '')
            if pinyin:
                data['pinyin'] = pinyin.lower()
            data['has_years'] = list(set(has_years))
            data['uptime'] = time.time()
            data['do_time'] = time.strftime('%Y-%m-%d')
            self.nbSave(data)
            return True
        return False

    def nbSave(self,data):
        '''
        年报信息存储到更新db
        :param data:
        :return:
        '''
        self.__db.update(data)

if __name__ == '__main__':
    nbxx = NbxxApiControler()
    #nbxx.visitJudgement(company_zch='123132123')
    #print nbxx.nbUpdate('')
    data = {'company_zch':'12354252345345X','do_time':'2016-03-14','uptime':'12312312',
            'id':'成都数联铭品科技有限公司|_|12354252345345X','has_years':list({2013,2012,2014})}
    #data={"company_name":"asdfasdfasdf123123"}
    #nbxx.nbUpdate(data)
    print nbxx.visitJudgement(company_name=u'成都数联铭品科技有限公司',company_zch='12354252345345X')
    #nbxx.nbUpdate(company_name = '成都数联铭品科技有限公司',company_zch = '12354252345345X',years_list=['2011',2033])

