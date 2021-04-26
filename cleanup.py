# -*- coding:utf-8 -*-

__doc__ = """This module cleans up empty directories.

By calling

```python
python cleanup.py --delete 1
```

this module cleans up the directories.
If ``--delete`` is given as ``1``, then the empty folders are deleted.
If ``--delete`` is given as ``0``, then the empty folders are printed to console only.

"""

import argparse
import pathlib
import shutil

from api import get_logger

LOGGER = get_logger(__name__)


def cleanup(path: pathlib.Path, delete: bool,) -> None:
    """Cleanup empty folders.

    Parameters
    ----------
    path : pathlib.Path
        The thesis directory.
    delete : bool
        Determine if empty folders should be deleted or only printed
        to console for user notification.

    """
    for child in path.iterdir():
        if child.is_dir():
            if any(child.iterdir()):
                cleanup(child, delete)
            else:
                LOGGER.debug(f"{child} is empty!")
                if delete:
                    LOGGER.debug(f"{child} is deleted since {delete=}!\n")
                    shutil.rmtree(child)
        else:
            continue


def main(delete: bool = False) -> None:
    """Main function.

    Parameters
    ----------
    delete : bool, optional
        Determine if the folders should be deleted or only printed to console,
        by default False.

    """
    thesis_dir = pathlib.Path(".")
    cleanup(thesis_dir, delete)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--delete",
        type=int,
        help="Determine if the folders should be deleted (1) or not (0)",
    )
    args = parser.parse_args()
    main(delete=bool(args.delete))
