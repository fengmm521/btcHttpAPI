#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys,os
import httplib
import time
import json
import urllib2
 

#https://www.okex.com/api/v1/future_ticker.do?symbol=ltc_usd&contract_type=this_week
def getTicker():
    try:
        req = urllib2.Request('https://www.okex.com/api/v1/future_ticker.do?symbol=ltc_usd&contract_type=this_week')
        req.add_header('User-agent', 'Mozilla 5.10')
        res = urllib2.urlopen(req,data=None,timeout=8)
        html = res.read()
        return html
    except Exception, e:
        print e
    return 0
#depth--https://www.okex.com/api/v1/future_depth.do?symbol=ltc_usd&size=30&contract_type=this_week
def getDepth(ttype = 'ltc'):
    tradetype = 'ltccny'
    if ttype == 'btc':
        tradetype = 'btccny'
    elif ttype == 'ltc':
        tradetype = 'ltccny'
    else:
        print 'ttype set erro'
        return
    urlrequ = 'https://www.okex.com/api/v1/future_depth.do?symbol=%s_usd&size=30&contract_type=this_week'%(ttype)
    try:
        req = urllib2.Request(urlrequ)
        req.add_header('User-agent', 'Mozilla 5.10')
        res = urllib2.urlopen(req,data=None,timeout=8)
        html = res.read()
        return html
    except Exception, e:
        print e
    return 0

#获取okex季合约5分钟k线数据
def get5minKlineWithStartTimetamp(ptimetamp,ttype = 'ltc'):
    psize = (24*60)/5
    # psize = 0

    daytime = int(ptimetamp)

    tmpdaytimestr = str(daytime)

    if len(tmpdaytimestr) == 10:
        daytime = daytime*1000
    elif len(tmpdaytimestr) != 13:
        print '时间戳格式出错，要求是13位毫秒时间戳'
        return

    tradetype = 'ltc_usd'
    if ttype == 'btc':
        tradetype = 'btc_usd'
    elif ttype == 'ltc':
        tradetype = 'ltc_usd'
    else:
        print 'ttype set erro'
        return
    print '开始下载5分钟k线数据...'
    urlrequ = 'https://www.okex.com/api/v1/future_kline.do?symbol=%s&type=5min&contract_type=quarter&size=%d&since=%d'%(tradetype,psize,daytime)
    print 'url:%s'%(urlrequ)
    try:
        req = urllib2.Request(urlrequ)
        req.add_header('User-agent', 'Mozilla 5.10')
        res = urllib2.urlopen(req,data=None,timeout=8)
        html = res.read()
        return html
    except Exception, e:
        print e
        print '下载超时...'
    return 0

def main():
    k5line = get5minKlineWithStartTimetamp(time.time() - 100000)
    k5line = json.loads(k5line)
    print len(k5line)
    print k5line
if __name__ == '__main__':
    main()
    # depstr = getDepth('ltc')
    # print depstr
