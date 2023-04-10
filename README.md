1. ingestion pipeline (scheduled 1/d)
- fetch raw stock data
- generate features
- push features in feature store

2. model training pipeline
- pull features/target from feature store
- train model
- push model to model registry

3. predict pipeline
- pull historical data
- generate features for next day
- pull model
- predict next day stock price from model

4. streamlit app (WIP)
- show features
- show prediction
- show difference between target & predictions
