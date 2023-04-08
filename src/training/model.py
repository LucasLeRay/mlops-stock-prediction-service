from sklearn.base import BaseEstimator
from sklearn.linear_model import LinearRegression


def get_model() -> BaseEstimator:
    """
    Instantiate a basic model.

    Further works will be dedicated (as with features) to improve model choice
    as well as hyperparameters.
    """
    return LinearRegression()
