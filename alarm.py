#!/usr/bin/env python
# --*-- coding:utf-8 --*--
import urllib2
import urllib

def alarm():
    post_url = 'http://www.test.com:8000/sms1.php'
    postData  = {'ip':'10.80.11.27','weight':'5','name':'6025.conf'}
    req = urllib2.Request(post_url)
    response = urllib2.urlopen(req,urllib.urlencode(postData))
    print response.read()

alarm()
