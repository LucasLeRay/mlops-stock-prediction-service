import hopsworks

from src.config import config

HOPSWORKS_PROJECT = hopsworks.login(api_key_value=config.credentials.hopsworks)
