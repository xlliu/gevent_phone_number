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
from target_site.xiaodai.youli import YouLi


class HitTheLibrary(object):
    """测试号码工具模块

    对电话号码进行测试，
    """

    def __init__(self):
        super(HitTheLibrary, self).__init__()
        self.session = requests.session()
        self.__sites = [YouLi()]
        self.__run()

    def __core(self, tel_num):
        # gevent.sleep(4)
        print('Running in tel_num: %s' %tel_num)
        
        tasks = [gevent.spawn(getattr(site, "run"), tel_num, self.session) for site in self.__sites]
        success_tasks_call_sites = gevent.joinall(tasks, timeout=3, raise_error=False)
        for greenlet in tasks:
            print "结束停止切没有异常: %s" %(greenlet.successful() if greenlet.successful() else False)
            print "结束停止: %s" %(greenlet.ready() if greenlet.ready() else False)
            print "没被捕获的异常: %s" %greenlet.exception
        # print tel_num, len(success_tasks)
        # print('Explicit context switch to foo again')

    def __run(self):
        with pd.ExcelFile('test.xlsx') as xls:
            df1 = pd.read_excel(xls, '10w')
        
        from pandas import Sereis, DataFrame
        # for n in 
        df2 = df1.loc[0:10, [u'电话号码']].values
        print "-"*10
        print df2.nrow()
        print "-"*10
        tasks = [gevent.spawn(self.__core, str(tel_num)) for tel_num in df2]
        # tasks = [gevent.spawn(self.__core, str(tel_num)) for tel_num in xrange(10)]
        
        success_tasks_call = gevent.joinall(tasks, raise_error=False)
        # print "all_success: %d" %len(success_tasks_call)
        # for greenlet in tasks:
        #     print "结束停止切没有异常: %s" %(greenlet.successful() if greenlet.successful() else False)
        #     print "结束停止: %s" %(greenlet.ready() if greenlet.ready() else False)
        #     print "没被捕获的异常: %s" %greenlet.exception
        
        print '============================='
        # gevent.sleep(2)
        # for greenlet in tasks:
        #     print "结束停止切没有异常: %s" %(greenlet.successful() if greenlet.successful() else False)
        #     print "结束停止: %s" %(greenlet.ready() if greenlet.ready() else False)
        #     print "没被捕获的异常: %s" %greenlet.exception
        # print self.count

HitTheLibrary()