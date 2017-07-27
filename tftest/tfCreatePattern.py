#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys,os
import datadown
import json
os.environ['PATH'] = '/usr/bin/:/usr/sbin/'
import numpy as np

logpth = './data'
linetmp = '1499443213.63={"bids":[[323.11,4.694431],[322.97,0.000958],[322.21,383.5],[322.2,6.246023],[322.1,2.573186],[322,4.949218],[320.02,1.55],[319.4,0.004696],[318.28,0.155533],[318,190.267365],[317.5,0.827036],[317,3],[316.3,310.263082],[316.25,18.46821],[316.01,4.659856],[316,9.106349],[315.07,1.932391],[315,10.05294],[314.58,0.157398],[314.33,2],[313.2,1.58997],[313,12.971468],[312,26.6393],[311.21,76],[311.02,34.885479],[310.78,0.159282],[310.11,20.322466],[310.1,2.027281],[310.06,74.913644],[310,585.941211]],"asks":[[324.48,1.954824],[324.5,14.840507],[325.5,58.342098],[325.86,0.004626],[325.97,0.153382],[326,9.92],[326.99,21.981108],[327,55.175224],[328,2],[329,103.791893],[329.5,96.416515],[330,452.882972],[330.01,0.151557],[331,31.682048],[332,5.206615],[332.96,94.00314],[332.99,19.96],[333,60],[333.84,0.149758],[335,114.894008],[335.62,212.71178],[335.88,1.094527],[336,10],[336.5,10],[336.96,15.396623],[337,15],[337.29,3],[337.85,0.147983],[338,11],[338.67,20.930765]]}'

basevalue = [] #基本价，最大挂单数量,数量数据比例缩放,最小值，最大值
countScale = 100.0
outmin = 99999
outmax = -9999

def getLogDataLines(logpth):
    f = open(logpth,'r')
    lines = f.readlines()
    f.close()
    return lines

def conventLineData(lineDat):
    dats = []
    if not lineDat:
        dats = linetmp.split('=')
    else:
        dats = lineDat.split('=')
    if not (len(dats) == 2 and len(dats[1]) > 10):
        return None
    datdic = json.loads(dats[1])
    dids = datdic['bids']
    asks = datdic['asks']
    if not basevalue:
        basevalue.append(dids[0][0])
        basevalue.append(0)
        basevalue.append(countScale)  #挂单数量，数值敏感度大小缩放
        basevalue.append(9999)       #最小值
        basevalue.append(-9999)        #最大值
    tmpbase = basevalue[0]
    outdats = []

    asks.reverse()
    for d in asks:
        tmpls = []
        tmpls.append(d[0] - tmpbase)
        if d[1] > basevalue[1]:
            basevalue[1] = d[1]
        tmpls.append(d[1])
        outdats.append(tmpls)
    outdats.append([dids[0][0] - tmpbase])
    for d in dids:
        tmpls = []
        tmpls.append(d[0] - tmpbase)
        if d[1] > basevalue[1]:
            basevalue[1] = d[1]
        tmpls.append(d[1])
        outdats.append(tmpls)
    outdatmp = []
    bassecount = basevalue[1]/countScale  #给数量数值进行缩放
    for p in outdats:
        if len(p) == 2:
            p[1] = p[1]/bassecount
        outdatmp = outdatmp + p
    mintmp = np.min(outdatmp)
    if mintmp < basevalue[3]:
        basevalue[3] = mintmp
    maxtmp = np.max(outdatmp)
    if maxtmp > basevalue[4]:
        basevalue[4] = maxtmp
    return outdatmp

def getPattern():
    _tlog,deplogs = datadown.allLogFiles()
    alllines = []
    for l in deplogs:
        tmppth = logpth + os.sep  + 'depth_' + l + '.txt'
        tmploglines = getLogDataLines(tmppth)
        alllines = alllines + tmploglines
    outlines = []
    for l in alllines:
        tmpl = l.replace('\n','')
        datline = conventLineData(tmpl)
        if datline:
            outlines.append(datline)
    return outlines

def savePatternToFile(pth):
    pattern = getPattern()
    f = open(pth,'w') #'a+'
    basestr = str(basevalue) + '\n'
    f.write(basestr)
    for p in pattern:
        linestr = str(p) + '\n'
        f.write(linestr)
    f.close()
    
def main():
    savePatternToFile('pattern/pattern.txt')
    # pattern = getPattern()
    # print len(pattern)
    # print pattern[-1]
if __name__ == '__main__':
    main()