from time import time
from dataclasses import dataclass
import os
from dotenv import load_dotenv

from rca_batch.application.ports import DataStoreConfig, MetricFetcherConfig

@dataclass
class Config:
    metric_fetcher_config: MetricFetcherConfig
    data_store_config: DataStoreConfig

def load_config_from_env() -> Config:
    load_dotenv()  # take environment variables from .env.

    source_url = os.getenv('METRICS_QUERY_URL', 'http://localhost:9090')
    end_time = parse_float_env('END_TIME', time())
    duration = parse_int_env('DURATION', 300)
    step = parse_int_env('STEP', 15)
    bucket = os.getenv('S3_BUCKET', './data')
    key = os.getenv('S3_KEY', 'test')

    return Config(
        metric_fetcher_config=MetricFetcherConfig(
            source_url=source_url,
            end_time=end_time,
            duration=duration,
            step=step,
        ),
        data_store_config=DataStoreConfig(
            bucket=bucket,
            key=key,
        )
    )

def parse_float_env(key: str, default: float):
    env: float
    env_str = os.getenv(key)
    if (env_str == None):
        env = default
    elif env_float := float(env_str):
        env = env_float
    else:
        env = default
    return env

def parse_int_env(key: str, default: int):
    env: int
    env_str = os.getenv(key)
    if (env_str == None):
        env = default
    elif env_int := int(env_str):
        env = env_int
    else:
        env = default
    return env
