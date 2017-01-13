# -*- coding: utf-8 -*-
import gevent

import gevent.monkey

gevent.monkey.patch_all()

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import pandas as pd
import random
import requests


class HitTheLibrary(object):
    """测试号码工具模块

    对电话号码进行测试，
    """

    def __init__(self):
        super(HitTheLibrary, self).__init__()
        self.session = requests.session()
        self.__sites = []
        self.__run()

    def __core(self, tel_num):
        # gevent.sleep(3)  
        print('Running in tel_num: %s' %tel_num)
        
        getattr()
        # print('Explicit context switch to foo again')

    def __run(self):
        with pd.ExcelFile('test.xlsx') as xls:
            df1 = pd.read_excel(xls, '10w')
        # print df1
        tasks = [gevent.spawn(self.__core, str(tel_num)) for tel_num in df1[u'电话号码']]
        # tasks = (gevent.spawn(self.__core, str(tel_num)) for tel_num in df1[u'手机号码'])
        
        gevent.joinall(tasks, timeout=2, raise_error=False)
        for greenlet in tasks:
            print "结束停止切没有异常: %s" %(greenlet.successful() if greenlet.successful() else False)
            print "结束停止: %s" %(greenlet.ready() if greenlet.ready() else False)
            print "没被捕获的异常: %s" %greenlet.exception
        
        print '============================='
        gevent.sleep(2)
        for greenlet in tasks:
            print "结束停止切没有异常: %s" %(greenlet.successful() if greenlet.successful() else False)
            print "结束停止: %s" %(greenlet.ready() if greenlet.ready() else False)
            print "没被捕获的异常: %s" %greenlet.exception
        # print self.count

