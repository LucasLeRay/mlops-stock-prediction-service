"""
Manage interacts with feature store.
"""

from datetime import datetime

import hopsworks
import pandas as pd

from src.columns import Feature
from src.config import config
from src.exceptions import FeatureGroupNotFound
from src.i_o import save_model

# TODO: Add '__all__' for explicit 'exports'
# TODO: split this module into a package
# TODO: import types on type checking

HOPSWORKS_PROJECT = hopsworks.login(api_key_value=config.credentials.hopsworks)
FEATURE_STORE = HOPSWORKS_PROJECT.get_feature_store()
MODEL_REGISTRY = HOPSWORKS_PROJECT.get_model_registry()

# Unique feature store (for the moment)
FEATURE_GROUP = "stock_price_batch_fg"
FEATURE_VIEW = "stock_price_batch_fv"


def push_features(features: pd.DataFrame):
    feature_group = FEATURE_STORE.get_or_create_feature_group(
        name=FEATURE_GROUP,
        version=1,
        description="Price features",
        primary_key=[Feature.DATETIME],
        event_time=Feature.DATETIME
    )

    feature_group.insert(features, write_options={"wait_for_job": True})


def _get_feature_group():
    try:
        return FEATURE_STORE.get_feature_group(FEATURE_GROUP, version=1)
    except:  # noqa: E722
        # TODO: except on precise exception
        raise FeatureGroupNotFound(
            f"Feature group {FEATURE_GROUP} has not been found on Hopsworks. "
            "Ingestion pipeline needs to run at least once to push features."
        )


def _get_or_create_feature_view(*, query):
    try:
        return FEATURE_STORE.get_feature_view(name=FEATURE_VIEW, version=1)
    except:  # noqa: E722
        # TODO: except on precise exception
        return FEATURE_STORE.create_feature_view(
            name=FEATURE_VIEW,
            version=1,
            query=query,
            labels=[config.target],
        )


def pull_features():
    """Get feature view from feature store"""
    query = _get_feature_group().select_except([Feature.DATETIME])

    return _get_or_create_feature_view(query=query)


def split_feature_sets(feature_view):
    """Create and return train test split"""
    td_version, _ = feature_view.create_train_test_split(
        description='transactions fraud batch training dataset',
        data_format='csv',
        test_size=config.test_size,
        write_options={'wait_for_job': True},
        coalesce=True,
    )

    return feature_view.get_train_test_split(td_version)


def push_model(model, *, metrics):
    model_name = str(datetime.now()) + ".pkl"
    model_path = save_model(model, name=model_name)
    (
        MODEL_REGISTRY.sklearn
        .create_model(model_path, metrics=metrics)
        .save(model_name)
    )
