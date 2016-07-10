# coding=utf-8
__author__ = 'rubin'

import time
import datetime
import smtplib
import traceback
import RedisQueue
from email.mime.text import MIMEText
import sys
reload(sys)
sys.path.append("../")
import robin_util.mongo_util as mongo_util


# 日常邮件列表
# mail_to_tuple = ("hehongjing@brandbigdata.com", "xuweiwei@brandbigdata.com", "liqian@brandbigdata.com", "yanrubin@brandbigdata.com", "yinkang@brandbigdata.com", "fumenglin@brandbigdata.com", "jiangtian@brandbigdata.com", "wutong@brandbigdata.com")
# 排查邮件列表
# mail_to_tuple_ourselves = ("hehongjing@brandbigdata.com", "xuweiwei@brandbigdata.com", "yanrubin@brandbigdata.com", "fumenglin@brandbigdata.com", "jiangtian@brandbigdata.com")
mail_to_tuple = ("yanrubin@brandbigdata.com",)
mail_to_tuple_ourselves = ("yanrubin@brandbigdata.com",)
# 设置服务器
mail_host = "smtp.ym.163.com"
# 账号
mail_user = "monitor@brandbigdata.com"
# 密码
mail_pass = "brandbigdata"
# 数据库对象
mongo = mongo_util.Mongo_Connection("master", 25017)
# 不遍历数据库以及表
db_black_list = ("admin", "config", "qyxx")
table_black_list = ("system.indexes", "monitor", "startup_log", "qyxx_monitor", "robin_test_monitor", "robin_test_qyxx_monitor", "qyxx_shard", "qyxx_shard_idhash", "jumei_hzp_product_short_old", "jumei_hzp_product_info_copy", "jumei_hzp_presale", "bigdata_higgs")
table_description_dic = {"zgcpwsw": u"中国裁判文书网", "ywg": u"义乌购", "jumei_hzp": u"聚美品牌信息", "qyxx": u"企业信息网", "jumei_hzp_product_info": u"聚美产品信息", "jumei_hzp_user_info": u"聚美用户信息", "jumei_hzp_product_reportp": u"聚美品牌信息", "jumei_hzp_user_buy": u"用户购买记录", "jumei_hzp_user_shortp": u"用户短评记录", "jumei_hzp_relation": u"用户关系", "jumei_hzp_user_reportp": u"聚美用户评论", "autohome_brand": u"汽车之家品牌信息", "autohome_car_comment": u"汽车之家评论", "autohome_car_deal": u"汽车之家经销商", "vip_brand_info": u"唯品会品牌信息", "vip_brand_expect": u"唯品会预期品牌", "vip_brand_daily": u"唯品会每日上新", "vip_brand_comment": u"唯品会评论", "vip_product_info": u"唯品会产品内容", "jumei_hzp_product_short": u"聚美商品短评", "jumei_hzp_top": u"聚美每日上新品牌", "jumei_hzp_top_product": u"聚美每日上新产品", "jumei_hzp_expect": u"聚美3日预期", "train_12306": u"火车票", "super_auditors": u"并购雷达（中财网）", "mafengwo": u"马蜂窝", "ktgg": u"开庭公告", "train_12306_checi": u"火车票车次", "qyxx_shangbiao": u"企业信息商标", "moji_airball": u"墨迹空气果站点", "moji_airball_info": u"墨迹空气果站点监测数据", "qyxx_zhuanli": u"企业信息专利", "sjt": u"数据堂", "wowotuan": u"窝窝团", "tdzr": u"土地转让", "tddy": u"土地抵押", "alibaba_category": u"阿里巴巴类别信息", "alibaba_company": u"阿里巴巴企业信息", "alibaba_company_girl": u"阿里巴巴企业女装信息", "zhilian_city": u"智联招聘城市", "zhilian_job": u"智联招聘职位", "recruit": u"招聘表", "job51_soure_url": u"51job城市职位", "dcos": u"双软认证", "overseas_investment": u"境外投资", "dishonesty": u"失信", "high_tech": u"高新企业", "chain_communication_auth": u"中国通信咨询认证网-增值电信业务经营许可证", "d_user": u"搜索系统用户表", "qyxx_haiguanzongshu": u"中国海关总署-海关登记信息", "management_system_certification": u"管理体系认证", "qyxx_food_prod_cert": u"食品生产许可获证企业", "qyxx_tjjfood_prod_cert": u"国家食品药品监督管理局-食品添加剂生产许可证", "qyxx_hzp_pro_prod_cert": u"国家食品药品监督管理局-化妆品生产许可证", "qyxx_medi_jy_prod_cert": u"国家食品药品监督管理局-药品经营许可证", "qyxx_medi_pro_prod_cert": u"国家食品药品监督管理局-药品生产许可证", "qyxx_gmpauth_prod_cert": u"国家食品药品监督管理局-GMP认证", "qyxx_miit10062": u"互联网服务许可证", "qyxx_food_cert": u"中国食品农产品认证", "qyxx_miit_jlzzdwmd": u"信息系统工程监理资质", "qyxx_nyscqyzzcx": u"农药生产企业资质查询", "qyxx_shuishou": u"税收优惠", "qyxx_comNotice": u"私募基金管理人", "qyxx_industrial_production_permit": u"工业产品生产许可证", "qyxx_enterpriseQualificationForeign": u"通信建设企业资质", "qyxx_wanfang_zhuanli": u"万方专利网", "qyxx_shigongxuke": u"北京建筑施工许可证", "qyxx_ck": u"探矿许可证", "qyxx_tk": u"采矿许可证", "qyxx_finance_xkz": u"金融许可证-金融许可证", "qyxx_sgxkrz": u"四川建设施工许可证", "qyxx_wuye": u"北京物业企业资质", "qyxx_jzsgxkz": u"建筑施工许可证", "qyxx_net_medijy_prod_cert": u"互联网药品交易服务许可证", "qyxx_scfdckf": u"四川房地产开发", "qyxx_gcjljz": u"建筑施工许可证", "qyxx_aqscxkz": u"北京安全生产许可证", "qyxx_sgxkbg": u"北京建筑施工许可证变更", "qyxx_scsgxkz": u"四川施工许可证", "qyxx_jsgcqyzz": u"北京建设工程企业资质", "qyxx_zhongdeng": u"中登网", "qyxx_net_mediinfo_prod_cert": u"国家食品药品监督管理局-互联网药品信息服务许可证"}
qyxx_column_list = (u'上海', u'浙江', u'广东', u"深圳信用网", u'北京', u'江苏', u'福建', u"重庆", u"四川", u"新疆", u"湖北", u"湖南", u'山东', u"河南", u'河北', u'安徽', u"陕西", u'内蒙古', u'天津', u'黑龙江', u'广西', u'辽宁', u'吉林', u'江西', u'山西', u"贵州", u"云南", u'海南', u"西藏", u"甘肃", u"青海", u"宁夏", u"总局")
qyxx_dict = {u'上海': "shanghai", u'浙江': "zhejiang", u'广东': "guangdong", u"深圳信用网": "shenzhenxinyong", u'北京': "beijing", u'江苏': "jiangsu", u'福建': "fujian", u"重庆": "chongqing", u"四川": "sichuan", u"新疆": "xinjiang", u"湖北": "hubei", u"湖南": "hunan", u'山东': "shandong", u"河南": "henan", u'河北': "hebei", u'安徽': "anhui", u"陕西": "shanxixian", u'内蒙古': "neimenggu", u'天津': "tianjin", u'黑龙江': "heilongjiang", u'广西': "guangxi", u'辽宁': "liaoning", u'吉林': "jilin", u'江西': "jiangxi", u'山西': "shanxitaiyuan", u"贵州": "guizhou", u"云南": "yunnan", u'海南': "hainan", u"西藏": "xizang", u"甘肃": "gansu", u"青海": "qinghai", u"宁夏": "ningxia", u"总局": "zongju"}
versions = (1, 2, 3, 4, 5)


