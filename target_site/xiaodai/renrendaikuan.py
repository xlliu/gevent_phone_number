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


class Renrendaikuan(object):
    """
    处理过程
    生成结果文件 ==>> xianhua.xlsx
    """

    def __init__(self):
        self.login_url = "http://apiv2.rrjk.xiaoweixuedai.com/"
        self.headers = headers = {
            # "Content-Type":"application/json; charset=utf-8",
            # "Host":"apiv2.rrjk.xiaoweixuedai.com",
            "User-Agent":"okhttp/3.3.1",
            "x-ua":"TB API [Android] V3.0",
            "x-plateform":"Android AOSP on HammerHead",
            "x-client-version":"3.0",
            "x-plateform-version":"6.0.1",
            "Cookie":"",
            "Content-Type":"application/json; charset=utf-8",
            "Content-Length":"96",
            "Host":"apiv2.rrjk.xiaoweixuedai.com",
            "Connection":"Keep-Alive",
            "Accept-Encoding":"gzip"
        }
        self.data = {
            "service":"account.login",
            "mobile": "",
            "password": "2e749230d7490b5536c0b5b0c9d3a33a"
        }

    def run(self, tel_num, session, table):
        print "Ready time: %d | tel: %s | class: %s" % (time.time(), tel_num, self.__class__.__name__)
        result = None
        self.data["mobile"] = tel_num
        try:
            result = session.post(self.login_url, data=self.data, headers=self.headers)
            res = json.loads(result.text)
        except ProxyError:
            try:
                time.sleep(1)
                result = session.post(self.login_url, params=self.data, headers=self.headers)
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
        if res['msg'] == u'帐号或密码错误，请重新输入!':
            table.ix[tel_num, 'renrendaikuan'] = 1
        # 没注册过
        elif res['msg'] == '帐号不存在，请重新输入!':
            table.ix[tel_num, 'renrendaikuan'] = 0
        else:
            table.ix[tel_num, 'renrendaikuan'] = -1


if __name__ == '__main__':
    import requests
    # tel_num = '18310502300'
    tel_num = '13661268212'
    session = requests.session()
    table = {}
    class Test(Renrendaikuan):
        def deal_result(self, res, table, tel_num):
            print res
            if res['msg'] == u'帐号或密码错误，请重新输入!':
                print 1
            # 没注册过
            elif res['msg'] == u'帐号不存在，请重新输入!':
                print 0
            else:
                print -1
    test = Test()
    test.run(tel_num, session, table)