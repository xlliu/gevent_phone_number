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


class Xiaoqian(object):
    """
    处理过程
    生成结果文件 ==>> xianhua.xlsx
    """

    def __init__(self):
        self.login_url = "http://www.xiaoqiandai.com/ajax/users/login"
        self.headers = {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36",
            "X-Requested-With": "XMLHttpRequest"
        }
        self.data = {
            "username": None,
            "password": '123123'
        }

    def run(self, tel_num, session, table):
        print "Ready time: %d | tel: %s | class: %s" % (time.time(), tel_num, self.__class__.__name__)
        result = None
        self.data["username"] = tel_num
        try:
            result = session.post(self.login_url, data=self.data, headers=self.headers)
            res = json.loads(result.text)
        except ProxyError:
            try:
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
            if result:
                print result.text
            print e
            print "================="
        else:
            self.deal_result(res, table, tel_num)

    def deal_result(self, res, table, tel_num):
        # 注册过
        if res['info'] == u'\u8d26\u53f7\u5bc6\u7801\u4e0d\u5339\u914d':
            table.ix[tel_num, 'xiaoqian2'] = 1
        # 没注册过
        elif res['info'] == u'\u7528\u6237\u4e0d\u5b58\u5728':
            table.ix[tel_num, 'xiaoqian2'] = 0
        else:
            table.ix[tel_num, 'xiaoqian2'] = -1

if __name__ == '__main__':
    import requests
    tel_num = '13661268212'
    session = requests.session()
    table = {}
    class Test(Xiaoqian):
        def deal_result(self, res, table, tel_num):
            print res
            # 注册过
            if res['info'] == u'\u8d26\u53f7\u5bc6\u7801\u4e0d\u5339\u914d':
                print 1
            # 没注册过
            elif res['info'] == u'\u7528\u6237\u4e0d\u5b58\u5728':
                print 0
            else:
                print -1
    test = Test()
    test.run(tel_num, session, table)
