from enum import auto

from src.utils import StrEnum


# For the moment, only one symbol is used in this project.
# In the future, we might train different models for different symbols.
class Symbol(StrEnum):
    """Stock symbols we want to predict"""
    AAPL = auto()
