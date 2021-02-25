# --*-- coding:utf-8 --*--

from Connect import api_instance
import yaml
import time
import os
from flask import g

def update_image(namespace,name,image):
    body = api_instance.read_namespaced_deployment(namespace=namespace, name=name)
    body.spec.template.spec.containers[0].image = image
    body.spec.template.spec.containers[0].name = name
    api_instance.replace_namespaced_deployment(namespace=namespace, name=name, body=body)
    deployment_info = api_instance.read_namespaced_deployment(namespace=namespace,name=name)
    print("NameSpace: {0} DeployMent: {1} Image: {2} Update Successful".format(deployment_info.metadata.namespace,deployment_info.spec.template.spec.containers[0].name,image))
 
if __name__ == '__main__':
#    namespace = 'default'
#    name = 'nginx-test11'
#    image = 'nginx'
    update_image(namespace,name,image)
