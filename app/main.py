import datetime

import streamlit as st

from src.columns import Feature, Index
from src.config import config
from src.store.features import pull_stock_features

# Get features since 1 month ago
CUTOFF = (datetime.datetime.now() - datetime.timedelta(days=30))


@st.cache_data
def load_historical():
    """Get historical features since last month."""
    rolling_means = [
        Feature.ROLLING_MEAN_TARGET_DAY.format(day=day)
        for day in config.features.rolling_mean_close_days
    ]

    historical = pull_stock_features([
        Index.DATETIME, config.target, *rolling_means
    ], since=CUTOFF)

    return historical.sort_values([Index.DATETIME])


historical = load_historical()
features = list(set(historical.columns) - set(Index.DATETIME))

st.line_chart(
    historical,
    y=features,
    x=Index.DATETIME
)
