import pytest

from rca_batch.infrastructure.prometheus.client import PrometheusResponse, PrometheusData, PrometheusResult

def test_from_dict_success():
    test_input = {
        "status": "success",
        "data": {
            "resultType": "matrix",
            "result": [
                {
                    "metric": {"deployment": "chain1"},
                    "values": [[1690900209.23, '16.24'], [1690900224.23, '16.24'], [1690900239.23, '16.80']]
                }
            ]
        }
    }
    result = PrometheusResponse.from_dict(test_input)
    assert result.status == 'success'
    assert result.data.result_type == 'matrix'
    assert isinstance(result.data.result[0], PrometheusResult)

def test_from_dict_error():
    test_input = {
        "status": "error",
        "error": "Test Error Message",
        "data": None
    }
    with pytest.raises(ValueError) as e:
        PrometheusResponse.from_dict(test_input)
    assert str(e.value) == 'Prometheus query error: Test Error Message'

def test_get_timestamps():
    res = PrometheusResponse(
        status='success',
        data=PrometheusData(
            result_type='matrix',
            result=[
                PrometheusResult(
                    metric={"deployment": "chain1"},
                    values=[(1690900209.23, '16.24'), (1690900224.23, '16.24'), (1690900239.23, '16.80')]
                )
            ]
        )
    )
    timestamps = res.get_timestamps()
    assert timestamps == [1690900209.23, 1690900224.23, 1690900239.23]

def test_get_timeseries():
    res = PrometheusResponse(
        status='success',
        data=PrometheusData(
            result_type='matrix',
            result=[
                PrometheusResult(
                    metric={"deployment": "chain1"},
                    values=[(1690900209.23, '16.24'), (1690900224.23, '16.24'), (1690900239.23, '16.80')]
                )
            ]
        )
    )
    timeseries = res.get_timeseries()
    assert timeseries == {"chain1": [16.24, 16.24, 16.80]}

def test_get_timeseries_no_deployment():
    res = PrometheusResponse(
        status='success',
        data=PrometheusData(
            result_type='matrix',
            result=[
                PrometheusResult(
                    metric={},
                    values=[(1690900209.23, '16.24'), (1690900224.23, '16.24'), (1690900239.23, '16.80')]
                )
            ]
        )
    )
    with pytest.raises(ValueError) as e:
        timeseries = res.get_timeseries()
    assert str(e.value) == 'metric object does not have key by the name "deployment".'
