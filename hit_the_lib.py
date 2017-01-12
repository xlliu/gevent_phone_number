# -*- coding: utf-8 -*-
import gevent

import gevent.monkey

gevent.monkey.patch_all()

import pandas as pd


class HitTheLibrary(object):
    """测试号码工具模块

    对电话号码进行测试，
    """

    def __init__(self):
        super(HitTheLibrary, self).__init__()

    def __core(self, tel_num):
        print('Running in tel_num: %s' + tel_num)

        print('Explicit context switch to foo again')

    def __run(self):
        with pd.ExcelFile(u'撞库号码.xlsx') as xls:
            df1 = pd.read_excel(xls, u'十万生活')
            print 'ssss'
            tasks = [gevent.spawn(self.__core, i) for i in range(0, 10)]
            gevent.joinall(tasks)

HitTheLibrary()
