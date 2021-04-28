# -*- coding: utf-8 -*-

__doc__ = """The API interface to the LaTeX project.

Note that this interface uses the Google style python docstrings,
as given in [1].

References
----------
[1] https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html

"""

import logging
import sys

import coloredlogs

__version__ = "0.0.1"


##################

ENCODING: str = "utf-8"
"""str: The encoding of all files.
"""

LATEX_CONFIG_DIC = {
    "arraystretch": 1.8,  # scaling of tables
    "si_round_precision": 3,  # round precision of siunitx
}
"""dict: The configurations in the LaTeX file.
"""

SCRBOOK_WIDTH: float = 14.89787  # the width of the scrbook class in [cm]
r"""float: The width in [cm].

This is the line width of the LaTeX class scrbook in [cm], which my be useful for tables, etc.
The line length can be obtained by including the package printlen in praeambel.tex and typing
\uselengthunit{cm}\printlength{\textwidth} in a file.
"""
LATEX_CONFIG_DIC["scrbook_width"] = SCRBOOK_WIDTH

TEMPLATES: dict[str, str] = {
    "figs": "figure.tex",
    "tabs": "table.tex",
    "code": "code.tex",
}
"""dict[str, str]: The mapping from the folder to the template to use.
"""

TEX_FILE: str = "tex"
"""str: The file ending for LaTeX files.
"""


class CustomFormatter(logging.Formatter):
    """Logging Formatter to add colors and count warning / errors"""

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
    # define the formatter for both handlers
    formatter = logging.Formatter("%(asctime)s:%(levelname)s:%(message)s")

    if stream:
        stream_handler = logging.StreamHandler(stream=sys.stdout)
        stream_handler.setLevel(logging.DEBUG)
        stream_handler.setFormatter(CustomFormatter())
        # add the stream handler
        logger.addHandler(stream_handler)
        # coloredlogs.install(level="DEBUG", logger=logger)
    else:
        file_handler = logging.FileHandler(
            name + ".log", mode="w", encoding=ENCODING
        )
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        # add the file handler
        logger.addHandler(file_handler)
    return logger
