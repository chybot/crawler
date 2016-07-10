# -*- coding: utf-8 -*-
__author__="xww"
import re
import chardet

def strip(str):
    """
    去除字符串左右空格，如果为None则转换为空unicode字符串
    :param (unicode): 字符串
    :return: (unicode)   去除左右空格后的字符串，如果为None则转换为空unicode字符串
    """
    if str is None:
        return u""
    else:
        return str.strip()


def stripall(str):
    """
    去除字符串所有全角半角空格，如果为None则转换为空unicode字符串
    :param str: (unicode) 字符串
    :return: （unicode) 去掉所有半角和全角空格的字符串
    """
    if str==None:
        return u""
    else:
        return str.strip().replace(' ',"").replace(u'　','').replace("\t","").replace("\r\n","")

def remove_all_space_char(ss):
    """
    去掉所有的不可见字符，包括空格，换行等等
    :param ss:
    :return:
    """
    result=  re.sub(r'[\x00-\x20]', ' ', ss)
    return re.sub(r'\s+',' ', result)


def is_chinese(uchar):
    """
    判断单个unicode字符是否是汉字
    :param uchar:  unicode字符
    :return: (bool) 是否是中午字符
    """
    if not isinstance(uchar,unicode):
        return False
    if uchar >= u'\u4e00' and uchar<=u'\u9fa5':
        return True
    else:
        return False


def is_number(uchar):
    """
     判断一个unicode是否是数字
    :param uchar: (unicode) 单个unicode
    :return:(bool) 是否是数字
    """
    if uchar >= u'\u0030' and uchar<=u'\u0039':
        return True
    else:
        return False

def is_alphabet(uchar):
    """
    判断一个unicode是否是英文字母
    :param uchar: (unicode) 单个unicode字符
    :return: (bool) 是否是英文字母
    """
    if (uchar >= u'\u0041' and uchar<=u'\u005a') or (uchar >= u'\u0061' and uchar<=u'\u007a'):
        return True
    else:
        return False


def is_other(uchar):
    """
     判断是否非汉字，数字和英文字符
    :param uchar:  (unicode) 单个unicode字符
    :return:  （bool) 是否非汉字，数字和英文字符
    """
    if not (is_chinese(uchar) or is_number(uchar) or is_alphabet(uchar)):
        return True
    else:
        return False


def B2Q(uchar):
    """
    半角转全角
    :param uchar: (unicode) 单个半角字符
    :return: (unicode) 转换后的单个半角字符
    """

    inside_code=ord(uchar)
    if inside_code<0x0020 or inside_code>0x7e:      #不是半角字符就返回原来的字符
            return uchar
    if inside_code==0x0020: #除了空格其他的全角半角的公式为:半角=全角-0xfee0
            inside_code=0x3000
    else:
            inside_code+=0xfee0
    return unichr(inside_code)



def Q2B(uchar):
    """
    单个全角字符转半角字符，如果不是全角则返回原来的字符
    :param uchar: (str) 单个全角字符
    :return: (str) 单个半角字符
    """
    inside_code=ord(uchar)
    if inside_code==0x3000:
        inside_code=0x0020
    else:
        inside_code-=0xfee0

    if inside_code<0x0020 or inside_code>0x7e:      #转完之后不是半角字符返回原来的字符
        return uchar

    return unichr(inside_code)


def stringQ2B(ustring):
    """
    把字符串全角转半角，如果不是全角则返回原来的字符
    :param ustring:  (str) 全角字符串转换为半角
    :return:
    """
    return "".join([Q2B(uchar) for uchar in ustring])

def stringB2Q(ustring):
    """
    把字符串全角转半角，如果不是全角则返回原来的字符
    :param ustring:  (str) 全角字符串转换为半角
    :return:
    """
    return "".join([B2Q(uchar) for uchar in ustring])

def uniform(ustring):
    """
    格式化字符串，完成全角转半角，大写转小写的工作
    :param ustring: (str)  字符串
    :return:  (str) 格式化后的字符串
    """

    return stringQ2B(ustring).lower()



def string2List(ustring):
    """
    将字符串按照中文，字母，数字分开，并放到集合里面
    :param ustring: (str) 字符串
    :return: (list) 分开后的字符串序列
    """
    retList=list()
    utmp=list()
    for uchar in ustring:
        if is_other(uchar):
            if len(utmp)==0:
                continue
            else:
                retList.append("".join(utmp))
                utmp=[]
        else:
            utmp.append(uchar)

    if len(utmp)!=0:
        retList.append("".join(utmp))

    return retList

def splitChinese(word):
    """
    把字符串分给为一个集合，一个汉字是1个元素，汉字之间的非汉字字符算一个元素
    :param word:  (str) 字符串
    :return:  分割后的集合，一个汉字是1个元素，汉字之间的非汉字字符算一个元素
    """
    word=word.strip().replace(u' ',u"").replace(u"　",u"")
    words=[]
    alpha=""
    for w in word:
        if is_chinese(w):
            if alpha !="":
                words.append(alpha)
            words.append(w)
            alpha=""
        else:
            alpha+=w
    if alpha !="":
        words.append(alpha)
    return words


