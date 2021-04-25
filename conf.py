# -*- coding: utf-8 -*-

__doc__ = """Configuration file
"""

import logging
import sys

import coloredlogs

ENCODING = "utf-8"
TEX_FILE = ".tex"


def get_logger(
    name: str
) -> logging.Logger:
    """Get the logger.

    Parameters
    ----------
    name : str
        The name of the module to be logged.

    Returns
    -------
    logging.Logger
        The logger object.

    """
    logger = logging.getLogger(name)

    logger.setLevel(logging.DEBUG)

    stream = logging.StreamHandler(stream=sys.stdout)
    stream.setLevel(logging.DEBUG)
    stream_formatter = logging.Formatter(
        "%(asctime)s:%(levelname)s:%(message)s")
    stream.setFormatter(stream_formatter)
    logger.addHandler(stream)

    coloredlogs.install(level="DEBUG", logger=logger)
    return logger
