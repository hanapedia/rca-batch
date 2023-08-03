from rca_batch.application.ports import MetricFetcher, DataStore
from rca_batch.domain.services import MetricsProcessor

class GatherMetricsUseCase:
    def __init__(self, metric_fetcher: MetricFetcher, data_store: DataStore):
        self.metric_fetcher = metric_fetcher
        self.data_store = data_store

    def execute(self):
        print(f'[INFO]: Start querying metrics.')
        metrics = self.metric_fetcher.get_metrics()
        print(f'[INFO]: Done querying metrics.')

        print(f'[INFO]: Start processing metrics.')
        df = MetricsProcessor.process(metrics)
        print(f'[INFO]: Done processing metrics.')

        print(f'[INFO]: Start saving metrics.')
        self.data_store.save(df)
        print(f'[INFO]: Done saving metrics.')
