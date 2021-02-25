# --*-- coding:utf-8 --*--

from Connect import api_instance
import yaml
import time
import os

def update_replicas(namespace,name,replicas):
    body = api_instance.read_namespaced_deployment(namespace=namespace, name=name)
    body.spec.replicas = replicas
    api_instance.replace_namespaced_deployment(namespace=namespace, name=name, body=body)
    deployment_info = api_instance.read_namespaced_deployment(namespace=namespace,name=name)
    print("NameSpace: {0} DeployMent: {1} Replicas: {2} Update Successful".format(deployment_info.metadata.namespace,deployment_info.spec.template.spec.containers[0].name,replicas))
 
if __name__ == '__main__':
#    namespace = 'default'
#    name = 'nginx-test11'
#    replicas = 2
    update_replicas(namespace,name,replicas)
