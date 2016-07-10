# -*- coding: utf-8 -*-
# Created by David on 2016/5/6.

import sys
import json
from CrawlerBeijing import CrawlerBeijing
from CrawlerJiangxi import CrawlerJiangxi
from CrawlerJilin import CrawlerJilin
from CrawlerShanghai import CrawlerShanghai
from CrawlerGuangdong import CrawlerGuangdong
from CrawlerChongqing import CrawlerChongqing
from CrawlerJiangsu import CrawlerJiangsu
from CommonLib.ClassFactory import ClassFactory
from CommonLib.CalcMD5 import calcFileMD5
from CommonLib.DB.DBManager import DBManager
from Seed.Seed import Seed
from CommonLib.WebContent import SeedAccessType
from CommonLib.UniField import UniField
from CommonLib.BbdSeedLogApi import get_logs,STATE
reload(sys)
sys.setdefaultencoding('utf-8')

class CrawlerTester(object):
    seed_dict = None
    pinyin = None
    db_inst = None

def callbackFromOuterControl(html_dict, company_dict):
    print "开始执行外部回调方法"
    result_json = json.dumps(company_dict, ensure_ascii=False)
    html_json = json.dumps(html_dict, ensure_ascii=False)
    print("企业信息抓取结果：\n" + result_json)
    print("企业信息页面内容：\n" + html_json)
    pass

def storeResult(src_dict, company_dict=None):
    src_dict = UniField.unifyRequestResult(src_dict, CrawlerTester.pinyin)
    src_dict.update({"BBD_SEED": CrawlerTester.seed_dict})
    if src_dict["status"] == 0:
        CrawlerTester.db_inst.changeTable("new_" + CrawlerTester.pinyin)
        CrawlerTester.db_inst.save(src_dict)
    else:
        CrawlerTester.db_inst.changeTable("new_" + CrawlerTester.pinyin + "_error")
        CrawlerTester.db_inst.save(src_dict)

def testByKeyword(crawler, pinyin, keyword):
    CrawlerTester.pinyin = pinyin
    CrawlerTester.seed_dict = {"name": keyword}
    CrawlerTester.db_inst = DBManager.getInstance("ssdb", "new_" + CrawlerTester.pinyin, host="spider5", port=57888)
    return crawler.crawl(CrawlerTester.seed_dict['name'])

#region 北京测试用例
def beijingTest():
    crawler = CrawlerBeijing('beijing', storeResult)
    # crawler = CrawlerBeijing('beijing', callbackFromOuterControl)
    # return crawler.crawl(u'北京中关村科技投资有限公司')
    # return crawler.crawl(u'北京博图广告有限公司')
    # return crawler.crawl(u'110101013146061')
    # return crawler.crawl(u'讯和创新科技（北京）有限公司') # 备案信息翻页
    # return crawler.crawl(u'北京我爱我家房地产经纪有限公司') # 分支机构翻页
    return testByKeyword(crawler, 'beijing', u'北京宝加通达商贸有限公司')

def beijingNoCompanyTest():
    crawler = CrawlerBeijing('beijing', callbackFromOuterControl)
    return crawler.crawl(u'额滴神')

def beijingNoUrlTest():
    crawler = CrawlerBeijing('beijing', callbackFromOuterControl)
    return crawler.crawl(u'')  # solr中未得到有效测试用例
#endregion

#region 吉林测试
def jilinTest():
    crawler = CrawlerJilin('jilin', storeResult)
    # return crawler.crawl(u'长春丽明科技开发股份有限公司') # 有股东信息、变更信息
    # return crawler.crawl(u'四平市铁东区东红商贸有限公司') # 有备案信息
    # return crawler.crawl(u'长白山森工集团安图林业有限公司安林物流中心分公司') # 页面上完全无备案信息、分支机构的展示
    return testByKeyword(crawler, 'jilin', u'暴风科技')

def jilinNoCompanyTest():
    crawler = CrawlerJilin('jilin', callbackFromOuterControl)
    return crawler.crawl(u'额滴神')

def jilinNoUrlTest():
    crawler = CrawlerJilin('jilin', callbackFromOuterControl)
    return crawler.crawl(u'')  # solr中未查询到有效测试用例

def jilinUrlTest():
    crawler = CrawlerJilin('jilin', callbackFromOuterControl)
    return crawler.crawlUrl('http://211.141.74.198:8081/aiccips/pub/gsgsdetail/1229/4a091d4728a4a6609970cfb781be8072fe98167674d68a164d038e94e2c39c6f7eee3f8fa4f3276bc1904b769f07c14b', u'长春丽明科技开发股份有限公司')  # 暂无有效测试用例
#endregion

#region 上海测试
def shanghaiTest():
    crawler = CrawlerShanghai('shanghai', callbackFromOuterControl)
    # return crawler.crawl(u'上海佳吉快运有限公司')
    return crawler.crawl(u'上海乾辉工贸有限公司')

