# --*-- coding:utf-8 --*--

from Connect import api_instance,CoreV1Api
from flask import g

def list_pods(namespace):
    a = []
    ret = CoreV1Api.list_pod_for_all_namespaces(watch=False)
    for i in ret.items:
        if namespace != '':
            a.append("{0}: {1}: {2}".format(namespace,i.status.pod_ip,i.metadata.name))
        else:
            a.append("{0}: {1}: {2}".format(i.metadata.namespace,i.status.pod_ip,i.metadata.name))
    b = ",".join(a)
    return(b)

if __name__ == '__main__':
    namespace = ''
    list_pods(namespace)
