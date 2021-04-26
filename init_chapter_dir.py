# -*- coding: utf-8 -*-

__doc__ = """Initialize a chapter directory with template files.
"""

import json
import pathlib

from api import ENCODING
from api.tools.maintenance import Maintainer


def main() -> None:
    """Main function.
    """
    thesis_dir = pathlib.Path("../aerospace-thesis")
    chapter_info = pathlib.Path("./api/tools/templates/chapter.json")
    maint = Maintainer(thesis_dir)
    with chapter_info.open(mode="r", encoding=ENCODING) as file:
        data = json.load(file)
    maint.init_chapter_dir(
        data["chapter"], data["sections"], data["subsections"]
    )


if __name__ == "__main__":
    main()
