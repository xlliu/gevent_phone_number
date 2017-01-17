# -*- coding: utf-8 -*-
# import gevent.monkey
# gevent.monkey.patch_all(socket=True, dns=True, time=True, select=True, thread=False, os=True, ssl=True, httplib=False,
#               subprocess=True, sys=False, aggressive=True, Event=False,
#               builtins=True, signal=True)
import sys

from target_site.common import CommonUtils

reload(sys)
sys.setdefaultencoding('utf8')

__author__ = 'xlliu'
import requests
import json

requests.packages.urllib3.disable_warnings()


class YeShouPai(object):
    """
    处理过程
    生成结果文件 ==>> xianhua.xlsx
    """

    def __init__(self):
        self.login_url = "http://www.thebeastshop.com/user/dologin.htm"
        self.headers = {
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Host": "www.thebeastshop.com",
            "Origin": "http://www.thebeastshop.com",
            "Referer": "http://www.thebeastshop.com/user/login.htm",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Ch",
        }
        self.data = {
            "loginName": None,
            "password": 123123123,
            "remeberme": None
        }

    def run(self, tel_num, session, table):
        # rr = random.randint(10, 20)
        # time.sleep(rr)

        # data.ix[['one', 'one'], ['a', 'e', 'd', 'd', 'd']]
        print "ready", tel_num, YeShouPai.__name__
        # table.ix[int(tel_num), 'youli'] = True
        # print tel_num, session

        self.data["loginName"] = tel_num
        res, result = CommonUtils.request_session(self.login_url, self.data, self.headers, session)
        # 注册过
        if not res:
            table.ix[int(tel_num), 'yeshoupai'] = 1
        # 没注册过
        elif not json.loads(res).get("success"):
            table.ix[int(tel_num), 'yeshoupai'] = 0
        else:
            table.ix[int(tel_num), 'yeshoupai'] = -1
