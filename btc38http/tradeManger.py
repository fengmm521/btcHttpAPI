#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys,os
import json
import math
import timetool
import httplib, urllib
import hashlib
import time
#datatype = 1498064693.62={"ticker":{"high":355.01,"low":301.1,"last":341.21,"vol":213413.588686,"buy":341.21,"sell":343.88}}


def getMd5Value():
    key = ''
    skey = ''
    uid = ''
    strtime = str(int(time.time()))
    instr = key + '_' + uid + '_' + skey + '_' + strtime
    outstr = hashlib.md5(instr).hexdigest()
    return strtime,outstr

#getaccount
def getAccountHttpRequest():
    httpClient = None
    try:
        strtime,md5str = getMd5Value()
        params = urllib.urlencode({'key': '', 'time': strtime,'md5':md5str})
        headers = {"Content-type": "application/x-www-form-urlencoded"
                        , "Accept": "text/plain"}
     
        httpClient = httplib.HTTPConnection("api.btc38.com", 80, timeout=30)
        httpClient.request("POST", "/v1/getMyBalance.php", params, headers)
     
        response = httpClient.getresponse()
        outstr = response.read()
        return outstr
    except Exception, e:
        print e
    finally:
        if httpClient:
            httpClient.close()
    return None


#account back id
def buyHttpRequest(amount,price):
    httpClient = None
    try:
        strtime,md5str = getMd5Value()
        params = urllib.urlencode({'key': 'pubkey', 'time': strtime,'md5':md5str,'type':1,'mk_type':'cny','price':'%.2f'%(price),'amount':'%.2f'%(amount),'coinname':'LTC'})
        headers = {"Content-type": "application/x-www-form-urlencoded"
                        , "Accept": "text/plain"}
     
        httpClient = httplib.HTTPConnection("api.btc38.com", 80, timeout=30)
        httpClient.request("POST", "/v1/submitOrder.php", params, headers)
     
        response = httpClient.getresponse()
        outstr = response.read()
        return outstr

    except Exception, e:
        print e
    finally:
        if httpClient:
            httpClient.close()
    return None

