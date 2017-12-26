#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-09-04 20:06:13
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$

import os
import codecs
import sys
import xlrd
import time
import urllib2
import socket  
import shutil 

import json
import time

#将所有Excel文件转为xml文件
reload(sys)
sys.setdefaultencoding( "utf-8" )

def cur_file_dir():
    #获取脚本路径
    path = sys.path[0]
    #判断为脚本文件还是py2exe编译后的文件，如果是脚本文件，则返回的是脚本的目录，如果是py2exe编译后的文件，则返回的是编译后的文件路径
    if os.path.isdir(path):
        return path
    elif os.path.isfile(path):
        return os.path.dirname(path)

#获取父目录
def GetParentPath(strPath):
    if not strPath:
        return None;
    lsPath = os.path.split(strPath);
    if lsPath[1]:
        return lsPath[0];
    lsPath = os.path.split(lsPath[0]);
    return lsPath[0];

#获取LTC的400天日K线数据
#https://www.okex.com/api/v1/future_kline.do?symbol=ltc_usd&type=1day&contract_type=this_week&size=400

#获取BTC的400天日K线数据
#https://www.okex.com/api/v1/future_kline.do?symbol=btc_usd&type=1day&contract_type=this_week&size=400

#获取LTC一年的难度变化数据,当要取几个月的数据就把month的值设为几
# http://ltc.btcfans.com/difficulty.php?month=12

#获取BTC一年的难度变化数据,当要取几个月的数据就把month的值设为几
# http://mining.btcfans.com/difficulty.php?month=12


#获取所有界面的json文件列表
def getAllExtFile(path,fromatx = ".txt"):
    jsondir = path
    jsonfilelist = []
    for root, _dirs, files in os.walk(jsondir):
        for filex in files:          
            #print filex
            name,text = os.path.splitext(filex)
            if cmp(text,fromatx) == 0:
                jsonArr = []
                rootdir = path
                dirx = root[len(rootdir):]
                pathName = dirx +os.sep + filex
                jsonArr.append(pathName)
                (newPath,_name) = os.path.split(pathName)
                jsonArr.append(newPath)
                jsonArr.append(name)
                jsonfilelist.append(jsonArr)
    return jsonfilelist

def btcupleve():
    #shutil.rmtree(dbDir)#删除目录下所有文件 
    strtmp = '''1 2017-07-02 08:00    14.04天  16,422,050  1,796 BTC   708,659,466,230 -0.4%
2   2017-07-14 16:00    12.33天  16,447,213  2,040 BTC   804,525,194,568 13.5%
3   2017-07-27 19:00    13.13天  16,472,500  1,927 BTC   860,221,984,436 6.9%
4   2017-08-09 20:00    13.04天  16,497,813  1,941 BTC   923,233,068,448 7.3%
5   2017-08-24 10:00    14.58天  16,522,850  1,717 BTC   888,171,856,257 -3.8%
6   2017-09-06 21:00    13.46天  16,548,038  1,872 BTC   922,724,699,725 3.9%
7   2017-09-18 14:00    11.71天  16,573,238  2,152 BTC   1,103,400,932,964   19.6%
8   2017-10-02 08:00    13.75天  16,598,425  1,832 BTC   1,123,863,285,132   1.9%
9   2017-10-15 12:00    13.17天  16,623,725  1,922 BTC   1,196,792,694,098   6.5%
10  2017-10-27 01:00    11.54天  16,648,875  2,179 BTC   1,452,839,779,145   21.4%
11  2017-11-10  0.0     14.92天  16,674,025  1,686 BTC   1,364,422,081,125   -6.1%
12  2017-11-25 04:00    14.21天  16,699,250  1,775 BTC   1,347,001,430,558   -1.3%
13  2017-12-07 00:00    11.83天  16,724,400  2,125 BTC   1,590,896,927,258   18.1%'''
    strtmp = strtmp.replace('\r','')
    strtmp = strtmp.replace('天','')
    strtmp = strtmp.replace('%','')
    lines = strtmp.strip().split('\n')

    dats = []
    daycount = 0
    precents = []
    for n in range(len(lines)):
        l = lines[n].replace('\n','')
        l = ' '.join(l.split())
        tmpls = l.split(' ')
        daycount += float(tmpls[3])
        precents.append(float(tmpls[8]))
        dats.append(tmpls)
        
    upleve = 1
    for f in precents:
        upleve = upleve * (1 + (f/100.0))
    startprice = 2571.0
    endprice = startprice*upleve
    realprice = 12780.0
    realleve = realprice/startprice
    subleve = realleve - upleve


    outstr = 'upleve:%.4f,startdate:20170615,enddate:20171207,daycount:%d,startprice:%.2f,endpricate:%.2f,realprice:%.2f'%(upleve,daycount,startprice,endprice,realprice)
    outstr = outstr.replace(',', '\n')

    print '---------------BTC------------------'
    print outstr
    print 'realleve:%.4f'%(realleve)
    print 'subleve:%.4f'%(subleve)


