# --*-- coding:utf-8 --*--

from Connect import api_instance
import yaml
import time
import os
from flask import g

def create_deployment():
    with open('template/deployment.yaml', mode='r') as f:
        body = yaml.safe_load(f)

    body['metadata']['name'] = g.name
    body['metadata']['namespace'] = g.ns
    body['spec']['replicas'] = g.replicas
    body['spec']['selector']['matchLabels']['app'] = g.name
    body['spec']['template']['metadata']['labels']['app'] = g.name
    api_instance.create_namespaced_deployment(namespace='default', body=body)
    time.sleep(2)
    body = api_instance.read_namespaced_deployment(namespace=g.ns, name=g.name)
    body.spec.template.spec.containers[0].image =  g.image
    body.spec.template.spec.containers[0].name = g.name
    api_instance.replace_namespaced_deployment(namespace=g.ns, name=g.name, body=body)
    deployment_info = api_instance.read_namespaced_deployment(namespace=g.ns,name=g.name)
    print("NameSpace-{0} DeployMent-{1} Create Successful".format(deployment_info.metadata.namespace,deployment_info.spec.template.spec.containers[0].name))
 
if __name__ == '__main__':
#    namespace = 'default'
#    name = 'nginx-test12'
#    replicas = 1
#    image = 'nginx'
#    create_deployment(namespace=namespace,name=name,replicas=replicas,image=image)
    create_deployment()
