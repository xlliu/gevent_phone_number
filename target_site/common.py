# -*- coding: utf-8 -*-
import json
import sys

import time

reload(sys)
sys.setdefaultencoding('utf8')
from requests.exceptions import ProxyError


class CommonUtils(object):
    """
    公共部分抽取
    """
    @staticmethod
    def request_session(login_url, data, headers, session):

        try:
            result = session.post(login_url, verify=False, data=data, headers=headers)
            res = json.loads(result.text)
            return res, result
        except ProxyError:
            try:
                time.sleep(2)
                result = session.post(login_url, verify=False, data=data, headers=headers)
                res = json.loads(result.text)
                return res, result
            except Exception as e:
                print "================="
                print result.text
                print e
                print "================="
        except Exception as e:
            print "================="
            print result.text
            print e
            print "================="