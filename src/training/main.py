from src.store import pull_features, push_model, split_feature_sets
from src.training.metrics import compute_metrics
from src.training.model import get_model


def main():
    model = get_model()
    feature_view = pull_features()
    X_train, X_test, y_train, y_test = split_feature_sets(feature_view)

    model.fit(X_train, y_train)
    metrics = compute_metrics(model, X_test=X_test, y_test=y_test)
    # TODO: log metrics

    push_model(model, metrics=metrics)


if __name__ == "__main__":
    main()
