#!/usr/bin/env python# -*- coding: utf-8 -*-import sys,osimport httplibimport timeimport tradeManger import timetoolhttpClient = Nonetradetool = tradeManger.TradeManger() def getTicker():    try:        httpClient = httplib.HTTPConnection('api.btc38.com', 80, timeout=30)        httpClient.request('GET', '/v1/ticker.php?c=ltc&mk_type=cny')        response = httpClient.getresponse()        data = response.read()        return data    except Exception, e:        print e    finally:        if httpClient:            httpClient.close()    return 0def main():    timeouttimes = 0    while True:        tickertmp = getTicker()        if tickertmp == 0:            timeouttimes += 1            f = open('timeoutlog.txt','a+')            savestr = 'timeout->times:' + str(timeouttimes) + ',time:' + str(timetool.getNowDate())            f.write(savestr)            time.sleep(15)        else:            fname = timetool.getDateDay() + '.txt'            f = open(fname,'a+')            savedat = str(time.time()) + '=' + tickertmp + '\n'            tradetool.addTicker(savedat)            f.write(savedat)            f.close()            time.sleep(30)if __name__ == '__main__':    main()