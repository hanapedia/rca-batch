from typing import List
import pandas as pd

from rca_batch.domain.entities import TimeSeries

class MetricsProcessor:
    @staticmethod
    def process(time_series: List[TimeSeries]) -> pd.DataFrame:
        deployment_dfs = []
        for ts in time_series:
            df = pd.DataFrame(ts.metrics.to_dict())
            df['timestamp'] = ts.timestamps
            df.set_index('timestamp', inplace=True)
            df.columns = [f'{ts.deployment_name}-{col}' for col in df.columns]
            deployment_dfs.append(df)

        # Join all the dataframes
        full_df = deployment_dfs[0].join(deployment_dfs[1:], how='outer')

        return full_df
