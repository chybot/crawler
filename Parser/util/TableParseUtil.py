# -*- coding: utf-8 -*-
# Created by David on 2016/4/20.

from lxml import etree
import chardet
import json
import parser_util_html as phtml
from Parser.ParserMapper import ParserMapper
from Parser.parser_map_config import transform

class ParseMapperConfig(object):
    pass

class TableElementType(object):
    '''
    表格类型枚举
    '''
    th = 0
    td = 1
    tr = 2

class TableColumnStructure(object):
    '''
    存放表格中列节点的结构，适用于th、td
    '''
    
    def __init__(self, type, value, hierarchy, col_span=1, row_span=1):
        '''
        :param type: 节点类型：td或th
        :param value: 存放节点的文本值
        :param hierarchy: 根据节点位于的层次结构和占用的列宽span计算而来,该值自树顶由上而下变化为自大至小
        :param col_span: 节点占用的列宽
        :param row_span: 节点占用的行宽
        :return:
        '''
        self.type = type
        self.value = value.strip() if value else ''
        self.hierarchy = (10-hierarchy)*10+col_span
        self.col_span = col_span
        self.row_span = row_span
        self.row_span_used = 1


class TableStructure(object):
    '''
    节点结构和信息层次构造的核心类
    '''

    def __init__(self):
        '''
        Initiate the parameters.
        '''
        self.th_list = []           # 存放所有th节点，其中每个th均按层次结构构造
        self.td_list = []         # 存放当前待处理的td节点
        self.th_last_list = []    # 存放self.th_list中最后一个节点中最底层节点集合
        self.info_dict = {}         # 以字典形式存放获取到的键值对信息
        self.info_list = []         # 存放字典的list
        self.reuse_times = 0        # 复用计数

    def canReuse(self):
        '''
        指出该Table是否可以被复用，以下三种情况会被复用
        1.仅有head
        2.复用次数小于1次
        3.value长度小于等于1，广东gzaic容错
        :return:
        '''
        if not self.hasOnlyHead():
            return False

        if self.reuse_times >= 1:
            return False

        if self.th_list and self.th_list[-1]:
            valid = False
            for tc in self.th_list[-1]:
                if tc.value and len(tc.value.strip()) > 1:
                    valid = True
            if not valid:
                return False

        self.reuse_times += 1
        return True

    def appendRow(self, row, hierarchy):
        '''
        append one row into the TableStructrue
        :param row: the row to append
        :param hierarchy: the hierarchy of the row
        :return:
        '''
        if row is None or len(row) == 0:
            return
        children = row.getchildren()
        self.appendList(children, hierarchy)

    def getTagText(self, child):
        if child is None:
            return ''
        value = child.text or ''
        grandson = child.getchildren()
        if not grandson:
            return value
        # 仅当当前节点不是主标题表头时，才提取补全text信息
        if self.th_list and grandson[0].tag in ["br","span", "a"]:
            txt = grandson[0].text or grandson[0].tail
            value += txt or ''
        '''
        if not value or not value.strip():
            if grandson[0].tag == "a" and grandson[0].attrib:
                value = str(grandson[0].attrib)
        '''
        return value

    def appendList(self, children, hierarchy):
        '''
        insert
        :param children:
        :param hierarchy:
        :return:
        '''
        if children is None or len(children) == 0:
            return

        self.th_last_list = []
        self.td_list = []
        for child in children:
            colspan = 1
            if child.attrib:
                if 'colspan' in child.attrib and child.attrib['colspan']:
                    colspan = int(child.attrib['colspan'])
            '''
            value = child.text
            if not value or not value.strip():
                grandson = child.getchildren()
                if grandson and len(grandson)>0:
                    if grandson[0].tag == "a" and grandson[0].attrib:
                        value = str(grandson[0].attrib)
                    elif grandson[0].tag == "span":
                        value = grandson[0].text
            '''
            value = self.getTagText(child)
            if child.tag == 'th':
                rowspan = 1
                if child.attrib:
                    if 'rowspan' in child.attrib and child.attrib['rowspan']:
                        rowspan = int(child.attrib['rowspan'])
                column = TableColumnStructure(TableElementType.th, value, hierarchy, colspan, rowspan)
                # 下层colspan比上层colspan大时，清空被重用的表标题
                if self.reuse_times >=1 and self.th_list and self.th_list[-1] and self.th_list[-1][0].col_span < colspan:
                    self.__init__()
                    self.reuse_times = 0
                self.appendHead(column)
            elif child.tag == 'td':
                column = TableColumnStructure(TableElementType.td, value, hierarchy, colspan)
                self.appendContent(column)
        # 是否同一行th、td混排
        mixed = len(self.th_last_list)>0 and len(self.td_list)>0
        if self.th_last_list:
            self.reuseHead()
            self.th_list.append(self.th_last_list)
        if self.td_list:
            self.zipHeadContent()
        if mixed:
            self.th_list.remove(self.th_last_list)

    def reuseHead(self):
        '''
        重用上一行占据多行的th
        :return:
        '''
        if not self.th_list:
            return
        th_reusable_list = self.th_list[-1]
        # 用于计算列偏移
        col_span = 0
        for i in range(0, len(th_reusable_list)):
            col = th_reusable_list[i]
            col_span += col.col_span-1
            # 若未跨行，或跨行扩展已经达到所跨行数，则不再扩展
            if col.row_span <= 1 or col.row_span_used >= col.row_span:
                continue
            insert_position = i+col_span
            if insert_position >= len(self.th_last_list):
                self.th_last_list.append(col)
            else:
                self.th_last_list.insert(insert_position, col)
            col.row_span_used += 1
            
    def appendHead(self, column):
        '''
        添加表头，并按colspan进行扩展
        :param column: 要加入的列
        :return:
        '''
        if not column or not column.value:
            return
        for i in range(0, column.col_span):
            self.th_last_list.append(column)

    def appendContent(self, column):
        '''
        添加表内容，并按colspan进行扩展
        :param column: 要加入的列
        :return:
        '''
        if not column:
            return
        for i in range(0, column.col_span):
            self.td_list.append(column)

    def zipHeadContent(self):
        '''
        zip标题与结果信息，分几种情况：
        1.key值有冲突，将上次dict存入list
        2.key值无冲突则直接存入
        :return:
        '''
        if not self.th_list or not self.td_list:
            return
        # 当表头重用后，若表头colspan出现前小后大的情况，对齐表头，例如：广东企业信息网年报
        if self.reuse_times >= 1 and len(self.th_list) >= 2:
            len_last = len(self.th_list[-1])
            for i in range(0, len(self.th_list)-1):
                len_cur = len(self.th_list[i])
                if len_cur != 1:
                    continue
                for j in range(len_cur, len_last):
                    self.th_list[i].append(self.th_list[i][0])
        # 计算最短的列表长度
        len_short = 9999
        for li in self.th_list:
            if len(li) < len_short:
                len_short = len(li)
        if len(self.td_list) < len_short:
            len_short = len(self.td_list)

        for i in range(0, len_short):
            key = ""
            for j in range(0, len(self.th_list)):
                li = self.th_list[j]
                # 应对跨行标题扩展的情况
                if j>0 and li[i] == self.th_list[j-1][i]:
                    continue
                key += li[i].value+"."
            '''
            for li in self.th_list:
                # 应对跨行标题扩展的情况
                if i>0 and li[i].value==li[i-1].value:
                    continue
                key += li[i].value+"."
            '''
            key = key.rstrip(".")
            # 处理同一行key值冲突问题，例如：主要人员信息中同一行会出现相同的key
            # 但类似广东股东详情中本应为认缴出资方式和实缴出资方式的head均为出资方式，此时需要额外计算
            if key in self.info_dict:
                # 此处判断sameHead做法不可行，广东股东详情问题需要额外处理
                # if self.sameHead(self.th_list[-1][0:i-1], self.th_list[-1][i:]):
                self.info_list.append(self.info_dict)
                self.info_dict = dict()
            self.info_dict[key] = self.td_list[i].value

    def sameHead(self, head_list1, head_list2):
        if head_list1 == head_list2:
            return True
        if not head_list2 or not head_list1:
            return False
        if len(head_list1) != len(head_list2):
            return False
        for i in range(0, len(head_list1)):
            if head_list1[i] != head_list2[i]:
                return False
        return True

    def cleanup(self):
        '''
        表格信息抽取和重构后的最后清理：
        1. 回收info字典中的结果
        '''
        if self.info_dict:
            self.info_list.append(self.info_dict)

    def hasOnlyHead(self):
        '''
        判断是否仅包含了标题，但收集的数据为空，适用于某些将表头和内容分开放置到不同表格的情况
        例如：西藏企业信息
        :return:
        '''
        if self.isEmpty() and self.th_list:
            return True
        return False

    def isEmpty(self):
        '''
        判断是否为空
        :return: True：为空，False：不为空
        '''
        if self.info_list or self.info_dict:
            return False
        return True

    def show(self):
        '''
        将获取到的所有信息输出到控制台
        :return:
        '''
        if not self.info_list:
            self.info_list.append(self.info_dict)
        for info in self.info_list:
            for key in info:
                print key+" = "+info[key]
            print "-----------------------------------------"


