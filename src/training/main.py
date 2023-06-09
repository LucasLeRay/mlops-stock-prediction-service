import logging

from src.config import config
from src.training.metrics import compute_metrics
from src.training.model import get_model

logger = logging.getLogger(__name__)


def main():
    # Store is imported here to avoid unnecessary compute at import time
    from src.store.features import get_feature_view, split_feature_sets
    from src.store.model import push_model

    logger.info("Get model...")
    model = get_model()

    logger.info("Pull features...")
    feature_view = get_feature_view()

    logger.info("Split train/test sets...")
    X_train, X_test, y_train, y_test = split_feature_sets(feature_view)

    logger.info("Fit model...")
    model.fit(X_train, y_train)

    logger.info("Compute metrics...")
    metrics = compute_metrics(model, X_test=X_test, y_test=y_test)
    logger.info(f"Metrics for new model is {metrics}")

    logger.info("Pushing model to registry...")
    push_model(model, metrics=metrics, name=config.symbol)
    logger.info("New model is pushed.")
