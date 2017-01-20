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


class Feidai(object):
    """
    处理过程
    生成结果文件 ==>> xianhua.xlsx
    """

    def __init__(self):
        self.login_url = "https://app.feidai.com/SJDKSer/sjdk/user/sendSmsCode"
        self.headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Host": "app.feidai.com",
            "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 6.0.1; AOSP on HammerHead Build/MOB30H)",
        }
        self.data = {
            "mobile": None,
            "mobileDeviceId":"95276306863246326",
            "mobileModel":"AOSP on HammerHead",
            "client":1,
            "mobileSystemId":"6.0.1",
            "versionId":"5.0.0",
            "mobileOtherInfo":{"width":1080,"height":1776,"brand":"Android","allApp":"你我贷借款,随借随还,RE文件管理器,Via,豌豆荚,diycode"},
            "flag":1
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
        if res['code'] == '0000':
            table.ix[tel_num, 'feidai'] = 1
        # 没注册过
        elif res['code'] == '-3003':
            table.ix[tel_num, 'feidai'] = 0
        else:
            table.ix[tel_num, 'feidai'] = -1
    
if __name__ == '__main__':
    import requests
    # tel_num = '18310502300'
    tel_num = '13661268212'
    session = requests.session()
    table = {}
    class Test(Feidai):
        def deal_result(self, res, table, tel_num):
            print res
            if res['code'] == '0000':
                print 1
            # 没注册过
            elif res['code'] == '-3003':
                print 0
            else:
                print -1
    test = Test()
    test.run(tel_num, session, table)