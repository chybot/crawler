# -*- coding: utf-8 -*-
"""
xpath解析工具模块
"""
__author__ = 'xww'

def get_objs(tree,xpath,errorinfo=""):
    """
    获取dom树种指定xpath表达式的节点
    :param tree:(lxml.etree._Element) dom树
    :param xpath: (str) xpath表达式 -> .//html/body/div
    :param errorinfo: (str） 错误信息
    :return: (lxml.etree._Element)节点
    """

    objs=tree.xpath(xpath)
    if len(objs)<1:
        if errorinfo:
            raise Exception(errorinfo+u" XPath解析错误,xpath:"+xpath)
        else:
            raise Exception(u"XPath解析错误,xpath:"+xpath)
    else:
        return objs



def getobject(tree,xpath,num=0,errorinfo=""):
    """
    获取dom树种指定xpath表达式的第num个节点
    :param tree: (lxml.etree._Element) dom树
    :param xpath: (str) xpath表达式 -> .//html/body/div
    :param num:(int)  位置 ->0
    :param errorinfo:(str)  错误信息  ->  公司名解析错误
    :return:  (lxml.etree._Element) 节点
    """
    content=tree.xpath(xpath)
    if len(content)<num+1:
        if errorinfo:
            raise Exception(errorinfo+u" XPath解析错误,xpath:"+xpath)
        else:
            raise Exception(u"XPath解析错误,xpath:"+xpath)
    else:
        return content[num]



def getatt(tree,xpath,num=0,errorinfo="",att=""):
    """
    返回dom树指定xpath位置的属性内容
    :param tree: (lxml.etree._Element) dom树
    :param xpath:(str) xpath表达式 -> .//html/body/div
    :param num:(int)  位置 ->0
    :param errorinfo:(str)  错误信息  ->  公司名解析错误
    :param att:(str) 属性名->href
    :return: (str) 属性内容
    """
    try:
        obj=getobject(tree,xpath,num,errorinfo)
        return obj.get(att)
    except Exception as e:
        if errorinfo:
            raise Exception(errorinfo+u" XPath解析错误,节点没有该属性。xpath:"+xpath+" "+"att:"+att)
        else:
            raise Exception(u"XPath解析错误,节点没有该属性。xpath:"+xpath+" "+"att:"+att)

def gethref(tree,xpath,num=0,errorinfo=""):
    """
    返回dom树指定xpath位置的href内容
    :param tree: (lxml.etree._Element) dom树
    :param xpath:(str) xpath表达式 -> .//html/body/div
    :param num:(int)  位置 ->0
    :param errorinfo:(str)  错误信息  ->  公司名解析错误
    :return:(str) href属性内容
    """
    return getatt(tree,xpath,num=num,errorinfo=errorinfo,att="href")

def getsrc(tree,xpath,num=0,errorinfo=""):
    """
    返回dom树指定xpath位置节点的src属性内容
    :param tree:  (lxml.etree._Element) dom树
    :param xpath: (str) xpath表达式 -> .//html/body/div
    :param num: (int)  位置 ->0
    :param errorinfo: (str)  错误信息  ->  公司名解析错误
    :return: (str) src属性内容
    """
    return getatt(tree,xpath,num=num,errorinfo=errorinfo,att="src")

def gettext(tree,xpath,num=0,errorinfo=""):
    """
    返回指定节点文本内容
    :param tree:  (lxml.etree._Element) dom树
    :param xpath: (str) xpath表达式 -> .//html/body/div
    :param num:    (int)  位置 ->0
    :param errorinfo:  (str)  错误信息  ->  公司名解析错误
    :return: (unicode) 文本内容
    """
    obj=getobject(tree,xpath,num,errorinfo)
    return obj.text

def gettexts(tree,xpath,errorinfo="",sepa=","):
    """
    获取xpath指定的多个节点的text内容，用分割符串成一个字符串返回
    :param tree: (lxml.etree._Element) dom树
    :param xpath: (str) xpath表达式 -> .//html/body/div
    :param errorinfo: (str)  错误信息  ->  公司名解析错误
    :param sepa:  （str) 分割字符 ->,
    :return:(str) 用分割符穿起来的多个节点的文本内容
    """
    result=""
    first=True
    for obj in get_objs(tree,xpath):
        if not first:
            result+=sepa
        else:
            first=False
        obj_text=obj.text
        if obj_text is None:
            obj_text=""
        else:
            obj_text=obj_text.strip()
        result+=obj_text
    return result

