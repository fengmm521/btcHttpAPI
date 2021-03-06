
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys,os
import json
import math

datapth = 'btc38/data.txt'
#1498064693.62={"ticker":{"high":355.01,"low":301.1,"last":341.21,"vol":213413.588686,"buy":341.21,"sell":343.88}}
def getTicker():
    f = open(datapth,'r')
    lines = f.readlines()
    f.close()
    outs = []
    for l in lines:
        tmp = l.split('=')
        if len(tmp[1]) > 10:
            tmp2 = tmp[1].replace('\n','')
            outs.append([tmp[0],tmp2])
    return outs


def printDat(dats,vs):
    for n in range(len(dats)):
        if dats[n] != 0 and abs(dats[n]) > 0.05:
            print dats[n],vs[n]


def main():
    
    lines = getTicker()

    print len(lines)
    print lines[0]
    dats = []
    vs = []
    t0 = float(lines[0][0])
    js0 = json.loads(lines[0][1])
    v0 = float(js0['ticker']['last'])
    print t0,v0
    isFirst = True
    for l in lines:
        if isFirst:
            t0 = float(l[0])
            js0 = json.loads(l[1])
            v0 = float(js0['ticker']['last'])
            isFirst = False
        else:
            t1 = float(l[0])
            if t1 > t0:
                js0 = json.loads(l[1])
                v1 = float(js0['ticker']['last'])
                print t0,t1
                dat = ( v1 - v0 )/(t1 - t0)
                dats.append(dat)
                vs.append(v1)
                t0 = t1
                v0 = v1


    print len(dats)
    print len(vs)
    printDat(dats, vs)

    
if __name__ == '__main__':
    main()