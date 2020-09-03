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
                    filename='/tmp/files.log',  
                    filemode='w')

def getIP(domain):
    myaddr = socket.getaddrinfo(domain, 'https')
    return(myaddr[0][4][0])

def post_loginHttps1():
    try:
        while True:
            url = "https://files.prof.wang/template/cloudcare-logo%403x.png"
            response = requests.get(url,verify=False)
            logging.info("%s:%s" % (response.status_code,getIP("files.prof.wang")))
            print getIP("files.prof.wang"),response.status_code
            sleep(1)
    except BaseException,e:
            logging.error(e)
            print(e)

post_loginHttps1()
