# -*- coding: utf-8 -*-
# import gevent.monkey
# gevent.monkey.patch_all(socket=True, dns=True, time=True, select=True, thread=False, os=True, ssl=True, httplib=False,
#               subprocess=True, sys=False, aggressive=True, Event=False,
#               builtins=True, signal=True)


__author__ = 'xlliu'
import requests
import time
import random
import json
import sys
requests.packages.urllib3.disable_warnings()

class HuaLi(object):
    """
    处理过程
    生成结果文件 ==>> xianhua.xlsx
    """
    def __init__(self):
        self.login_url = "http://www.hua.com/Passport/Login/SendPhoneLoginSMSCode"
        self.headers = {
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Host": "www.hua.com",
            "Origin": "http://www.hua.com",
            "Referer": "http://www.hua.com/Passport/Login/",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Ch",
        }
        self.data = {
            "phone": None,
            "imgCode": None,
        }
    def run(self, tel_num, session, table):
        # rr = random.randint(10, 20)
        # time.sleep(rr)
        
        # data.ix[['one', 'one'], ['a', 'e', 'd', 'd', 'd']]
        print "ready", tel_num, HuaLi.__name__
        # table.ix[int(tel_num), 'youli'] = True
        # print tel_num, session
        
        self.data["phone"] = tel_num
        result = session.post(self.login_url, verify=False, data=self.data, headers=self.headers)
        res = json.loads(result.text)

        # res = "-2"
        # print res
        # 注册过
        if res.get("Code") == 1:
            table.ix[int(tel_num), 'huali'] = 1
        # 没注册过
        elif res.get("Code") == -5:
            table.ix[int(tel_num), 'huali'] = 0
        else:
            table.ix[int(tel_num), 'huali'] = -1