class TableParseUtil(object):
    '''
    解析页面中关心的标题和值信息，目前仅支持table
    未来考虑扩展到其它情况
    '''

    def __init__(self, html):
        '''
        初始化
        :param html: 传入的页面内容
        :return:
        '''
        self.html = html
        self.tables = []

    def parse(self):
        '''
        开始解析，外部调用解析器的入口
        :return: 返回所有解析出来的table中的关键信息
        '''
        # 页面编码检测
        try:
            encoding = chardet.detect(self.html)['encoding']  # 此处检测有时会出异常
            tree = etree.HTML(self.html.decode(encoding))
        except:
            tree = etree.HTML(self.html)
        tables_html = tree.xpath(".//table")
        for table in tables_html:
            # 当上一个表格无数据但有标题时，复用上一次表格
            if self.tables and self.tables[-1].canReuse():
                ts = self.tables[-1]
                self.parseElement(ts, table, 1)
            else:
                ts = TableStructure()
                self.parseElement(ts, table, 1)
                self.tables.append(ts)
            # 清理工作:回收未触发zip条件的剩余结果
            ts.cleanup()
        # 封装结果给出以list和dict包装的标准输出
        result_list = []
        for ts in self.tables:
            ts.show()
            if ts.info_list:
                result_list.extend(ts.info_list)
            elif ts.info:
                result_list.append(ts.info)

        return result_list

    def parseElement(self, ts, element, hierarchy):
        '''
        递归调用解析，直至将所有节点遍历完成
        :param ts: 存放解析结果的Table结构
        :param element: 当前需要解析的节点
        :param hierarchy: 当前节点所处的层次，每递归一次加1
        :return:返回本次遇到的标签格式，若跳过tr直接遇到th或td，则会返回th或td,暂未考虑tr或th下再次嵌套的情况
        '''
        if element.tag == 'tr':
            ts.appendRow(element, hierarchy)
            return TableElementType.tr
        elif element.tag == 'th':
            return TableElementType.th
        elif element.tag == 'td':
            return TableElementType.td

        children = element.getchildren()
        if children:
            col_list = []
            for i in range(0, len(children)):
                child = children[i]
                # 用于处理th成行但tr标签不规范的情况，若不提前处理col_list，将可能导致th和td处理先后顺序发生颠倒
                if col_list and child.tag in ['th','td'] and i<len(children)-1 and children[i+1].tag == "tr":
                    col_list.append(child)
                    ts.appendList(col_list, hierarchy)
                    col_list = []
                    continue
                ele_type = self.parseElement(ts, child, hierarchy+1)
                if ele_type == TableElementType.th or ele_type == TableElementType.td:
                    col_list.append(child)
            if col_list:
                ts.appendList(col_list, hierarchy)
        return None


