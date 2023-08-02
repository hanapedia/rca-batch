import textwrap
from typing import Dict, List

from rca_batch.application.ports import MetricFetcher
from rca_batch.domain.entities import Metrics, TimeSeries
from rca_batch.infrastructure.prometheus.client import PrometheusClient, PrometheusResponse

class PrometheusQuery:
    def __init__(self, query: str):
        if not isinstance(query, str) or not query.strip():
            raise ValueError("Query must be a non-empty string.")
        self.query = query

    def sum_by_relabeled_deployment(self):
        """Returns query summed by deployment.

        :param:
        :return: returns self for chaining
        :rtype: PrometheusQuery
        :raises ValueError: If query is not a string or is empty
        """
        self.query = textwrap.dedent(f"""
            sum by (deployment) (
              label_replace(
                {self.query},
                "deployment",
                "$1",
                "pod",
                "(.*)-[^-]+-[^-]+"
              )
            )
        """).strip()
        return self

    def take_ratio_by(self, other):
        """Returns query ratiod by another query.

        :param: another instance of the same class
        :return: returns self for chaining
        :rtype: PrometheusQuery
        :raises ValueError: if other
        """
        if not isinstance(other, PrometheusQuery):
            raise ValueError("other must be instance of PrometheusQuery.")

        self.query = textwrap.dedent(f"""
            {self.query}
            /
            {other.query}
        """).strip()
        return self

class PrometheusAdapter(MetricFetcher):
    def __init__(self, prometheus_url: str, namespace: str):
        self.client = PrometheusClient(prometheus_url)
        self.namespace = namespace

        self.cpu_usage_query = f'irate(container_cpu_usage_seconds_total{{namespace="{namespace}", container=""}}[5m])'
        self.cpu_limit_query = f'kube_pod_container_resource_limits{{job="kube-state-metrics", namespace="{namespace}", resource="cpu"}}'

        self.memory_usage_query = f'container_memory_working_set_bytes{{namespace="{namespace}", container!=""}}'
        self.memory_limit_query = f'kube_pod_container_resource_limits{{job="kube-state-metrics", namespace="{namespace}", resource="memory"}}'

        self.latency_query = f'histogram_quantile(0.95, sum(irate(response_latency_ms_bucket{{namespace="{namespace}", direction="inbound"}}[5m])) by (le, deployment))'

    def get_cpu_usage(self) -> PrometheusResponse:
        query_numerator = PrometheusQuery(self.cpu_usage_query).sum_by_relabeled_deployment()
        query_denominator = PrometheusQuery(self.cpu_limit_query).sum_by_relabeled_deployment()

        query_numerator.take_ratio_by(query_denominator)

        return self.client.query_range(query_numerator.query)

    def get_memory_usage(self) -> PrometheusResponse:
        query_numerator = PrometheusQuery(self.memory_usage_query).sum_by_relabeled_deployment()
        query_denominator = PrometheusQuery(self.memory_limit_query).sum_by_relabeled_deployment()

        query_numerator.take_ratio_by(query_denominator)

        return self.client.query_range(query_numerator.query)

    def get_latency(self) -> PrometheusResponse:
        return self.client.query_range(self.latency_query)

    def get_metrics(self):
        cpu_usage = self.get_cpu_usage()
        memory_usage = self.get_memory_usage()
        latency = self.get_latency()

        cpu_usage_dict = cpu_usage.get_timeseries()
        memory_usage_dict = memory_usage.get_timeseries()
        latency_dict = latency.get_timeseries()

        if not have_same_keys(cpu_usage_dict, memory_usage_dict, latency_dict):
            raise ValueError('Miss match in length of the metrics retrieved.')

        timestamps = cpu_usage.get_timestamps()

        time_series: List[TimeSeries] = []
        for deployment_name in cpu_usage_dict.keys():
            metrics = Metrics(
                cpu_usage=cpu_usage_dict[deployment_name],
                memory_usage=memory_usage_dict[deployment_name],
                network_latency=latency_dict[deployment_name],
            )
            time_series.append(TimeSeries(
                deployment_name=deployment_name,
                timestamps=timestamps,
                metrics=metrics,
            ))

        return time_series


def have_same_keys(*dicts: Dict) -> bool:
    """util function to validate if dicts have same set of keys.

    :param: dicts to compare.
    :return: boolean indicating if the dicts have same set of keys.
    :rtype: bool.
    """
    return len(set.intersection(*map(set, (d.keys() for d in dicts)))) == len(dicts[0])
