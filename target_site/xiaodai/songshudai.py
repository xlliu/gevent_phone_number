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
import urllib

requests.packages.urllib3.disable_warnings()


class Songshudai(object):
    """
    处理过程
    生成结果文件 ==>> xianhua.xlsx
    """

    def __init__(self):
        self.login_url = "https://app.squloan.com/msg/getVerifyCode?"
        self.headers = {
            "Accept":"Application/Json",
            "Host":"app.squloan.com",
        }
        self.data = {
            "access_token":"127a065d16cf2c3d9234be714417859f07bf2f1b",
            "type": 0,
            "business": "forgotPassword",
            "mobile": None,
            "source": "android"
        }

    def run(self, tel_num, session, table):
        print "Ready time: %d | tel: %s | class: %s" % (time.time(), tel_num, self.__class__.__name__)
        result = None
        self.data["mobile"] = tel_num
        self.login_url = self.login_url + urllib.urlencode(self.data)
        try:
            result = session.get(self.login_url, headers=self.headers)
            res = json.loads(result.text)
        except ProxyError:
            try:
                time.sleep(2)
                result = session.get(self.login_url, headers=self.headers)
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
        if res['errorCode'] == 0:
            table.ix[tel_num, 'songshudai'] = 1
        # 没注册过
        elif res['errorCode'] == 1:
            table.ix[tel_num, 'songshudai'] = 0
        else:
            table.ix[tel_num, 'songshudai'] = -1

if __name__ == '__main__':
    session = requests.Session()
    login_url = "https://app.squloan.com/msg/getVerifyCode?"
    headers = {
        "Accept":"Application/Json",
        "Host":"app.squloan.com",
    }
    data = {
        "access_token":"127a065d16cf2c3d9234be714417859f07bf2f1b",
        "type": 0,
        "business": "forgotPassword",
        "mobile": "13661268212",
        "source": "android"
    }
    login_url = login_url + urllib.urlencode(data)
    # print login_url
    result = session.get(login_url, headers=headers)
    print result.text
    res = json.loads(result.text)
    if res['errorCode'] == 0:
        print 1
    # 没注册过
    elif res['errorCode'] == 1:
        print 0
    else:
        print -1
