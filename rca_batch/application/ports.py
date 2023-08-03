from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List
import pandas as pd

from rca_batch.domain.entities import TimeSeries

@dataclass
class MetricFetcherConfig:
    """Config that must be passed to any class that implement MetricFetcher.
    Attributes:
    -----------
    source_url: str
        The base URL of the source from which to fetch metrics.
    end_time: float
        The end time of the time range for which to fetch metrics, in seconds since the epoch.
    duration: int
        The duration of the time range for which to fetch metrics, in seconds.
    step: int
        The step size for fetching metrics, in seconds.
    """
    source_url: str
    end_time: float
    duration: int
    step: int

class MetricFetcher(ABC):
    def __init__(self, config: MetricFetcherConfig):
        self.source_url = config.source_url
        self.end_time = config.end_time
        self.duration = config.duration
        self.step = config.step

    @abstractmethod
    def get_metrics(self) -> List[TimeSeries]:
        pass

@dataclass
class DataStoreConfig:
    """Config that must be passed to any class that implement DataStore.
    Attributes:
    -----------
    bucket: str
        Name of the bucket or directory to store metrics file.
    key: str
        Name of the key or file to store metrics as.
    """
    bucket: str
    key: str

class DataStore(ABC):
    def __init__(self, config: DataStoreConfig):
        self.bucket = config.bucket
        self.key = config.key

    @abstractmethod
    def save(self, df: pd.DataFrame):
        pass

