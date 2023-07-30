from .entities import TimeSeries
from typing import List
import pandas as pd

class MetricsProcessor:
    @staticmethod
    def process(time_series: List[TimeSeries]) -> pd.DataFrame:
        pod_dfs = []
        for ts in time_series:
            df = pd.DataFrame(ts.metrics.to_dict())
            df['pod'] = ts.pod_name
            df.set_index('pod', inplace=True)
            df['timestamp'] = ts.timestamps
            df.set_index('timestamp', append=True, inplace=True)
            pod_dfs.append(df)

        # Concatenate all the dataframes
        full_df = pd.concat(pod_dfs, axis=0)

        return full_df