def send_mail(to_list, sub, content):
    # 这里的hello可以任意设置，收到信后，将按照设置显示
    me = "server" + "<" + mail_user + ">"
    # 创建一个实例，这里设置为html格式邮件
    msg = MIMEText(content, _subtype='html', _charset='utf-8')
    # 设置主题
    msg['Subject'] = sub
    msg['From'] = me
    msg['To'] = ";".join(to_list)
    s = smtplib.SMTP()
    # 连接smtp服务器
    s.connect(mail_host)
    # 登陆服务器
    s.login(mail_user, mail_pass)
    # 发送邮件
    s.sendmail(me, to_list, msg.as_string())
    s.close()
    return "Sent successfully!"


def get_time_stamp(day):
    """

    :param day: 2014-11-20
    :return: 2014-11-20 00:00:00的时间戳
    """
    day = '{0} {1}'.format(day, '00:00:00')
    time_array = time.strptime(day, "%Y-%m-%d %H:%M:%S")
    time_stamp = int(time.mktime(time_array))
    return time_stamp


def queue_number(key):
    """

    计算每个省份的队列
    :param key:province_pingyin
    :return:
    """
    while True:
        try:
            qu = RedisQueue.getredisQueue(key)
            return qu.size()
        except Exception as e:
            print "Exception:queue_number", e