#sell http
def sellHttpRequest(amount,price):
    httpClient = None
    try:
        strtime,md5str = getMd5Value()
        params = urllib.urlencode({'key': 'pubkey', 'time': strtime,'md5':md5str,'type':2,'mk_type':'cny','price':'%.2f'%(price),'amount':'%.2f'%(amount),'coinname':'LTC'})
        
        headers = {"Content-type": "application/x-www-form-urlencoded"
                        , "Accept": "text/plain"}
     
        httpClient = httplib.HTTPConnection("api.btc38.com", 80, timeout=30)
        httpClient.request("POST", "/v1/submitOrder.php", params, headers)
     
        response = httpClient.getresponse()
        outstr = response.read()
        return outstr

    except Exception, e:
        print e
    finally:
        if httpClient:
            httpClient.close()
    return None


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

        self.tradeCount = 10.0   #单次交易数量

        self.cny = 0
        self.lockcny = 0
        self.ltc = 0
        self.lockltc = 0

        self.getAccountData()
    #init account
    def getAccountData(self):
        accountjson = getAccountHttpRequest()
        adic = json.loads(accountjson)
        self.cny = float(adic['cny_balance'])
        self.lockcny = float(adic['cny_balance_lock'])
        self.ltc = float(adic['ltc_balance'])
        self.ltc = float(adic['ltc_balance_lock'])
        tmplog = 'cny:' + str(self.cny) + ',lockcny:' + str(self.lockcny) + ',ltc:' + str(self.ltc) + ',lockltc:' + str(self.lockltc) + '\n'
        f = open('heavelog.txt','a+')
        f.write(tmplog)
        f.close()
    #buy
    def buy(self,amount,price):
        buyjson = buyHttpRequest(amount,price) + '\n'
        if not buyjson or buyjson.find('<html>') != -1:
            time.sleep(3)
            self.buy(amount, price)
        else:
            savestr = 'buy->(%.2f,%.2f)'%(amount,price) + buyjson + '\n'
            f = open('tradebacklog.txt','a+')
            f.write(savestr)
            f.close()
            self.getAccountData()

    def sell(self,amount,price):
        selljson = sellHttpRequest(amount,price)
        if not selljson or selljson.find('<html>') != -1:
            time.sleep(3)
            self.sell(amount, price)
        else:
            savestr = 'sell->(%.2f,%.2f)'%(amount,price) + selljson + '\n'
            f = open('tradebacklog.txt','a+')
            f.write(savestr)
            f.close()
            self.getAccountData()

    def saveTradelog(self,ptype,price):
        rlog = ptype + '|' + str(price) + '|' + self.lastTicker +  '|' + str(timetool.getNowDate(float(self.lastTime))) + '\n'
        f = open('tradelog.txt','a+')
        f.write(rlog)
        f.close()

    def buyTrade(self):
        self.saveTradelog('buy',self.lastJsonDat['ticker']['sell'])
        self.buy(self.tradeCount, float(self.lastJsonDat['ticker']['sell']))
    def sellTrade(self):
        self.saveTradelog('sel',self.lastJsonDat['ticker']['buy'])
        self.sell(self.tradeCount, float(self.lastJsonDat['ticker']['buy']))

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
    # md5str = getMd5Value()
    # print md5str
    # account = getAccountHttpRequest()
    # print account
    # tradetool = TradeManger()
    # tradetool.buy(1.0, 115)
    # tradetool.sell(1.0, 415)
    # testticeers = []
    # testticeers.append('1498064545.11={"ticker":{"high":355.01,"low":301.1,"last":348.3,"vol":213292.292369,"buy":341.3,"sell":344.21}}')
    # testticeers.append('1498064565.11={"ticker":{"high":355.01,"low":301.1,"last":340.3,"vol":213292.292369,"buy":341.3,"sell":344.21}}')
    # testticeers.append('1498064585.11={"ticker":{"high":355.01,"low":301.1,"last":335.3,"vol":213292.292369,"buy":341.3,"sell":344.21}}')
    # testticeers.append('1498064615.11={"ticker":{"high":355.01,"low":301.1,"last":330.3,"vol":213292.292369,"buy":341.3,"sell":344.21}}')
    # testticeers.append('1498064635.11={"ticker":{"high":355.01,"low":301.1,"last":325.3,"vol":213292.292369,"buy":341.3,"sell":344.21}}')
    # testticeers.append('1498064645.11={"ticker":{"high":355.01,"low":301.1,"last":323.3,"vol":213292.292369,"buy":341.3,"sell":344.21}}')
    # testticeers.append('1498064655.11={"ticker":{"high":355.01,"low":301.1,"last":320.3,"vol":213292.292369,"buy":341.3,"sell":344.21}}')
    # testticeers.append('1498064675.11={"ticker":{"high":355.01,"low":301.1,"last":315.3,"vol":213292.292369,"buy":341.3,"sell":344.21}}')
    # testticeers.append('1498064695.11={"ticker":{"high":355.01,"low":301.1,"last":310.3,"vol":213292.292369,"buy":341.3,"sell":344.21}}')
    # testticeers.append('1498064715.11={"ticker":{"high":355.01,"low":301.1,"last":305.3,"vol":213292.292369,"buy":341.3,"sell":344.21}}')
    # testticeers.append('1498064725.11={"ticker":{"high":355.01,"low":301.1,"last":302.3,"vol":213292.292369,"buy":341.3,"sell":344.21}}')
    # testticeers.append('1498064735.11={"ticker":{"high":355.01,"low":301.1,"last":300.3,"vol":213292.292369,"buy":341.3,"sell":344.21}}')
    # testticeers.append('1498064755.11={"ticker":{"high":355.01,"low":301.1,"last":295.3,"vol":213292.292369,"buy":341.3,"sell":344.21}}')
    # testticeers.append('1498064765.11={"ticker":{"high":355.01,"low":301.1,"last":285.3,"vol":213292.292369,"buy":341.3,"sell":344.21}}')
    # testticeers.append('1498064775.11={"ticker":{"high":355.01,"low":301.1,"last":310.3,"vol":213292.292369,"buy":341.3,"sell":344.21}}')
    # testticeers.append('1498064795.11={"ticker":{"high":355.01,"low":301.1,"last":320.3,"vol":213292.292369,"buy":341.3,"sell":344.21}}')
    # testticeers.append('1498064815.11={"ticker":{"high":355.01,"low":301.1,"last":330.3,"vol":213292.292369,"buy":341.3,"sell":344.21}}')
    # testticeers.append('1498064835.11={"ticker":{"high":355.01,"low":301.1,"last":340.3,"vol":213292.292369,"buy":341.3,"sell":344.21}}')
    # testticeers.append('1498064855.11={"ticker":{"high":355.01,"low":301.1,"last":350.3,"vol":213292.292369,"buy":341.3,"sell":344.21}}')
    # testticeers.append('1498064875.11={"ticker":{"high":355.01,"low":301.1,"last":360.3,"vol":213292.292369,"buy":341.3,"sell":344.21}}')
    # testticeers.append('1498064895.11={"ticker":{"high":355.01,"low":301.1,"last":370.3,"vol":213292.292369,"buy":341.3,"sell":344.21}}')
    # testticeers.append('1498064915.11={"ticker":{"high":355.01,"low":301.1,"last":380.3,"vol":213292.292369,"buy":341.3,"sell":344.21}}')
    # testticeers.append('1498064935.11={"ticker":{"high":355.01,"low":301.1,"last":390.3,"vol":213292.292369,"buy":341.3,"sell":344.21}}')
    # testticeers.append('1498064955.11={"ticker":{"high":355.01,"low":301.1,"last":395.3,"vol":213292.292369,"buy":341.3,"sell":344.21}}')
    # testticeers.append('1498064975.11={"ticker":{"high":355.01,"low":301.1,"last":400.3,"vol":213292.292369,"buy":341.3,"sell":344.21}}')
    # testticeers.append('1498065015.11={"ticker":{"high":355.01,"low":301.1,"last":390.3,"vol":213292.292369,"buy":341.3,"sell":344.21}}')
    # testticeers.append('1498065035.11={"ticker":{"high":355.01,"low":301.1,"last":385.3,"vol":213292.292369,"buy":341.3,"sell":344.21}}')
    # for t in testticeers:
    #     tradetool.addTicker(t)
    pass