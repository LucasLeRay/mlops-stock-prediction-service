import logging

import pandas as pd

from src.config import config
from src.ingestion.features import build_feature_set
from src.ingestion.postprocess import postprocess_stock_data
from src.ingestion.stock import fetch_stock_data

logger = logging.getLogger(__name__)


def get_stock_data() -> pd.DataFrame:
    return (
        fetch_stock_data(symbol=config.symbol, interval="60min")
        .pipe(postprocess_stock_data)
    )


def main():
    # Store is imported here to avoid unnecessary compute at import time
    from src.store.features import push_features

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
