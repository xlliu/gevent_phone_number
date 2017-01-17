# -*- coding: utf-8 -*-
# import gevent.monkey
# gevent.monkey.patch_all(socket=True, dns=True, time=True, select=True, thread=False, os=True, ssl=True, httplib=False,
#               subprocess=True, sys=False, aggressive=True, Event=False,
#               builtins=True, signal=True)
import sys

reload(sys)
sys.setdefaultencoding('utf8')

__author__ = 'xlliu'
import requests
import time
import random
import json
requests.packages.urllib3.disable_warnings()

class ErShouChe(object):
    """
    处理过程
    生成结果文件 ==>> xianhua.xlsx
    """
    def __init__(self):
        self.login_url = "http://account.che168.com/password/checkusername"
        self.headers = {
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Host": "account.che168.com",
            "Origin": "http://account.che168.com",
            "Referer": "http://account.che168.com/password/",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Ch",
        }
        self.data = {
            "username": None,
            "usertype": 2,
        }
    def run(self, tel_num, session, table):
        # rr = random.randint(10, 20)
        # time.sleep(rr)
        
        # data.ix[['one', 'one'], ['a', 'e', 'd', 'd', 'd']]
        print "ready", tel_num, ErShouChe.__name__
        # table.ix[int(tel_num), 'youli'] = True
        # print tel_num, session
        
        self.data["username"] = tel_num
        result = session.post(self.login_url, verify=False, data=self.data, headers=self.headers)
        try:
            res = json.loads(result.text)
        except Exception as e:
            print "================="
            print result.text
            print e
            print "================="
        # res = "-2"
        # print res
        # print json.loads(res).get("success")
        # 注册过
        # print res.get("returncode")
        # print "====="
        # print res.get("message") == u"该用户名不存在"
        if not res.get("returncode"):
            table.ix[int(tel_num), 'ershouche'] = 1
        # 没注册过
        elif res.get("message") == u"该用户名不存在":
            table.ix[int(tel_num), 'ershouche'] = 0
        else:
            table.ix[int(tel_num), 'ershouche'] = -1