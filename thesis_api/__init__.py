# -*- coding: utf-8 -*-

__doc__ = """The API interface to the LaTeX project.

Note that this interface uses the Numpy style python docstrings.

"""

import logging
import sys

__version__ = "0.2.1"


##################

LATEX_CONFIG_DIC = {
    "arraystretch": 1.8,  # scaling of tables
    "si_round_precision": 3,  # round precision of siunitx
    "encoding": "utf-8",  # the encoding of the LaTeX files
    "tex_file": ".tex",  # the file ending of LaTeX files
    "scrbook_width": 14.89787,  # the width of the scrbook class in [cm]
    # This is the line width of the LaTeX class scrbook in [cm], which my be useful for tables, etc.
    # The line length can be obtained by including the package printlen in praeambel.tex and typing
    # \uselengthunit{cm}\printlength{\textwidth} in a file.
}
"""dict[str, Union[float, int, str]]: The configurations in the LaTeX file.
"""


class CustomFormatter(logging.Formatter):
    """Logging Formatter to add colors and count warning / errors."""

    grey = "\x1b[38;21m"
    yellow = "\x1b[33;21m"
    red = "\x1b[31;21m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"

    FORMATS = {
        logging.DEBUG: grey + format + reset,
        logging.INFO: grey + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: bold_red + format + reset,
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


def get_logger(name: str, stream: bool = False) -> logging.Logger:
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

    if stream:
        stream_handler = logging.StreamHandler(stream=sys.stdout)
        stream_handler.setLevel(logging.DEBUG)
        stream_handler.setFormatter(CustomFormatter())
        # add the stream handler
        logger.addHandler(stream_handler)
        # coloredlogs.install(level="DEBUG", logger=logger)
    else:
        file_handler = logging.FileHandler(
            name + ".log", mode="w", encoding=LATEX_CONFIG_DIC["encoding"]
        )
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(CustomFormatter())
        # add the file handler
        logger.addHandler(file_handler)
    return logger
