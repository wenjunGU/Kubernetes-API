# --*-- coding:utf-8 --*--
from flask import Flask,g, request
import json,os,sys
from node_labels import label_node
from lists_ns import list_namespace
import logging
from lists_pod import list_pods
from deploy_create import create_deployment
from service_create import create_service
from update_pod_image import update_image
from update_pod_replicas import update_replicas
from deploy_delete import delete_deployment
from service_delete import delete_service

try:
    import http.client as http_client
except ImportError:
    import httplib as http_client
http_client.HTTPConnection.debuglevel = 1

app = Flask(__name__)
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
requests_log = logging.getLogger("requests.packages.urllib3")
requests_log.setLevel(logging.DEBUG)
requests_log.propagate = True
app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.DEBUG)

@app.route('/label',methods=['POST'])
def node_label_k8s():
    try:
        data = json.loads(request.data)
        g.key = data.get('key')
        g.value = data.get('value')
        g.node = data.get('node')
        if g.key == '' or g.value == '' or g.node == '':
            return('Make sure the POST value is correct！\n')
        else:
            label_node(g.node)
    except Exception as e:
        logging.error(e)
        print(e)
    return('OK\n')


@app.route('/ns-list',methods=['POST'])
def list_ns_k8s():
    data = json.loads(request.data)
    g.key = data.get('key')
    g.value = data.get('value')
    if g.key != 'get' or g.value != 'ns':
        return('Make sure the POST value is correct！\n')
    else:
        return(list_namespace() + '\n')

@app.route('/pods-list',methods=['POST'])
def list_pods_k8s():
    data = json.loads(request.data)
    g.namespace = data.get('ns')
    return(list_pods(g.namespace))

@app.route('/deploy-create',methods=['POST'])
def create_deployment_k8s():
    try:
        data = json.loads(request.data)
        g.ns = data.get('ns')
        g.name = data.get('name')
        g.replicas = data.get('replicas')
        g.image = data.get('image')
        if g.ns == '':
            g.ns = 'default'
        if g.name == '' or g.replicas == '' or g.image == '':
            return('Make sure the POST value is correct！\n')
        else:
            create_deployment()
    except Exception as e:
        logging.error(e)
        print(e)
    return('OK\n')

@app.route('/service-create',methods=['POST'])
def create_service_k8s():
    try:
        data = json.loads(request.data)
        g.ns = data.get('ns')
        g.name = data.get('name')
        g.port = data.get('port')
        g.nodeport = data.get('nodeport')
        g.model = data.get('model')
        if g.model == '':
            g.model = 'ClusterIP'
        if g.ns == '':
            g.ns = 'default'
        if g.name == '' or g.port == '' or g.nodeport == '':
            return('Make sure the POST value is correct！\n')
        else:
            create_service(g.ns,g.name,g.port,g.nodeport,g.model)
    except Exception as e:
        logging.error(e)
        print(e)
    return('OK\n')

@app.route('/update-image',methods=['POST'])
def update_image_k8s():
    try:
        data = json.loads(request.data)
        g.ns = data.get('ns')
        g.name = data.get('name')
        g.image = data.get('image')
        if g.ns == '':
            g.ns = 'default'
        if g.name == '' or g.image == '':
            return('Make sure the POST value is correct！\n')
        else:
            update_image(g.ns,g.name,g.image)
    except Exception as e:
        logging.error(e)
        print(e)
    return('OK\n')

@app.route('/update-replicas',methods=['POST'])
def update_replicas_k8s():
    try:
        data = json.loads(request.data)
        g.ns = data.get('ns')
        g.name = data.get('name')
        g.replicas = data.get('replicas')
        if g.ns == '':
            g.ns = 'default'
        if g.name == '' or g.replicas == '':
            return('Make sure the POST value is correct！\n')
        else:
            update_replicas(g.ns,g.name,g.replicas)
    except Exception as e:
        logging.error(e)
        print(e)
    return('OK\n')

@app.route('/delete-deploy',methods=['POST'])
def delete_deploy_k8s():
    try:
        data = json.loads(request.data)
        g.ns = data.get('ns')
        g.name = data.get('name')
        if g.ns == '':
            g.ns = 'default'
        if g.name == '':
            return('Make sure the POST value is correct！\n')
        else:
            delete_deployment(g.ns,g.name)
    except Exception as e:
        logging.error(e)
        print(e)
    return ('OK\n')

@app.route('/delete-service',methods=['POST'])
def delete_service_k8s():
    try:
        data = json.loads(request.data)
        g.ns = data.get('ns')
        g.name = data.get('name')
        if g.ns == '':
            g.ns = 'default'
        if g.name == '':
            return('Make sure the POST value is correct！\n')
        else:
            delete_service(g.ns,g.name)
    except Exception as e:
        logging.error(e)
        print(e)
    return ('OK\n')

if __name__ == '__main__':
    app.run(debug=True, port=5555, host='0.0.0.0')
