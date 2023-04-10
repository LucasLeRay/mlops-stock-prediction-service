import pandas as pd
import requests

from src.config import config
from src.utils import StrEnum

ALPHA_VANTAGE_BASE_URL = "https://www.alphavantage.co/"
ALPHA_VANTAGE_API_URL = (
    ALPHA_VANTAGE_BASE_URL
    + "query?"
    + "function={function}"
    + "&symbol={symbol}"
    + "&interval={interval}"
    + "&outputsize=full"
    + f"&apikey={config.credentials.alpha_vantage}"
)


class StockFunction(StrEnum):
    """
    Values are defined by Alpha Vantage API
    (https://www.alphavantage.co/documentation/)
    """
    INTRA_DAY = "TIME_SERIES_INTRADAY"
    DAILY = "TIME_SERIES_DAILY_ADJUSTED"


def fetch_stock_data(
    function: str = StockFunction.DAILY, *, symbol: str, interval: str
) -> pd.DataFrame:
    url = ALPHA_VANTAGE_API_URL.format(
        function=function,
        symbol=symbol,
        interval=interval
    )

    # TODO: send an email notification if this query crashes
    res = requests.get(url).json()

    # Metadata is ignored, but might be of interest in the future.
    data = res[list(res.keys())[1]]

    stocks = pd.DataFrame(data).T
    stocks.index = pd.to_datetime(stocks.index)
    return stocks
