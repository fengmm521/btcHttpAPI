#!/usr/bin/env python
#-*- coding: utf-8 -*-
import os
import sys
import time
import chardet  #中文编码判断

import json

import pylab as pl

reload(sys)
sys.setdefaultencoding( "utf-8" )

class MatplotTool(object):
    """docstring for ClassName"""
    def __init__(self, isPoint = False):
        
        self.isPoint = isPoint
        
    def drawPlot(self,listx,listy,pcolor = 'g'):
        pl.plot(listx,listy,pcolor)
    def show(self):
        pl.show()

    def drawDifficult(self,datas,count = 0):
        x = []
        y1 = []
        y2 = []
        if count == 0:
            count = len(datas)
        tmpdats = datas[:count]
        datasback = tmpdats[::-1] 
        dates = []
        for n in range(len(datasback)):
            if n == 0:
                x.append(n + 1)
                pdif = datasback[n][4][:-1]
                pmon = datasback[n][4][:-1]
                difp = float(pdif)
                monp = float(pmon)
                y1.append(difp)
                y2.append(monp)
                dates.append(datasback[n][0])
            elif n < len(datasback) - 1:
                x.append(n + 1)
                pdif = datasback[n][4][:-1]
                pmon = (float(datasback[n][5]) - float(datasback[n-1][5]))/float(datasback[n-1][5])
                difp = float(pdif)
                monp = float(pmon)*100
                y1.append(difp)
                y2.append(monp)
                dates.append(datasback[n][0])

        print 'draw update count:',count
        print 'day from %s to %s'%(dates[0],dates[-1])

        self.drawPlot(x, y1,'g')
        self.drawPlot(x, y2,'b')
        self.show()

    def drarDiffcultWithAdd(self,datas,count = 0):
        x = []
        y1 = []
        y2 = []
        if count == 0:
            count = len(datas)
        tmpdats = datas[:count]
        datasback = tmpdats[::-1] 
        dates = []
        dicdat = {}
        basedif = float(datasback[0][2])
        baseprice = float(datasback[0][5])

        y1add = []
        y2add = []
        for n in range(len(datasback)):
            if n == 0:
                x.append(n + 1)
                pdif = datasback[n][4][:-1]
                pmon = datasback[n][4][:-1]
                difp = float(pdif)
                monp = float(pmon)

                y1.append(difp)
                y2.append(monp)

                y1addtmp = basedif / basedif
                y2addtmp = baseprice / baseprice
                y1add.append(y1addtmp)
                y2add.append(y2addtmp)

                dates.append(datasback[n][0])
                dicdat[datasback[n][0]] = datasback[n]
            else:
                x.append(n + 1)
                pdif = datasback[n][4][:-1]
                pmon = (float(datasback[n][5]) - float(datasback[n-1][5]))/float(datasback[n-1][5])
                difp = float(pdif)
                monp = float(pmon)*100
                y1.append(difp)
                y2.append(monp)

                y1addtmp = float(datasback[n][2]) / basedif
                y2addtmp = float(datasback[n][5]) / baseprice
                y1add.append(y1addtmp)
                y2add.append(y2addtmp)

                dates.append(datasback[n][0])
                dicdat[datasback[n][0]] = datasback[n]
        
        for n in range(len(y1add)):
            tmpstr1 = 'd:%.2f'%(y1add[n])
            dicdat[dates[n]].append(tmpstr1)
            tmpstr2 = 'p:%.2f'%(y2add[n])
            dicdat[dates[n]].append(tmpstr2)
            print n,dicdat[dates[n]]
        print 'draw update count:',count
        print 'day from %s to %s'%(dates[0],dates[-1])

        self.drawPlot(x, y1add,'g')
        self.drawPlot(x, y2add,'b')
        # self.show()

#   b   兰色线
#   g   绿色线
#   r   红色线
#   c   cyan色
#   m   magenta色
#   y   黄色
#   k   黑色
#   w   白色

