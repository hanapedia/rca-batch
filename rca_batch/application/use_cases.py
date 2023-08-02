from .ports import MetricFetcher, DataStore
from rca_batch.domain.services import MetricsProcessor

class GatherMetricsUseCase:
    def __init__(self, metric_fetcher: MetricFetcher, data_store: DataStore):
        self.metric_fetcher = metric_fetcher
        self.data_store = data_store

    def execute(self):
        metrics = self.metric_fetcher.get_metrics()
        df = MetricsProcessor.process(metrics)
        self.data_store.save(df)
