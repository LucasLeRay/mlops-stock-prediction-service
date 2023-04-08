import joblib

from src.config import config


def save_model(model, *, filename):
    path = config.artifact_dir / filename

    joblib.dump(model, path)
    return path
