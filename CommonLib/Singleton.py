# -*- coding: utf-8 -*-
# Created by Leo on 16/05/12
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


class Singleton(type):
    """Singleton Metaclass"""

    def __init__(cls, name, bases, dic):
        super(Singleton, cls).__init__(name, bases, dic)
        cls.instance = None

    def __call__(cls, *args, **kwargs):
        # print "__CALL__ used"
        if cls.instance is None:
            cls.instance = super(Singleton, cls).__call__(*args, **kwargs)
        return cls.instance

    def getInstance(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = super(Singleton, cls).__call__(*args, **kwargs)
        return cls.instance



if __name__ == '__main__':
    pass