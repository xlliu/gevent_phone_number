# -*- coding: utf-8 -*-
from __future__ import division
import gevent
import gevent.monkey
gevent.monkey.patch_all()

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import pandas as pd
import numpy as np
import random
import requests
import math
import time
from multiprocessing import Pool
from target_site.xiaodai.youli import YouLi


class HitTheLibrary(object):
    """测试号码工具模块

    对电话号码进行测试，
    """

    def __init__(self):
        super(HitTheLibrary, self).__init__()
        self.session = requests.session()
        self._sites = [YouLi()]
        self._step = 10
        self._sleep = 1
        self._pool = Pool(processes=1)
        self.__run()

    def __core(self, tel_num):
        # gevent.sleep(4)
        print('Running in tel_num: %s' %tel_num)
        tasks = [gevent.spawn(getattr(site, "run"), tel_num, self.session, self._TABLE) for site in self._sites]
        success_tasks_call_sites = gevent.joinall(tasks, timeout=20, raise_error=False)
        # for greenlet in tasks:
        #     print "结束停止切没有异常: %s" %(greenlet.successful() if greenlet.successful() else False)
        #     print "结束停止: %s" %(greenlet.ready() if greenlet.ready() else False)
        #     print "没被捕获的异常: %s" %greenlet.exception
        # print tel_num, len(success_tasks)
        # print('Explicit context switch to foo again')

    def __table(self, phone_numbers, sites):
        sites = ["youli"]
        # for v in phone_numbers.values:
        #     print v, type(v), np.array(v.tolist()), type(np.array(v.tolist()))
        pn_list = map(lambda x: x.tolist()[0], phone_numbers.values)
        # print pn_list
        data = pd.DataFrame(index=pn_list, columns=sites)
        print data.index
        # test_a = 13351011100
        # print test_a, type(test_a)
        # print data.ix[test_a, 'youli']
        return data

    @staticmethod
    def __generator_tasks(tasks):
        gevent.joinall(tasks, raise_error=False)


    def __run(self):
        with pd.ExcelFile('test.xlsx') as xls:
            df1 = pd.read_excel(xls, '10w')

        # 测试截取30
        df1 = df1.loc[0:31, [u'电话号码']]
        self._TABLE = self.__table(df1, None)
        print self._TABLE
        time_num = int(math.ceil(len(df1.index) / self._step))
        # gt = self.__generator_tasks()
        # gt.next()
        
        for n in xrange(time_num):
            df2 = df1.loc[n*self._step:(n+1)*self._step, [u'电话号码']].values
            print "-"*10
            print df2
            print "-"*10
            tasks = [gevent.spawn(self.__core, str(tel_num[0])) for tel_num in df2]
            self._pool.apply_async(self.__generator_tasks, [tasks])
            # gt.send(tasks)
            time.sleep(self._sleep)

        print self._TABLE
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

if __name__ == '__main__':
#   pool = Pool(processes=1)
  # Start a worker processes.
#   result = pool.apply_async(f, [10])
    HitTheLibrary()