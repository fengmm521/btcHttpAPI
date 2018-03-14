#!/usr/bin/env python
#-*- coding: utf-8 -*-
import os
import sys
import time
import chardet  #中文编码判断
import urllib2
import hashlib
import datetime
import json
import requests

reload(sys)
sys.setdefaultencoding( "utf-8" )

class DifficultyLTCTool(object):
    """docstring for ClassName"""
    def __init__(self, isCmdMode = True):
        
        self.isCmdMode = isCmdMode
        self.wdriver = None

        # self.klineURL = 'https://www.okex.com/api/v1/future_kline.do?symbol=ltc_usd&type=1day&contract_type=this_week&size=400'
        self.klineURL = 'https://104.25.20.25/api/v1/future_kline.do?symbol=ltc_usd&type=1day&contract_type=this_week&size=400'
        self.dayKlines = []

        self.dayData = {}

        self.get300DayKline()

    def get300DayKline(self):
        
        tmpstr= self.getUrl(self.klineURL)
        
        self.dayKlines = json.loads(tmpstr)

        print 'klines:',len(self.dayKlines)

    def getDayPrice(self,daystr):

        if self.dayKlines and len(self.dayData.keys()) == 0:
            #获取3天的平均价格
            tmpdic = {}
            dates = []

            for d in self.dayKlines:
                tmpdate = self.getDateDayWithTime(int(d[0])/1000)
                tmpdic[tmpdate] = (float(d[1]) + float(d[4]))/2.0
                dates.append(tmpdate)
            tmpcount = len(dates)
            for n in range(len(dates)):
                if n < tmpcount - 2:
                    pav = (tmpdic[dates[n]] + tmpdic[dates[n + 1]] + tmpdic[dates[n + 2]])/3.0
                    tmpdic[dates[n]] = pav
                elif n == tmpcount - 2:
                    pav = (tmpdic[dates[n]] + tmpdic[dates[n + 1]])/2.0
                    tmpdic[dates[n]] = pav
                else:
                    continue
            self.dayData = tmpdic

        if not self.dayData.has_key(daystr):
            self.testerro()


        if len(self.dayData.keys()) != 0 and self.dayData.has_key(daystr):
            return self.dayData[daystr]
        else:
            days = self.dayData.keys()
            days.sort()
            tmpdays = []
            for n in range(len(days)):
                d = days[n]
                if d > daystr:
                    tmpdays = [days[n-1],days[n]]
                    break
            print tmpdays
            tmp = (self.dayData[tmpdays[0]] + self.dayData[tmpdays[1]])/2
            return tmp
    def testerro(self):
        isNext = False
        for kl in self.dayKlines:
            tmpdate = self.getDateDayWithTime(int(kl[0])/1000)

            if isNext:
                print tmpdate,kl[0]

            if tmpdate == '2018-02-06':
                print tmpdate,kl[0]
                isNext = True
            else:
                isNext = False
            print tmpdate

    # def getManager(wdriver,tid):
    def conventStrTOUtf8(self,oldstr):
        try:
            nstr = oldstr.encode("utf-8")
            return nstr
        except Exception as e:
            print 'nstr do not encode utf-8'
        cnstrtype = chardet.detect(oldstr)['encoding']
        utf8str =  oldstr.decode(cnstrtype).encode('utf-8')
        return utf8str

    def getYearMathDay(self,pstr):
        tmptime = time.strptime(pstr,'%a %d %b %Y')
        stemtime = int(time.mktime(tmptime)) + (22 * 60 * 60) #转为中国时间
        outdate = time.strftime("%Y-%m-%d", time.gmtime(stemtime))
        wday = time.strftime("%w", time.gmtime(stemtime))
        return outdate,wday

    def getDiffcultFromWeb(self,browser):

        # hurl = 'http://basic.10jqka.com.cn/%s/company.html'%(tid)
        # browser = wdriver
        
        # browser.get(hurl)
        browser.implicitly_wait(10)

        diftab = browser.find_element_by_xpath('/html/body/div[2]/table/tbody')                       

        tmpstr = diftab.text

        lines = tmpstr.split('\n')

        outdic = {}
        for n in range(len(lines)):
            tmps = lines[n].split(':')
            if n == 0:
                outdic['difficulty'] = int(tmps[1].replace(',',''))
            elif n == 1:      
                ntmps = tmps[1].replace(')','')
                ntmps = ntmps.split('(')

                outdic['nextDif'] = int(ntmps[0].replace(',',''))
                outdic['addDif'] = int(ntmps[1].replace(',',''))
            elif n == 2:
                tmpps = tmps[1].split(',')
                tmpps[0] = ' '.join(tmpps[0].split())
                tmpps[1] = ' '.join(tmpps[1].split())
                afterblocks = int(tmpps[0].split(' ')[1])
                nextdays = float(tmpps[1].split(' ')[1])
                nextHours = nextdays*24.0
                outdic['afterblocks'] = afterblocks
                outdic['nextdays'] = nextdays
                outdic['nextHours'] = nextHours
            elif n == 8:
                tmpl = lines[n]
                tmpl = tmpl[tmpl.find(':') + 1:]
                tmpl = ' '.join(tmpl.split())
                # print tmpl
                # print tmpl[:-4]
                tmptime = time.strptime(tmpl[:-4],'%a,%d %b %Y %H:%M:%S %p')
                # print tmptime
                # print time.mktime(tmptime)
                stemtime = int(time.mktime(tmptime)) + (22 * 60 * 60) #转为中国时间
                outdic['updated'] = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(stemtime))

                if outdic['difficulty'] == 0:
                    outdic['uppencent'] = '0.00%'
                else:
                    outdic['uppencent'] = '%.2f%%'%(float(outdic['addDif'])/float(outdic['difficulty']) * 100)


        lastupdatetab = browser.find_element_by_xpath('//*[@id="result"]/tbody')

        #获取历史难度变化数据
        historydats = self.conventLastUpdate(lastupdatetab.text)
        historydats[0][3] = u'%d'%(outdic['addDif'])

        if outdic['difficulty'] == 0 and outdic['addDif'] == outdic['nextDif']:
            outdic['addDif'] = float(outdic['nextDif'] - float(historydats[0][2]))
            historydats[0][4] =  '%.2f%%'%(float(outdic['addDif'])/float(historydats[0][2]) * 100)
            outdic['uppencent'] = historydats[0][4]
        else:
            historydats[0][4] = outdic['uppencent']
        
        return outdic,historydats


    def getDateDayWithTime(self,ptime = None):
        loctim = time.localtime(ptime)
        #time.struct_time(tm_year=2015, tm_mon=8, tm_mday=2, tm_hour=12, tm_min=16, tm_sec=47, tm_wday=6, tm_yday=214, tm_isdst=0)
        m = str(loctim.tm_mon)
        if len(m) == 1:
            m = '0' + m

        d = str(loctim.tm_mday)
        if len(d) == 1:
            d = '0' + d

        sendmsg = str(loctim.tm_year) + '-' + m + '-' +  d
        return sendmsg


    def getNextDay(self,daystr):
        pass

    def conventLastUpdate(self,linestrs):
        tmpstrs = linestrs.split('\n')
        lastdifs = []
        for l in tmpstrs:
            tmpl = l.replace('\n','')
            tmpl = ' '.join(tmpl.split())
            tmpls = tmpl.split(' ')
            tmpls[1] = tmpls[1][:-2]
            datetmp = ' '.join(tmpls[0:4])
            diftmp = tmpls[4]
            adddiftmp = tmpls[5]
            addpencent = '%.2f%%'%((float(adddiftmp)/float(diftmp))*100)
            datestr,wday = self.getYearMathDay(datetmp)
            dateprice = self.getDayPrice(datestr)
            print dateprice,type(dateprice)
            datepricestr = '%.2f'%(dateprice)
            lastdifs.append([datestr,wday,diftmp,adddiftmp,addpencent,datepricestr])
        return lastdifs

    #获取公司资料
    def moneyMsg(self,ptype):

        if not self.wdriver:
            if self.isCmdMode:
                print 'used phantomjs'
                import selenium.webdriver.phantomjs.webdriver as wd
                self.wdriver = wd.WebDriver('/usr/local/bin/phantomjs')       #test
                self.wdriver.maximize_window()
            else:
                print 'used chrome'
                import selenium.webdriver.chrome.webdriver as  wd
                self.wdriver = wd.WebDriver('/Users/mage/Documents/tool/cmdtool/chromedriver')       #test
                self.wdriver.maximize_window()

        hurl = ''
        if ptype == 'btc':
            hurl = 'http://btcwisdom.net'
        else:
            hurl = 'http://ltcwisdom.net'

        self.wdriver.get(hurl)

        #难度信息 
        datdic= self.getDiffcultFromWeb(self.wdriver)                                               
        return datdic

    def getUrltmp(self,purl):
        try:
            req = urllib2.Request(purl)
            req.add_header('User-agent', 'Mozilla 5.10')
            res = urllib2.urlopen(req)
            html = self.conventStrTOUtf8(res.read())
            return html
        except Exception, e:
            print e
        return None
    def getUrl(self,purl):
        try:
            s = requests.Session()
            #104.25.20.25,国内ip被墙，这个ip可以
            dat = s.get(purl, headers={"Host": "www.okex.com"},verify=False)
            html = self.conventStrTOUtf8(dat.text)
            return html
        except Exception as e:
            raise e
        

def main():

    sharetool = DifficultyLTCTool(isCmdMode = False)

    ggdats,historydats = sharetool.moneyMsg('ltc')

    for k in ggdats.keys():
        print k,ggdats[k]

    raw_input('input enter for end.')

    sharetool.wdriver.quit()

#测试
if __name__ == '__main__':
    main()
    # test()




