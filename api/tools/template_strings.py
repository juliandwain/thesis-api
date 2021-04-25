# -*- coding: utf-8 -*-

__doc__ = """
This module implements some LaTeX template strings as Python
template strings, which makes it easy to use them and write to files.
"""

import string
from typing import Mapping

__all__ = [
    "ChapterTemplate",
    "SectionTemplate",
    "SubsectionTemplate",
    "FigureTemplate",
    "TableTemplate",
    "CodeTemplate",
]


class ChapterTemplate(string.Template):
    def __init__(self) -> None:
        template: str = (
            "% !TEX root = ../../main.tex\n\n"
            "\\chapter{$title}\n"
            "\\label{cha:$label}\n\n"
            "This is a chapter.\n"
        )
        super().__init__(template)

    def __add__(self, other: string.Template):
        pass


class SectionTemplate(string.Template):
    def __init__(self) -> None:
        template: str = (
            "\\section{$title}\n"
            "\\label{sec:$label}\n\n"
            "This is a section within a chapter.\n"
        )
        super().__init__(template)


class SubsectionTemplate(string.Template):
    def __init__(self) -> None:
        template: str = (
            "\\subsection{$title}\n"
            "\\label{subsec:$label}\n\n"
            "This is a subsection within a section.\n"
        )
        super().__init__(template)


class _CaptionTemplate(string.Template):
    def __init__(self, template: str, short_caption: bool = False) -> None:
        self._short_caption = short_caption
        super().__init__(template)

    def substitute(
        self, __mapping: Mapping[str, object], **kwds: object
    ) -> str:
        if self._short_caption:
            long_caption, short_caption = _CaptionTemplate__mapping["caption"]
            _CaptionTemplate__mapping["short_caption"] = short_caption
            _CaptionTemplate__mapping["long_caption"] = long_caption
            _CaptionTemplate__mapping.pop("caption")
        return super().substitute(_CaptionTemplate__mapping, **kwds)

    def safe_substitute(
        self, __mapping: Mapping[str, object], **kwds: object
    ) -> str:
        if self._short_caption:
            long_caption, short_caption = _CaptionTemplate__mapping["caption"]
            _CaptionTemplate__mapping["short_caption"] = short_caption
            _CaptionTemplate__mapping["long_caption"] = long_caption
            _CaptionTemplate__mapping.pop("caption")
        return super().safe_substitute(_CaptionTemplate__mapping, **kwds)


class FigureTemplate(_CaptionTemplate):
    def __init__(self, short_caption: bool = False) -> None:
        if short_caption:
            template: str = (
                "\\begin{figure}[$position]\n"
                "\t\\centering\n"
                "\t\\includegraphics[width=$width\\textwidth]{$fname}\n"
                "\t\\caption[$short_caption]{$long_caption}\n"
                "\t\\label{fig:$label}\n"
                "\\end{figure}\n"
            )
        else:
            template: str = (
                "\\begin{figure}[$position]\n"
                "\t\\centering\n"
                "\t\\includegraphics[width=$width\\textwidth]{$fname}\n"
                "\t\\caption{$caption}\n"
                "\t\\label{fig:$label}\n"
                "\\end{figure}\n"
            )
        super().__init__(template, short_caption)


class TableTemplate(string.Template):
    def __init__(self) -> None:
        template: str = (
            "\\begingroup\n"
            "\\renewcommand{\\arraystretch}{$arraystretch}\n"
            "$data\n"
            "\\endgroup\n"
        )
        super().__init__(template)


class CodeTemplate(_CaptionTemplate):
    def __init__(self, short_caption: bool = False) -> None:
        if short_caption:
            template: str = (
                "\\begin{listing}[$position]\n"
                "\t\\inputminted{$language}{$fname}\n"
                "\t\\caption[$short_caption]{$long_caption}\n"
                "\t\\label{lst:$label}\n"
                "\\end{listing}\n"
            )
        else:
            template: str = (
                "\\begin{listing}[$position]\n"
                "\t\\inputminted{$language}{$fname}\n"
                "\t\\caption{$caption}\n"
                "\t\\label{lst:$label}\n"
                "\\end{listing}\n"
            )
        super().__init__(template, short_caption)
