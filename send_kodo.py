# -*- coding: utf-8 -*-

'''
title字段:告警标题
alert_id:告警ID
content:告警的内容
level:告警级别
source:告警来源
extra:json类型，可传多指 「选填参数」
create_at:所需时间段范围内的数据,脚本自动生成
执行方式: python Send_Kodo.py "CloudCare-Production-Biz-CloudCare-Home" "zy-devops-demo的CPU 使用率大于90%" "Average" "probelem" "10.0.0.0" "2019.03.14 17:44:00"
'''
import MySQLdb
import string
import random
import json
import requests
import time
import base64
import hashlib
import hmac
import sys
import logging
import urllib2

class Send_kodo(object):

    #定义常量
    def __init__(self):
        self.api_password = "xxxxxx"
        self.url = ["https://xxxxx/v1/write/alert","https://xxxxx/v1/write/alert","https://xxxx/v1/write/alert"]
        self.api_url = ["https://xxxx/v1/internal/ak","https://xxxx/v1/internal/ak","https://xxxx/v1/internal/ak"]
        self.date = time.strftime("%a, %d %b %Y %H:%M:%S GMT", time.gmtime())
        self.content_type = 'application/json'
        self.methods = "POST"
        self.alert = "".join(map(lambda x:random.choice(string.digits), range(8)))

    #通过传入的project取得运维平台里的team_id
    def get_team_id(self,project):
        conn = MySQLdb.connect(host='1.0.2.3',user='readonaly',passwd='xxxx',db='xxxx',charset='utf8')
        cursor = conn.cursor()
        count = cursor.execute("select c.unique_id from projects p, customers c where  p.name = '%s' and p.customer_id = c.uuid;"%project)
        ip_list = []
        try:
            results = cursor.fetchall()
        except Exception,e:
            print("code error",e)
            conn.close()
        result=list(results)
        for r in result:
            ip_list.append(('%s' % r))
        for i in ip_list:
            return str("team-"+i)
        conn.close()

    #通过kodo开放接口取得用户ak
    def get_aksk(self,k,s):
        try:
            headers = {'content-type': "application/json"}
            team_id = self.get_team_id(sys.argv[1])
            internal_password = self.api_password
            url = "{0}?team_id={1}&internal_password={2}".format(s,team_id,internal_password)
            response = requests.post(url,headers = headers)
            if response:
                hjson = json.loads(response.text)
                return str(hjson['content']['%s'%k])
            else:
                return("code error")
        except Exception,e:
            print("code error",e)

    #做接口md5验证
    def get_md5(self,s):
        h = hashlib.md5()
        h.update(s.encode('utf8'))
        return h.hexdigest()

    #转义level字段，转成kodo接口接受的字段名
    def get_level(self):
        level = sys.argv[3]
        if level == "Average":
            level = "warning"
            return level
        elif level == "High":
            level = "danger"
            return level
        else:
            return level
    #转义status字段，转成kodo接口接受的字段名
    def get_status(self):
        status = sys.argv[4]
        if status == "":
            status = "info"
            return status
        else:
            return status
    #接受传入kodo的告警信息，json字符串格式
    def payload(self):
        title = sys.argv[1]
        content = sys.argv[2]
        level = self.get_level()
        alert_id = self.alert
        status = self.get_status()
        hostip = sys.argv[5]
        alert_time = sys.argv[6]
        content = json.dumps([
                {
                    "title": "{}".format(title),
                    "content": "{0} -- {1} -- {2}".format(alert_time,hostip,content),
                    "level": "{}".format(level),
                    "source": "bj-monitor",
                    "extra": {"status":"%s"%status,"type":"alarm"},
                    "alert_id": "{}".format(alert_id),
                    "create_at": int(time.time())
                }
            ])
        return content

    #做kodo接口验证
    def sign(self,ak=None, sk=None, method=None, date_sign=None, team_id=None, type_sign=None, content=None):
        method_sign = method.upper()
        md5_sign = self.get_md5(content)
        type_sign = type_sign if type_sign else ''
        date_sign = date_sign if date_sign else ''
        team_sign = team_id
        array_sign = [method_sign, md5_sign, type_sign, date_sign, team_sign]
        string_to_sign = '\n'.join(array_sign)
        h = hmac.new(sk, string_to_sign, hashlib.sha1)
        d = h.digest()
        signature = base64.encodestring(d).strip()
        return "kodo %s:%s" % (ak, signature)

    #日志模块
    logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename='/tmp/send_kodo.log',
                    filemode='a+')

   #定义post的header头，kodo接口二次验证
    def headers(self,access_key,secret_key):
        headers = {
            "Authorization": self.sign(ak=access_key,
                sk=secret_key, method=self.methods, date_sign=self.date,
                team_id=self.get_team_id(sys.argv[1]), type_sign=self.content_type, content=self.payload()),
            "X-Team-Id": self.get_team_id(sys.argv[1])}
        headers["Content-Type"] = self.content_type
        headers["Date"] = self.date
        return headers

    #执行主体
    def run(self):
        try:
            for i in range(0,len(self.api_url)):
                resp = requests.request(self.methods, self.url[i], headers=self.headers(self.get_aksk('access_key',self.api_url[i]),self.get_aksk('secret_key',self.api_url[i])), data=self.payload())
                print('url:%s headers:%s body:%s' % (resp.request.url, resp.request.headers, resp.request.body))                                                                   
                print(resp.status_code, resp.text)
                logging.info('url:%s headers:%s body:%s' % (resp.request.url, resp.request.headers, resp.request.body))
                logging.info("%s:%s" % (resp.status_code, resp.text))
        except Exception as e:
            print(e)

if __name__ == '__main__':
    #实例化类的对象obj，并运行对象的执行主体类
    obj = Send_kodo()
    obj.run()
