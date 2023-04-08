1. ingestion script (scheduled 1/h)
- fetch raw data
- feature engineering
- push features in feature store

2. model training script
- fetch features/target from feature store
- train model
- push model to model registry

3. streamlit app
- fetch model from model registry
- predict
