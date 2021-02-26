# coding:utf-8

import dingtalkchatbot.chatbot as cb
import datetime
import sys
import platform
import json
import base64
from commands import getoutput
import urllib2
class dingRobot():

    def __init__(self):
        self.url = "https://oapi.dingtalk.com/robot/send?access_token=9d7fe3c78e99867130125bffef2f4359027308016a9968b613cedae4eae040f1"

    def getMessage(self):
        post_url = 'http://47.96.182.222:5555/?name=cloudcare-core&status=error&ip=10.1.0.2'
        req = urllib2.Request(post_url)
        response = urllib2.urlopen(req)
        return response.read()

    def dingStart(self):
        msg = self.getMessage()
        xiaoding = cb.DingtalkChatbot(self.url)
        xiaoding.send_markdown(title="您有新的告警信息", text=msg)

if __name__ == "__main__":
  dingding = dingRobot()
  dingding.dingStart()
