from unittest.mock import Mock
from datetime import datetime, timedelta
from rca_batch.domain.services import MetricsProcessor
from rca_batch.domain.entities import Metrics, TimeSeries
import pandas as pd
import pandas.testing as pdt

def test_MetricsProcessor_process():
    ts1 = Mock(
        spec=TimeSeries,
        pod_name='pod1',
        timestamps=[datetime(2023, 7, 21, 0, 0, 0), datetime(2023, 7, 21, 0, 0, 15)],
        metrics=Metrics(cpu_usage=[1.0, 1.5], memory_usage=[100, 110], network_latency=[5, 6], tcp_bytes_in=[50, 60], tcp_bytes_out=[70, 80])
    )
    ts2 = Mock(
        spec=TimeSeries,
        pod_name='pod2',
        timestamps=[datetime(2023, 7, 21, 0, 0, 0), datetime(2023, 7, 21, 0, 0, 15)],
        metrics=Metrics(cpu_usage=[2.0, 2.5], memory_usage=[200, 210], network_latency=[7, 8], tcp_bytes_in=[80, 90], tcp_bytes_out=[100, 110])
    )

    df = MetricsProcessor.process([ts1, ts2])

    expected_df = pd.DataFrame({
        'cpu_usage': [1.0, 1.5, 2.0, 2.5],
        'memory_usage': [100, 110, 200, 210],
        'network_latency': [5, 6, 7, 8],
        'tcp_bytes_in': [50, 60, 80, 90],
        'tcp_bytes_out': [70, 80, 100, 110],
    }, index=pd.MultiIndex.from_tuples([
        ('pod1', datetime(2023, 7, 21, 0, 0, 0)),
        ('pod1', datetime(2023, 7, 21, 0, 0, 15)),
        ('pod2', datetime(2023, 7, 21, 0, 0, 0)),
        ('pod2', datetime(2023, 7, 21, 0, 0, 15)),
    ], names=['pod', 'timestamp']))
    print(df.columns, df.index)
    print(expected_df.columns)
    
    pdt.assert_frame_equal(df, expected_df)

