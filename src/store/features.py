import pandas as pd

from src.columns import Index
from src.config import config
from src.exceptions import FeatureGroupNotFound
from src.store.main import HOPSWORKS_PROJECT

FEATURE_STORE = HOPSWORKS_PROJECT.get_feature_store()

# Unique feature group (for the moment)
FEATURE_GROUP = "stock_price_batch_fg"
FEATURE_VIEW = "stock_price_batch_fv"


def push_features(features: pd.DataFrame):
    """Push features into store"""
    # Note that, currently, new features are not automatically added.
    # If new features need to be added to the group, the user have to manually
    # delete the feature group, and recreate it through this pipeline.
    feature_group = FEATURE_STORE.get_or_create_feature_group(
        name=FEATURE_GROUP,
        version=1,
        description="Price features",
        primary_key=[Index.DATETIME],
        event_time=Index.DATETIME
    )
    feature_group.insert(features, write_options={"wait_for_job": True})


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


def get_feature_view():
    """Get feature view from feature store"""
    query = _get_feature_group().select_except([Index.DATETIME])

    return _get_or_create_feature_view(query=query)


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


def pull_stock_features(features):
    """Pull features from stock group"""
    return _get_feature_group().select(features).read()
