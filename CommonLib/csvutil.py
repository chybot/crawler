# -*- coding: utf-8 -*-
__author__ = 'xww'


def filter(item):
    """
    把全角的逗号转换为半角的逗号
    :param str: (str) 字符串
    :return: 转换后的字符串
    """
    if not isinstance(item,basestring):
        item=unicode(item)
    return  item.replace(u',',u'，').replace("\n","").replace("\r","").replace("\r\n","")

def write(f,*line,**config):
    """
    把行迭代器的内容导入文件
    :param f:  (file) 文件句柄
    :param line:  (tuple) 包含零行或多行内容的元组
    :return: (None)
    """
    encoding="UTF-8"
    if isinstance(config,dict) and config.has_key("encoding"):
        encoding=config["encoding"]
    first=True
    for item in line:
        if not first:
            f.write(u','.encode(encoding))
        else:
            first=False
        f.write(filter(item).encode(encoding,"ignore"))
    f.write("\n")
