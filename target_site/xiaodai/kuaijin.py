# -*- coding: utf-8 -*-
# import gevent.monkey
# gevent.monkey.patch_all(socket=True, dns=True, time=True, select=True, thread=False, os=True, ssl=True, httplib=False,
#               subprocess=True, sys=False, aggressive=True, Event=False,
#               builtins=True, signal=True)

"""
Token 及 签名
"""
from requests.exceptions import ProxyError

__author__ = 'xlliu'
import requests
import time
import json

requests.packages.urllib3.disable_warnings()


class Kuaijin(object):
    """
    处理过程
    生成结果文件 ==>> xianhua.xlsx
    """

    def __init__(self):
        self.login_url = "https://capi.timecash.cn/v2/Token/Create"
        self.headers = {
            "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 6.0.1; AOSP on HammerHead Build/MOB30H)",
            "Content-Type": "application/json"
        }
        self.data = {
            "mobile": None,
            "app":{
                "ver": "1.3.4",
                "os": "6.0.1",
                "unique_id": "867451026298049",
                "trid": "1484211727187",
                "time": "2017-01-12 05:02:07",
                "app_id": "android",
                "token": "",
                "sign": "ccdd0695913d92f0202f794bb2034ee6"
            }
        }

    def run(self, tel_num, session, table):
        print "Ready time: %d | tel: %s | class: %s" % (time.time(), tel_num, self.__class__.__name__)
        result = None
        self.data["mobile"] = tel_num
        try:
            result = session.post(self.login_url, verify=False, data=self.data, headers=self.headers)
            res = json.loads(result.text)
        except ProxyError:
            try:
                time.sleep(2)
                result = session.post(self.login_url, verify=False, data=self.data, headers=self.headers)
                res = json.loads(result.text)
            except Exception as e:
                print "================="
                print e
                print "================="
            else:
                self.deal_result(res, table, tel_num)
        except Exception as e:
            print "================="
            if result:
                print result.text
            print e
            print "================="
        else:
            self.deal_result(res, table, tel_num)

    def deal_result(self, res, table, tel_num):
        # 注册过
        if res['code'] == '1000':
            table.ix[tel_num, 'kuaijin'] = 1
        # 没注册过
        elif res['code'] == '2000':
            table.ix[tel_num, 'kuaijin'] = 0
        else:
            table.ix[tel_num, 'kuaijin'] = -1

if __name__ == '__main__':
    session = requests.Session()
    login_url = "https://capi.timecash.cn/v2/User/ResetPasswordVerifySMS"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36",
        "Content-Type": "application/json",
        "TCSERVERVER": "1.0",
        # "Transfer-Encoding": "chunked",
        # "X-Powered-By": "PHP/5.6.24",
    }
    data = {
        "mobile": '18310502300',
    }
    result = session.post(login_url, verify=False, data=data, headers=headers)
    print result.text
    res = json.loads(result.text)
    if res['code'] == '1000':
        print 1
    # 没注册过
    elif res['code'] == '2000':
        print 0
    else:
        print -1
