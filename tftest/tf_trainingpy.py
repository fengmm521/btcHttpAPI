#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys,os
os.environ['PATH'] = '/usr/bin/:/usr/sbin/'
import tensorflow as tf
import json
import tf_trainingPattern as pat

logpth = './pattern'
BV = 'basevalue'
DD = 'dynamicvalue'

HourTime = 120
labWtime = 120

def tfWorkerDo(pattern):

    print '进入tensorflow,创建网络模型'
    netmode = '''
输入层                          隐藏层             隐藏层2            输出层
(120x121个数据源)               (500节点)          (300节点)          (2个节点)
(一小时数据)                                                         (预测未来时间内最大值和最小值)

i1                              h1
        
i1                              
                                                h1
.   
.
.                               .               .                   O1
                                .               .                   O2
                                .               .
ix
                                                
                                                h300
. 
.                               h500
.

i14520
    '''
    print netmode

    w1 = tf.Variable(tf.random_normal([14520,500],stddev=1.0,seed=1))
    w2 = tf.Variable(tf.random_normal([500,300],stddev=1.0,seed=1))
    out = tf.Variable(tf.random_normal([300,2],stddev=1.0,seed=1))

    x = tf.placeholder(tf.float32,shape=(None,14520),name='input')

    sess = tf.Session()

    init_op = tf.initialize_all_variables()
    
    sess.run(init_op)

    print sess.run(y,feed_dict={x:[[0.7,0.9],[0.1,0.4],[0.5,0.8]]})

    sess.close()
    
def main():
    print '初始化数据对象'
    patobj = pat.makeTrainingDataForBaseValue(HourTime, labWtime)
    # tfWorkerDo(patobj)
if __name__ == '__main__':
    main()