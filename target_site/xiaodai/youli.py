# -*- coding: utf-8 -*-
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
    def run(self, tel_num, session):
        rr = random.randint(0, 6)
        time.sleep(rr)
        print tel_num, rr, session
        self.params["nickName"] = tel_num
        # result = session.get(self.login_url, verify=False, params=self.params)
        
        # return result