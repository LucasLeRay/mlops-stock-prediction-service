from datetime import datetime

import joblib

from src.config import config


def save_model(model):
    filename = str(datetime.now()) + ".pkl"
    path = config.artifact_dir / filename

    joblib.dump(model, config.artifact_dir / filename)
    return path
