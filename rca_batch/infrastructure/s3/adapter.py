import boto3
import pandas as pd
from io import BytesIO

from rca_batch.application.ports import DataStore, DataStoreConfig

class S3Adapter(DataStore):
    def __init__(self, config: DataStoreConfig):
        super().__init__(config)
        self.s3 = boto3.resource('s3')

    def save(self, df: pd.DataFrame):
        """save pandas dataframe as parquet in s3 with given key.

        :param df: pandas dataframe to save.
        """
        parquet_buffer = BytesIO()
        df.to_parquet(parquet_buffer)
        self.s3.Object(self.bucket, self.key).put(Body=parquet_buffer.getvalue())
