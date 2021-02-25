# --*-- coding:utf-8 --*--

from Connect import CoreV1Api

def delete_service(namespace,name):

    CoreV1Api.delete_namespaced_service(namespace=namespace,name=name)

if __name__ == '__main__':
#    namespace = 'default'
#    name = 'nginx-test2'
    delete_service(namespace,name)




