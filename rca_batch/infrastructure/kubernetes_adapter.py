from kubernetes import client, config
from rca_batch.application.ports import PodFetcher

class KubernetesAdapter(PodFetcher):
    def __init__(self, namespace: str):
        config.load_kube_config()
        self.api = client.CoreV1Api()
        self.namespace = namespace

    def get_pods(self):
        return [i.metadata.name for i in self.api.list_namespaced_pod(self.namespace).items]
