
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys,os

import httplib

import time
 
httpClient = None
 
def getTicker():
    try:
        httpClient = httplib.HTTPConnection('api.btc38.com', 80, timeout=30)
        httpClient.request('GET', '/v1/ticker.php?c=ltc&mk_type=cny')
        response = httpClient.getresponse()
        data = response.read()
        return data
    except Exception, e:
        print e
    finally:
        if httpClient:
            httpClient.close()

def main():
    
    while True:
        tickertmp = getTicker()
        f = open('data.txt','a+')
        savedat = str(time.time()) + '=' + tickertmp + '\n'
        f.write(savedat)
        f.close()
        time.sleep(30)
if __name__ == '__main__':
    main()