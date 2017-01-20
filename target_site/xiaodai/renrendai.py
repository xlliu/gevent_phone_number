# -*- coding: utf-8 -*-
# import gevent.monkey
# gevent.monkey.patch_all(socket=True, dns=True, time=True, select=True, thread=False, os=True, ssl=True, httplib=False,
#               subprocess=True, sys=False, aggressive=True, Event=False,
#               builtins=True, signal=True)
import sys

from requests.exceptions import ProxyError

reload(sys)
sys.setdefaultencoding('utf8')

__author__ = 'xlliu'
import requests
import time
import json

requests.packages.urllib3.disable_warnings()


class RenRenDai(object):
    """
    处理过程
    生成结果文件 ==>> xianhua.xlsx
    """

    def __init__(self):
        self.login_url = "https://nirvana.ucredit.com/nirvana/user/login"
        self.headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Host": "nirvana.ucredit.com",
            "Origin": "chrome-extension://fhbjgbiflinjbdggehcddcbncdddomop",
            # "Referer": "https://borrower.dianrong.com/borrower-static/wallet/v6.12/forget.html",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36",
            # "Postman-Token": "a6c8fea8-25f0-66a8-77ea-af3ef06919aa"
        }
        self.data = {
            "mobile": None,
            "password": '123123123',
            "passwordType": 0,
        }

    def run(self, tel_num, session, table):
        print "Ready time: %d | tel: %s | class: %s" % (time.time(), tel_num, self.__class__.__name__)
        result = None
        self.data["mobile"] = tel_num
        try:
            result = session.post(self.login_url, verify=False, data=self.data, headers=self.headers)
            res = json.loads(result.text)
        except ProxyError as e:
            try:
                result = session.post(self.login_url, verify=False, data=self.data, headers=self.headers)
                res = json.loads(result.text)
            except Exception as e:
                print "================="
                print self.__class__.__name__, e
                print "================="
            else:
                self.deal_result(res, table, tel_num)
        except Exception as e:
            print "================="
            if result:
                print result.text
            print self.__class__.__name__, e
            print "================="
        else:
            self.deal_result(res, table, tel_num)

    def deal_result(self, res, table, tel_num):
        if res.get("code") == 10031:
            table.ix[tel_num, 'renrendai'] = 1
        # 没注册过
        elif res.get("code") == 10022:
            table.ix[tel_num, 'renrendai'] = 0
        else:
            table.ix[tel_num, 'renrendai'] = -1

if __name__ == '__main__':
    import requests
    # tel_num = '18310502300'
    tel_num = '13661268212'
    session = requests.session()
    table = {}
    class Test(RenRenDai):
        def deal_result(self, res, table, tel_num):
            print res
            if res.get("code") == 10031:
                print 1
            # 没注册过
            elif res.get("code") == 10022:
                print 0
            else:
                print -1
    test = Test()
    test.run(tel_num, session, table)