if __name__ == "__main__":
    a_tag = '<a rel="2" href="javascript:">2</a>'
    page_no = a_tag[a_tag.find('>')+1:a_tag.find('</a')]
    et = etree.HTML(a_tag)
    pass
    '''
    parser = TableParseUtil(phtml.enterprise_html_base)
    parser.parse()
    parser = TableParseUtil(phtml.enterprise_html_partner)
    parser.parse()
    parser = TableParseUtil(phtml.enterprise_html_changedinfo)
    parser.parse()
    parser = TableParseUtil(phtml.enterprise_html_key_member)
    parser.parse()


    parser = TableParseUtil(phtml.enterprise_html_xizang)
    parser.parse()

    parser = TableParseUtil(phtml.enterprise_html_gdxx_xizang)
    parser.parse()

    parser = TableParseUtil(phtml.enterprise_html_lilezhongguo)
    parser.parse()
    parser = TableParseUtil(phtml.enterprise_html_jingxi_zyry)
    parser.parse()
    parser = TableParseUtil(phtml.enterprise_html_guangdong_szxy)
    parser.parse()
    parser = TableParseUtil(phtml.enterprise_html_jiangxi_jbxx)
    parser.parse()
    parser = TableParseUtil(phtml.enterprise_html_beijing_gdxq)
    parser.parse()

    parser = TableParseUtil(phtml.enterprise_html_jiangxi_fzjg)
    parser.parse()

    parser = TableParseUtil(phtml.enterprise_html_guangdong_gdxq)
    parser.parse()
    parser = TableParseUtil(phtml.enterprise_html_jiangxi_gdxx)
    parser.parse()
    '''

    '''
    parser = TableParseUtil(phtml.enterprise_jyyc)
    result_list = parser.parse()
    company_mapped = ParserMapper.doMap(transform, result_list)
    result_json = json.dumps(company_mapped, ensure_ascii=False)
    print ("企业信息映射结果：\n" + result_json)
    pass
    '''

    '''
    parser = TableParseUtil(phtml.en_beijing_xzcf)
    parser.parse()

    parser = TableParseUtil(phtml.en_bj_dengjijiguan)
    parser.parse()
    '''
    parser = TableParseUtil(phtml.en_beijing_xzcf)
    parser.parse()

    pass









