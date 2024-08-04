#!/usr/bin/env python
# coding: utf-8

import pytest
import pandas as pd
from datetime import datetime
from batch_task3 import prepare_data


def dt(hour, minute, second=0):
    return datetime(2023, 1, 1, hour, minute, second)


def test_prepare_data():
    data = [
        (None, None, dt(1, 1), dt(1, 10)),
        (1, 1, dt(1, 2), dt(1, 10)),
        (1, None, dt(1, 2, 0), dt(1, 2, 59)),
        (3, 4, dt(1, 2, 0), dt(2, 2, 1)),
    ]

    columns = ['PULocationID', 'DOLocationID', 'tpep_pickup_datetime', 'tpep_dropoff_datetime']
    df = pd.DataFrame(data, columns=columns)

    categorical = ['PULocationID', 'DOLocationID']
    actual_df = prepare_data(df, categorical)
    print(actual_df[columns].head())

    expected_data = [
        (str(-1), str(-1), dt(1, 1), dt(1, 10)),
        (str(1), str(1), dt(1, 2), dt(1, 10)),
    ]
    expected_df = pd.DataFrame(expected_data, columns=columns)
    print(expected_df[columns].head())

    assert actual_df[columns].equals(expected_df)==True


if __name__ == '__main__':
    pytest.main()