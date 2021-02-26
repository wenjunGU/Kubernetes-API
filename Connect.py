from kubernetes  import  client, config
from kubernetes.client.rest import ApiException
import yaml
# kubernetes生成时/root目录下.kube目录下的认证配置文件
config.kube_config.load_kube_config(config_file="/root/.kube/config")
# config.load_kube_config(kube_conf)

#管理deployment时使用
api_instance = client.AppsV1Api()

#管理service时使用
CoreV1Api = client.CoreV1Api()
