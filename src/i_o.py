from contextlib import contextmanager

import joblib

from src.config import config


@contextmanager
def save_model(model, *, name):
    """Save the model to be push and remove it at the end"""

    # Ideally, the model would be saved in a dedicated folder, like
    # '$ROOT_PATH/artifacts/' or '$ROOT_PATH/_tmp/', but Hopsworks seems
    # to accept only models in the same folder or in parent folders.
    path = (config.directories.project / (name + ".pkl")).resolve()
    joblib.dump(model, path)

    yield str(path)

    path.unlink()
