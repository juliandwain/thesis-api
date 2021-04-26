# -*- coding:utf-8 -*-

__doc__ = """Check the if the file in input statements exists.

"""

# TODO: Check if an existing file is not mentioned in input statements

import pathlib
import re

from api import get_logger
from api.tools.maintenance import Maintainer

LOGGER = get_logger(__name__)


def main() -> None:
    """Main function.
    """
    thesis_dir = pathlib.Path("../aerospace-thesis/")
    maint = Maintainer(thesis_dir)
    maint.check_inputs(thesis_dir)
    maint.check_main()
    if maint.counter == 0:
        LOGGER.debug(f"All files in \\input{{}} statements do exist!\n")


if __name__ == "__main__":
    main()
