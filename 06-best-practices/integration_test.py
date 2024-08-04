#!/usr/bin/env python
# coding: utf-8

import os
import pandas as pd
from datetime import datetime

# Define the S3 endpoint and bucket for localstack
S3_ENDPOINT_URL = os.getenv('S3_ENDPOINT_URL', 'http://localhost:4566')
S3_BUCKET = 'nyc-duration'
S3_INPUT_PATH = 'in/2023-01.parquet'

# Define the test DataFrame
def dt(hour, minute, second=0):
    return datetime(2023, 1, 1, hour, minute, second)

data = [
    (None, None, dt(1, 1), dt(1, 10)),
    (1, 1, dt(1, 2), dt(1, 10)),
    (1, None, dt(1, 2, 0), dt(1, 2, 59)),
    (3, 4, dt(1, 2, 0), dt(2, 2, 1)),
]

columns = ['PULocationID', 'DOLocationID', 'tpep_pickup_datetime', 'tpep_dropoff_datetime']
df_input = pd.DataFrame(data, columns=columns)

# Define storage options for S3
options = {
    'client_kwargs': {
        'endpoint_url': S3_ENDPOINT_URL
    }
}

# Save the DataFrame to S3 as a Parquet file
input_file = f's3://{S3_BUCKET}/{S3_INPUT_PATH}'
df_input.to_parquet(
    input_file,
    engine='pyarrow',
    compression=None,
    index=False,
    storage_options=options
)

print(f'DataFrame saved to {input_file}')
