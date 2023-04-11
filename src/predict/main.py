import logging

from src.ingestion.main import SYMBOL
from src.config import config
from src.predict.features import build_online_features

logger = logging.getLogger(__name__)


def main(*, model_name: str, model_version: int = 1):
    """Predict next day closing stock price"""
    from src.store import get_model, pull_historical_targets

    if model_name is None:
        logger.error("No model has been provided for prediction.")
        return

    logger.info("Get historical features...")
    historical_targets = pull_historical_targets()

    logger.info("Compute features...")
    next_day_features = build_online_features(historical_targets)

    logger.info("Get model from registry...")
    with get_model(name=model_name, version=model_version) as model:
        pred = model.predict(next_day_features)[0][0]
        logger.info(
            f"Close price predicted for '{config.symbol}' next day is: {pred}."
        )
