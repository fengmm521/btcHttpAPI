#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys,os
os.environ['PATH'] = '/usr/bin/:/usr/sbin/'
import tensorflow as tf
import json
import numpy as np
import math
import time

logpth = './pattern'
BV = 'basevalue'
DD = 'dynamicvalue'
patPth = 'pattern/pattern.txt'

HourTime = 120

basevalue = []

softcount = 31
softmin = -15
softmax = 15

def getPattern(pth):
    f = open(pth,'r')
    lines = f.readlines()
    f.close()
    outlines = []
    for l in lines:
        tmpline = l.replace('\n','')
        tmpls = json.loads(tmpline)
        outlines.append(tmpls)
    for v in outlines[0]:
        basevalue.append(v)
    return outlines[1:]

class Pattern():
    """docstring for ClassName"""
    def __init__(self, pth,wtime,softmin = -20,softmax = 20):  #wtime:第次取出的数据时间宽度
        self.pattern = getPattern(pth)
        self.wtime = wtime
        self.bValue = basevalue[0]
        self.maxCount = basevalue[1]
        self.lcount = len(self.pattern)
        self.countScale = basevalue[2]
        self.minDat = basevalue[3]
        self.maxDat = basevalue[4]
        self.maxPattenr = (self.maxDat - self.minDat) * 2 #为了使数据变成在0～1之间的可处理数据，maxPattern就是当有数据等于这个值时基结果会设为1，比他小的按比例输出
        self.patType = 'basevalue'      #数据类型,basevalue:训练数据，有基础值，basevalue:训练数据，动态基础值
        self.pos = 0                    #当前获取的数据号,训练数据从前向后每次取一组数据，数据会根据不同数据类型来生成训练数据
        self.posDic = {}                #生成的训练数据
        self.prices = {}                #当前的买一价和卖一价
        self.lableprices = {}           #当前预测的下一个时间的最大值和最小值
        self.posBase = {}               #基础值变动的数据一致性基础数据
        self.labelWtime = self.wtime    #预测标记未来数据的时间宽度
        self.posLabel = {}              #标签数据
        self.outpattern = []            #每次数据变化的基础值
        self.flogs = []
        self.maxPos = self.lcount - self.wtime - self.labelWtime - 2
        
        self.softmin = softmin
        self.softmax = softmax
        self.softcount = self.softmax - self.softmin + 1
        self.halfCount = int(math.floor(self.softcount/2.0))
        self.initFlogs()
    def conventSoftmax(self,datamin,datamax,datstate):
        #数据从-15到15一共31个数，取最大值和最小值为softmax分类
        lstmin = [0]*self.softcount     #预测的最小值,这里要将预测最小值和预测最大值分开处理
        lstmax = [0]*self.softcount     #预测的最大值,这里要将预测最小值和预测最大值分开处理
        if datamin <= self.softmin:
            mintmp = 0
        elif datamin >= self.softmax:
            lstmax[self.softcount - 1] = 1
            lstmin[self.softcount - 1] = 1
            return lstmin,lstmax,datstate
        else:
            mintmp = int(math.floor((datamin+self.halfCount)%self.softcount))
        if datamax >= self.softmax:
            maxtmp = self.softcount - 1
        elif datamax <= self.softmin:
            lstmin[0] = 1
            lstmax[0] = 1
            return lstmin,lstmax,datstate
        else:
            maxtmp = int(math.floor((datamax+self.halfCount)%self.softcount))
        lstmin[mintmp] = 1
        lstmax[maxtmp] = 1
        return lstmin,lstmax,datstate
    def initFlogs(self):
        self.flogs = []
        for i in range(60):
            if i < 30:
                self.flogs.append(2*i)
            else:
                self.flogs.append(2*i + 1)
    #每次取50组数据作为一个批此
    def getBatchPats(self,count = 50):
        dics = []
        labs = []
        for i in range(count):
            dic,lab = self.getNextTrainingData()
            if dic and lab:
                dics.append(dic)
                labs.append(lab)
        return dics,labs
    def setLabeWtime(self,wtime):
        self.labelWtime = wtime
    def setPatternType(self,ptype = 'basevalue',labelWtime = 0):
        if ptype == self.patType:
            return
        elif ptype == 'dynamicvalue':
            self.patType = ptype
        elif ptype == 'basevalue':
            self.patType = ptype
        else:
            print 'set Pattern ptype erro'
            return
        self.posDatDic = {}             #清空上次生成的数据
        self.posLabel = {}              #清空上次生成的数据
        if labelWtime != 0:
            self.labelWtime = labelWtime

    #获取价格改变的6种未来趋势
    def _getPrictFuture(self,lastsell,lastbuy,minselldat,maxbuydat,isUp):
        out = 0
        #第一种:
        #              max
        #   o    
        #       min        
        if isUp and lastbuy > minselldat and lastsell < maxbuydat:
            out = 0
        #第二种
        #   o
        #               max
        #       min
        elif isUp and lastbuy > minselldat and lastbuy > maxbuydat:
            out = 1
        #第三种
        #   o
        #       max
        #               min
        elif (not isUp) and lastbuy > minselldat and lastbuy > maxbuydat:
            out = 2
        #第四种
        #               max
        #       min
        #   o
        elif isUp and lastsell < minselldat and lastsell < maxbuydat:
            out = 3
        #第五种
        #       max    
        #               min
        #   o
        elif (not isUp) and lastsell < minselldat and lastsell < maxbuydat:
            out = 4
        #第六种
        #       max
        #   o
        #               min    
        elif (not isUp) and lastsell > maxbuydat and lastbuy > minselldat:
            out = 5
        return out


    def _getPatternLable(self): #获取当前数据的预测标记数据,wtime为下次数据时间宽度
        nextpos = self.pos + 1
        tmppat = self.pattern[nextpos:nextpos + self.labelWtime]
        tmplbuy = []
        tmplsell = []
        lastdats = self.pattern[self.pos]
        lastsell = lastdats[58]
        lastbuy = lastdats[60]
        for d in tmppat:
            tmplbuy.append(d[60])
            tmplsell.append(d[58])
        if self.patType == 'basevalue':
            mindat = np.min(tmplsell)
            maxdat = np.max(tmplbuy)
            mindatpos = np.where(np.min(tmplsell) == tmplsell)[0][0]
            maxdatpos = np.where(np.max(tmplsell) == tmplsell)[0][0]
            isUp = False
            if mindatpos > maxdatpos:
                isUp = True
            inmin = mindat - self.posBase[self.pos]
            inmax = maxdat - self.posBase[self.pos]
            self.lableprices[self.pos] = [mindat + self.bValue,maxdat + self.bValue,self.posBase[self.pos]]
            datstate = self._getPrictFuture(lastsell, lastbuy, mindat, maxdat, isUp)
            outlabs = self.conventSoftmax(inmin, inmax, datstate)
            # return [np.min(tmplsell) - self.posBase[self.pos],np.max(tmplbuy) - self.posBase[self.pos]]
            return outlabs
        elif self.patType == 'dynamicvalue':
            return []

    def _conventWithNewBaseValue(self,plist):
        tmpbv = plist[0][60]
        outlist = []
        self.prices[self.pos] = []
        for n in range(len(plist)):
            tmpd = plist[n]
            tmplist = list(plist[n])
            self.prices[self.pos].append([tmpd[58] + self.bValue,tmpd[60] + self.bValue])
            for i in self.flogs:
                tmplist[i] = tmplist[i] - tmpbv
            outlist.append(tmplist)
        self.posBase[self.pos] = tmpbv
        return outlist
    #生成静态基数数据,生成三个网络训练数据，第一个预测最小值，第二个预测最大值，第三个预测未来趋势,
    #使用两个隐层网络，计划第一隐层500个节点，第二隐层300节点,三个网络，将会有6个隐层，三个网络的输出分别为41,41,6的softmax层来计算交叉商损失函数
    def _getNextTrainingDataBaseVale(self):
        outls = []
        if self.pos < self.lcount - self.wtime - self.labelWtime - 1:
            tmppat = self.pattern[self.pos:self.pos + self.wtime]
            tmppat = self._conventWithNewBaseValue(tmppat)
            tmpdicdat = []
            for d in tmppat:
                tmpdicdat = tmpdicdat + d
            tmpd = np.array(tmpdicdat)
            self.posDic[self.pos] = (tmpd - self.minDat)/self.maxPattenr  #数据标准化，使输入层数据在0~1之间
            self.posLabel[self.pos] = list(self._getPatternLable())
            outls.append(self.posDic[self.pos])
            outls.append(self.posLabel[self.pos])
            self.outpattern.append(outls)
            self.pos += 1
        else:
            self._saveCompletPattern()
            self.outpattern = []
            self.posBase = {}
            return None,None
        return outls[0],outls[1]

    def _saveCompletPattern(self):
        f1 = open(logpth + os.sep + str(self.wtime) + '_' + str(self.labelWtime) + '_labelpat.txt','w')
        for d in self.outpattern:
            savestr = str(d[1]) + '\n'
            f1.write(savestr)
        f1.close()
        f2 = open(logpth + os.sep + str(self.wtime) + '_' + str(self.labelWtime) + '_pat.txt','w')
        for d in self.prices.keys():
            savestr2 = str(self.prices[d]) + ',' + str(self.lableprices[d]) + '\n'
            f2.write(savestr2)
        f2.close()
        print 'save1 ok'
        f3 = open(logpth + os.sep + str(self.wtime) + '_' + str(self.labelWtime) + '_Offset.txt','w')
        print 'persave2'
        print len(self.posBase.keys())
        outdic = json.dumps(self.posBase)
        f3.write(outdic)
        f3.close()

    def _getNextTrainingDataDynamic(self):#生成动态基数数据
        pass
    def getNextTrainingData(self):          #获取下一个训练或者验证数据
        if self.patType == 'basevalue':
            return self._getNextTrainingDataBaseVale()
        elif self.patType == 'dynamicvalue':
            return self._getNextTrainingDataDynamic()
        else:
            print 'pattype erro'
        return None,None


