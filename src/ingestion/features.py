"""
Build feature set for the model.

For the moment, only historical data is taken into account.
The resulting model will certainly perform poorly.

We can easily imagine different data sources (such as news),
with some of them requiring real time feature engineering.
"""

import pandas as pd

from src.columns import Feature, Index, Stock
from src.config import config


def _lagged_close(close: pd.Series, *, day: int) -> pd.Series:
    return close.shift(day).fillna(method="bfill")


def _rolling_mean_close(close: pd.Series, *, day: int) -> pd.Series:
    return close.rolling(day).mean().fillna(method="bfill")


# NOTE: This function is the offline feature generation. It's different from
# online feature generation (defined in src.predict.features).
# Tests should assert consistency between these two processes.
def build_feature_set(stocks: pd.DataFrame, keep_target=True):
    to_drop = list(Stock)
    if keep_target:
        to_drop.remove(Stock.CLOSE)

    return stocks.assign(
        **{
            Feature.LAGGED_TARGET_DAY.format(day=day):
                _lagged_close(stocks[Stock.CLOSE], day=day)
            for day in config.features.lagged_close_days
        },
        **{
            Feature.ROLLING_MEAN_TARGET_DAY.format(day=day):
                _rolling_mean_close(stocks[Stock.CLOSE], day=day)
            for day in config.features.rolling_mean_close_days
        },
        **{Index.DATETIME: stocks.index}
    ).drop(to_drop, axis=1)
