# --*-- coding:utf-8 --*--

from Connect import CoreV1Api
import json
from flask import g

def label_node(node):

    body = {
        "metadata": {
            "labels": {
                "%s"%g.key: "%s"%g.value,
                "project": None}
        }
    }

    api_response = CoreV1Api.patch_node(node, body)
    print('Node Pod_Cidr is {0}'.format(api_response.spec.pod_cidr))
#    ret = CoreV1Api.list_node()
#    ret = ret.items[0]
#    pprint(ret.items.metadata.labels.kubernetes.io/hostname)
    

if __name__ == '__main__':
    label_node(node)
