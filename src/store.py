"""
Manage interacts with feature store.
"""

import hopsworks
import pandas as pd

from src.columns import Feature
from src.config import config

HOPSWORKS_PROJECT = hopsworks.login(api_key_value=config.credentials.hopsworks)


def push_features(features: pd.DataFrame):
    feature_store = HOPSWORKS_PROJECT.get_feature_store()

    feature_group = feature_store.get_or_create_feature_group(
        name="stock_price_batch_fg",
        version=1,
        description="Price features",
        primary_key=[Feature.DATETIME],
        event_time=Feature.DATETIME
    )

    feature_group.insert(features, write_options={"wait_for_job": True})
