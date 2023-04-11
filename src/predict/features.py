import numpy as np
import pandas as pd

from src.columns import Index
from src.config import config


def _lagged_close(close: pd.Series, *, day: int) -> pd.Series:
    return close.iloc[day - 1]


def _rolling_mean_close(close: pd.Series, *, day: int) -> pd.Series:
    return close.iloc[:day].mean()


def build_online_features(targets: pd.DataFrame) -> np.array:
    """Build features for next day, from historical targets"""

    targets = (
        targets
        .sort_values(Index.DATETIME, ascending=False)
        .reset_index(drop=True)
    )[config.target]

    return np.array([
        *[
            _lagged_close(targets, day=day)
            for day in config.features.lagged_close_days
        ],
        *[
            _rolling_mean_close(targets, day=day)
            for day in config.features.rolling_mean_close_days
        ]
    ]).reshape(1, -1)
