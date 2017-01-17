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
import random
import json
requests.packages.urllib3.disable_warnings()

class GongPengJia(object):
    """
    处理过程
    生成结果文件 ==>> xianhua.xlsx
    """
    def __init__(self):
        self.login_url = "http://api8.gongpingjia.com/mobile/account/login/"
        self.headers = {
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Host": "api8.gongpingjia.com",
            "Origin": "http://api8.gongpingjia.com",
            # "Referer": "http://orders.roseonly.com.cn/pcEntrance/tologin",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Ch",
        }
        self.data = {
            "account": None,
            "password": "hgfgk",
            "login_type": "username_password",
            "device\_code": "ffffffff-afae-b8a2-efd9-72b60033c587"
        }
    def run(self, tel_num, session, table):
        # rr = random.randint(10, 20)
        # time.sleep(rr)
        
        # data.ix[['one', 'one'], ['a', 'e', 'd', 'd', 'd']]
        print "ready", tel_num, GongPengJia.__name__
        # table.ix[int(tel_num), 'youli'] = True
        # print tel_num, session
        result = None
        self.data["account"] = tel_num
        try:
            result = session.post(self.login_url, data=self.data, headers=self.headers)
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
            if not result.text:
                print result.text
            print e
            print "================="
        else:
            self.deal_result(res, table, tel_num)
        # res = "-2"
        # print res
        # print json.loads(res).get("success")
        # 注册过

    def deal_result(self, res, table, tel_num):
        if res.get("msg") == u"密码错误":
            table.ix[int(tel_num), 'gongpingjia'] = 1
        # 没注册过
        elif res.get("msg") == u"该账号不存在":
            table.ix[int(tel_num), 'gongpingjia'] = 0
        else:
            table.ix[int(tel_num), 'gongpingjia'] = -1