def ltcupleve():
    strtmp = '''1   2017-06-11 12:00    4.46天   51,492,000  11,243 LTC  197,309 -21.8%
2   2017-06-14 12:00    3天  51,542,375  16,792 LTC  230,315 16.7%
3   2017-06-18 01:00    3.54天   51,593,050  14,308 LTC  228,364 -0.8%
4   2017-06-21 0.0 2.96天   51,643,500  17,054 LTC  271,188 18.8%
5   2017-06-24 17:00    3.71天   51,693,575  13,503 LTC  255,206 -5.9%
6   2017-06-28 09:00    3.67天   51,744,000  13,752 LTC  243,262 -4.7%
7   2017-07-01 18:00    3.38天   51,794,450  14,948 LTC  252,730 3.9%
8   2017-07-05 07:00    3.54天   51,845,100  14,301 LTC  250,000 -1.1%
9   2017-07-08 11:00    3.17天   51,895,375  15,876 LTC  275,721 10.3%
10  2017-07-11 0.0      3.5天    51,945,725  14,386 LTC  275,264 -0.2%
11  2017-07-15 10:00    3.46天   51,996,150  14,581 LTC  279,351 1.5%
12  2017-07-18 15:00    3.21天   52,047,050  15,865 LTC  306,983 9.9%
13  2017-07-21 16:00    3.04天   52,095,107  15,800 LTC  350,564 14.2%
14  2017-07-24 19:00    3.13天   52,145,332  16,072 LTC  391,487 11.7%
15  2017-07-28 07:00    3.5天    52,196,107  14,507 LTC  394,147 0.7%
16  2017-07-31 10:00    3.13天   52,246,257  16,048 LTC  437,853 11.1%
17  2017-08-03 21:00    3.46天   52,296,507  14,530 LTC  442,599 1.1%
18  2017-08-07 09:00    3.5天    52,346,932  14,407 LTC  442,811 0.0%
19  2017-08-10 19:00    3.42天   52,397,482  14,795 LTC  455,770 2.9%
20  2017-08-14 05:00    3.42天   52,448,157  14,832 LTC  468,690 2.8%
21  2017-08-17 21:00    3.67天   52,498,457  13,718 LTC  445,867 -4.9%
22  2017-08-21 10:00    3.54天   52,548,507  14,132 LTC  439,031 -1.5%
23  2017-08-24 16:00    3.25天   52,599,357  15,646 LTC  476,041 8.4%
24  2017-08-27 20:00    3.17天   52,649,307  15,774 LTC  521,706 9.6%
25  2017-08-30 17:00    2.88天   52,699,957  17,617 LTC  636,921 22.1%
26  2017-09-02 0.0      3.25天   52,750,482  15,546 LTC  688,280 8.1%
27  2017-09-06 12:00    3.54天   52,800,832  14,216 LTC  680,770 -1.1%
28  2017-09-09 14:00    3.08天   52,851,307  16,370 LTC  776,333 14.0%
29  2017-09-13 04:00    3.58天   52,901,482  14,002 LTC  753,144 -3.0%
30  2017-09-16 13:00    3.38天   52,952,057  14,985 LTC  782,789 3.9%
31  2017-09-19 22:00    3.38天   53,002,432  14,926 LTC  811,072 3.6%
32  2017-09-23 06:00    3.33天   53,052,857  15,128 LTC  854,939 5.4%
33  2017-09-26 14:00    3.33天   53,102,957  15,030 LTC  891,545 4.3%
34  2017-09-30 01:00    3.46天   53,153,632  14,653 LTC  904,466 1.4%
35  2017-10-03 08:00    3.29天   53,204,007  15,304 LTC  964,781 6.7%
36  2017-10-06 19:00    3.46天   53,254,582  14,624 LTC  977,964 1.4%
37  2017-10-10 07:00    3.5天    53,304,857  14,364 LTC  976,769 -0.1%
38  2017-10-14 0.0       3.71天   53,355,132  13,557 LTC  919,587 -5.9%
39  2017-10-17 03:00    3.13天   53,405,757  16,200 LTC  1,034,782   12.5%
40  2017-10-20 16:00    3.54天   53,455,732  14,111 LTC  1,014,437   -2.0%
41  2017-10-24 04:00    3.5天    53,506,482  14,500 LTC  1,020,641   0.6%
42  2017-10-27 17:00    3.54天   53,556,932  14,245 LTC  1,008,067   -1.2%
43  2017-10-30 0.0      3.25天   53,607,107  15,438 LTC  1,081,832   7.3%
44  2017-11-03 16:00    3.71天   53,657,757  13,658 LTC  1,026,309   -5.1%
45  2017-11-07 03:00    3.46天   53,707,932  14,508 LTC  1,033,245   0.7%
46  2017-11-10 15:00    3.5天    53,758,332  14,400 LTC  1,032,184   -0.1%
47  2017-11-13 17:00    3.08天   53,809,057  16,451 LTC  1,180,143   14.3%
48  2017-11-17 13:00    3.83天   53,859,058  13,044 LTC  1,074,570   -8.9%
49  2017-11-20 16:00    3.13天   53,909,383  16,104 LTC  1,198,339   11.5%
50  2017-11-24 03:00    3.46天   53,959,908  14,610 LTC  1,222,812   2.0%
51  2017-11-27 12:00    3.38天   54,010,508  14,993 LTC  1,260,400   3.1%
52  2017-11-30 11:00    2.96天   54,061,158  17,121 LTC  1,502,849   19.2%
53  2017-12-04 05:00    3.75天   54,111,033  13,300 LTC  1,391,848   -7.4%'''
    strtmp = strtmp.replace('\r','')
    strtmp = strtmp.replace('天','')
    strtmp = strtmp.replace('%','')
    lines = strtmp.strip().split('\n')

    dats = []
    daycount = 0
    precents = []
    for n in range(len(lines)):
        l = lines[n].replace('\n','')
        l = ' '.join(l.split())
        tmpls = l.split(' ')
        daycount += float(tmpls[3])
        precents.append(float(tmpls[8]))
        dats.append(tmpls)

    upleve = 1
    for f in precents:
        upleve = upleve * (1 + (f/100.0))
    startprice = 31.0
    endprice = startprice*upleve
    realprice = 106.0
    realleve = realprice/startprice
    subleve = realleve - upleve

    outstr = 'upleve:%.4f,startdate:20170610,enddate:20171204,daycount:%d,startprice:%.2f,endpricate:%.2f,realprice:%.2f'%(upleve,daycount,startprice,endprice,realprice)
    outstr = outstr.replace(',', '\n')

    print '---------------LTC------------------'
    print outstr
    print 'realleve:%.4f'%(realleve)
    print 'subleve:%.4f'%(subleve)


