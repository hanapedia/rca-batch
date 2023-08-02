from rca_batch.domain.entities import TimeSeries
from typing import List
import pandas as pd

class MetricsProcessor:
    @staticmethod
    def process(time_series: List[TimeSeries]) -> pd.DataFrame:
        deployment_dfs = []
        for ts in time_series:
            df = pd.DataFrame(ts.metrics.to_dict())
            df['deployment'] = ts.deployment_name
            df.set_index('deployment', inplace=True)
            df['timestamp'] = ts.timestamps
            df.set_index('timestamp', append=True, inplace=True)
            deployment_dfs.append(df)

        # Concatenate all the dataframes
        full_df = pd.concat(deployment_dfs, axis=0)

        return full_df
