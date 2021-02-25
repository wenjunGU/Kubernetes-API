# --*-- coding:utf-8 --*--

from Connect import api_instance
from flask import g

def delete_deployment(namespace,name):

    api_instance.delete_namespaced_deployment(namespace=namespace,name=name)

if __name__ == '__main__':
   # namespace = 'default'
   # name = 'nginx-test12'
    delete_deployment(namespace,name)




