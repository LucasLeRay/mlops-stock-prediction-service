from sklearn.metrics import mean_squared_error


def compute_metrics(model, *, X_test, y_test):
    """
    Compute basic metrics.

    As other modeling processes, it should be improved"""

    y_pred = model.predict(X_test)
    return {"m2": mean_squared_error(y_test, y_pred)}
