#!/usr/bin/python
# -*- coding: UTF-8 -*-

import requests
import socket,re,sys
import json

def check_server(ip='127.0.0.1',port='80'):
        sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sk.settimeout(2)
        try:
            sk.connect((str(ip),int(port)))
            return 'ok'
        except Exception:
            return 'fail'
        sk.close()


def read_ip():
  with open('ip.txt','r') as f:
    s = []
    dates = {}
    for line in f:
        ip = {}
        line=line.strip('\n')
        str = check_server(line,80)
        if str == "ok":
            ip.update({"ip":line,"status":"ok"})
        else:
            ip.update({"ip":line,"status":"err"})
        s.append(ip)
    dates.update({"date":s})
    return json.dumps(dates)

if __name__ == '__main__':
    print(read_ip())
