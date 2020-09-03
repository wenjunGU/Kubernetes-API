# coding:utf-8

import dingtalkchatbot.chatbot as cb
import datetime
import sys
import platform
import json
import base64
from commands import getoutput
import urllib2
Today = datetime.datetime.now().strftime('%Y%m%d')
Hour = datetime.datetime.now().strftime('%Y%m%d%H')

os = platform.system()
if os == 'Windows':
    path_day = "C:\\Users\\hehe\\Desktop\\临时\\" +  Today + ".txt"
    path_hour = "C:\\Users\\hehe\\Desktop\\临时\\" +  Hour + ".txt"
else:
    path_day = "/tmp/" +  Today + ".txt"
    path_hour = "/tmp/" +  Hour + ".txt"


class dingRobot():

    def __init__(self,filepath):
        self.url = "https://oapi.dingtalk.com/robot/send?access_token=9d7fe3c78e99867130125bffef2f4359027308016a9968b613cedae4eae040f1"
        self.path = filepath

    def getMessage(self):
        post_url = 'http://47.96.182.222:5555/check/?name=cloudcare-core&status=error&ip=10.1.0.2'
        req = urllib2.Request(post_url)
        response = urllib2.urlopen(req)
        return response.read()

    def dingStart(self):
        msg = self.getMessage()
        xiaoding = cb.DingtalkChatbot(self.url)
        xiaoding.send_markdown(title="您有新的告警信息", text=msg)

if __name__ == "__main__":
    if sys.argv[1] == 'run1':
        dingding = dingRobot(path_day)
        dingding.dingStart()

    elif sys.argv[1] == 'run2':
        dingding = dingRobot(path_hour)
        dingding.dingStart()
    else:
        print("The argument was wrong! please use 'run1' or 'run2'")
