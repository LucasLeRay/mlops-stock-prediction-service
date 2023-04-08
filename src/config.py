import os
from pathlib import Path
from types import SimpleNamespace

from dotenv import load_dotenv

from src.exceptions import EnvNotFound

ENV_PATH = Path(__file__).parents[1] / ".env"


class _Config:
    def __init__(self):
        if not ENV_PATH.exists():
            raise EnvNotFound(f"Environment file {ENV_PATH} not found.")
        load_dotenv(ENV_PATH)

        self.credentials = SimpleNamespace(
            alpha_vantage=os.environ["ALPHA_VANTAGE_API_KEY"]
        )


config = _Config()
