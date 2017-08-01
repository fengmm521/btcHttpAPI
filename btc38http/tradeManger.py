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


        self.bigprice = 155         #是否是大单的下限
        self.bigbuys = []
        self.bigsells = []
        self.buyAllCount = 0.0      #所有买单数量
        self.sellAllCount = 0.0     #所有卖单数量
        self.priceRange = 0.0       #买卖单数量的价格范围
        self.buyLenth = 0.0         #买单长度
        self.sellLenth = 0.0        #卖单长度

        self.lastOpt = 0            #0：未操作，1：买操作，-1：卖操作

        self.netBuyPrice = 0.0      #购买价
        self.netBuyCount = 0.0      #购买量

        self.netSellPrice = 0.0     #出售价
        self.netSellCount = 0.0     #出售量


        self.nowTradePrice = 0.0    #当前市场价
        self.nowBuyPrice = 0.0      #当前买一价
        self.nowSellPrice = 0.0     #当前卖一价

        #根据市场深度动态调整的买触发价,买触发价为价格跌到了购买价以下，并且在一个大单（大于50）成交后,还有购买单大于100的量在支撑时
        #可进行买入操作,否则买入价自动向下移动到下一个大单（大于100）前
        self.changeBuyPrice = 0.0   
        #根据市场深度动态调整的卖触发价，单卖出价在成交了一个大单（50）后，卖单还有大于(100)的卖单在作支持压价时，
        #可作卖出操作,否则卖出操作自动向上移到下一个大单(大于100)前
        self.changeSellPrice = 0.0  

        self.getAccountData()

    def setNowPrice(self,tbuy,tsell,ttrade):
        self.nowTradePrice = ttrade
        self.nowBuyPrice = tbuy
        self.nowSellPrice = tsell
    #设置网络交易范围
    def setNetBuyAndSellConfig(self,buyPrice,buyCount,sellPrice,sellCount):
        if buyPrice >= sellPrice:
            print '买的价格大于卖价格错误'
        else:
            self.netBuyPrice = buyPrice
            self.netSellPrice = sellPrice
            self.netBuyCount = buyCount
            self.netSellCount = sellCount
            netlog = '设置买入价:%.2f,买入量:%.2f,卖出价:%.2f,卖出量:%.2f'%(self.netBuyPrice,self.netBuyCount,self.netSellPrice,self.netSellCount)
            print netlog
            f  = open('netlog.txt','w')
            f.write(netlog)
            f.close()
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
            self.lastOpt = 1
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
            self.lastOpt = -1
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

    
    #得到当前最新深度数据
    # {"bids":[[285.01,1.848972],[285,17.787401],[284.13,0.0106],[284.12,432.37],[284.05,87.418972],[283.8,0.738],[283,3.2123],[282.28,8],[282.18,8],[282,78.191489],[281.9,70.947144],[281.8,0.184213],[281,4.80427],[280.8,9.981125],[280.48,432.37],[280,85.427669],[279.5,1.252236],[278,3.561511],[276.2,30],[275.51,100],[275,50.195061],[273,80.428881],[272.39,1.000036],[272.24,0.1],[272.1,0.973814],[272.07,0.5],[272.01,38.548836],[272,5],[271.95,18.54],[271,1]],"asks":[[289.19,2.034594],[289.2,8.084384],[289.37,0.1],[289.4,16.492278],[289.89,12.927245],[289.91,1.828025],[289.99,84.15371],[290,87.27043],[290.88,50.50909],[290.89,0.154857],[290.98,10],[291,49.907735],[291.7,2],[291.75,0.010282],[291.8,12],[292,57.939598],[292.98,9.739233],[293,1217.590741],[293.3,17.900664],[293.7,52.106786],[293.78,0.371766],[293.79,15.364027],[293.8,4.818481],[293.99,3.589798],[294,127.664955],[294.4,14.471],[294.47,3.057539],[294.88,2],[294.9,30],[294.97,16]]}
    def addDepth(self,depth):
        if self.netBuyPrice > 1.0 and self.netSellPrice > 1.0:
            tmps = depth.split('=')
            depstr = ''
            if len(tmps[1]) > 100:
                depstr = tmps[1]
            depdic = json.loads(depstr)
            buys = depdic['bids']
            sells = depdic['asks']

            self.buyAllCount = 0.0      #所有买单数量
            self.sellAllCount = 0.0     #所有卖单数量
            self.priceRange = 0.0       #买卖单数量的价格范围
            self.buyLenth = 0.0         #买单长度
            self.sellLenth = 0.0        #卖单长度

            buyrange = buys[0][0] - buys[-1][0]
            sellrange = sells[-1][0] - sells[0][0]
            self.priceRange = min(buyrange,sellrange)

            buysmall = buys[0][0] - self.priceRange
            sellbig = sells[0][0] + self.priceRange

            buycount = 0.0
            sellcount = 0.0

            for bn in range(len(buys)):
                b = buys[bn]
                if b[0] >= buysmall:
                    self.buyAllCount += b[1]
                    self.buyLenth = bn
                if b[0] >= self.netSellPrice:
                    buycount += b[1]
                if b[1] > self.bigprice:
                    tmplist = list(b)
                    tmplist.append(bn)
                    self.bigbuys.append(tmplist)

            for sn in range(len(sells)):
                s = sells[sn]
                if s[0] <= sellbig:
                    self.sellAllCount += s[1]
                    self.sellLenth = sn
                if s[0] <= self.netBuyPrice:
                    sellcount += s[1]
                if s[1] > self.bigprice:
                    tmplist = list(s)
                    tmplist.append(sn)
                    self.bigsells.append(tmplist)
            #买入操作
            if (self.lastOpt == 0 or self.lastOpt == -1) and self.netBuyCount < sellcount and self.sellAllCount < self.buyAllCount and self.buyAllCount - self.sellAllCount > 200 and self.buyLenth > self.sellLenth:
                self.buy(self.netBuyCount, self.netBuyPrice)
            #卖出操作
            elif self.lastOpt == 1 and self.netSellCount < buycount and self.sellAllCount > self.buyAllCount and self.sellAllCount - self.buyAllCount > 200 and self.sellLenth > self.buyLenth:
                self.sell(self.netSellCount, self.netSellPrice)
        

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
    datstr = '{"bids":[[285.01,1.848972],[285,17.787401],[284.13,0.0106],[284.12,432.37],[284.05,87.418972],[283.8,0.738],[283,3.2123],[282.28,8],[282.18,8],[282,78.191489],[281.9,70.947144],[281.8,0.184213],[281,4.80427],[280.8,9.981125],[280.48,432.37],[280,85.427669],[279.5,1.252236],[278,3.561511],[276.2,30],[275.51,100],[275,50.195061],[273,80.428881],[272.39,1.000036],[272.24,0.1],[272.1,0.973814],[272.07,0.5],[272.01,38.548836],[272,5],[271.95,18.54],[271,1]],"asks":[[289.19,2.034594],[289.2,8.084384],[289.37,0.1],[289.4,16.492278],[289.89,12.927245],[289.91,1.828025],[289.99,84.15371],[290,87.27043],[290.88,50.50909],[290.89,0.154857],[290.98,10],[291,49.907735],[291.7,2],[291.75,0.010282],[291.8,12],[292,57.939598],[292.98,9.739233],[293,1217.590741],[293.3,17.900664],[293.7,52.106786],[293.78,0.371766],[293.79,15.364027],[293.8,4.818481],[293.99,3.589798],[294,127.664955],[294.4,14.471],[294.47,3.057539],[294.88,2],[294.9,30],[294.97,16]]}'
    dicdat = json.loads(datstr)
    buys = dicdat['bids']
    sells = dicdat['asks']
    print buys[-1]
    buyrange = buys[0][0] - buys[-1][0]
    sellrange = sells[-1][0] - sells[0][0]
    print buyrange,sellrange
    pass