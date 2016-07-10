# -*- coding: utf-8 -*-
# Created by Leo on 16/04/20
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.append('../qyxx_all')
sys.path.append('qyxx_all')
sys.path.append('xgxx')
sys.path.append('../xgxx')

import importlib


class ClassFactory:
    """
    The factory is for creating class.

    @version:1.0
    @author:Leo
    @modify:
    """

    def __init__(self):
        """Construct the factory instance
        """
        pass;

    @staticmethod
    def getClassInst(module_name, class_name=None, package_name=None, **kwargs):
        """
        static method used to get class instance in a module ,
        default class name is the module name
        :param module_name: python file name which include the class definition
        :param class_name: class name used to create a instance
        :return: instance created use class name
        """
        if not class_name:
            class_name = module_name
            # if no class name ,make module name as the class name

        try:
            # import module
            # if package_name:
            #     module_name = package_name +"."+ module_name
            module = importlib.import_module(module_name, package_name)
            # get class
            klass = getattr(module, class_name)
            inst = klass(**kwargs)

        except Exception as e:
            print (str(e))
            # inst = "Can't import " + str(class_name) + "\n" + str(sys.exc_info()[1]);
            raise
        return inst;


if __name__ == '__main__':
    pass
