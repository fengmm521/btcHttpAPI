#!/usr/bin/env python
#-*- coding: utf-8 -*-
import os
import sys
import time
import chardet  #中文编码判断
import urllib2
import hashlib
import datetime

reload(sys)
sys.setdefaultencoding( "utf-8" )

class GongGaoTool(object):
    """docstring for ClassName"""
    def __init__(self, isCmdMode = True):
        
        self.isCmdMode = isCmdMode
        self.wdriver = None
    #获取高官信息
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
                outdic['uppencent'] = '%.2f%%'%(float(outdic['addDif'])/float(outdic['difficulty']) * 100)


        lastupdatetab = browser.find_element_by_xpath('//*[@id="result"]/tbody')

        #获取历史难度变化数据
        self.conventLastUpdate(lastupdatetab.text)
        
        return outdic

    def conventLastUpdate(self,linestrs):
        tmpstrs = linestrs.split('\n')
        for l in tmpstrs:
            print l

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

        #企业高管信息
        datdic = self.getDiffcultFromWeb(self.wdriver)                                                #获取高管信息
        return datdic

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

    sharetool = GongGaoTool(isCmdMode = False)

    ggdats = sharetool.moneyMsg('ltc')

    for k in ggdats.keys():
        print k,ggdats[k]

    raw_input('input enter for end.')

    sharetool.wdriver.quit()

#测试
if __name__ == '__main__':
    main()
    # test()




