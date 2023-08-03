from io import BytesIO
import boto3
import pandas as pd
from moto import mock_s3
from rca_batch.application.ports import DataStoreConfig
from rca_batch.infrastructure.s3.adapter import S3Adapter

@mock_s3
def test_s3_save():
    # Create mock S3 bucket
    conn = boto3.resource('s3', region_name='ap-northeast-1')
    conn.create_bucket(Bucket='test',  CreateBucketConfiguration={'LocationConstraint': 'ap-northeast-1'})

    # Create S3Adapter
    s3_adapter = S3Adapter(DataStoreConfig('test', 'test.parquet'))

    # Create DataFrame
    df = pd.DataFrame({
        'A': [1, 2, 3],
        'B': ['a', 'b', 'c']
    })

    # Use S3Adapter to save DataFrame
    s3_adapter.save(df)

    # Check that the file was saved correctly
    saved_data = conn.Object('test', 'test.parquet').get()['Body'].read()

    # Load the saved data into a DataFrame
    loaded_df = pd.read_parquet(BytesIO(saved_data))

    pd.testing.assert_frame_equal(df, loaded_df)

