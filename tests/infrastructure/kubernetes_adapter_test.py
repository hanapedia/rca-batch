from kubernetes import client, config
import pytest

from rca_batch.infrastructure.kubernetes_adapter import KubernetesAdapter

def test_kube_config():
    config.load_kube_config()

    v1 = client.CoreV1Api()
    print("Listing pods with their IPs:")
    ret = v1.list_pod_for_all_namespaces(watch=False)

    assert len(ret.items) > 0, "There are no pods in the cluster"

    for item in ret.items:
        print(f'{item.status.pod_ip} {item.metadata.namespace} {item.metadata.name}')

def test_KubernetesAdapter_get_pods():
    kubernetesAdapter = KubernetesAdapter("default")
    ret = kubernetesAdapter.get_pods()

    assert len(ret) > 0, "There are no pods in the namespace"

    for item in ret:
        print(item)