def test():
    testlist = '''['2017-12-25', '1', u'3569151', u'106847', '2.99%', '271.52']
['2017-12-21', '4', u'3414696', u'154454', '4.52%', '287.29']
['2017-12-18', '1', u'3553474', u'-138777', '-3.91%', '347.88']
['2017-12-15', '5', u'3166857', u'386617', '12.21%', '327.27']
['2017-12-11', '1', u'3032110', u'134746', '4.44%', '246.60']
['2017-12-08', '5', u'2473053', u'559057', '22.61%', '132.00']
['2017-12-06', '3', u'1736261', u'736791', '42.44%', '104.04']
['2017-12-03', '0', u'1391827', u'344434', '24.75%', '106.36']
['2017-11-29', '3', u'1502826', u'-110999', '-7.39%', '95.33']
['2017-11-26', '0', u'1260381', u'242445', '19.24%', '97.06']
['2017-11-23', '4', u'1222794', u'37587', '3.07%', '81.33']
['2017-11-20', '1', u'1198321', u'24472', '2.04%', '74.01']
['2017-11-16', '4', u'1074554', u'123767', '11.52%', '71.24']
['2017-11-13', '1', u'1180125', u'-105571', '-8.95%', '66.16']
['2017-11-09', '4', u'1032168', u'147957', '14.33%', '66.19']
['2017-11-06', '1', u'1033229', u'-1061', '-0.10%', '62.69']
['2017-11-03', '5', u'1026293', u'6936', '0.68%', '58.22']
['2017-10-30', '1', u'1081815', u'-55522', '-5.13%', '58.08']
['2017-10-27', '5', u'1008052', u'73763', '7.32%', '56.50']
['2017-10-23', '1', u'1020625', u'-12573', '-1.23%', '57.08']
['2017-10-20', '5', u'1014422', u'6203', '0.61%', '60.93']
['2017-10-16', '1', u'1034767', u'-20344', '-1.97%', '63.57']
['2017-10-13', '5', u'919573', u'115193', '12.53%', '65.68']
['2017-10-09', '1', u'976754', u'-57181', '-5.85%', '49.26']
['2017-10-06', '5', u'977949', u'-1194', '-0.12%', '51.15']
['2017-10-02', '1', u'964767', u'13182', '1.37%', '50.69']
['2017-09-29', '5', u'904453', u'60313', '6.67%', '51.38']
['2017-09-25', '1', u'891531', u'12921', '1.45%', '49.77']
['2017-09-22', '5', u'854926', u'36604', '4.28%', '40.39']
['2017-09-19', '2', u'811060', u'43866', '5.41%', '42.77']
['2017-09-15', '5', u'782777', u'28283', '3.61%', '43.79']
['2017-09-12', '2', u'753133', u'29644', '3.94%', '56.82']
['2017-09-08', '5', u'776322', u'-23188', '-2.99%', '64.05']
['2017-09-05', '2', u'680760', u'95561', '14.04%', '71.55']
['2017-09-02', '6', u'688270', u'-7509', '-1.09%', '74.80']
['2017-08-30', '3', u'636911', u'51358', '8.06%', '70.10']
['2017-08-27', '0', u'521698', u'115212', '22.08%', '61.70']
['2017-08-24', '4', u'476034', u'45664', '9.59%', '52.31']
['2017-08-20', '0', u'439024', u'37009', '8.43%', '47.21']
['2017-08-17', '4', u'445861', u'-6836', '-1.53%', '45.68']
['2017-08-13', '0', u'468683', u'-22822', '-4.87%', '46.09']
['2017-08-10', '4', u'455763', u'12919', '2.83%', '47.70']
['2017-08-06', '0', u'442804', u'12958', '2.93%', '47.26']
['2017-08-03', '4', u'442592', u'212', '0.05%', '45.08']
['2017-07-30', '0', u'437853', u'4739', '1.08%', '41.04']
['2017-07-27', '4', u'394147', u'43705', '11.09%', '41.10']
['2017-07-24', '1', u'391487', u'2660', '0.68%', '43.38']
['2017-07-21', '5', u'350559', u'40927', '11.67%', '46.11']
['2017-07-18', '2', u'306983', u'43576', '14.19%', '43.29']
['2017-07-14', '5', u'279350', u'27632', '9.89%', '41.52']
['2017-07-11', '2', u'275263', u'4086', '1.48%', '46.30']
['2017-07-07', '5', u'275720', u'-456', '-0.17%', '49.24']
['2017-07-04', '2', u'250000', u'25720', '10.29%', '52.61']
['2017-07-01', '6', u'252730', u'-2729', '-1.08%', '42.40']
['2017-06-27', '2', u'243261', u'9468', '3.89%', '41.30']
['2017-06-24', '6', u'255206', u'-11944', '-4.68%', '46.40']
['2017-06-20', '2', u'271187', u'-15981', '-5.89%', '48.96']
['2017-06-17', '6', u'228363', u'42824', '18.75%', '46.75']
['2017-06-13', '2', u'230314', u'-1951', '-0.85%', '30.95']
['2017-06-10', '6', u'197309', u'33005', '16.73%', '31.80']
['2017-06-06', '2', u'252310', u'-55001', '-21.80%', '30.03']
['2017-06-02', '5', u'257730', u'-5419', '-2.10%', '28.25']
['2017-05-30', '2', u'241458', u'16271', '6.74%', '24.72']
['2017-05-27', '6', u'240940', u'518', '0.21%', '23.95']
['2017-05-23', '2', u'241294', u'-354', '-0.15%', '31.93']
['2017-05-20', '6', u'224826', u'16468', '7.32%', '25.92']
['2017-05-16', '2', u'232423', u'-7597', '-3.27%', '21.86']
['2017-05-13', '6', u'213651', u'18772', '8.79%', '24.01']
['2017-05-10', '3', u'189978', u'23672', '12.46%', '25.67']
['2017-05-07', '0', u'179053', u'10925', '6.10%', '24.73']
['2017-05-03', '3', u'163668', u'15384', '9.40%', '19.48']
['2017-05-01', '1', u'125655', u'38013', '30.25%', '14.86']
['2017-04-27', '4', u'146317', u'-20662', '-14.12%', '13.17']
['2017-04-23', '0', u'131639', u'14678', '11.15%', '11.86']
['2017-04-20', '4', u'132015', u'-376', '-0.28%', '9.81']
['2017-04-17', '1', u'102266', u'29748', '29.09%', '9.27']
['2017-04-14', '5', u'93015', u'9251', '9.95%', '9.54']
['2017-04-11', '2', u'91853', u'1161', '1.26%', '8.82']
['2017-04-07', '5', u'102135', u'-10281', '-10.07%', '8.85']
['2017-04-04', '2', u'92957', u'9178', '9.87%', '8.57']
['2017-03-31', '5', u'87420', u'5536', '6.33%', '6.41']
['2017-03-28', '2', u'89105', u'-1684', '-1.89%', '4.45']
['2017-03-24', '5', u'94374', u'-5268', '-5.58%', '4.00']
['2017-03-21', '2', u'89024', u'5350', '6.01%', '3.93']
['2017-03-17', '5', u'93785', u'-4760', '-5.08%', '3.99']
['2017-03-14', '2', u'87513', u'6271', '7.17%', '4.16']
['2017-03-10', '5', u'88481', u'-968', '-1.09%', '3.89']
['2017-03-07', '2', u'89872', u'-1390', '-1.55%', '3.87']
['2017-03-03', '5', u'98387', u'-8515', '-8.65%', '3.92']
['2017-02-27', '1', u'99024', u'-637', '-0.64%', '3.81']
['2017-02-24', '5', u'92301', u'6722', '7.28%', '3.89']
['2017-02-20', '1', u'99011', u'-6709', '-6.78%', '3.87']
['2017-02-17', '5', u'95184', u'3826', '4.02%', '3.79']
['2017-02-13', '1', u'92762', u'2421', '2.61%', '3.74']
['2017-02-10', '5', u'98674', u'-5911', '-5.99%', '3.75']
['2017-02-06', '1', u'96127', u'2546', '2.65%', '4.17']
['2017-02-03', '5', u'102398', u'-6270', '-6.12%', '4.15']
['2017-01-30', '1', u'98710', u'3687', '3.74%', '4.12']
['2017-01-27', '5', u'99113', u'-403', '-0.41%', '3.89']
['2017-01-23', '1', u'96311', u'2802', '2.91%', '3.83']'''
    testlist = '['  + testlist.replace('\n', ',').replace("u'",'"').replace("'",'"') + ']'
    dats = json.loads(testlist)
    print len(dats)
    mattool = MatplotTool()
    # mattool.drawDifficult(dats)
    mattool.drarDiffcultWithAdd(dats)

def main():
    mattool = MatplotTool()
    x = [1,2,3,4,5]
    y = [1,4,9,16,25]
    mattool.drawPlot(x,y)
    x2 = [1,2,4,6,8]
    y2 = [2,4,8,12,16]
    mattool.drawPlot(x2,y2,'r')

    mattool.show()

#测试
if __name__ == '__main__':
    # main()
    test()




