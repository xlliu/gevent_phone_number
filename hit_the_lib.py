# -*- coding: utf-8 -*-
import gevent

import gevent.monkey

gevent.monkey.patch_all()

import pandas as pd
import random


class HitTheLibrary(object):
    """测试号码工具模块

    对电话号码进行测试，
    """

    def __init__(self):
        super(HitTheLibrary, self).__init__()
        self.count = 0
        self.__run()

    def __core(self, tel_num):
        gevent.sleep(1)
        self.count += 1
        print('Running in tel_num: %s' %tel_num)
        # print('Explicit context switch to foo again')

    def __run(self):
        with pd.ExcelFile('test.xlsx') as xls:
            # df1 = pd.read_excel(xls, '10w')
            tasks = [gevent.spawn(self.__core, str(tel_num)) for tel_num in xrange(10)]
            # tasks = (gevent.spawn(self.__core, str(tel_num)) for tel_num in df1[u'手机号码'])
            print gevent.joinall(tasks,timeout=2)
            # print self.count

HitTheLibrary()
