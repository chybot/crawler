# -*- coding: utf-8 -*-
# Created by David on 2016/5/6.

import sys
import json

sys.path.append("qyxx_all")
from CrawlerBeijing import CrawlerBeijing
from CrawlerJiangxi import CrawlerJiangxi
from util.HolderUtil import HolderUtil
from CrawlerGuangdong import CrawlerGuangdong
from CommonLib.WebContent import SeedAccessReport

reload(sys)
sys.setdefaultencoding('utf-8')


def callbackFromOuterControl(company_dict, html_dict):
    print "开始执行外部回调方法"
    result_json = json.dumps(company_dict, ensure_ascii=False)
    print("企业信息抓取结果：\n" + result_json)
    pass


def testFunction():
    from PIL import ImageGrab
    im = ImageGrab.grab()
    im.save("D:\\snap.jpg")
    pass


def beijingTest():
    crawler = CrawlerBeijing('beijing', callbackFromOuterControl)
    return crawler.crawl(u'北京中关村科技投资有限公司')


def jiangxiTest():
    crawler = CrawlerJiangxi('jiangxi', callbackFromOuterControl)
    return crawler.crawl(u'江西丰谷米业有限公司')


def jiangxiUrlTest():
    crawler = CrawlerJiangxi('jiangxi', callbackFromOuterControl)
    # crawler.crawl_url('http://gsxt.jxaic.gov.cn/ECPS/ccjcgs/ccjcgs_ccjcgsIndexDetail.pt?qylx=1229&qyid=3606002012081600243944&zch=9136060006346630XD&tabName=1', u'鹰潭市信江海融小额贷款股份有限公司')
    crawler.crawlUrl(
        'http://gsxt.jxaic.gov.cn/ECPS/ccjcgs/ccjcgs_ccjcgsIndexDetail.pt?qylx=1130&qyid=362123001022006083000030&zch=9136072278728603X7&tabName=1',
        u'江西丰谷米业有限公司')


def guangdongTest():
    crawler = CrawlerGuangdong('guangdong', callbackFromOuterControl)
    use_case_failed = [u'乐星电缆（无锡）有限公司广州分公司', u'中铁四局集团电气化工程有限公司广州分公司', u'中建担保有限公司广州分公司', ]
    use_case = [u'东莞市中兆房地产开发有限公司', u'东莞市中交车联通讯技术有限公司', u'北京利凯时科工贸有限公司深圳分公司', u'北京中海外物业管理有限公司深圳分公司',
                u'前海优仕艾（深圳）国际商务有限公司', u'深圳市亚克喜多斯电子科技', ]
    for case in use_case:
        report = crawler.crawl(case)
        pass


if __name__ == '__main__':
    report = jiangxiTest()
    pass
