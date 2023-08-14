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
        'deployment1-cpu_usage': [1.0, 1.5],
        'deployment1-memory_usage': [100, 110],
        'deployment1-network_latency': [5, 6],
        'deployment2-cpu_usage': [2.0, 2.5],
        'deployment2-memory_usage': [200, 210],
        'deployment2-network_latency': [7, 8],
    }, index=pd.Index([timestamp1, timestamp2], name='timestamp'))

    pdt.assert_frame_equal(df, expected_df)

