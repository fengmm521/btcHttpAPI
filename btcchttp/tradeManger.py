
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys,os
import json
import math
import timetool

#datatype = 1498064693.62={"ticker":{"high":355.01,"low":301.1,"last":341.21,"vol":213413.588686,"buy":341.21,"sell":343.88}}

class TradeManger():
    def __init__(self,pDot = 0.03,pmaxdot = 100,tradeCondtion = 10):
        self.dot = pDot
        self.dotlist = []
        self.maxdotlist = pmaxdot
        self.tradeNum = 10.0
        self.lastPrice = 0.0
        self.lastTime = 0.0
        self.lastTicker = None
        self.lastJsonDat = None
        self.lastDot = 0.0
        self.CPV = 0
        self.CNV = 0
        self.perChangeCPV = 0
        self.perChangeCNV = 0
        self.maxPV = 0.0
        self.maxNV = 0.0
        self.tradeCondtion = tradeCondtion


    def saveTradelog(self,ptype,price):
        rlog = ptype + '|' + str(price) + '|' + self.lastTicker +  '|' + str(timetool.getNowDate(float(self.lastTime))) + '\n'
        f = open('tradelog.txt','a+')
        f.write(rlog)
        f.close()

    def buyTrade(self):
        self.saveTradelog('buy',self.lastJsonDat['ticker']['sell'])

    def sellTrade(self):
        self.saveTradelog('sel',self.lastJsonDat['ticker']['buy'])

    def saveChangeLog(self,logmsg):
        outstr = logmsg + '|' + str(timetool.getNowDate(float(self.lastTime))) + '\n'
        f = open('changelog.txt','a+')
        f.write(outstr)
        f.close()

    def addTicker(self,ticker):
        tmp = ticker.split('=')
        if len(tmp[1]) > 10:
            tmp2 = tmp[1].replace('\n','')
            jstmp = json.loads(tmp2)
            self.lastTicker = tmp2
            self.lastJsonDat = jstmp
            if self.lastTime < 10:
                self.lastTime = float(tmp[0])
                self.lastPrice = float(jstmp['ticker']['last'])
            else:
                tmplastTime = float(tmp[0])
                tmplastPrice = float(jstmp['ticker']['last'])
                if tmplastTime > self.lastTime:
                    tmpDot = (tmplastPrice - self.lastPrice)/(tmplastTime - self.lastTime)
                    self.lastTime = tmplastTime
                    self.lastPrice = tmplastPrice
                    if abs(tmpDot) >= self.dot:
                        if self.lastDot == 0.0:
                            self.lastDot = tmpDot
                        else:
                            self.perChangeCPV = 0
                            self.perChangeCNV = 0
                            if tmpDot > 0:
                                if self.lastDot > 0:
                                    self.CPV += 1
                                else:
                                    self.perChangeCNV = self.CNV
                                    self.CNV = 0
                                    self.CPV = 1
                            elif tmpDot < 0:
                                if self.lastDot < 0:
                                    self.CNV += 1
                                else:
                                    self.perChangeCPV = self.CPV
                                    self.CPV = 0
                                    self.CNV = 1
                            self.dotlist.append(tmpDot)
                            # print 'lastDot:',self.lastDot,'tmpDot:',tmpDot
                            self.lastDot = tmpDot
                            if len(self.dotlist) > self.maxdotlist:
                                self.dotlist = self.dotlist[(len(self.dotlist)-(self.maxdotlist)):]
                            if self.perChangeCNV > self.tradeCondtion:
                                self.buyTrade()
                            elif self.perChangeCPV > self.tradeCondtion:
                                self.sellTrade()
                        tmpdic = {'CNV':self.CNV,'CPV':self.CPV,'perChangeCNV':self.perChangeCNV,'perChangeCPV':self.perChangeCPV,'lastDot':self.lastDot,'lastprice':self.lastPrice}
                        self.saveChangeLog(str(tmpdic))
                    # print self.CNV,self.CPV,self.perChangeCNV,self.perChangeCPV,self.lastDot
            # print self.lastTicker,self.lastTime
    
if __name__ == '__main__':
    tradetool = TradeManger()
    f = open('2017_6_26.txt','r')
    testticeers = f.readlines()
    f.close()
    for t in testticeers:
        tradetool.addTicker(t)
