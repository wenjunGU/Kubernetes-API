# --*-- coding:utf-8 --*--

from flask import g
import requests
import random
import logging
import string
import sys
import datetime 
import re

reload(sys)
sys.setdefaultencoding('utf-8')

class send_ding(object):

    def __init__(self):
        self.url = "http://xxxx/jkgj/ReceiveAlert.php"
        self.token = "xxxx"
        self.methods = "POST"

    def get_status(self):
        if g.STATUS == "firing":
            return "PROBLEM"
        elif g.STATUS == "resolved":
            return "OK"
        else:
            return "PROBLEM"

    def get_hostip(self):
        result = re.findall(r"\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b", g.HOSTIP)
        if result:
            for i in result:
                return i
        else:
            return g.HOSTIP

    def data_load(self):
        content = {
                    "hostgroup": "{0}".format(g.PROJECT),
                    "hostname": "{0}".format(g.HOSTNAME),
                    "hostip": "{0}".format(self.get_hostip()),
                    "trigger": "{0}".format(g.DESCRIPTION),
                    "datetime": "{0}".format(datetime.datetime.now().strftime('%Y.%m.%d %H:%M:%S')),
                    "status": "{0}".format(self.get_status()),
                    "event_id": "{0}".format("".join(map(lambda x:random.choice(string.digits), range(8))))
                  }
        return content

    logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename='/tmp/send_kodo.log',
                    filemode='a+')

    def headers(self):
        headers = {
            "token": self.token
                  }
        return headers

    def run(self):
        try:
            resp = requests.request(self.methods, self.url, headers=self.headers(), data=self.data_load())                            
            print('url:%s headers:%s body:%s' % (resp.request.url, resp.request.headers, resp.request.body))                                                                   
            print(resp.status_code, resp.text)
            logging.info('url:%s headers:%s body:%s' % (resp.request.url, resp.request.headers, resp.request.body))
            logging.info("%s:%s" % (resp.status_code, resp.text))
        except Exception as e:
            print(e)

obj = send_ding()
