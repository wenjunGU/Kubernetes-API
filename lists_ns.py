# --*-- coding:utf-8 --*--

from Connect import api_instance,CoreV1Api
from kubernetes import watch

def list_namespace():
    count = 7
    ns = []
    w = watch.Watch()
    for event in w.stream(CoreV1Api.list_namespace, _request_timeout=60):
        ns.append((event['object'].metadata.name))
        count -= 1
        if not count:
            w.stop()
    #print("All Namespace: {}".format(ns))
    b = ",".join(ns)
    return(b)


if __name__ == '__main__':
    list_namespace()