def len_cmp(x,y):
    """
    比较字符串,返回比较结果。
    :param x:  (unicode) 字符串x
    :param y:  (unicode) 字符串y
    :return:  (int)  比较结果 -> 0:字符串长度相等，1:字符串x长度大于字符串y 2:字符串x长度小于字符串y
    """
    if len(x)>len(y):
        return -1
    elif len(x)<len(y):
        return 1
    else:
        return 0

def analyzer(word_old,min=1,max=0,filter_start=None,filter_end=None):
    """
    把字符串分词，返回分词集合
    1、如果字符串以filter_start集合中某个元素开头则过滤掉前缀，如果有多个元素默认过滤最长的一个
    2、如果字符串以filter_end集合中某个元素结尾则过滤掉该后缀，如果有多个元素默认过滤最长的一个
    3.使用暴力分词，分出的词长度在min-max之间，包含min和max。max为0则默认为字符串长度
    :param word_old: (unicode)字符串
    :param min: (int) 字符最小分割长度
    :param max: (int)分割出来的最大字符长度
    :param filter_start:(set) 前缀字符过滤
    :param filter_end: (set) 过滤字符规律
    :return: (list)  分词后的集合，集合的每个元素就是一个分词
    """
    word=word_old
    if filter_start is not None:
        filter_start=list(filter_start)
        filter_start.sort(cmp=len_cmp)
        for filter_k in filter_start:
            if word.startswith(filter_k):
                word=word[len(filter_k):]
                break

    if filter_end is not None:
        filter_end=list(filter_end)
        filter_end.sort(cmp=len_cmp)
        for filter_k in filter_end:
            if word.endswith(filter_k):
                word=word[0:word.find(filter_k)]
                break

    words=splitChinese(word)
    list_result=[]
    words_len=len(words)
    if min>1:
        if words_len>=min:
            if max==0:
                max=len(words)
            for i in range(min,max+1):
                for j in range(0,words_len-i+1):
                    word1=u"".join(words[j:j+i])
                    list_result.append(word1)
    if word!=word_old:
        list_result.append(word_old)
    return list_result



def analyzer_prefix(word_old,min=1,max=0,filter_start=None,filter_end=None):
    """
    对关键字进行切分。分出的词必须是关键字的前缀
    1、如果字符串以filter_end集合中某个元素结尾则过滤掉该后缀，如果有多个元素默认过滤最长的一个
    2.使用暴力分词，分出的词长度在min-max之间，包含min和max。max为0则默认为字符串长度
    :param word_old:  关键字
    :param min:  最小分割长度
    :param max:  最大分割长度
    :param filter_start: (set)  前缀过滤词集合,废弃
    :param filter_end: (set) 后缀过滤词集合
    :return: (list)  分词后的词组集合
    """
    word=word_old
    if filter_end is not None:
        filter_end=list(filter_end)
        filter_end.sort(cmp=len_cmp)
        for filter_k in filter_end:
            if word.endswith(filter_k):
                word=word[0:word.find(filter_k)]
                break
    words=splitChinese(word)
    list_result=[]
    words_len=len(words)
    if min>1:
        if words_len>=min:
            if max==0:
                max=len(words)
            for i in range(min,max+1):
                word1="".join(words[0:i])
                list_result.append(word1)
    if word!=word_old:
        list_result.append(word_old)
    return list_result


def is_code(rawdata):
    """
    自动检测字符串的编码格式并返回
    :param rawdata:  (str) 字符串
    :return: (str) 编码
    """
    info = chardet.detect(rawdata)
    return info['encoding']

def strQ2B(ustring):
    """全角转半角"""
    rstring = ""
    for uchar in ustring:
        inside_code=ord(uchar)
        if inside_code == 12288:                              #全角空格直接转换
            inside_code = 32
        elif (inside_code >= 65281 and inside_code <= 65374): #全角字符（除空格）根据关系转化
            inside_code -= 65248

        rstring += unichr(inside_code)
    return rstring

def strB2Q(ustring):
    """半角转全角"""
    rstring = ""
    for uchar in ustring:
        inside_code=ord(uchar)
        if inside_code == 32:                                 #半角空格直接转化
            inside_code = 12288
        elif inside_code >= 32 and inside_code <= 126:        #半角字符（除空格）根据关系转化
            inside_code += 65248

        rstring += unichr(inside_code)
    return rstring

if __name__=="__main__":
    import webutil
    # rawdata=webutil.request("http://www.jumei.com/")
    # print  is_code(rawdata)
    # for i in analyzer(u"张三丰",min=2):
    #     print i.encode("GBK")
    # list_result=analyzer(u'中国上海张三丰有限公司',min=2, filter_start={u"上海",u"中国上海",u"中国"},filter_end={u"公司",u"有限公司"})
    # for l in list_result:
    #     print l
    # for word in analyzer_prefix(u'福州豪亨世家餐饮管理有限公司',min=3,filter_end=[u"有限公司"]):
    #     print word
    ss="惠而浦（中国）投资有限公司"
    ss=ss.decode("UTF-8","ignore").strip()

   # ss=ss.encode("UTF-8")

    import chardet
    #print chardet.detect(ss)
    print strQ2B(u"%s"%ss)
    print strB2Q(u"%s"%ss)
    sss =set()
    sss.add(u"%s"%ss)
    sss.add(strQ2B(u"%s"%ss))
    sss.add(strB2Q(u"%s"%ss))
    print sss