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

def sortLogDate(logs):
    dates = []
    if logs[0].find('depth') != -1:
        dates = getLogDateDic(logs,False)
    else:
        dates = getLogDateDic(logs,True)
    sorts = dates.keys()
    tmpls = sorted(sorts,reverse=False)
    outlogs = []
    for k in tmpls:
        outlogs.append(dates[k])
    return outlogs

def allLogFiles():
    tlogfiles,deplogfiles = getHeaveLogFiles()
    outlogs = sortLogDate(tlogfiles)
    outdlogs = sortLogDate(deplogfiles)
    if len(outlogs) != len(outdlogs):
        print 'depdata not eque logdata!'
    return outlogs,outdlogs

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

def getDataLogFromServer(logDate):
    localfilepth = './data/%s.txt'%(logDate)
    cmd = ''
    if os.path.exists(localfilepth):
        cmd = '/bin/rm %s'%(localfilepth)
        os.system(cmd)
    cmd = 'scp root@btc.woodcol.com:/home/woodcol/btcctrade/test/btc38http/data/%s.txt ./data/'%(logDate)
    os.system(cmd)
    cmd = 'scp root@btc.woodcol.com:/home/woodcol/btcctrade/test/btc38http/data/depth_%s.txt ./data/'%(logDate)
    os.system(cmd)
    print 'downd %s end'%(logDate)
def getNewLogFromServer():
    tradefs,depthfs = getHeaveLogFiles()
    lastdate = getlastLogDate(tradefs)
    firstDate = getFirstLogDate(tradefs)
    print firstDate,lastdate
    lastdate = getlastLogDate(depthfs,False)
    firstDate = getFirstLogDate(depthfs,False)
    print firstDate,lastdate
    lastdate = timetool.getLastDayDate(lastdate)
    print lastdate
    needdowndays = timetool.getDateDaysFromOneDate(lastdate)
    print needdowndays
    for d in needdowndays:
        print 'start downloding %s...'%(d)
        getDataLogFromServer(d)



def main():
    getNewLogFromServer()
    
    

if __name__ == '__main__':
    main()