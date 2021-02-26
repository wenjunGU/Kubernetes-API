#!/usr/bin/env pyrhon
# --*-- coding:utf-8 --*--


import requests,time
from os import system
from time import sleep
import socket
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename='/tmp/library.log',
                    filemode='w')

def getIP(domain):
    myaddr = socket.getaddrinfo(domain, 'https')
    return(myaddr[0][4][0])

def post_loginHttps1():
    try:
        while True:
            url = "https://library.prof.wang/avatar.png"
            response = requests.get(url,verify=False)
            logging.info("%s:%s" % (response.status_code,getIP("library.prof.wang")))
            print response.status_code,getIP("library.prof.wang")
            sleep(1)
    except BaseException,e:
            logging.error(e)
            print(e)

post_loginHttps1()
