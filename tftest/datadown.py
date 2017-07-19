#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys,os
import pathtool
import timetool

# scp root@btc.woodcol.com:/home/woodcol/btcctrade/test/btc38http/*.txt ./data/
    
datapth = 'data'


def getLogDateDic(logfs,isLog = True):
    logs = []
    if isLog:
        logs = logfs
    else:
        for l in logfs:
            logs.append(l[6:])
    dates = {}
    for d in logs:
        ds = d.split('_')
        tmpd = int(ds[0])*10000 + int(ds[1])*100 + int(ds[2])
        dates[tmpd] = d
    return dates

#获取最近一天数据日期
def getlastLogDate(logfs,isLog = True):
    dates = getLogDateDic(logfs,isLog)
    sorts = dates.keys()
    tmpls = sorted(sorts,reverse=True)
    return dates[tmpls[0]]

#获取log数据开始保存的第一天时间
def getFirstLogDate(logfs,isLog = True):
    dates = getLogDateDic(logfs,isLog)
    sorts = dates.keys()
    tmpls = sorted(sorts)
    return dates[tmpls[0]]

def getHeaveLogFiles():
    atxtfiles = pathtool.getAllExtFile(datapth,'.txt')
    tradetxtfs = []
    depthfs = []
    for n in atxtfiles:
        if n[2][:4] == '2017':
            tradetxtfs.append(n[2])
        elif n[2][:5]== 'depth':
            depthfs.append(n[2])
    return tradetxtfs,depthfs

def getDataLogFromServer(startDate):
    todeydate = timetool.getDateDay()
    print todeydate
    if startDate == todeydate:
        return
    


def main():
    tradefs,depthfs = getHeaveLogFiles()
    lastdate = getlastLogDate(tradefs)
    firstDate = getFirstLogDate(tradefs)
    print firstDate,lastdate
    lastdate = getlastLogDate(depthfs,False)
    firstDate = getFirstLogDate(depthfs,False)
    print firstDate,lastdate
    

if __name__ == '__main__':
    main()