#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys,os

import httplib

import time

import tradeManger
 
import timetool

httpClient = None
tradetool = tradeManger.TradeManger()
tradetool.setNetBuyAndSellConfig(278.1, 0.8, 288.1, 0.8)
 
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
            fname = 'depth_' + timetool.getDateDay() + '.txt'
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
            fname = timetool.getDateDay() + '.txt'
            f = open(fname,'a+')
            savedat = str(time.time()) + '=' + tickertmp + '\n'
            tradetool.addTicker(savedat)
            f.write(savedat)
            f.close()
            time.sleep(27)
if __name__ == '__main__':
    main()