def try_except_all(func):
    """

    :param func:
    :return:
    """
    def _deco():
        print("before myfunc() called.")
        while True:
            try:
                func()
                break
            except Exception as e:
                print "Exception:try_except_all", e
                print sys.exc_traceback.tb_frame.f_back
                print traceback.print_stack()
                time.sleep(10)
                continue
        print("after myfunc() called.")
        # 不需要返回func，实际上应返回原函数的返回值
    return _deco


def get_today_time_stamp():
    """

    :return:
    """
    today = datetime.date.today()
    today_time_stamp = int(get_time_stamp(today))
    return today_time_stamp


def get_yesterday_time_stamp():
    """

    :return:
    """
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)
    yesterday_time_stamp = int(get_time_stamp(yesterday))
    return yesterday_time_stamp


@try_except_all
def yesterday_count():
    """
    日常
    :return:
    """
    today_time_stamp = get_today_time_stamp()
    yesterday_time_stamp = get_yesterday_time_stamp()

    # 全表统计
    html_1 = u'<table  width="100%" border="1" cellpadding="2" cellspacing="0"><tr><td>数据库</td><td>表</td><td>备注</td><td>今日凌晨0点总条数</td><td>昨日增量条数</td></tr>'
    db_names = mongo.get_db_names()
    html_1_temp = u""
    for db_name in db_names:
        while True:
            html_temp = u""
            try:
                if db_name in db_black_list:
                    break
                table_names = mongo.get_table_names(db_name)
                for table_name in table_names:
                    if table_name in table_black_list:
                        continue
                    table = mongo.get_conn_table(db_name, table_name)
                    sum_count = table.find({'uptime': {"$lt": today_time_stamp}}).count()
                    oneday_count = table.find({'uptime': {'$gte': yesterday_time_stamp, '$lt': today_time_stamp}}).count()
                    table_description = ""
                    if table_name in table_description_dic.keys():
                        table_description = table_description_dic[table_name]
                    html_temp += u"<tr><td>" + db_name + u"</td><td>" + table_name + u"</td><td>" + table_description + u"</td><td>" + str(sum_count) + u"</td><td>" + str(oneday_count) + u"</td></tr>"
                    print "yesterday_count:", table_name
                html_1_temp += html_temp
                break
            except Exception as e:
                print "Exception:html_1_temp", e
                continue
    html_1_temp += u"</table>"
    html_1 += html_1_temp

    # 企业信息统计
    html_3 = u'</br></br><table  width="100%" border="1" cellpadding="2" cellspacing="0"><tr><td>表</td><td>列</td><td>今日凌晨0点总条数</td><td>昨日增量条数</td></tr>'
    out_other_sum = 0
    day_out_other_sum = 0
    html_3_temp = u""
    for column in qyxx_column_list:
        while True:
            html_temp = u""
            try:
                table = mongo.get_conn_table("bigdata_higgs", "qyxx")
                count = table.find({'type': column, 'uptime': {'$lt': today_time_stamp}}).count()
                day_count = table.find({'type': column, 'uptime': {'$gte': yesterday_time_stamp, '$lt': today_time_stamp}}).count()
                html_temp += u"<tr><td>" + 'qyxx' + u"</td><td>" + column + u"</td><td>" + str(count) + u"</td><td>" + str(day_count) + u"</td></tr>"
                out_other_sum += count
                day_out_other_sum += day_count
                print "yesterday_count:", "qyxx", column.encode("gbk", "ignore")
                html_3_temp += html_temp
                break
            except Exception as e:
                print "Exception:html_3_temp", e
                continue
    # 今日凌晨0点总共
    table = mongo.get_conn_table("bigdata_higgs", "qyxx")
    sum_count = table.find({'uptime': {"$lt": today_time_stamp}}).count()
    # 昨日总共增量
    day_sum_count = table.find({'uptime': {'$gte': yesterday_time_stamp, '$lt': today_time_stamp}}).count()
    # 今日凌晨0点其他
    other_count = (sum_count - out_other_sum)
    # 其他昨日总共增量
    day_other_sum = day_sum_count - day_out_other_sum
    html_3_temp += u"<tr><td>" + 'qyxx' + u"</td><td>" + u'其他' + u"</td><td>" + str(other_count) + u"</td><td>" + str(day_other_sum) + u"</td></tr>"
    html_3_temp += u"<tr><td>" + 'qyxx' + u"</td><td>" + u'总共' + u"</td><td>" + str(sum_count) + u"</td><td>" + str(day_sum_count) + u"</td></tr></table>"
    html_3 += html_3_temp

    html = html_1 + html_3

    sub = u"[日常]MongoDB监控报告,时间:" + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print "Mail is sending......"
    while True:
        try:
            print send_mail(mail_to_tuple, sub, html)
            break
        except Exception as e:
            print "Exception:send_mail", e
            time.sleep(10)
            continue


