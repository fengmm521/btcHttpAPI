
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys,os

import urllib2

import time
 
httpClient = None
 
def getTicker():
    req = urllib2.Request('http://api.btc38.com/v1/ticker.php?c=ltc&mk_type=cny')
    req.add_header('User-agent', 'Mozilla 5.10')
    res = urllib2.urlopen(req)
    html = res.read()
    return html
def main():
    tickertmp = getTicker()
    print tickertmp
if __name__ == '__main__':
    main()