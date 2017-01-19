# -*- coding: utf-8 -*-
# import gevent.monkey
# gevent.monkey.patch_all(socket=True, dns=True, time=True, select=True, thread=False, os=True, ssl=True, httplib=False,
#               subprocess=True, sys=False, aggressive=True, Event=False,
#               builtins=True, signal=True)
import sys

from requests.exceptions import ProxyError

reload(sys)
sys.setdefaultencoding('utf8')

__author__ = 'rae.zhao'
import requests
import time
import random
import json
requests.packages.urllib3.disable_warnings()

class TouNa(object):
    """
    处理过程
    生成结果文件 ==>> xianhua.xlsx
    """
    def __init__(self):
        self.login_url = "https://tnhdapp.touna.cn/tounacn/account.do?"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36",
        }
        self.data = {

            "method": 'resetPswReminder',
            "type": '1',
            "subtime":str(int(time.time()*1000))
        }
    def run(self, tel_num, session, table):
        # rr = random.randint(10, 20)
        # time.sleep(rr)

        # data.ix[['one', 'one'], ['a', 'e', 'd', 'd', 'd']]
        print "ready", tel_num, TouNa.__name__
        # table.ix[int(tel_num), 'youli'] = True
        # print tel_num, session
        result = None
        self.data["proof"] = tel_num
        try:
            result = session.get(self.login_url, verify=False, params=self.data, headers=self.headers)
            res = json.loads(result.text)
        except ProxyError:
            try:
                time.sleep(2)
                result = session.get(self.login_url, params=self.data, headers=self.headers)
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
        if res.get("status") == 200:
            table.ix[int(tel_num), 'touna'] = 1
        # 没注册过
        elif res.get("status") == 500:
            table.ix[int(tel_num), 'touna'] = 0
        else:
            table.ix[int(tel_num), 'touna'] = -1
if __name__ == '__main__':
    import requests
    tel_num = '15541860723'
    session = requests.session()
    table = {}
    class Test(TouNa):
        def deal_result(self, res, table, tel_num):
            # 注册过
            if res.get("status") == 200:
                print u'注册过'
            # 没注册过
            elif res.get("status") == 500:
                print u'没注册过'
            else:
                print u'未知'
    test = Test()
    test.run(tel_num, session, table)