def shanghaiNoCompanyTest():
    crawler = CrawlerShanghai('shanghai', callbackFromOuterControl)
    return crawler.crawl(u'额滴神')

def shanghaiNoUrlTest():
    crawler = CrawlerShanghai('shanghai', callbackFromOuterControl)
    return crawler.crawl(u'')  # solr中未查询到有效测试用例

def shanghaiUrlTest():
    crawler = CrawlerShanghai('shanghai', callbackFromOuterControl)
    return crawler.crawlUrl('https://www.sgs.gov.cn/notice/notice/view?uuid=.9hSOfdfnXHnMSj10ENrtjwgrGN7qdly&tab=01', u'上海佳吉快运有限公司')
#endregion

#region 江西测试
def jiangxiTest():
    crawler = CrawlerJiangxi('jiangxi', callbackFromOuterControl)
    return crawler.crawl(u'大润发投资有限公司')

def jiangxiNoCompanyTest():
    crawler = CrawlerJiangxi('jiangxi', callbackFromOuterControl)
    return crawler.crawl(u'额滴神')

def jiangxiNoUrlTest():
    crawler = CrawlerJiangxi('jiangxi', callbackFromOuterControl)
    return crawler.crawl(u'360406210006292')

# 此用例未测试
def jiangxiSearchListPageTest():
    crawler = CrawlerJiangxi('jiangxi', callbackFromOuterControl)
    return crawler.crawl(u'汽车')

def jiangxiUrlTest():
    crawler = CrawlerJiangxi('jiangxi', callbackFromOuterControl)
    # crawler.crawl_url('http://gsxt.jxaic.gov.cn/ECPS/ccjcgs/ccjcgs_ccjcgsIndexDetail.pt?qylx=1229&qyid=3606002012081600243944&zch=9136060006346630XD&tabName=1', u'鹰潭市信江海融小额贷款股份有限公司')
    crawler.crawlUrl('http://gsxt.jxaic.gov.cn/ECPS/ccjcgs/ccjcgs_ccjcgsIndexDetail.pt?qylx=1130&qyid=362123001022006083000030&zch=9136072278728603X7&tabName=1', u'江西丰谷米业有限公司')
#endregion

def chongqing():
    crawler = CrawlerChongqing('chongqing',callbackFromOuterControl)
    crawler.crawl(u'力帆')

def jiangsu():
    crawler = CrawlerJiangsu('jiangsu',callbackFromOuterControl)
    crawler.crawl(u'科技')

# 广东测试
def guangdongTest():
    crawler = CrawlerGuangdong('guangdong', callbackFromOuterControl)
    # 广州广之旅国际旅行社股份有限公司 有股东、备案翻页， 广州顺丰速运有限公司有变更翻页，未找到分支机构翻页用例
    use_case_gz_page = [u'广州荷银财富投资管理有限公司', u'广州广之旅国际旅行社股份有限公司', u'广州顺丰速运有限公司', ]
    # 佛山市南湖国际旅行社股份有限公司 有股东、变更、备案、分支机构翻页
    use_case_qyxx = [u'佛山市南湖国际旅行社股份有限公司', u'东莞市中兆房地产开发有限公司']
    # 深圳所有信息均显示在一个页面，暂未发现翻页情况
    use_case_szxy = [u'深圳市赛格导航科技股份有限公司', u'深圳市富安娜家居用品股份有限公司', u'深圳市泰富华投资发展有限公司', ]
    for case in use_case_gz_page:
        crawler.crawl(case)
        pass

def guangdongUrlTest():
    crawler = CrawlerGuangdong('guangdong', callbackFromOuterControl)
    #crawler.crawlUrl("http://gsxt.gzaic.gov.cn/aiccips/GSpublicity/GSpublicityList.html?service=entInfo_VyznKbbsOHihyw1haIERaq0ZDWNtFjBQpdN5IZEHByA=-7PUW92vxF0RgKhiSE63aCw==", u"广州顺丰速运有限公司")
    crawler.crawlUrl("http://gsxt.gdgs.gov.cn/aiccips/GSpublicity/GSpublicityList.html?service=entInfo_8ib+VekqC3GPzaIBEnVY2vixZG4tLbsXct4lf4uHtcJTAOYLpc4gxgb5a3wjX8k3-Yo1vDaPPmlocGn8BN2rqNg==", u"佛山市南湖国际旅行社股份有限公司")
    #crawler.crawlUrl("http://www.szcredit.com.cn/web/GSZJGSPT/QyxyDetail.aspx?rid=c86af17328134138a78574c90e49d585", u"深圳市赛格导航科技股份有限公司")

def guangdongNoCompanyTest():
    crawler = CrawlerGuangdong('guangdong', callbackFromOuterControl)
    return crawler.crawl(u'额滴神')

if __name__ == '__main__':
    beijingTest()
    pass
