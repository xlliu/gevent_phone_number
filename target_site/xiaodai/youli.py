# -*- coding: utf-8 -*-
import numpy as np

__author__ = 'xlliu'
import requests
import time
import random

class YouLi(object):
    """
    处理过程
    生成结果文件 ==>> xianhua.xlsx
    """
    def __init__(self):
        self.login_url = "https://www.yooli.com/secure/ssoLogin.action"
        self.params = {
            "nickName": None,
            "password": "123456",
            "verifycode": None,
            "chkboxautologin": "false",
        }
    def run(self, tel_num, session, table):
        rr = random.randint(0, 20)
        time.sleep(rr)
        # data.ix[['one', 'one'], ['a', 'e', 'd', 'd', 'd']]
        print "ready", tel_num, type(tel_num)
        table.ix[int(tel_num), 'youli'] = True
        print tel_num, session
        self.params["nickName"] = tel_num
        # result = session.get(self.login_url, verify=False, params=self.params)
        
        # return result