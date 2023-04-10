import pandas as pd

from src.ingestion.features import build_feature_set
from src.ingestion.postprocess import postprocess_stock_data
from src.ingestion.stock import fetch_stock_data

# For the moment, only one symbol is used in this project.
# In the future, we might train different models for different symbols.
SYMBOL = "AAPL"


def get_stock_data() -> pd.DataFrame:
    return (
        fetch_stock_data(symbol=SYMBOL, interval="60min")
        .pipe(postprocess_stock_data)
    )


def main():
    # Store is imported here to avoid unnecessary compute at import time
    from src.store import push_features

    get_stock_data().pipe(build_feature_set).pipe(push_features)


if __name__ == "__main__":
    main()
