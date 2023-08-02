from datetime import datetime
from typing import List, Dict

class Metrics:
    def __init__(self,
                 cpu_usage: List[float],
                 memory_usage: List[float],
                 network_latency: List[float],
                 ):
        self.cpu_usage = cpu_usage
        self.memory_usage = memory_usage
        self.network_latency = network_latency

    def to_dict(self) -> Dict[str, List[float]]:
        return {
            'cpu_usage': self.cpu_usage,
            'memory_usage': self.memory_usage,
            'network_latency': self.network_latency,
        }

class TimeSeries:
    def __init__(self, deployment_name: str, timestamps: List[float], metrics: Metrics):
        self.deployment_name = deployment_name
        self.timestamps = timestamps
        self.metrics = metrics
