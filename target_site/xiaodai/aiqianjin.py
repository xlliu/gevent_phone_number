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


class AiQianJin(object):
    """
    处理过程
    生成结果文件 ==>> xianhua.xlsx
    """

    def __init__(self):
        self.login_url = "http://v3.iqianjin.com/C2000/M2006/"
        self.headers = {
            "Host": "v3.iqianjin.com"
        }
        self.data = {
            "body":
                {
                    "content": None
                },
            "comm":
                {
                    "pid": "352136069077002",
                    "type": 3,
                    "us": 67,
                    "version": "4.9.0"
                },
            "token": ""
        }

    def run(self, tel_num, session, table):
        print "Ready time: %d | tel: %s | class: %s" % (time.time(), tel_num, self.__class__.__name__)
        result = None
        self.data["body"]["content"] = tel_num
        try:
            result = session.post(self.login_url, verify=False, json=self.data, headers=self.headers)
            res = json.loads(result.text)
        except ProxyError as e:
            try:
                result = session.post(self.login_url, verify=False, json=self.data, headers=self.headers)
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
        file_name = "aiqianjin"
        if res.get("code") == 1:
            table.ix[tel_num, file_name] = 1
            #table.ix[int(tel_num)] = [1,]
        # 没注册过
        elif res.get("code") == -21:
            table.ix[tel_num, file_name] = 0
            #table.ix[int(tel_num)] = [0,]
        else:
            table.ix[tel_num, file_name] = -1
            #table.ix[int(tel_num)] = [-1,]

if __name__ == '__main__':
    import requests
    import pandas as pd
    tel_num = u'15541860723'
    table = pd.DataFrame(columns=[u"aiqianjin"])
    print table
    session = requests.session()
    test = AiQianJin()
    test.run(tel_num, session, table)
    print table
