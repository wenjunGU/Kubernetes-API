# Kubernetes Python Client

Python client for the [kubernetes](http://kubernetes.io/) API.

##基于Flask写了一个轻量简便的K8S API，使用POST请求该接口使用，方便集成至CI或者CMDB。「写的比较简陋」
##属于轮子上搭棚子，感谢https://github.com/kubernetes-client/python.git。

## Installation

From source:

```
git clone --recursive https://github.com/kubernetes-client/python.git
cd python
python setup.py install
git clone --recursive https://github.com/JUNgege10/Kubernetes-API.git
cd Kubernetes-API
```


From [PyPI](https://pypi.python.org/pypi/kubernetes/) directly:

```
pip install kubernetes
pip install flask
```

## Examples

list all pods:

```python
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
```

watch on namespace object:

```python
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
```

//可直接使用python启动，实际应用建议使用guincorn
//docs下有所有API列表，本文只是列出几个常用的，如有问题欢迎交流
```
ls -al docs
```

//接口参数如下「包含所有路由」
key str
value str
node str
ns str
name str
replicas int
image str
port int
nodeport int
model str


//使用curl模拟POST测试如下，例如获取Pod信息
```
curl -H "Content-Type:application/json" -X POST -d '{"key":"get","value":"cattle-system"}' http://x.x.x.x:5555/pods-list
//返回字符串
```

//例如更新镜像
```
curl -H "Content-Type:application/json" -X POST -d '{"ns":"留空默认为default","name":"nginx-test","image":"nginx"}' http://x.x.x.x:5555/update-image
```

//例如创建新的deployment，template下有deployment模板，可以按照实际情况自己修改
```
curl -H "Content-Type:application/json" -X POST -d '{"ns":""空默认为default,"name":"api-test","replicas":2,"image":"ubuntu"}' http://x.x.x.x:5555/deploy-create
```


#使用前建议将Connect.py放入python Lib库目录中
