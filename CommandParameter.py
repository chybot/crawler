# -*- coding: utf-8 -*-
# Created by Leo on 16/04/20
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class CommandParameter:
    """CMDParameter is the class for initializing args from commandline
    @version:1.0
    @author:leoding
    @modify:
    """
    def __init__(self):
        """Initiate the parameter dict.
        """
        self.parameters = {}
    def setProperty(self,key,value):
        """Input the (key,value) into the parameter dict.
        @param:key
        @param:value
        """
        self.parameters[key] = value
    def getProperty(self, key):
        """get value from parameter dict. If no such key, return None.
        @param:key
        @return:value
        """
        value = None
        if(self.parameters.has_key(key)):
            value = self.parameters[key]
        return value

if __name__ == '__main__':
    pass