def get_all_text(tree,xpath,num=0,split=u" "):
    """
    获取指定节点的所有子节点的文本内容，用分割符分割并返回
    :param tree: (lxml.etree._Element) dom树
    :param xpath:  (str) xpath表达式 -> .//html/body/div
    :param num: (int) 位置 ->0
    :param split (unicode) 分隔符
    :return: (unicode) 用分隔符分割的指定节点的所有子节点的文本内容
    """
    text_all=u""
    entry=tree.xpath(xpath)
    if len(entry)>num:
        texts=entry[num].xpath(".//text()")
        for text in texts:
            text_all+=text
            text_all+=split
    return text_all

def parse_single_table0(table):
    """
    处理键值对的table类型数据
    :param table: table
    :return: (dict) 数据内容
    """
    result=dict()


    #处理tbody
    tbody=table.xpath("./tbody")
    if tbody!=None and len(tbody)>0:
        trs=tbody[0].xpath("./tr")
    else:
        trs=table.xpath("./tr")

    if trs==None or  len(trs)==0:
        raise Exception(u"找不到tr")

    for tr in trs:
        tds=tr.xpath("./td")
        ths=tr.xpath("./th")

        if  len(tds)+len(ths)<2:
            continue
        elif len(ths)>0 and len(tds)>0:
            i=0
            for th in ths:
                if len(tds)<=i:
                    break
                td=tds[i]
                if th.text!=None and  len(th.text)>0 and td.text!=None and len(td.text)>0:
                    th_text=th.text.strip().replace(":","").replace(u"：","")
                    td_text=td.text.strip().replace(":","").replace(u"：","")
                    if len(td_text)>0 and len(th_text)>0:
                        result[th_text]=td_text
                i+=1

        elif len(ths)==0 and len(tds)>=2:
            for i in range(len(tds)/2):
                if tds[i*2].text!=None and len(tds[i*2].text)>0 and tds[i*2+1].text!=None and len(tds[i*2+1].text)>0:
                    key_text=tds[i*2].text.strip().replace(":","").replace(u"：","")
                    value_text=tds[i*2+1].text.strip().replace(":","").replace(u"：","")
                    if len(key_text)>0 and len(value_text)>0:
                        result[key_text]=value_text
        else:
            print len(ths),len(tds)
            raise Exception(u"格式不匹配")

    if len(result)>0:
        return result
    else:
        raise Exception(u"没有数据")


def parse_single_table(tree,xpath,index=0):
    """
    处理键值对的table类型数据
    :param tree: 目录数
    :param xpath: （str） table标签的xpath表达式
    :return: (dict) 数据内容
    """
    result=dict()

    #找到存在的table标签
    table=tree.xpath(xpath)

    #找不到table
    if table==None or len(table)<=index:
        raise Exception(u"找不到table标签")


    #处理tbody
    tbody=table[index].xpath("./tbody")
    if tbody!=None and len(tbody)>0:
        trs=tbody[0].xpath("./tr")
    else:
        trs=table[index].xpath("./tr")

    if trs==None or  len(trs)==0:
        raise Exception(u"找不到tr")


    for tr in trs:
        tds=tr.xpath("./td")
        ths=tr.xpath("./th")

        if  len(tds)+len(ths)<2:
            continue
        elif len(ths)>0 and len(tds)>0:
            i=0
            for th in ths:
                if len(tds)<=i:
                    break
                td=tds[i]
                if th.text!=None and  len(th.text)>0 and td.text!=None and len(td.text)>0:
                    th_text=th.text.strip().replace(":","").replace(u"：","")
                    td_text=td.text.strip().replace(":","").replace(u"：","")
                    if len(td_text)>0 and len(th_text)>0:
                        result[th_text]=td_text
                i+=1

        elif len(ths)==0 and len(tds)>=2:
            for i in range(len(tds)/2):
                if tds[i*2].text!=None and len(tds[i*2].text)>0 and tds[i*2+1].text!=None and len(tds[i*2+1].text)>0:
                    key_text=tds[i*2].text.strip().replace(":","").replace(u"：","")
                    value_text=tds[i*2+1].text.strip().replace(":","").replace(u"：","")
                    if len(key_text)>0 and len(value_text)>0:
                        result[key_text]=value_text
        else:
            print len(ths),len(tds)
            raise Exception(u"格式不匹配")

    if len(result)>0:
        return result
    else:
        raise Exception(u"没有数据")