#生成以初始基础值为基准的训练数据
def makeTrainingDataForBaseValue(wtime,labWtime):
    pat = Pattern(patPth, wtime)
    pat.setLabeWtime(labWtime)
    isNotEnd = True
    count = 0
    while isNotEnd:
        t,l = pat.getNextTrainingData()
        count += 1
        if count % 100 == 0:
            print count
        if not l:
            isNotEnd = False
        time.sleep(0.001)
    print 'getdataEnd'
        
    #121 [323.11, 3246.639174, 100.0, -77.43, 100.0]，每行121个数据，所有数据中最大值为100，最小值为-77，首次输入120个数据，之后每次输入一组数据移出一组数据，并重新生成一个下一小时结果数据
    return pat

#生成以单次动太计算基础值为基准的训练数据
def makeTrainingDataForDynamicValue():
    pattern = getPattern('pattern/pattern.txt')
    #121 [323.11, 3246.639174, 100.0, -77.43, 100.0]，每行121个数据，所有数据中最大值为100，最小值为-77，首次输入120个数据，之后每次输入一组数据移出一组数据，并重新生成一个下一小时结果数据
    return pattern

def tfWorkerDo(pattern):

    w1 = tf.Variable(tf.random_normal([2,3],stddev=1.0,seed=1))
    w2 = tf.Variable(tf.random_normal([3,1],stddev=1.0,seed=1))


    x = tf.placeholder(tf.float32,shape=(3,2),name='input')

    a = tf.matmul(x, w1)
    y = tf.matmul(a, w2)

    sess = tf.Session()

    init_op = tf.initialize_all_variables()

    sess.run(init_op)

    print sess.run(w1)
    print sess.run(w2)
    print sess.run(y,feed_dict={x:[[0.7,0.9],[0.1,0.4],[0.5,0.8]]})

    sess.close()
    
def main():
    makeTrainingDataForBaseValue(HourTime,30)
if __name__ == '__main__':
    main()