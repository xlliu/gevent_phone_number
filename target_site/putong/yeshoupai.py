# -*- coding: utf-8 -*-
# import gevent.monkey
# gevent.monkey.patch_all(socket=True, dns=True, time=True, select=True, thread=False, os=True, ssl=True, httplib=False,
#               subprocess=True, sys=False, aggressive=True, Event=False,
#               builtins=True, signal=True)
from requests.exceptions import ProxyError

__author__ = 'xlliu'
import requests
import time
import json

requests.packages.urllib3.disable_warnings()


class YeShouPai(object):
    """
    处理过程
    生成结果文件 ==>> xianhua.xlsx
    """

    def __init__(self):
        self.login_url = "http://www.thebeastshop.com/user/dologin.htm"
        self.headers = {
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Host": "www.thebeastshop.com",
            "Origin": "http://www.thebeastshop.com",
            "Referer": "http://www.thebeastshop.com/user/login.htm",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Ch",
        }
        self.data = {
            "loginName": None,
            "password": 123123123,
            "remeberme": None
        }

    def run(self, tel_num, session, table):
        print "Ready time: %d | tel: %s | class: %s" % (time.time(), tel_num, self.__class__.__name__)
        result = None
        self.data["loginName"] = tel_num
        try:
            result = session.post(self.login_url, verify=False, data=self.data, headers=self.headers)
            res = result.text
        except ProxyError:
            try:
                time.sleep(2)
                result = session.post(self.login_url, data=self.data, headers=self.headers)
                res = json.loads(result.text)
            except Exception as e:
                print "================="
                print e
                print "================="
            else:
                self.deal_result(res, table, tel_num)
        except Exception as e:
            print "================="
            if result.text:
                print result.text
            print e
            print "================="
        else:
            self.deal_result(res, table, tel_num)

    def deal_result(self, res, table, tel_num):
        # 注册过
        if not res:
            table.ix[int(tel_num), 'yeshoupai'] = 1
        # 没注册过
        elif not json.loads(res).get("success"):
            table.ix[int(tel_num), 'yeshoupai'] = 0
        else:
            table.ix[int(tel_num), 'yeshoupai'] = -1
