# -*- coding: utf-8 -*-
__author__ = 'xww'
import  logging


def get_logger(filename):
    """
    通过文件名获取日志对象并返回
    :param filename: 日志文件名
    :return: 日志对象
    """

    logger1 = logging.getLogger(filename)
    logger1.setLevel(logging.DEBUG)

    fh = logging.FileHandler(filename.decode("utf-8").encode("gb18030"))
    formatter = logging.Formatter(fmt="%(asctime)s %(filename)s [line:%(lineno)d] %(levelname)s %(message)s'",datefmt='%a,%Y-%m-%d %H:%M:%S')
    fh.setFormatter(formatter)
    logger1.addHandler(fh)

    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('%(name)s:%(levelname)-7s %(message)s')
    console.setFormatter(formatter)
    logger1.addHandler(console)

    return logger1