@try_except_all
def today_count():
    """
    排查
    :return:
    """
    # 全表统计
    html_1 = u'<table width="100%" border="1" cellpadding="2" cellspacing="0"><tr><td>数据库</td><td>表</td><td>备注</td><td>当前总条数</td><td>当日增量条数</td></tr>'
    today_time_stamp = get_today_time_stamp()
    db_names = mongo.get_db_names()
    html_1_temp = u""
    for db_name in db_names:
        while True:
            html_temp = u""
            try:
                if db_name in db_black_list:
                    break
                table_names = mongo.get_table_names(db_name)
                for table_name in table_names:
                    if table_name in table_black_list:
                        continue
                    table = mongo.get_conn_table(db_name, table_name)
                    oneday_count = table.find({'uptime': {'$gte': today_time_stamp}}).count()
                    sum_count = table.find().count()
                    table_description = u""
                    if table_name in table_description_dic.keys():
                        table_description = table_description_dic[table_name]
                    html_temp += u"<tr><td>" + db_name + u"</td><td>" + table_name + u"</td><td>" + table_description + u"</td><td>" + str(sum_count) + u"</td><td>" + str(oneday_count) + u"</td></tr>"
                    print "today_count:", table_name
                html_1_temp += html_temp
                break
            except Exception as e:
                print "Exception:html_1_temp", e
                continue
    html_1_temp += u"</table>"
    html_1 += html_1_temp

    # 招聘表统计
    html_2 = u"</br></br><table  width='100%' border='1' cellpadding='2' cellspacing='0'>" + u"<tr><td>表</td><td>列</td><td>现有队列没抓取URL数</td>" + u"<td>当前总条数</td><td>当日增量条数</td>" + u"</tr>"
    source_list = ("zhilian", "51job", "chinahr")
    table = mongo.get_conn_table("bigdata_higgs", "recruit")
    recruit_sum_qu = 0
    html_2_temp = u""
    for src in source_list:
        while True:
            html_temp = u""
            try:
                queue_num = 0
                if src == "zhilian":
                    queue_num = queue_number(u"zhilian:job")
                    recruit_sum_qu += queue_num
                if src == "51job":
                    queue_num = queue_number(u"51job_url:urls")
                    recruit_sum_qu += queue_num
                if src == "chinahr":
                    queue_num = queue_number(u"chinahr_content_queue")
                    recruit_sum_qu += queue_num
                count = table.find({'source': src}).count()
                day_count = table.find({'source': src, 'uptime': {'$gte': today_time_stamp}}).count()
                html_temp += u"<tr><td>" + u"recruit" + u"</td><td>" + src + u"</td><td>" + str(queue_num) + u"</td><td>" + str(count) + u"</td><td>" + str(day_count) + u"</td></tr>"
                print "today_count:", "recruit", src.encode("gbk", "ignore")
                html_2_temp += html_temp
                break
            except Exception as e:
                print "Exception:html_2_temp", e
                continue
    # 当前总共
    sum_count = table.find().count()
    # 当日总共增量
    day_sum_count = table.find({'uptime': {'$gte': today_time_stamp}}).count()
    html_2_temp += u"<tr><td>" + u"recruit" + u"</td><td>" + u'总共' + u"</td><td>" + str(recruit_sum_qu) + u"</td><td>" + str(sum_count) + u"</td><td>" + str(day_sum_count) + u"</td></tr></table>"
    html_2 += html_2_temp

    # 企业信息统计
    title_column = u""
    for ver in versions:
        title_column += u"<td>当前总条数(V%d)</td><td>当日增量条数(V%d)</td>" % (ver, ver)
    html_3 = u"</br></br><table  width='100%' border='1' cellpadding='2' cellspacing='0'>" + u"<tr><td>表</td><td>列</td><td>现有队列未抓取公司数</td>" + title_column + u"</tr>"
    table = mongo.get_conn_table("bigdata_higgs", "qyxx")
    sum_qu = 0
    html_3_temp_1 = u""
    for column in qyxx_column_list:
        # 各省企业信息
        while True:
            html_temp = u"<tr><td>" + u"qyxx" + u"</td>"
            try:
                # 获取当前队列长度
                queue_num = queue_number(u"%s:company_name" % qyxx_dict[column])
                sum_qu += queue_num
                html_temp += u"<td>" + column + u"</td><td>" + str(queue_num) + u"</td>"
                for ver in versions:
                    # 当前条数
                    count = table.find({'type': column, 'version': ver}).count()
                    # 当日增量条数
                    day_count = table.find({'type': column, 'version': ver, 'uptime': {'$gte': today_time_stamp}}).count()
                    html_temp += u"<td>" + str(count) + u"</td><td>" + str(day_count) + u"</td>"
                html_temp += u"</tr>"
                print "today_count:", "qyxx", column.encode("gbk", "ignore")
                html_3_temp_1 += html_temp
                break
            except Exception as e:
                print "Exception:html_3_temp", e
                continue
    # 企业信息总量统计
    html_3_temp_2_1 = u"<tr><td>" + u"qyxx" + u"</td><td>" + u'其他' + u"</td><td>" + u"0" + u"</td>"
    html_3_temp_2_2 = u"<tr><td>" + u"qyxx" + u"</td><td>" + u'总共' + u"</td><td>" + str(sum_qu) + u"</td>"
    for ver in versions:
        while True:
            html_temp_1 = u""
            html_temp_2 = u""
            try:
                # 各省当前条数统计
                count_sum = 0
                # 各省当日增量条数统计
                day_count_sum = 0
                for column in qyxx_column_list:
                    count_sum += table.find({'type': column, 'version': ver}).count()
                    day_count_sum += table.find({'type': column, 'version': ver, 'uptime': {'$gte': today_time_stamp}}).count()
                # 当前总共
                sum_count = table.find({'version': ver}).count()
                other_sum = sum_count - count_sum
                # 当日总共增量
                day_sum_count = table.find({'version': ver, 'uptime': {'$gte': today_time_stamp}}).count()
                day_other_sum = day_sum_count - day_count_sum

                html_temp_1 += u"<td>" + str(other_sum) + u"</td><td>" + str(day_other_sum) + u"</td>"
                html_temp_2 += u"<td>" + str(sum_count) + u"</td><td>" + str(day_sum_count) + u"</td>"
                html_3_temp_2_1 += html_temp_1
                html_3_temp_2_2 += html_temp_2
                break
            except Exception as e:
                print "Exception:html_3_temp_2", e
                continue
    html_3_temp_2_1 += u"</tr>"
    html_3_temp_2_2 += u"</tr>"
    html_3 += html_3_temp_1
    html_3 += html_3_temp_2_1
    html_3 += html_3_temp_2_2
    html_3 += u"</table>"

    html = html_1 + html_2 + html_3

    sub = u"[排查]MongoDB监控报告,时间:" + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    print time.strftime("%Y-%m-%d %H:%M:%S")
    print "Mail is sending......"
    while True:
        try:
            print send_mail(mail_to_tuple_ourselves, sub, html)
            break
        except Exception as e:
            print "Exception:send_mail", e
            time.sleep(10)
            continue


if __name__ == '__main__':
    mistake_second = 0
    now = time.localtime()
    hour = now[3]
    if hour == 7:
        start_time = time.time()
        yesterday_count()
        print "yesterday_count elapse time:", time.time() - start_time
        mistake_second += time.time() - start_time

    start_time = time.time()
    yesterday_count()
    print "yesterday_count elapse time:", time.time() - start_time

    start_time = time.time()
    today_count()
    print "today_count elapse time:", time.time() - start_time
    mistake_second += time.time() - start_time
    time.sleep(60 * 60 - mistake_second)

    while True:
        mistake_second = 0
        now = time.localtime()
        hour = now[3]
        if hour == 7:
            start_time = time.time()
            yesterday_count()
            print "yesterday_count elapse time:", time.time() - start_time
            mistake_second += time.time() - start_time
            start_time = time.time()
            today_count()
            print "today_count elapse time:", time.time() - start_time
            mistake_second += time.time() - start_time
        elif 7 <= hour <= 23:
            start_time = time.time()
            today_count()
            print "today_count elapse time:", time.time() - start_time
            mistake_second += time.time() - start_time

        time.sleep(60 * 60 - mistake_second)