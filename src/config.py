import os
from pathlib import Path
from types import SimpleNamespace

from dotenv import load_dotenv

from src.columns import Stock

ROOT_PATH = Path(__file__).parents[1]
ENV_PATH = ROOT_PATH / ".env"


class _Config:
    def __init__(self):
        # If env path doesn't exist, it's supposed that env is injected
        # (e.g.: by CI)
        if ENV_PATH.exists():
            load_dotenv(ENV_PATH)

        self.directories = SimpleNamespace(
            project=ROOT_PATH
        )
        self.credentials = SimpleNamespace(
            alpha_vantage=os.environ["ALPHA_VANTAGE_API_KEY"],
            hopsworks=os.environ["HOPSWORKS_API_KEY"]
        )
        self.features = SimpleNamespace(
            lagged_close_days=[1, 2, 3, 4, 5, 6, 7, 10, 20, 30, 50],
            rolling_mean_close_days=[2, 3, 4, 5, 6, 7, 10, 20, 30, 50]
        )
        self.target = Stock.CLOSE  # we try to predict close price of the day.
        self.test_size = .2


config = _Config()
