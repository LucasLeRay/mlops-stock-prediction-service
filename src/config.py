import os
from pathlib import Path
from types import SimpleNamespace

from dotenv import load_dotenv

from src.columns import Stock
from src.exceptions import EnvNotFound

ROOT_PATH = Path(__file__).parents[1]
ENV_PATH = ROOT_PATH / ".env"


class _Config:
    def __init__(self):
        if not ENV_PATH.exists():
            raise EnvNotFound(f"Environment file {ENV_PATH} not found.")
        load_dotenv(ENV_PATH)

        # TODO: create a dedicated singleton for artifacts, and a dedicated
        # module for filenames.
        self.artifacts_dir = ROOT_PATH / "artifacts"
        self.artifacts_dir.mkdir(exist_ok=True, parents=True)

        self.credentials = SimpleNamespace(
            alpha_vantage=os.environ["ALPHA_VANTAGE_API_KEY"],
            hopsworks=os.environ["HOPSWORKS_API_KEY"]
        )
        self.features = SimpleNamespace(
            lagged_close_days=[1, 2, 3, 4, 5, 6, 7],
            rolling_mean_close_days=[1, 2, 3, 4, 5, 6, 7]
        )
        self.target = Stock.CLOSE  # we try to predict close price of the day.
        self.test_size = .2


config = _Config()
