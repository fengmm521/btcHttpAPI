#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import datetime
# loctim = time.localtime()
# #time.struct_time(tm_year=2015, tm_mon=8, tm_mday=2, tm_hour=12, tm_min=16, tm_sec=47, tm_wday=6, tm_yday=214, tm_isdst=0)
# sendmsg = str(loctim.tm_mon) + '_' +  str(loctim.tm_mday) + '_' + str(loctim.tm_hour) + '_' + str(loctim.tm_min) + '_' + str(loctim.tm_sec)

# print sendmsg


# datex = time.localtime(1459179579)
# sendmsg = str(datex.tm_mon) + '.' +  str(datex.tm_mday) + '_' + str(datex.tm_hour) + ':' + str(datex.tm_min) + ':' + str(datex.tm_sec)
# print sendmsg


# a = [1,2,3,6]
# b = [5,9,10]
# a = a + b
# print a

# print "aa", time.time()
# print time.localtime(time.time() + 60 *3)


def datetime2timestamp(dt, convert_to_utc=False):
    ''' Converts a datetime object to UNIX timestamp in milliseconds. '''
    if isinstance(dt, datetime.datetime):
        if convert_to_utc: # 是否转化为UTC时间
            dt = dt + datetime.timedelta(hours=-8) # 中国默认时区
        timestamp = datetime.timedelta.total_seconds(dt - datetime.datetime(1970,1,1))
        return long(timestamp)
    return dt
def timestamp2datetime(timestamp, convert_to_local=False):
    ''' Converts UNIX timestamp to a datetime object. '''
    if isinstance(timestamp, (int, long, float)):
        dt = datetime.datetime.utcfromtimestamp(timestamp)
        if convert_to_local: # 是否转化为本地时间
            dt = dt + datetime.timedelta(hours=8) # 中国默认时区
        return dt
    return timestamp

def timestamp_utc_now():
    return datetime2timestamp(datetime.datetime.utcnow())

def getNowDate(ptime = None):
    if ptime:
        return timestamp2datetime(int(ptime),True)
    return timestamp2datetime(int(time.time()),True)

def getDateDay():
    loctim = time.localtime()
    #time.struct_time(tm_year=2015, tm_mon=8, tm_mday=2, tm_hour=12, tm_min=16, tm_sec=47, tm_wday=6, tm_yday=214, tm_isdst=0)
    sendmsg = str(loctim.tm_year) + '_' + str(loctim.tm_mon) + '_' +  str(loctim.tm_mday)
    return sendmsg


if __name__ == '__main__':
    # print datetime.datetime.utcnow()
    # print timestamp_utc_now()
    print timestamp2datetime(int(time.time()),True)
    # outstr = timestamp2datetime(int(time.time() + 60 * 5),True)
    # print outstr