#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys,os
sys.path.append('../tftest')
sys.path.append('../httptool')

import pathtool
import timetool
import btchttpstool
import json


#获取okex季合约某一天的5分钟k线数据
def getOneDay5minKline(tday):
    psize = (24*60)/5
    daytime = int(timetool.geTimeStampFromStrDate(tday))
    jsonstr = btchttpstool.get5minKlineWithStartTimetamp(daytime)
    k5linedats = None
    if jsonstr:
        k5linedats = json.loads(jsonstr)
    else:
        print '获取 %s 5分钟k线数据错误...'%(tday)
    return k5linedats

def main():
    
    # print pathtool.cur_file_dir()
    # print len(dates)
    daytime = int(timetool.geTimeStampFromStrDate('2017_8_10'))

    print daytime
    print timetool.getNowDate(daytime)

    todaydats = getOneDay5minKline('2017_8_10')

    print len(todaydats)
    print todaydats[0]
    print todaydats[-1]
    # print todaydats

    print timetool.getNowDate(todaydats[0][0]/1000)
    print timetool.getNowDate(todaydats[-1][0]/1000)

if __name__ == '__main__':
    main()