# -*- coding: utf-8 -*-
# Created by David on 2016/4/29.

import sys
sys.path.append('../')
reload(sys)
sys.setdefaultencoding('utf-8')

class ParserMapper(object):
    @staticmethod
    def doMap(map_config, result_list):
        """
        crawlerResultMap is used to map the table key-value pair into final result structure
        @version:1.0
        @author:david ding
        @modify:
        """
        if not map_config or not result_list:
            return
        # 提取transform中的替换信息
        transform_replace = {}
        for key in map_config:
            key_list = key.split('.')
            value_list = map_config[key].split('.')
            for i in range(0, min(len(key_list), len(value_list))):
                if key_list[i] == value_list[i]:
                    continue
                transform_replace[key_list[i]] = value_list[i]

        result_mapped_dict = {}
        for info_dict in result_list:
            if not info_dict:
                continue
            for key in info_dict:
                key_list = key.split('.')
                # 当前处理的节点
                cur_dict = result_mapped_dict
                # 当前处理节点的前一个节点，list封装需要
                cur_pre_dict = cur_dict
                cur_pre_dict_key = None
                for i in range(0, len(key_list) - 1):
                    kl = key_list[i]
                    # 替换键值
                    if kl in transform_replace:
                        kl = transform_replace[kl]
                    if not kl:
                        continue
                    # 生成字典树
                    if kl not in result_mapped_dict:
                        cur_dict[kl] = {}
                    cur_pre_dict = cur_dict
                    cur_pre_dict_key = kl
                    cur_dict = cur_dict[kl]
                if cur_dict == result_mapped_dict:
                    pass
                value = info_dict[key]
                last_key = key_list[-1]
                # 类似多个股东信息的存储结构
                if isinstance(cur_dict, list):
                    cur_list = cur_dict
                    cur_dict = cur_list[-1]
                    if last_key in cur_dict:
                        cur_dict = dict()
                        cur_list.append(cur_dict)
                    cur_dict[last_key] = value
                elif last_key not in cur_dict:
                    cur_dict[last_key] = value
                # 需要将最后一层dict提取封装到list
                elif cur_pre_dict_key:
                    cur_list = list()
                    # 前一个节点不再指向dict,而将指向新封装的list
                    cur_pre_dict[cur_pre_dict_key] = cur_list
                    cur_list.append(cur_dict)
                    # 当前待处理键值对被封装到新的字典
                    cur_dict = dict()
                    cur_dict[last_key] = value
                    cur_list.append(cur_dict)
        return result_mapped_dict


if __name__ == "__main__":
    pass
