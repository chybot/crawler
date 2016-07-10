# -*- coding: utf-8 -*-
import string

def listToCoupleList(lst):
    """
    change list to a list with couple element in a touple
    such as [1,2,3,4]=>[(1,2),(3,4)]
    :param lst:
    :return:
    """
    return zip(lst[::2],lst[1::2])

def listToDict(lst):
    return dict(zip(lst[::2],lst[1::2]))

def doubleListToDict(lst1,lst2):
    return dict(zip(lst1,lst2))

def doubleListToDictLong(lst1,lst2):
    pass
def removeEmptyItemInList(value_list):
    """
    remove the empty item in a list
    :param value_list:
    :return: processed list
    """
    # while '' in value_list:
    #     value_list.remove('')
    # return value_list
    return filter(lambda x:x, value_list)

def removeEmptyInListItem(value_list):
    """
    remove empty and other useless characters of an item in the list

    :param value_list:
    :return: list with useless characters removed
    """
    list=[]
    for item in value_list:
        list.append(item.strip())
    return list
def removeEmptyInListItemMap(value_list):
    """
    remove empty and other useless characters of an item in the list

    :param value_list:
    :return: list with useless characters removed
    """
    return map(string.strip, value_list)


def removeUselessChar(str):
    """
    used to process some special string if strip() is not work
    :param str:
    :return:
    """
    return "".join(str.split()).replace("\t","")

if __name__ =="__main__":
    ll = ["axx    ","    b"]

    removeEmptyInListItemMap(ll)
    print ll
