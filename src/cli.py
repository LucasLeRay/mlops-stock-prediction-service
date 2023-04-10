import argparse
import logging
from enum import auto
from functools import partial

from src.ingestion.main import main as ingestion_pipeline
from src.predict.main import main as predict_pipeline
from src.training.main import main as training_pipeline
from src.utils import StrEnum


class Pipeline(StrEnum):
    ingestion = auto()
    training = auto()
    predict = auto()
    deploy = auto()  # NOTE: not implemented yet


parser = argparse.ArgumentParser()
parser.add_argument("pipeline", choices=list(Pipeline))
parser.add_argument("-mn", "--model-name", default=None)
parser.add_argument("-mv", "--model-version", default=1)

logger = logging.getLogger(__name__)


def main(args):
    pipeline_to_function = {
        Pipeline.ingestion: ingestion_pipeline,
        Pipeline.training: training_pipeline,
        Pipeline.predict: partial(
            predict_pipeline,
            model_name=args.model_name,
            model_version=args.model_version,
        )
    }

    try:
        pipeline = pipeline_to_function[args.pipeline]
    except KeyError:
        logger.error(f"Pipeline '{args.pipeline}' is not implemented yet.")

    pipeline()


if __name__ == "__main__":
    args = parser.parse_args()
    main(args)
