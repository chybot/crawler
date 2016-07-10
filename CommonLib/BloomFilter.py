# -*- coding: utf-8 -*-
# Created on 2014/9/25 20:42.


#http://palydawn.blog.163.com/blog/static/182969056201210260470485/

#!/usr/local/bin/python2.7
#coding=gbk
'''
Created on 2012-11-7

@author: palydawn

http://www.cnblogs.com/haippy/archive/2012/07/13/2590351.html
error_rate是False Positive的概率，定为0.001
elementNum是需要放到布隆过滤器中的url条数
'''

import io
import cmath
import time
from BitVector import BitVector

class BloomFilter(object):
    def __init__(self, error_rate=0.001, elementNum=10000000):
        #计算所需要的bit数
        self.bit_num = -1 * elementNum * cmath.log(error_rate) / (cmath.log(2.0) * cmath.log(2.0))

        #四字节对齐
        self.bit_num = self.align_4byte(self.bit_num.real)

        #分配内存
        self.bit_array = BitVector(size=self.bit_num)

        #计算hash函数个数
        self.hash_num = cmath.log(2) * self.bit_num / elementNum

        self.hash_num = self.hash_num.real

        #向上取整
        self.hash_num = int(self.hash_num) + 1

        #产生hash函数种子
        self.hash_seeds = self.generate_hashseeds(self.hash_num)

    def open_from_file(self, fn):
        bv = BitVector(filename = fn)
        print str(self.bit_array.size)
        bv1 = bv.read_bits_from_file(self.bit_array.size)
        self.bit_array = self.bit_array | bv1
        bv.close_file_object()
        #print self.bit_array.size
        #print str(self.bit_array)

    def write_file(self, fn):
        with open(fn, 'wb') as FILEOUT:
            #print str(self.bit_array)
            self.bit_array.write_to_file(FILEOUT)


    def insert_element(self, element):
        for seed in self.hash_seeds:
            hash_val = self.hash_element(element, seed)
            #取绝对值
            hash_val = abs(hash_val)
            #取模，防越界
            hash_val = hash_val % self.bit_num
            #设置相应的比特位
            self.bit_array[hash_val] = 1

    #检查元素是否存在，存在返回true，否则返回false
    def is_element_exist(self, element):
        for seed in self.hash_seeds:
            hash_val = self.hash_element(element, seed)
            #取绝对值
            hash_val = abs(hash_val)
            #取模，防越界
            hash_val = hash_val % self.bit_num

            #查看值
            if self.bit_array[hash_val] == 0:
                return False
        return True

    #内存对齐
    def align_4byte(self, bit_num):
        num = int(bit_num / 32)
        num = 32 * (num + 1)
        return num

    #产生hash函数种子,hash_num个素数
    def generate_hashseeds(self, hash_num):
        count = 0
        #连续两个种子的最小差值
        gap = 50
        #初始化hash种子为0
        hash_seeds = []
        for index in xrange(hash_num):
            hash_seeds.append(0)
        for index in xrange(10, 10000):
            max_num = int(cmath.sqrt(1.0 * index).real)
            flag = 1
            for num in xrange(2, max_num):
                if index % num == 0:
                    flag = 0
                    break

            if flag == 1:
                #连续两个hash种子的差值要大才行
                if count > 0 and (index - hash_seeds[count - 1]) < gap:
                    continue
                hash_seeds[count] = index
                count = count + 1

            if count == hash_num:
                break
        return hash_seeds

    def hash_element(self, element, seed):
        hash_val = 1
        for ch in str(element):
            chval = ord(ch)
            hash_val = hash_val * seed + chval
        return hash_val

if __name__ == "__main__":
    #测试代码
    '''
    bv1 = BitVector( bitstring = '00001010' )
    FILEOUT = open( 'test', 'wb' )
    bv1.write_to_file( FILEOUT )
    FILEOUT.close()
    open_from_file('test')

    bv2 = BitVector( filename = 'test.txt' )
    bv3 = bv2.read_bits_from_file( 32 )
    print len(bv3)

    bv = BitVector(filename = 'test.txt')
    print len(bv)

    print time.time()
    bf = BloomFilter()
    #bf.open_from_file('test')
    print time.time()

    bf = BloomFilter(0.001, 1000)
    element = 'palydawn'
    #print bf.is_element_exist(element)
    bf.insert_element(element)
    #print bf.is_element_exist(element)
    element = '阿萨德发123123palydaw安德森n'
    #print bf.is_element_exist(element)
    bf.insert_element(element)
    #print bf.is_element_exist(element)
    element = 'http://channel.jd.com/decoration.html'
    #print bf.is_element_exist(element)
    bf.insert_element(element)
    #print bf.is_element_exist(element)

    print len(bf.bit_array)
    raw_input()
    #bf.write_file('test')
    #bf.open_from_file('test')
    '''
