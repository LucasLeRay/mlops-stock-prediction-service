from ingestion.stock import fetch_stock_data

# For the moment, only one symbol is used in this project.
# In the future, we might train different models for different symbols.
SYMBOL = "APPL"


def main():
    fetch_stock_data(symbol=SYMBOL, interval="60min")


if __name__ == "__main__":
    main()
