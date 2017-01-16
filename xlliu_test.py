# from multiprocessing import Pool
# import gevent.monkey
# gevent.monkey.patch_select()
# gevent.monkey.patch_socket()

# import copy_reg
# import types


# def _pickle_method(m):
#     if m.im_self is None:
#         return getattr, (m.im_class, m.im_func.func_name)
#     else:
#         return getattr, (m.im_self, m.im_func.func_name)

# copy_reg.pickle(types.MethodType, _pickle_method)


# class TT(object):
#     aa=100
#     # def __init__(self):
#     # #     self.pool = pool
#     #     self.aa = 100
    
#     @classmethod    
#     def f(cls, x):
#         cls.aa = x
        
#     def u(self):
#         global aa
#         print saa
#         # self.pool.apply_async(self.f, [10]) 
        
  
# if __name__ == '__main__':
#   print 'uu'
#   pool = Pool(processes=1)
#   tt = TT()
#   print tt.aa
  
#   # Start a worker processes.
#   result = pool.apply_async(TT.f, [10]) 
#   pool.close()
#   pool.join()
#   print tt.aa
#   print 'ii'
# -*- coding: utf-8 -*-
from __future__ import division
# from multiprocessing import Pool
import multiprocessing
import gevent
import gevent.monkey
# gevent.monkey.patch_all()
gevent.monkey.patch_select()
gevent.monkey.patch_socket()

# import sys
# reload(sys)
# sys.setdefaultencoding('utf-8')

import pandas as pd
import numpy as np
import random
import requests
import math
import time

from target_site.xiaodai.youli import YouLi
  
  
import copy_reg
import types
import multiprocessing


def _pickle_method(m):
    if m.im_self is None:
        return getattr, (m.im_class, m.im_func.func_name)
    else:
        return getattr, (m.im_self, m.im_func.func_name)

copy_reg.pickle(types.MethodType, _pickle_method)


class Controler(object):
    def __init__(self):
        nProcess = 10
        pages = 10
        self.__result = []
        self.manageWork(nProcess, pages)

    def BarcodeSearcher(self, x):
        return x*x

    def resultCollector(self, result):
        self.__result.append(result)

    def manageWork(self, nProcess, pages):
        pool = multiprocessing.Pool(processes=nProcess)
        for pag in range(pages):
            pool.apply_async(self.BarcodeSearcher, args=(pag,),
                             callback=self.resultCollector)
        pool.close()
        pool.join()

        print(self.__result)

if __name__ == '__main__':
    Controler()