from dataclasses import dataclass
from time import time
from typing import Dict, List, Tuple, Union
import requests

@dataclass
class PrometheusResult:
    metric: Dict[str,str]
    values: List[Tuple[float, str]]

@dataclass
class PrometheusData:
    result_type: str
    result: List[PrometheusResult]

@dataclass
class PrometheusResponse:
    status: str
    data: PrometheusData

    @staticmethod
    def from_dict(obj: Dict) -> 'PrometheusResponse':
        if obj['status'] == 'error':
            raise ValueError(f'Prometheus query error: {obj["error"]}')

        data_obj = obj['data']
        result_type = data_obj['resultType']
        result = [PrometheusResult(
                        result_obj['metric'],
                        [tuple(value) for value in result_obj['values']],
                    ) for result_obj in data_obj['result']]

        return PrometheusResponse(
            status = obj['status'],
            data = PrometheusData(
                result_type,
                result,
            )
        )

    def _validate(self):
        if len(self.data.result) < 1:
            raise ValueError('PrometheusResponse.data.result is empty.')

        if len(self.data.result[0].values) < 1:
            raise ValueError('PrometheusResponse.data.result[0].values is empty.')

        if len(self.data.result[0].values[0]) < 2:
            raise ValueError('PrometheusResponse.data.result[0].values tuple does not have sufficient length.')

    def get_timestamps(self) -> List[float]:
        """get the list of timestamps.
        returns singles list of timestamps, assuming that all the metrics have same timestamps.

        :rtype: List[float]
        """
        self._validate()

        return [value[0] for value in self.data.result[0].values]

    def get_timeseries(self) -> Dict[str, List[float]]:
        """get the dict of timeseries indexed by deployment_name.
        converts the metrics value from string to float.

        :rtype: Dict[str, List[float]]
        """
        self._validate()

        result_dict: Dict[str, List[float]] = {}
        for result in self.data.result:
            if deployment_name := result.metric.get('deployment'):
                result_dict[deployment_name] = [float(value[1]) for value in result.values]
            else:
                raise ValueError('metric object does not have key by the name "deployment".')

        return result_dict

class PrometheusClient:
    def __init__(self, base_url):
        self.base_url = base_url

    def query_range(self, query, end=time(), minutes=5, step='15s') -> PrometheusResponse:
        # Calculate start and end times
        start = end - minutes * 60

        response = requests.get(
            f"{self.base_url}/api/v1/query_range",
            params={
                "query": query,
                "start": start,
                "end": end,
                "step": step
            }
        )

        obj = response.json()
        prometheus_response = PrometheusResponse.from_dict(obj)

        return prometheus_response
