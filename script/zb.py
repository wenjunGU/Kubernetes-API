#!/usr/bin/env python
# coding=utf-8
import requests
import json

class GetZabbix:
    def __init__(self):
        self.username = "zabbixtemp"
        self.password = "xxx"
        self.url = "https://xxxx/api_jsonrpc.php"
        self.token = self.getToken()

    def headers(self):
        headers = {
            "Content-Type": "application/json"
                  }
        return headers

    def getToken(self):
        data = {
            "jsonrpc": "2.0",
            "method": "user.login",
            "params": {
                "user": self.username,
                "password": self.password
            },
            "id": 1,
            "auth": None
        }
        r = requests.post(url=self.url, headers=self.headers(), data=json.dumps(data),verify=False)
        token = json.loads(r.content).get("result")
        return token

    def getHosts(self):
        data = {
            "jsonrpc": "2.0",
            "method": "host.get",
            "params": {
                "output": [
                    "hostid",
                    "host"
                ]
            },
            "id": 2,
            "auth": self.token
        }
        r = requests.post(url=self.url, headers=self.headers(), data=json.dumps(data),verify=False)
        return(json.loads(r.content).get("result"))


if __name__ == "__main__":
    start = GetZabbix()
    print start.getHosts()