def parse_single_table2(tree,xpath,index=0):
    """
    处理键值对的table类型数据
    :param tree: 目录数
    :param xpath: （str） table标签的xpath表达式
    :return: (dict) 数据内容
    """
    result=dict()

    #找到存在的table标签
    table=tree.xpath(xpath)

    #找不到table
    if table==None :
        raise Exception(u"找不到table标签")

    #处理tbody
    tbody=table[index].xpath("./tbody")
    if tbody!=None and len(tbody)>0:
        trs=tbody[0].xpath("./tr")
    else:
        trs=table[index].xpath("./tr")

    if trs==None or  len(trs)==0:
        raise Exception(u"找不到tr")


    for tr in trs:
        tds=tr.xpath("./td")
        ths=tr.xpath("./th")
        number=2
        if  len(tds)+len(ths)<2:
            continue
        elif len(ths)>0 and len(tds)>0:
            i=0
            for th in ths:
                if len(tds)<=i:
                    break
                td=tds[i]
                th_text="".join(th.xpath(".//text()")).replace(":","").replace(u"：","")
                td_text="".join(td.xpath(".//text()")).replace(":","").replace(u"：","")
                if len(td_text)>0 and len(th_text)>0:
                    if key_text in result.keys():
                            key_text=key_text+str(number)
                            number+=1
                    result[th_text]=td_text
                i+=1

        elif len(ths)==0 and len(tds)>=2:
            for i in range(len(tds)/2):
                if tds[i*2].text!=None and len(tds[i*2].text)>0 and tds[i*2+1].text!=None and len(tds[i*2+1].text)>0:
                    key_text="".join(tds[i*2].xpath(".//text()")).strip().replace(":","").replace(u"：","")
                    value_text="".join(tds[i*2+1].xpath(".//text()")).strip().replace(":","").replace(u"：","")

                    if len(key_text)>0 and len(value_text)>0:
                        if key_text in result.keys():
                            key_text=key_text+str(number)
                            number+=1
                        result[key_text]=value_text
        else:
            print len(ths),len(tds)
            raise Exception(u"格式不匹配")

    if len(result)>0:
        return result
    else:
        raise Exception(u"没有数据")
import functions
def parse_multi_table(tree,xpath,index=0):
    """
    处理多行的的table类型数据
    :param tree: 目录数
    :param xpath: （str） table标签的xpath表达式
    :return: (dict) 数据内容
    """
    result=list()

    #找到存在的table标签
    table=tree.xpath(xpath)

    #找不到table
    if table==None or len(table)<=index:
        raise Exception(u"找不到table标签")

    #处理tbody
    tbody=table[index].xpath("./tbody")
    if tbody!=None and len(tbody)>0:
        trs=tbody[0].xpath("./tr")
    else:
        trs=table[index].xpath("./tr")

    if trs==None or  len(trs)<2:
        raise Exception(u"找不到tr")


    tds=trs[0].xpath("./td")
    tds_len=len(tds)
    if tds_len<1:
        ths=trs[0].xpath("./th")
        tds_len=len(ths)
        if tds_len<1:
            raise  Exception(u"没有标题项")
        title=list()
        for th in ths:
            title.append( u" ".join(th.xpath(".//text()")))

    else:
        title=list()
        for td in tds:
            title.append( u" ".join(td.xpath(".//text()")))


    for tr in trs[1:]:
        data_tds=tr.xpath("./td")
        if len(data_tds) !=tds_len:
            continue
        line=dict()
        i=0
        for data_td in data_tds:
            title[i]=functions.remove_all_space_char(title[i])
            line[title[i]]=  u" ".join(data_td.xpath(".//text()"))
            i+=1
        result.append(line)


    if len(result)>0:
        return result
    else:
        raise Exception(u"没有数据")

