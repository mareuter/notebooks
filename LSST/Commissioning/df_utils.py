from typing import List

import pandas as pd

def convert_timestamps(df: pd.DataFrame, columns: List):
    for column in columns:
        df[column] = pd.to_datetime(df[column] * 1e9, utc=True)
    return df
