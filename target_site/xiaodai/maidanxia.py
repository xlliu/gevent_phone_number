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


class MaiDanXia(object):
    """
    处理过程
    生成结果文件 ==>> xianhua.xlsx
    """

    def __init__(self):
        self.login_url = "https://common-mobile.fenqi.im:8443/rest/validationCode"
        self.headers = {
            "Content-Type": "application/json",
            "Host": "common-mobile.fenqi.im:8443",
            "app-version": "1.25.0",
            "Referer": "https://borrower.dianrong.com/borrower-static/wallet/v6.12/forget.html",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Ch",
        }
        self.json = {
            "category": "AuthValidationCode",
            "mobile": None,
            "app-version": "1.25.0",
            "Content-Type": "application/json"
        }

    def run(self, tel_num, session, table):
        print "Ready time: %d | tel: %s | class: %s" % (time.time(), tel_num, self.__class__.__name__)
        result = None
        self.json["mobile"] = tel_num
        try:
            result = session.post(self.login_url, verify=False, json=self.json, headers=self.headers)
            res = json.loads(result.text)
        except ProxyError as e:
            print "================="
            print self.__class__.__name__, e
            print "================="
            try:
                time.sleep(2)
                result = session.post(self.login_url, verify=False, json=self.json, headers=self.headers)
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
        if res.has_key("data"):
            table.ix[tel_num, 'maidanxia'] = 1
        # 没注册过
        elif not res.has_key("data"):
            table.ix[tel_num, 'maidanxia'] = 0
        else:
            table.ix[tel_num, 'maidanxia'] = -1


if __name__ == '__main__':
    import requests
    import pandas as pd
    tel_num = u'15541860723'
    table = pd.DataFrame(index=[tel_num, ], columns=[u"dianrong", ])
    print table
    session = requests.session()
    test = DianRong()
    test.run(tel_num, session, table)
    print table