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

from thesis_api import get_logger
from thesis_api.tools.maintenance import Maintainer

LOGGER = get_logger(__name__)


def main(delete: bool = False) -> None:
    """Main function.

    Parameters
    ----------
    delete : bool, optional
        Determine if the folders should be deleted or only printed to console,
        by default False.

    """
    thesis_dir = pathlib.Path("./tests/data")
    maint = Maintainer(thesis_dir)
    maint.check_main()
    # maint.cleanup(thesis_dir, delete)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--delete",
        type=int,
        help="Determine if the folders should be deleted (1) or not (0)",
    )
    args = parser.parse_args()
    main(delete=bool(args.delete))
