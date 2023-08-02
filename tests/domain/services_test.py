from unittest.mock import Mock
from datetime import datetime
from rca_batch.domain.services import MetricsProcessor
from rca_batch.domain.entities import Metrics, TimeSeries
import pandas as pd
import pandas.testing as pdt

def test_MetricsProcessor_process():
    timestamp1 = datetime(2023, 7, 21, 0, 0, 0).timestamp()
    timestamp2 = datetime(2023, 7, 21, 0, 0, 15).timestamp()

    ts1 = Mock(
        spec=TimeSeries,
        deployment_name='deployment1',
        timestamps=[timestamp1, timestamp2],
        metrics=Metrics(cpu_usage=[1.0, 1.5], memory_usage=[100, 110], network_latency=[5, 6])
    )
    ts2 = Mock(
        spec=TimeSeries,
        deployment_name='deployment2',
        timestamps=[timestamp1, timestamp2],
        metrics=Metrics(cpu_usage=[2.0, 2.5], memory_usage=[200, 210], network_latency=[7, 8])
    )

    df = MetricsProcessor.process([ts1, ts2])

    expected_df = pd.DataFrame({
        'cpu_usage': [1.0, 1.5, 2.0, 2.5],
        'memory_usage': [100, 110, 200, 210],
        'network_latency': [5, 6, 7, 8],
    }, index=pd.MultiIndex.from_tuples([
        ('deployment1', timestamp1),
        ('deployment1', timestamp2),
        ('deployment2', timestamp1),
        ('deployment2', timestamp2),
    ], names=['deployment', 'timestamp']))
    print(df.columns, df.index)
    print(expected_df.columns)

    pdt.assert_frame_equal(df, expected_df)

