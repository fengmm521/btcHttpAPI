#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys,os

import httplib

import time

import tradeManger
 
import timetool


DataDIR = 'data/'

httpClient = None
tradetool = tradeManger.TradeManger()
tradetool.setNetBuyAndSellConfig(307.8, 10.1, 342.1, 10.1)
 
def getTicker():
    try:
        httpClient = httplib.HTTPConnection('api.btc38.com', 80, timeout=30)
        httpClient.request('GET', '/v1/ticker.php?c=ltc&mk_type=cny')
        response = httpClient.getresponse()
        data = response.read()
        return data
    except Exception, e:
        print e
    finally:
        if httpClient:
            httpClient.close()
    return 0

#depth--http://api.btc38.com/v1/depth.php?c=ltc&mk_type=cny

def getDepth():
    try:
        httpClient = httplib.HTTPConnection('api.btc38.com', 80, timeout=30)
        httpClient.request('GET', '/v1/depth.php?c=ltc&mk_type=cny')
        response = httpClient.getresponse()
        data = response.read()
        return data
    except Exception, e:
        print e
    finally:
        if httpClient:
            httpClient.close()
    return 0





def main():
    timeouttimes = 0
    htmltimes = 0
    while True:
        depthtmp = getDepth()  #market depth
        if depthtmp == 0:
            timeouttimes += 1
            f = open('timeoutlog.txt','a+')
            savestr = 'timeoutdepth->times:' + str(timeouttimes) + ',time:' + str(timetool.getNowDate()) + '\n'
            f.write(savestr)
            f.close()
            time.sleep(3)
        elif depthtmp.find('<html>') != -1:
            htmltimes += 1
            f = open('htmllog.txt','a+')
            savestr = 'htmloutdepth->times:' + str(htmltimes) + ',time:' + str(timetool.getNowDate()) + '\n'
            f.write(savestr)
            f.close()
            time.sleep(3)
        else:
            fname = DataDIR + 'depth_' + timetool.getDateDay() + '.txt'
            f = open(fname,'a+')
            savedat = str(time.time()) + '=' + depthtmp + '\n'
            tradetool.addDepth(savedat)
            f.write(savedat)
            f.close()
            time.sleep(3)

        tickertmp = getTicker()
        if tickertmp == 0:
            timeouttimes += 1
            f = open('timeoutlog.txt','a+')
            savestr = 'timeout->times:' + str(timeouttimes) + ',time:' + str(timetool.getNowDate()) + '\n'
            f.write(savestr)
            f.close()
            time.sleep(15)
        elif tickertmp.find('<html>') != -1:
            htmltimes += 1
            f = open('htmllog.txt','a+')
            savestr = 'htmlout->times:' + str(htmltimes) + ',time:' + str(timetool.getNowDate()) + '\n'
            f.write(savestr)
            f.close()
            time.sleep(15)
        else:
            fname = DataDIR + timetool.getDateDay() + '.txt'
            f = open(fname,'a+')
            savedat = str(time.time()) + '=' + tickertmp + '\n'
            tradetool.addTicker(savedat)
            f.write(savedat)
            f.close()
            time.sleep(27)
def test():
    # depthtmp = getDepth()  #market depth
    # savedat = str(time.time()) + '=' + depthtmp + '\n'
    savedat = '1502248327.53={"bids":[[324.51,1.504],[324.49,2.805017],[324.13,155.544292],[324.02,10.052547],[324.01,0.31],[323,0.613061],[322.1,0.153662],[322.01,456.39976],[322,2.263802],[321.17,22.633035],[321.01,61.984715],[320.4,15.6055],[320.33,0.103348],[320.28,0.134597],[320,7],[319.37,0.009393],[319.05,0.04588],[319.04,18.2],[319.03,0.816391],[319,14.539445],[318.6,2.291274],[318.28,0.155499],[318,0.501572],[317.5,40.027719],[317,0.503154],[316.39,432.37],[316.07,1.978864],[316,0.504746],[315.76,19.362427],[315,1.850781]],"asks":[[325.98,13.814],[326,155.071045],[326.43,4.039766],[326.52,26.063943],[326.6,11.418557],[326.98,5],[327,21.792507],[327.02,4.67],[327.13,0.009188],[327.8,20],[327.99,35.600786],[328,785.028464],[328.14,0.01542],[328.21,151],[328.59,432.37],[328.6,8.479],[329,73.506902],[329.72,0.09],[329.8,1],[329.9,30],[329.98,1],[330,416.790075],[330.38,0.12],[330.42,0.151549],[330.7,0.01],[331,1.510972],[331.32,50],[331.7,0.09],[332,3.726208],[332.07,52.45048]]}'
    savedat = '''1502248327.53={"bids":['''
    outstr = '''1502248327.53={"bids":['''
    for i in range(29):#buy
        outstr += '[355.1,100],'
    outstr += '''[350.1,101.1]],"asks":['''
    for i in range(29):#sell
        outstr += '[360.1,200],'
    outstr += '''[362.1,52.45048]]}'''

    aaa = outstr.split('=')[1]

    jsdat = json.loads(aaa)
    print jsdat['bids']
    tradetool.lastOpt = 1
    tradetool.addDepth(outstr)
if __name__ == '__main__':
    # test()
    main()