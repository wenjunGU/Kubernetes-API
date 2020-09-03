#!/usr/bin/env python
# --*-- coding:utf-8 --*--

import redis
from commands import getoutput
import os,time

#name = ['hvj','cdvf','defe','vfvf','efd','adsd','vffed','wdww','ggfr','swdd','fff','jkhje','yudh','njndn']
#value = ['7384','3221','8763','5453','8930','3922','8932','1483','9876','3283','9322','7843','8390','8745']

cace_name = ['check_httpd','check_svn']

class Database:
    def __init__(self):
        self.host = '127.0.0.1'
        self.port = 6379

    def write(self,mony,deal_number):
        try:
            key = mony
            val = deal_number
            r = redis.StrictRedis(host=self.host,port=self.port)
            r.set(key,val)
        except Exception, exception:
            print exception

    def read(self,key):
        try:
            r = redis.StrictRedis(host=self.host,port=self.port)
            value = r.get(key)
            return value
        except Exception, exception:
            print exception

    def items(self,key,value):
        try:
            info = getoutput("zabbix_get -s %s -p 10050 -k '%s'" % (key,value))
            return info
        except IOError:
            print("no input")

    def reads(self):
        try:
            r = redis.StrictRedis(host=self.host,port=self.port)
            value = r.keys()
            return value
        except Exception, exception:
            print exception

    def check(self):
        for i in db.reads():
            info = db.read(i)
            if db.items(info,'check_httpd') != '0':
                os.system("ansible {0} -m shell -a 'systemctl start httpd.service' > /dev/null".format(info))
                print("监控机器{0}:{1},httpd进程Down!".format(i,info))
            elif db.items(info,'check_svn') != '0':
                os.system("ansible {0} -m shell -a 'svnserve -d -r /svnroot/ --listen-port 3690 > /dev/null'".format(info))
                print("监控机器{0}:{1},svn进程Down!".format(i,info))
            else:
                print("监控机器{0}:{1},系统应用进程OK!".format(i,info))

if __name__ == '__main__':
    a = 0
    while True:
        db = Database()
        db.check()
        time.sleep(10)
        a += 1
