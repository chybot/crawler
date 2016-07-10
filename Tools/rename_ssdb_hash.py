# -*- coding: utf-8 -*-
# Created by Leo on 16/05/24
import sys



reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.append('../')
from CommonLib.DB.DBManager import DBManager
import json
def rename():
    """
    把 ssdb 里面hash 重命名，把旧的拷贝到新的里面
    :return:
    """
    # name_list = ["beijing"]
    q_name = "new_beijing"
    db_inst = DBManager.getInstance("ssdb", q_name, host = "spider5", port = 57888)
    # rowkey = 4
    rk=u"4ab61b0438638de25f6a68ba9b2834a5|_|北京梅牡易贷科技服务有限公司|_|beijing|_|2016-05-25"
    src_dic = db_inst.hget(rk)
    print src_dic
    with open("ttt.txt","w") as f:
        f.write(src_dic)
    # for name in name_list:
    #     get_table = "new_" + name+ "_data"
    #     put_table = "new_" + name
    #
    #     db_inst.changeTable(get_table)
    #     while db_inst.hsize()>0:
    #
    #         src_dic = db_inst.hget()
    #         k=json.loads(src_dic)["rowkey"]
    #         print "get key:",k
    #         db_inst.changeTable(put_table)
    #         db_inst.hset(k,src_dic)
    #         db_inst.changeTable(get_table)




if __name__ == '__main__':
    rename()