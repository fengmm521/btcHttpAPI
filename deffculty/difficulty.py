#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-09-04 20:06:13
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$

import os
import sys

import difficultTool

#将所有Excel文件转为xml文件
reload(sys)
sys.setdefaultencoding( "utf-8" )

def cur_file_dir()
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


def getLTCDiffculty():
    moneyTool = difficultTool.DifficultyLTCTool()
    ggdats = moneyTool.moneyMsg('ltc')

    for k in ggdats.keys():
        print k,ggdats[k]

    moneyTool.wdriver.quit()

def getBTCDiffculty():
    moneyTool = difficultTool.DifficultyLTCTool()
    ggdats = moneyTool.moneyMsg('btc')

    for k in ggdats.keys():
        print k,ggdats[k]

    moneyTool.wdriver.quit()

def getLTCDiffcultyCNWeb():
    pass

def getBTCDiffcultyCNWeb():
    pass

def main(ptype):
    if ptype == 'ltc' or ptype == 'LTC':
        getLTCDiffculty()
    elif ptype == 'ltccn' or ptype == 'LTCCN':
        getLTCDiffcultyCNWeb()
    elif ptype == 'btc' or ptype == 'BTC':
        getBTCDiffculty()
    elif ptype == 'btccn' or ptype == 'BTCCN':
        getBTCDiffcultyCNWeb()

if __name__ == '__main__':  
    args = sys.argv
    fpth = ''
    if len(args) == 2 :
        ptype = args[1]
        print ptype
        main(ptype)
    else:
        print "请加上要获取的数据货币类型，目前支持ltc,ltccn,btc,btccn"
    