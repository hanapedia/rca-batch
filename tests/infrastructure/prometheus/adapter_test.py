import unittest.mock as mock
from rca_batch.domain.entities import TimeSeries, Metrics
from rca_batch.infrastructure.prometheus.client import PrometheusResponse, PrometheusResult, PrometheusData
from rca_batch.infrastructure.prometheus.adapter import PrometheusAdapter

# The following data will be used for mocking purposes
dummy_prometheus_response = PrometheusResponse(
    status='success',
    data=PrometheusData(
        result_type='matrix',
        result=[
            PrometheusResult(
                metric={"deployment": "chain1"},
                values=[(1690900209.23, '16.24'), (1690900224.23, '16.24'), (1690900239.23, '16.80')]
            ),
            PrometheusResult(
                metric={"deployment": "chain2"},
                values=[(1690900209.23, '16.24'), (1690900224.23, '16.24'), (1690900239.23, '16.80')]
            ),
        ]
    )
)

def test_get_metrics():
    instance = PrometheusAdapter("http://localhost:9090", "the-bench")

    with mock.patch.object(instance, 'get_cpu_usage', return_value=dummy_prometheus_response) as cpu_mock, \
         mock.patch.object(instance, 'get_memory_usage', return_value=dummy_prometheus_response) as mem_mock, \
         mock.patch.object(instance, 'get_latency', return_value=dummy_prometheus_response) as lat_mock:

        result = instance.get_metrics()

        # Assert the mock methods were called once
        cpu_mock.assert_called_once()
        mem_mock.assert_called_once()
        lat_mock.assert_called_once()

        # Validate the results
        assert len(result) == 2
        assert isinstance(result[0], TimeSeries)
        assert result[0].deployment_name == 'chain1'
        assert result[0].timestamps == [1690900209.23, 1690900224.23, 1690900239.23]
        assert isinstance(result[0].metrics, Metrics)
        assert result[0].metrics.cpu_usage == [16.24, 16.24, 16.80]
        assert result[0].metrics.memory_usage == [16.24, 16.24, 16.80]
        assert result[0].metrics.network_latency == [16.24, 16.24, 16.80]

        assert isinstance(result[1], TimeSeries)
        assert result[1].deployment_name == 'chain2'
        assert result[1].timestamps == [1690900209.23, 1690900224.23, 1690900239.23]
        assert isinstance(result[1].metrics, Metrics)
        assert result[1].metrics.cpu_usage == [16.24, 16.24, 16.80]
        assert result[1].metrics.memory_usage == [16.24, 16.24, 16.80]
        assert result[1].metrics.network_latency == [16.24, 16.24, 16.80]
