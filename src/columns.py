from enum import auto

from src.utils import StrEnum


class Stock(StrEnum):
    """Columns contained in the stock set"""
    OPEN = auto()
    HIGH = auto()
    LOW = auto()
    CLOSE = auto()
    ADJUSTED_CLOSE = auto()
    VOLUME = auto()
    DIVIDEND_AMOUNT = auto()
    SPLIT_COEF = auto()


class Feature(StrEnum):
    """Columns contained in the feature set"""
    DATETIME = "datetime"  # TODO: put this elsewhere, it's not a feature
    LAGGED_TARGET_DAY = "lagged_target_{day}d"
    ROLLING_MEAN_TARGET_DAY = "rolling_mean_target_{day}d"
