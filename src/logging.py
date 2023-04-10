import logging


def setup_logging(*, debug=False):
    format = '[%(asctime)s | %(levelname)s]\t%(message)s'
    level = logging.DEBUG if debug else logging.INFO

    logging.basicConfig(format=format, level=level)
