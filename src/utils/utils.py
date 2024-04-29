import pandas as pd

def expand_time_series(df, key_columns, time_col, freq="W-MON"):
    """for each of the groups in the df grouped by key columns,
    expand the time series based on the min and max entries in the time col"""
    if df.empty:
        return df

    def ff(x):
        res = pd.date_range(x.min(), x.max(), freq=freq).to_series()
        res.index.name = "TMP"
        return res

    res_df = (
        df[key_columns + [time_col]]
        .groupby(key_columns)[time_col]
        .apply(ff)
        .reset_index()
        .drop(columns="TMP")
    )

    res_df = res_df.merge(df, how="left", on=key_columns + [time_col])
    return res_df