#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-01-17 16:53:27
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$

import os,sys
import urllib2
import chardet
import json
import time

#获取脚本路径
def cur_file_dir():
    pathx = sys.argv[0]
    tmppath,_file = os.path.split(pathx)
    if cmp(tmppath,'') == 0:
        tmppath = sys.path[0]
    #判断为脚本文件还是py2exe编译后的文件，如果是脚本文件，则返回的是脚本的目录，如果是py2exe编译后的文件，则返回的是编译后的文件路径
    if os.path.isdir(tmppath):
        return tmppath
    elif os.path.isfile(tmppath):
        return os.path.dirname(tmppath)
    
#获取父目录
def GetParentPath(strPath):
    if not strPath:
        return None;
    lsPath = os.path.split(strPath);
    if lsPath[1]:
        return lsPath[0];
    lsPath = os.path.split(lsPath[0]);
    return lsPath[0];

#获取目录下的所有类型文件
def getAllExtFile(pth,fromatx = ".erl"):
    jsondir = pth
    jsonfilelist = []
    for root, _dirs, files in os.walk(jsondir):
        for filex in files:          
            #print filex
            name,text = os.path.splitext(filex)
            if cmp(text,fromatx) == 0:
                jsonArr = []
                rootdir = pth
                dirx = root[len(rootdir):]
                pathName = dirx +os.sep + filex
                jsonArr.append(pathName)
                (newPath,_name) = os.path.split(pathName)
                jsonArr.append(newPath)
                jsonArr.append(name)
                jsonfilelist.append(jsonArr)
            elif fromatx == ".*" :
                jsonArr = []
                rootdir = pth
                dirx = root[len(rootdir):]
                pathName = dirx +os.sep + filex
                jsonArr.append(pathName)
                (newPath,_name) = os.path.split(pathName)
                jsonArr.append(newPath)
                jsonArr.append(name)
                jsonfilelist.append(jsonArr)
    return jsonfilelist

class CoinesTool(object):
    """docstring for CoinesTool"""
    def __init__(self):
        self.ltcPriceS = []
        self.btcPrice = []
        self.ethPrice = []
        self.bchPrice = []
        self.usdtPrice = 1.0

        self.bases = ['btc','usdt','eth','bch']

        self.lastGetTime = 0 

    def conventStrTOUtf8(self,oldstr):
        try:
            nstr = oldstr.encode("utf-8")
            return nstr
        except Exception as e:
            print 'nstr do not encode utf-8'
        cnstrtype = chardet.detect(oldstr)['encoding']
        utf8str =  oldstr.decode(cnstrtype).encode('utf-8')
        return utf8str


    def getBasePrice(self):
        jstr = self.getUrl('https://www.okex.com/api/v1/depth.do?symbol=eth_usdt')
        jdic = json.loads(jstr)
        if jdic:
            print '-------eth usdt------------'
            print jdic['ticker']

        time.sleep(0.1)
        jstr = self.getUrl('https://www.okex.com/api/v1/depth.do?symbol=btc_usdt')
        jdic = json.loads(jstr)
        if jdic:
            print '-------btc usdt------------'
            print jdic['ticker']
        else:
            print '-------btc usdt-------erro-----' 
        time.sleep(0.1)
        
        jstr = self.getUrl('https://www.okex.com/api/v1/depth.do?symbol=eth_btc')
        jdic = json.loads(jstr)
        if jdic:
            print '-------eth btc------------'
            print jdic['ticker']
        else:
            print '-------eth btc-------erro-----' 
        time.sleep(0.1)

        jstr = self.getUrl('https://www.okex.com/api/v1/depth.do?symbol=bch_usdt')
        jdic = json.loads(jstr)
        if jdic:
            print '-------bch usdt------------'
            print jdic['ticker']
        else:
            print '-------bch usdt-------erro-----' 
        time.sleep(0.1)

        jstr = self.getUrl('https://www.okex.com/api/v1/depth.do?symbol=bch_btc')
        jdic = json.loads(jstr)
        if jdic:
            print '-------btc btc------------'
            print jdic['ticker']   
        else:
            print '-------btc btc-------erro-----' 
        time.sleep(0.1)

        jstr = self.getUrl('https://www.okex.com/api/v1/depth.do?symbol=bch_eth')
        jdic = json.loads(jstr)
        if jdic:
            print '-------bch eth------------'
            print jdic['ticker']   
        else:
            print '-------bch eth-------erro-----'
        time.sleep(0.1)

    def getPriceWithCoinName(self,coinname):

        symbols = []
        bases = ['btc','usdt','eth','bch']

        for b in self.bases:
            tmpsy = coinname + '_' + b
            
            print tmpsy
            tmpurl = 'https://www.okex.com/api/v1/depth.do?symbol=%s'%(tmpsy)
            jstr = self.getUrl(tmpurl)
            jdic = json.loads(jstr)
            if jdic:
                print '-------%s------------'%(tmpsy)
                print jdic['ticker']
            else:
                print '-------%s-------erro-----'%(tmpsy)
            time.sleep(0.1)


    def getURLFroPrices(self,symbols):
        for s in symbols:
            print s
            tmpurl = 'https://www.okex.com/api/v1/depth.do?symbol=%s'%(s)
            jstr = self.getUrl(tmpurl)
            jdic = json.loads(jstr)
            if jdic:
                print '-------%s------------'%(s)
                print jdic['ticker']
            else:
                print '-------%s-------erro-----'%(s)
            time.sleep(0.1)

    def getUrl(self,purl):
        try:
            req = urllib2.Request(purl)
            req.add_header('User-agent', 'Mozilla 5.10')
            res = urllib2.urlopen(req)
            html = self.conventStrTOUtf8(res.read())
            return html
        except Exception, e:
            print e
        return None

def main():
    ctool = CoinesTool()
    ctool.getBasePrice()

#测试
if __name__ == '__main__':
    main()
    # args = sys.argv
    # fpth = ''
    # if len(args) == 2 :
    #     if os.path.exists(args[1]):
    #         fpth = args[1]
    #     else:
    #         print "请加上要转码的文件路径"
    # else:
    #     print "请加上要转码的文件路径"


    
