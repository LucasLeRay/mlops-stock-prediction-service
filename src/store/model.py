from contextlib import contextmanager
from pathlib import Path

import joblib

from src.i_o import save_model
from src.store.main import HOPSWORKS_PROJECT

MODEL_REGISTRY = HOPSWORKS_PROJECT.get_model_registry()


def push_model(model, *, metrics: dict, name: str):
    """Push model to registry"""
    # TODO: give input example, as well as schemas
    with save_model(model, name=name) as model_path:
        (
            MODEL_REGISTRY.sklearn
            .create_model(name, metrics=metrics)
            .save(model_path)
        )


@contextmanager
def pull_model(*, name: str, version: int):
    """Pull model from registry"""
    # NOTE: One alternative is to get the best model using
    # ModelRegistry.get_best_model. It's something to investigate.
    hs_model = MODEL_REGISTRY.get_model(name, version=version)

    model_path = Path(hs_model.download()) / (name + ".pkl")
    yield joblib.load(model_path)

    model_path.unlink()
