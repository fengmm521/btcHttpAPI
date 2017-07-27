
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys,os
import pathtool
import datadown

logpth = './data'

def allLogFiles():
    tlogfiles,deplogfiles = datadown.allLogFiles()
    return tlogfiles,deplogfiles
def getlogAllLineCount(logpth):
    f = open(logpth,'r')
    lines = f.readlines()
    f.close()
    return len(lines)
def main():
    tlogfiles,deplogfiles = allLogFiles()
    print tlogfiles
    print deplogfiles
    loglinecount = 0
    for l in tlogfiles:
        tmppth = logpth + os.sep + l + '.txt'
        counttmp = getlogAllLineCount(tmppth)
        print counttmp
        loglinecount += counttmp
    print 'trade logcount =',loglinecount
    deploglinecount = 0
    for l in deplogfiles:
        tmppth = logpth + os.sep  + 'depth_' + l + '.txt'
        counttmp = getlogAllLineCount(tmppth)
        print counttmp
        deploglinecount += counttmp
    print 'depth logcount =',deploglinecount

if __name__ == '__main__':
    main()