from .ports import PodFetcher, MetricFetcher, DataStore
from rca_batch.domain.services import MetricsProcessor

class GatherMetricsUseCase:
    def __init__(self, pod_fetcher: PodFetcher, metric_fetcher: MetricFetcher, data_store: DataStore):
        self.pod_fetcher = pod_fetcher
        self.metric_fetcher = metric_fetcher
        self.data_store = data_store

    def execute(self):
        pods = self.pod_fetcher.get_pods()
        metrics = self.metric_fetcher.get_metrics(pods)
        df = MetricsProcessor.process(metrics)
        self.data_store.save(df)
