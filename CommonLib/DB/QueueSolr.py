# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from solrcloudpy import SolrConnection#,SearchOptions
import logging
import json
import QueueBase
log = logging.getLogger(__name__)

class QueueSolr(object):
    """
    SolrDB 连接模块
    """
    def __init__(self,table,server=None,**kwargs):
        """
        :param server: list or str
        :param table: collection
        :param kwargs:  detect_live_nodes=False,
                         user=None,
                         password=None,
                         timeout=10,
                         webappdir='solr'
        :return:
        """
        if 'host' in kwargs:
            del kwargs['host']
        if 'port' in kwargs:
            del kwargs['port']
        self.conn = SolrConnection(server = server,**kwargs)
        self.table=table
        self.collection=self.conn[table]
    @QueueBase.catch
    def collections(self):
        """
        获取所以集合列表
        :return:
        """
        return self.conn.list()

    @QueueBase.catch
    def find(self,*args,**kwargs):
        """
        查找某个集合下的field
        查找的字段必须键索引
        否则会报400 error
        :param args:
        :param kwargs:
        :return:
        """
        for dict_ in args:
            if isinstance(dict_,dict):
                kwargs.update(dict_)
        valuess = ' AND '.join(['%s:%s'%(k,v) for k,v in kwargs.items()]) if len(kwargs)>1 else ':'.join(kwargs.keys() + kwargs.values())
        q_item={'q':valuess}
        #q_item=SearchOptions().commonparams.q(valuess)
        return self.collection.search(q_item).result['response']

    @QueueBase.catch
    def update(self,*args,**kwargs):
        """
        更新数据
        更新的数据字段
        原表必须存在，*_temp都可以
        :param args:
        :param kwargs:
        :return:
        """
        for dict_ in args:
            if isinstance(dict_,dict):
                kwargs.update(dict_)
        self.collection.add([kwargs])
        log.info(u"%s Storage success!"% json.dumps(kwargs))

    @QueueBase.catch
    def delete(self,*args,**kwargs):
        """
        删除数据
        删除的字段原表也必须存在
        否则400 Client Error: Bad Request
        :param args:
        :param kwargs:
        :return:
        """
        for dict_ in args:
            if isinstance(dict_,dict):
                kwargs.update(dict_)
        valuess = ' AND '.join(['%s:%s'%(k,v) for k,v in kwargs.items()]) if len(kwargs)>1 else ':'.join(kwargs.keys() + kwargs.values())
        q_item={'q':valuess}
        self.collection.delete(q_item,commit=False)
        log.info(u"%s deleted!"% json.dumps(kwargs))

if __name__ == '__main__':
    # from solrcloudpy import     SearchOptions
    # se=SearchOptions().commonparams.q()
    solr=QueueSolr('qyxx',server=["118.123.9.77:8983","118.123.9.77:8984","118.123.9.77:8985"])
    data={"name_seed":"京文唱片有限公司",
        "type":"anhui",
          "mse_seed":'您搜索的条件无查询结果'}
    print solr.update(data)
    print solr.find(data)