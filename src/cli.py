import argparse
from enum import auto

from src.ingestion.main import main as ingestion_pipeline
from src.training.main import main as training_pipeline
from src.utils import StrEnum


class Pipeline(StrEnum):
    ingestion = auto()
    training = auto()
    deploy = auto()  # NOTE: not implemented yet
    predict = auto()  # NOTE: not implemented yet


PIPELINE_TO_FUNCTION = {
    Pipeline.ingestion: ingestion_pipeline,
    Pipeline.training: training_pipeline
}


parser = argparse.ArgumentParser()
parser.add_argument("pipeline", choices=list(Pipeline))


def main(args):
    try:
        PIPELINE_TO_FUNCTION[args.pipeline]()
    except KeyError:
        # TODO: change into a logger
        print(f"Pipeline '{args.pipeline}' is not implemented yet.")


if __name__ == "__main__":
    args = parser.parse_args()
    main(args)
