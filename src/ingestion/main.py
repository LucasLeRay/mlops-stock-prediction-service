import logging

import pandas as pd

from src.ingestion.features import build_feature_set
from src.ingestion.postprocess import postprocess_stock_data
from src.ingestion.stock import fetch_stock_data

logger = logging.getLogger(__name__)

# For the moment, only one symbol is used in this project.
# In the future, we might train different models for different symbols.
# TODO: define it elswehere, as other pipelines depends on it.
SYMBOL = "AAPL"


def get_stock_data() -> pd.DataFrame:
    return (
        fetch_stock_data(symbol=SYMBOL, interval="60min")
        .pipe(postprocess_stock_data)
    )


def main():
    # Store is imported here to avoid unnecessary compute at import time
    from src.store import push_features

    # Using the logger prevents me from piping dataframes between functions.
    # I could decorate functions that needs logging and add the logging message
    # directly in the decorator. To be investigated.
    logger.info("Get stock data...")
    stocks = get_stock_data()

    logger.info("Build feature set...")
    features = build_feature_set(stocks)

    logger.info("Push features to store...")
    push_features(features)
    logger.info("Features are pushed to store.")
