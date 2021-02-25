#! coding:utf-8

from flask import Flask,g,render_template,request
from datetime import datetime
from elasticsearch import *
import sys
import logging
import json
import time

def index_message(project,alertTime,host,hostname,status,description):
        try:
            es = Elasticsearch("120.27.215.65:9201")                                                                                                                  
            data = {                                                                                                                                                   
            "@timestamp":datetime.now().strftime( "%Y-%m-%dT%H:%M:%S.000+0800" ),                                                                                      
            "project":"{0}".format(project),                                                                                                                           
            "alertTime":"{0}".format(alertTime),                                                                                                                       
            "host":"{0}".format(host),                                                                                                                                 
            "hostname":"{0}".format(hostname),                                                                                                                         
            "status":"{0}".format(status),                                                                                                                             
            "description":"{0}".format(description),                                                                                           
            "region":"hz-monitor"
            }                                                                                                                                                          
            es.index( index="monitor-%s"%time.strftime('%Y-%m-%d',time.localtime(time.time())), doc_type="error_code", body=data )                                     
            logging.info(es.index)                                                                                                                                     
        except Exception,e:                                                                                                                                            
            logging.error(e)                                                                                                                                           
            print e 

app = Flask(__name__)

@app.route('/prom',methods=['GET','POST'])
def login():
    if request.method == 'GET':
        username = request.args
        keys = username.to_dict().keys()
        try:
            status =   keys[0]
            hostname = keys[1]
            hostip = keys[2]
            hostgroup = keys[3]
            datetime = keys[4]
            trigger = keys[5]
            index_message(hostgroup,datetime,hostip,hostname,status,trigger)
            return status
            #return  keys[0] +  keys[1] + keys[2] + keys[3] + keys[4] + keys[5]
        except Exception,e:
            return e
    else:
        return "methods is not get"

if __name__ == '__main__':
    app.run(debug=True, port=5555, host='0.0.0.0')
