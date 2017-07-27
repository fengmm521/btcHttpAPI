
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys,os
os.environ['PATH'] = '/usr/bin/:/usr/sbin/'
import tensorflow as tf
import json

logpth = './pattern'

basevalue = []

def getPattern(pth):
    f = open(pth,'r')
    lines = f.readlines()
    f.close()
    outlines = []
    for l in lines:
        tmpline = l.replace('\n','')
        tmpls = json.loads(tmpline)
        outlines.append(tmpls)
    for v in outlines[0]:
        basevalue.append(v)
    return outlines[1:]

def tfWorkerDo(pattern):

    w1 = tf.Variable(tf.random_normal([2,3],stddev=1.0,seed=1))
    w2 = tf.Variable(tf.random_normal([3,1],stddev=1.0,seed=1))


    x = tf.placeholder(tf.float32,shape=(3,2),name='input')

    a = tf.matmul(x, w1)
    y = tf.matmul(a, w2)

    sess = tf.Session()

    init_op = tf.initialize_all_variables()

    sess.run(init_op)

    print sess.run(w1)
    print sess.run(w2)
    print sess.run(y,feed_dict={x:[[0.7,0.9],[0.1,0.4],[0.5,0.8]]})

    sess.close()
    
def main():
    pattern = getPattern('pattern/pattern.txt')
    print len(pattern)
    isEqu = True
    lcount = len(pattern[0])
    for p in pattern:
        if lcount != len(p):
            isEqu = False
            break
    print pattern[0]
    print isEqu,lcount,basevalue
if __name__ == '__main__':
    main()