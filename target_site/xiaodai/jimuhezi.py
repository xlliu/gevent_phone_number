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


class JiMuHeZi(object):
    """
    处理过程
    生成结果文件 ==>> xianhua.xlsx
    """

    def __init__(self):
        self.login_url = "https://passport.jimubox.com/authentication/login?redirectUrl=https://www.jimu.com/User/AssetOverview"
        self.headers = {
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Host": "passport.jimubox.com",
            "Origin": "https://passport.jimubox.com",
            "Referer": "https://passport.jimubox.com/authentication/login?redirectUrl=https://www.jimu.com/User/AssetOverview",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36",
            "Upgrade-Insecure-Requests": "1"
        }
        self.data = {
            "site": "B662B0F090BE31C1DCB6A13D70E81429",
            "username": None,
            "password": "abcde12345",
            "agreeContract": "on",
        }

    def run(self, tel_num, session, table):
        print "Ready time: %d | tel: %s | class: %s" % (time.time(), tel_num, self.__class__.__name__)
        result = None
        self.data["username"] = tel_num
        try:
            result = session.get(self.login_url, verify=False, data=self.data, headers=self.headers)
            res = result.text
        except ProxyError as e:
            try:
                time.sleep(1)
                result = session.get(self.login_url, verify=False, data=self.data, headers=self.headers)
                res = result.text
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
        if u"密码" in res:
            table.ix[tel_num, 'jimuhezi'] = 1
        # 没注册过
        elif u"不存在" in res:
            table.ix[tel_num, 'jimuhezi'] = 0
        else:
            table.ix[tel_num, 'jimuhezi'] = -1

if __name__ == '__main__':
    import requests
    tel_num = '15541860723'
    session = requests.session()
    table = {}
    class Test(JiMuHeZi):
        def deal_result(self, res, table, tel_num):
            print res
            print "-"
            # 注册过
            if u"密码" in res:
                print u'注册过'
            # 没注册过
            elif u"不存在" in res:
                print u'没注册过'
            else:
                print u'未知'
    test = Test()
    test.run(tel_num, session, table)