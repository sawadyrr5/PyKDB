# -*- coding: utf-8 -*-
import pandas as pd


def indexing(df: pd.DataFrame, index_cols: list) -> pd.DataFrame:
    df.set_index(keys=index_cols, inplace=True)
    df.sort_index(axis=0, level=index_cols, ascending=True, inplace=True)
    return df
