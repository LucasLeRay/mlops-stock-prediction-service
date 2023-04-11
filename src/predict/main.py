import logging

from src.columns import Index
from src.config import config
from src.predict.features import build_online_features

logger = logging.getLogger(__name__)


def main(*, model_name: str, model_version: int = 1):
    """Predict next day closing stock price"""

    # Store is imported here to avoid unnecessary compute at import time
    from src.store.features import pull_stock_features
    from src.store.model import pull_model

    if model_name is None:
        logger.error("No model has been provided for prediction.")
        return

    logger.info("Get historical features...")
    historical_targets = pull_stock_features([config.target, Index.DATETIME])

    logger.info("Compute features...")
    next_day_features = build_online_features(historical_targets)

    logger.info("Get model from registry...")
    with pull_model(name=model_name, version=model_version) as model:
        pred = model.predict(next_day_features)[0][0]
        logger.info(
            f"Close price predicted for '{config.symbol}' next day is: {pred}."
        )
