from src.utils import StrEnum


class Stock(StrEnum):
    """Columns contained in the stock set"""
    OPEN = "open"
    HIGH = "high"
    LOW = "low"
    CLOSE = "close"
    ADJUSTED_CLOSE = "adjusted_close"
    VOLUME = "volume"
    DIVIDEND_AMOUNT = "dividend_amount"
    SPLIT_COEF = "split_coef"


class Index(StrEnum):
    """Columns defining index"""
    DATETIME = "datetime"


class Feature(StrEnum):
    """Columns contained in the feature set"""
    LAGGED_TARGET_DAY = "lagged_target_{day}d"
    ROLLING_MEAN_TARGET_DAY = "rolling_mean_target_{day}d"