import time  
import datetime  
import pytz

def test():




    times='Mon,18 Dec 2017 7:40:09 am'  #PST = GTM-8
    time_format=datetime.datetime.strptime(times,'%a,%d %b %Y %H:%M:%S %p')  
    print time_format 

    print time.strftime('%Z', time.gmtime())
    times='Mon,18 Dec 2017 7:40:09 am'
    outtime = time.strptime(times,'%a,%d %b %Y %H:%M:%S %p')
    print outtime

    print 'utctime:',time.gmtime()

    now_utc = pytz.utc.localize(datetime.datetime.now())
    now_pst = now_utc.astimezone(pytz.timezone('US/Pacific'))

    print now_utc
    print now_pst

    tmpt = pytz.timezone('US/Pacific')
    print tmpt


def getUrl(purl):
    try:
        req = urllib2.Request(purl)
        req.add_header('User-agent', 'Mozilla 5.10')
        res = urllib2.urlopen(req)
        html = res.read()
        return html
    except Exception, e:
        print e
    return None

def getDateDayWithTime(ptime = None):
    loctim = time.localtime(ptime)
    #time.struct_time(tm_year=2015, tm_mon=8, tm_mday=2, tm_hour=12, tm_min=16, tm_sec=47, tm_wday=6, tm_yday=214, tm_isdst=0)
    sendmsg = str(loctim.tm_year) + '-' + str(loctim.tm_mon) + '-' +  str(loctim.tm_mday)
    return sendmsg
if __name__ == '__main__':  
    # btcupleve()
    # ltcupleve()

    # test()

    purl = 'https://www.okex.com/api/v1/future_kline.do?symbol=ltc_usd&type=1day&contract_type=this_week&size=400'

    dats = getUrl(purl)
    print dats

    dats = json.loads(dats)

    for d in dats:
        print getDateDayWithTime(int(d[0])/1000),d
    