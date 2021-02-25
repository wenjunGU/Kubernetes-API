# --*-- coding:utf-8 --*--

from Connect import CoreV1Api
import yaml
import time
import os,sys
from flask import g

def create_service(namespace,name,container_port,nodeport,type):
    with open('template/service.yaml', mode='r') as f:
        body = yaml.safe_load(f)
    body['metadata']['name'] = name
    body['metadata']['namespace'] = namespace
    body['metadata']['labels']['app'] = name
    if type == 'ClusterIP':
        body['spec'] = dict(type=type,
                                        selector={'app': name},
                                        ports=[
                                            {'protocol': 'TCP', 'port': container_port, 'targetPort': container_port}])
    elif type == 'NodePort':
        body['spec'] = dict(type=type,
                                        selector={'app': name},
                                        ports=[
                                            {'protocol': 'TCP', 'port': container_port, 'targetPort': container_port, 'nodePort': nodeport}])
    else:
        print('Type Fail! Only ClusterIP or NodePort')
        return('Type Fail! Only ClusterIP or NodePort')
        sys.exit(255)
    CoreV1Api.create_namespaced_service(
        namespace=namespace,
        body=body,
    )

if __name__ == '__main__':
    #namespace = 'default'
    #name = 'nginx-test5'
    #port = 80
    #nodeport = 80
    create_service(namespace,name,container_port,nodeport,type)
