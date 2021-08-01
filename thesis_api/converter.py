# -*- coding: utf-8 -*-

import pathlib
from typing import Any, Optional

import pypandoc

ENCODING: str = "utf-8"


class BasePandocService(object):
    """
    Base class for converting provided HTML to a doc or docx
    """

    def __init__(self):
        self._file_object = None
        self.service = self.get_service()

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        return super().__call__(*args, **kwds)

    def get_service(self):
        return pypandoc

    def generate(self, **kwargs):
        raise NotImplementedError


class PandocLaTeXService(BasePandocService):
    """Generate LaTex documents"""

    def __init__(self):
        super().__init__()
        self._to_format: str = "tex"

    def __call__(self, doc, from_format: str, **kwds: Any) -> Optional[str]:
        return self.generate(doc, from_format, **kwds)

    def generate(self, doc: str, from_format: str, **kwargs) -> Optional[str]:
        if from_format == "docx":
            kwargs["from_format"] = from_format
            return self._generate_from_docx(doc, **kwargs)

    def _generate_from_docx(self, doc, **kwargs) -> Optional[str]:
        from_format = kwargs.get("from_format", "docx")
        extra_args: tuple = (
            # "--standalone",
        )
        content = self.service.convert_file(
            doc, self._to_format, format=from_format, extra_args=extra_args,
        )
        return content


if __name__ == "__main__":
    doc = "test.docx"
    if isinstance(doc, pathlib.Path):
        from_format = doc.parts[-1].split(".")[-1]
    else:
        from_format = doc.split(".")[-1]
    service = PandocLaTeXService()
    content = service.generate(doc, from_format)
    print(content)
