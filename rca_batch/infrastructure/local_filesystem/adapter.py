import os
import pandas as pd

from rca_batch.application.ports import DataStore, DataStoreConfig

class LocalFileSystemAdapter(DataStore):
    def __init__(self, config: DataStoreConfig):
        super().__init__(config)
        os.makedirs(self.bucket, exist_ok=True)

    def save(self, df: pd.DataFrame):
        file_path = os.path.join(self.bucket, f"{self.key}.csv")
        df.to_csv(file_path, index=True)
