from datetime import datetime
from typing import List, Dict

class Metrics:
    def __init__(self, 
                 cpu_usage: List[float], 
                 memory_usage: List[float], 
                 network_latency: List[float], 
                 tcp_bytes_in: List[float], 
                 tcp_bytes_out: List[float]):
        self.cpu_usage = cpu_usage
        self.memory_usage = memory_usage
        self.network_latency = network_latency
        self.tcp_bytes_in = tcp_bytes_in
        self.tcp_bytes_out = tcp_bytes_out

    def to_dict(self) -> Dict[str, List[float]]:
        return {
            'cpu_usage': self.cpu_usage,
            'memory_usage': self.memory_usage,
            'network_latency': self.network_latency,
            'tcp_bytes_in': self.tcp_bytes_in,
            'tcp_bytes_out': self.tcp_bytes_out,
        }

class TimeSeries:
    def __init__(self, pod_name: str, timestamps: List[datetime], metrics: Metrics):
        self.pod_name = pod_name
        self.timestamps = timestamps
        self.metrics = metrics
