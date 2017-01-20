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

class YiLongDai(object):
    """
    处理过程
    生成结果文件 ==>> xianhua.xlsx
    """
    def __init__(self):
        self.login_url = "https://wap.eloancn.com/mobile/checkMobile.action"
        self.headers = {
            "Host": "wap.eloancn.com",
            # "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36",
        }
        self.data = {
        }
    def run(self, tel_num, session, table):
        # rr = random.randint(10, 20)
        # time.sleep(rr)

        # data.ix[['one', 'one'], ['a', 'e', 'd', 'd', 'd']]
        print "Ready time: %d | tel: %s | class: %s" % (time.time(), tel_num, self.__class__.__name__)
        # table.ix[tel_num, 'youli'] = True
        # print tel_num, session
        result = None
        self.data["mobile"] = tel_num
        try:
            result = session.post(self.login_url, verify=False, data=self.data, headers=self.headers)
            res = json.loads(result.text)
        except ProxyError:
            try:
                time.sleep(2)
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
            if result.text:
                print result.text
            print e
            print "================="
        else:
            self.deal_result(res, table, tel_num)

    def deal_result(self, res, table, tel_num):
        # 注册过
        if res.get("jsonData",{}).get('tip') == u"此手机号已经被注册过":
            table.ix[tel_num, 'yidongdai'] = 1
        # 没注册过
        elif res.get("jsonData",{}).get('tip') == "success":
            table.ix[tel_num, 'yidongdai'] = 0
        else:
            table.ix[tel_num, 'yidongdai'] = -1
if __name__ == '__main__':
    import requests
    tel_num = '15541860723'
    session = requests.session()
    table = {}
    class Test(YiLongDai):
        def deal_result(self, res, table, tel_num):
            # 注册过
            if res.get("jsonData",{}).get('tip') == u"此手机号已经被注册过":
                print u'注册过'
            # 没注册过
            elif res.get("jsonData",{}).get('tip') == "success":
                print u'没注册过'
            else:
                print u'未知'
    test = Test()
    test.run(tel_num, session, table)
