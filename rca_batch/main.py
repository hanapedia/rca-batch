import os

from rca_batch.application.use_cases import GatherMetricsUseCase
from rca_batch.application.ports import DataStore
from rca_batch.infrastructure.config.adapter import load_config_from_env
from rca_batch.infrastructure.local_filesystem.adapter import LocalFileSystemAdapter
from rca_batch.infrastructure.prometheus.adapter import PrometheusAdapter
from rca_batch.infrastructure.s3.adapter import S3Adapter

def main():

    config = load_config_from_env()

    kube_namespace = os.getenv('KUBE_NAMESPACE', 'the-bench')
    storage = os.getenv('STORAGE', 'local_filesystem')

    dataStoreAdapter: DataStore
    if storage == 'local_filesystem':
        dataStoreAdapter = LocalFileSystemAdapter(config.data_store_config)
        print(f'[INFO]: using local_filesystem ({config.data_store_config.bucket}/{config.data_store_config.key}) as storage.')
    else:
        dataStoreAdapter = S3Adapter(config.data_store_config)
        print(f'[INFO]: using s3 ({config.data_store_config.bucket}/{config.data_store_config.key}) as storage.')

    gather_metrics = GatherMetricsUseCase(
        PrometheusAdapter(config.metric_fetcher_config, kube_namespace),
        dataStoreAdapter,
    )
    gather_metrics.execute()

if __name__ == "__main__":
    main()
