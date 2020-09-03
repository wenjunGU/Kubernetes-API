#!/usr/bin/env python
# --*--coding:utf-8--*--

import socket
import time

a = 0
while True:
    class main:
        def __init__(self,uid,uuid):
            self.uid = uid
            self.uuid = uuid

        def run(self):
            print self.uid
            print self.uuid

        def port(self):
            sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sk.settimeout(1)
            try:
                sk.connect(('%s' % self.uid, self.uuid))
                print '%s port %s OK' % (self.uid,self.uuid)
            except Exception:
                print '%s port %s not connect' % (self.uid,self.uuid)
            sk.close()

#ip = raw_input("plese input your's ip: ")
#port = input("plese input your's port: ")
    obj = main('101.251.233.156',80)
    obj.run()
    obj.port()
    time.sleep(2)
    a += 1
