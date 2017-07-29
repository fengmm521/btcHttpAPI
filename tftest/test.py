#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-07-27 14:52:00
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$

import os
os.environ['PATH'] = '/usr/bin/:/usr/sbin/'
import codecs
import sys
import xlrd
import time
import urllib2
import socket  
import shutil 
import math
import numpy as np
#将所有Excel文件转为xml文件
reload(sys)
sys.setdefaultencoding( "utf-8" )


class Test():
    """docstring for Test"""
    def __init__(self,softmin,softmax):
        self.softmin = softmin
        self.softmax = softmax
        self.softcount = self.softmax - self.softmin + 1
        self.halfCount = int(math.floor(self.softcount/2.0))
        self.initPrint()
    def initPrint(self):
        print self.softmin,self.softmax,self.softcount,self.halfCount

    def conventSoftmax(self,datamin,datamax):
        #数据从-15到15一共31个数，取最大值和最小值为softmax分类
        lst = [0]*self.softcount
        if datamin <= self.softmin:
            mintmp = 0
        elif datamin >= self.softmax:
            lst[self.softcount - 1] = 1
            return lst
        else:
            mintmp = int(math.floor((datamin+self.halfCount)%self.softcount))
            print math.floor((datamin+self.halfCount)%self.softcount)
            print datamin,datamin%self.halfCount,-11.4%20
        if datamax >= self.softmax:
            maxtmp = self.softcount - 1
        elif datamax <= self.softmin:
            lst[0] = 1
            return lst
        else:
            maxtmp = int(math.floor((datamax+self.halfCount)%self.softcount))
            print math.floor((datamax+self.halfCount)%self.softcount)
        lst[mintmp] = 1
        lst[maxtmp] = 1
        return lst


def numpyTest():
    a = np.array([2,4,5,6,3,1,9,1])
    print a
    s = np.mean(a)
    print s
    d = np.std(a)
    print d
    xa = (a - np.mean(a))/np.std(a)
    print xa
    

def main():
    numpyTest()
    # obj = Test(-20, 20)
    # lstmp = obj.conventSoftmax(-17.3, -2)
    # print lstmp
if __name__ == '__main__':  
    main()
    