import pandas as pd

from src.columns import Stock

COLUMNS_MAPPING = {
    "1. open": Stock.OPEN,
    "2. high": Stock.HIGH,
    "3. low": Stock.LOW,
    "4. close": Stock.CLOSE,
    "5. adjusted close": Stock.ADJUSTED_CLOSE,
    "6. volume": Stock.VOLUME,
    "7. dividend amount": Stock.DIVIDEND_AMOUNT,
    "8. split coefficient": Stock.SPLIT_COEF,
}


def postprocess_stock_data(stocks: pd.DataFrame) -> pd.DataFrame:
    return stocks.rename(columns=COLUMNS_MAPPING).sort_index()
