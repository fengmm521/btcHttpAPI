#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys,os
os.environ['PATH'] = '/usr/bin/:/usr/sbin/'
import tensorflow as tf
import json

logpth = './pattern'
BV = 'basevalue'
DD = 'dynamicvalue'
patPth = 'pattern/pattern.txt'

HourTime = 120

basevalue = []

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
    def __init__(self, pth,wtime):  #wtime:第次取出的数据时间宽度
        self.pattern = getPattern(pth)
        self.wtime = wtime
        self.bValue = basevalue[0]
        self.maxCount = basevalue[1]
        self.lcount = len(self.pattern)
        self.countScale = basevalue[2]
        self.minDat = basevalue[3]
        self.maxDat = basevalue[4]
        self.patType = 'basevalue'      #数据类型,basevalue:训练数据，有基础值，basevalue:训练数据，动态基础值
        self.pos = 0                    #当前获取的数据号,训练数据从前向后每次取一组数据，数据会根据不同数据类型来生成训练数据
        self.posDic = {}                #生成的训练数据
        self.posBase = {}               #基础值变动的数据一致性基础数据
        self.labelWtime = self.wtime    #预测标记未来数据的时间宽度
        self.posLabel = {}              #标签数据
        self.outpattern = []            #每次数据变化的基础值
        self.flogs = []
        self.maxPos = self.lcount - self.wtime - self.labelWtime - 2
        self.initFlogs()
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
        for i in range(count)
            dic,lab = self.getNextTrainingData()
            if dic and lab:
                dics.append(dic)
                labs.append(lab)
        return dics,labs
    def setLabeWtime(self,wtime):
        self.labelWtime = wtime
    def setPatternType(self,ptype = 'basevalue',labelWtime = self.labelWtime):
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
        self.labelWtime = labelWtime

    def _getPatternLable(self): #获取当前数据的预测标记数据,wtime为下次数据时间宽度
        nextpos = self.pos + 1
        tmppat = self.pattern[nextpos:nextpos + self.labelWtime]
        tmplbuy = []
        tmplsell = []
        for d in tmppat:
            tmplbuy.append(d[60])
            tmplsell.append(d[58])
        if self.patType == 'basevalue':
            return [np.min(tmplsell) - self.posBase[self.pos],np.max(tmplbuy) - self.posBase[self.pos]]
        elif self.patType == 'dynamicvalue':
            return []

    def _conventWithNewBaseValue(self,plist):
        tmpbv = plist[0][60]
        for n in range(len(plist)):
            for i in self.flogs:
                plist[n][i] = plist[n][i] - tmpbv
        self.posBase[self.pos] = tmpbv

    def _getNextTrainingDataBaseVale(self):#生成静态基数数据
        outls = []
        if self.pos < self.lcount - self.wtime - self.labelWtime - 1:
            tmppat = self.pattern[self.pos:self.pos + self.wtime]
            self._conventWithNewBaseValue(tmppat)
            tmpdicdat = []
            for d in tmppat:
                tmpdicdat = tmpdicdat + d
            self.posDic[self.pos] = tmpdicdat
            self.posLabel[self.pos] = self._getPatternLable()
            outls.append(self.posDic[self.pos])
            outls.append(self.posLabel[self.pos])
            self.outpattern.append(outls)
            self.pos += 1
        else:
            self._saveCompletPattern()
            self.outpattern = []
            self.posBase = []
            outls = [[],[]]
        return outls[0],outls[1]

    def _saveCompletPattern(self):
        f = open(logpth + os.sep + str(self.wtime) + '_' + str(self.labelWtime) + '_labelpat.txt','w')
        for d in self.outpattern:
            savestr = str(d) + '\n'
            f.write(savestr)
        f.close()
        f = open(logpth + os.sep + str(self.wtime) + '_' + str(self.labelWtime) + '_labelpatOffset.txt','w')
        for d in self.posBase:
            savestr = str(d) + '\n'
            f.write(savestr)
        f.close()

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
    makeTrainingDataForBaseValue(HourTime,120)
if __name__ == '__main__':
    main()