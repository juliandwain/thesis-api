# -*- coding:utf-8 -*-

__doc__ = """Check the if the file in input statements exists.

"""

# TODO: Check if an existing file is not mentioned in input statements

import pathlib
import re

from conf import ENCODING, TEX_FILE, get_logger

LOGGER = get_logger(__name__)

COUNTER = 0
PATTERN = re.compile("(?<=input{).*?(?=})")


def find_input(
    path: pathlib.Path
) -> list:
    """Find all ``\\input`` statements in a given file.

    Parameters
    ----------
    path : pathlib.Path
        The file which should be examined.

    Returns
    -------
    list
        A list of all input statements.

    """
    with path.open(mode="r", encoding=ENCODING) as file:
        temp = file.read()
        inputs = [pathlib.Path(p.group(0)) for p in PATTERN.finditer(temp)]
    return inputs


def check_inputs(
    path: pathlib.Path
) -> None:
    """Check the ``\\input`` statements.

    Parameters
    ----------
    path : pathlib.Path
        The folder which .tex files should be checked.

    """
    for child in path.iterdir():
        if child.is_dir():
            if any(child.iterdir()):
                check_inputs(child)
        else:
            if TEX_FILE in child.parts[-1]:
                inputs = find_input(child)
                for inp in inputs:
                    if not inp.exists():
                        COUNTER += 1
                        LOGGER.warning(
                            f"File {inp} is included in {child} but does not exist!\n")


def main() -> None:
    """Main function.
    """
    thesis_dir = pathlib.Path(".")
    check_inputs(thesis_dir)
    if COUNTER == 0:
        LOGGER.debug(f"All files in \\input{{}} statements do exist!\n")


if __name__ == "__main__":
    main()
