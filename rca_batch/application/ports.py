from abc import ABC, abstractmethod
from typing import List
import pandas as pd
from rca_batch.domain.entities import TimeSeries

class PodFetcher(ABC):
    @abstractmethod
    def get_pods(self) -> List[str]:
        pass

class MetricFetcher(ABC):
    @abstractmethod
    def get_metrics(self, pods: List[str]) -> List[TimeSeries]:
        pass

class DataStore(ABC):
    @abstractmethod
    def save(self, df: pd.DataFrame):
        pass

