# -*- coding: utf-8 -*-

__doc__ = """
This module implements some LaTeX template strings as Python
template strings, which makes it easy to use them and write to files.

Note that the # type: ignore comment should generally not be used,
although it seems that in this case there is no other solution
to the linting problem.

"""

import string
import pathlib
from typing import Mapping, Optional

__all__ = [
    "ChapterTemplate",
    "SectionTemplate",
    "SubsectionTemplate",
    "FigureTemplate",
    "TableTemplate",
    "CodeTemplate",
    "InputTemplate",
    "SiUnitxTemplate",
]


def reformat_path(path: pathlib.Path) -> str:
    """Reformat the path structure.

    The ``path`` structure is replaced by the actual path,
    but the path starts at ``chapters`` and the windows backslashes \\
    are replaced by slashes /.

    Parameters
    ----------
    path : pathlib.Path
        The path which should be formatted.

    Returns
    -------
    str
        A string representation of the reformatted path.

    """
    for i, part in enumerate(path.parts):
        if part == "chapters":
            child: str = "/".join(path.parts[i:])
            break
        else:
            child: str = f"{path}"
    return child


class SiUnitxTemplate(string.Template):
    def __init__(self, unit: Optional[str], kwds: dict = {}) -> None:
        """Generate a siunitx macro.

        Parameters
        ----------
        unit : Optional[str]
            The unit of the quantitity.
        kwds : dict, optional
            Additional keyword arguments the macros of the siunitx package
            take, by default {}.
        
        """
        if kwds:
            opt_args = "\n"
            for k, v in kwds.items():
                opt_args += k + "=" + v + ",\n"
            if unit:
                template: str = "\\qty[" + opt_args + "]{$num}{$unit}"

            else:
                template: str = "\\num[" + opt_args + "]{$num}"
        else:
            if unit:
                template: str = "\\qty{$num}{$unit}"
            else:
                template: str = "\\num{$num}"
        super().__init__(template)


class InputTemplate(string.Template):
    """A template class for ``input`` statements.

    This template class provides an interface to LaTeX by
    generating template strings for the LaTeX ``input``
    command.
    
    """

    def __init__(self) -> None:
        template: str = "\n\\input{$path}\n"
        super().__init__(template)

    def substitute(
        self, __mapping: Mapping[str, object], **kwds: object
    ) -> str:
        """Substitute the placeholder.

        The ``path`` placeholder is replaced by the actual path,
        but the path starts at ``chapters`` and the windows backslashes \\
        are replaced by slashes /.

        Returns
        -------
        str
            The substituted template string.

        """
        path = _InputTemplate__mapping["path"]  # type: ignore
        child = reformat_path(path)
        _InputTemplate__mapping["path"] = child  # type: ignore
        return super().substitute(_InputTemplate__mapping, **kwds)  # type: ignore


class ChapterTemplate(string.Template):
    """A template class for chapters.

    This template class provides an interface to LaTeX by
    generating use-ready LaTeX files which contain chapters.
    
    """

    def __init__(self) -> None:
        template: str = (
            "% !TEX root = ../../main.tex\n\n"
            "\\chapter{$title}\n"
            "\\label{cha:$label}\n\n"
            "This is a chapter.\n"
        )
        super().__init__(template)


class SectionTemplate(string.Template):
    """A template class for sections.

    This template class provides an interface to LaTeX by
    generating use-ready LaTeX files which contain sections.
    
    """

    def __init__(self) -> None:
        template: str = (
            "\\section{$title}\n"
            "\\label{sec:$label}\n\n"
            "This is a section within a chapter.\n"
        )
        super().__init__(template)


class SubsectionTemplate(string.Template):
    """A template class for subsections.

    This template class provides an interface to LaTeX by
    generating use-ready LaTeX files which contain subsections.
    
    """

    def __init__(self) -> None:
        template: str = (
            "\\subsection{$title}\n"
            "\\label{subsec:$label}\n\n"
            "This is a subsection within a section.\n"
        )
        super().__init__(template)


class _CaptionTemplate(string.Template):
    """Base class.

    This is a base class for LaTeX templates which can provide a short
    caption, like figures and pseudo codes.
    
    """

    def __init__(self, template: str, short_caption: bool = False) -> None:
        """Init the class.

        Parameters
        ----------
        template : str
            The template to use.
        short_caption : bool, optional
            Determine if a short caption should be used,
            by default False.

        """
        self._short_caption = short_caption
        super().__init__(template)

    def substitute(
        self, __mapping: Mapping[str, object], **kwds: object
    ) -> str:
        """Overwrite the substitute method.

        Depending on the value of ``self._short_caption``, the template is
        filled differently.

        Returns
        -------
        str
            The template with replaced values.

        """
        if self._short_caption:
            long_caption, short_caption = _CaptionTemplate__mapping["caption"]  # type: ignore
            _CaptionTemplate__mapping["short_caption"] = short_caption  # type: ignore
            _CaptionTemplate__mapping["long_caption"] = long_caption  # type: ignore
            _CaptionTemplate__mapping.pop("caption")  # type: ignore
        path = _CaptionTemplate__mapping["path"]  # type: ignore
        child = reformat_path(path)
        _CaptionTemplate__mapping["path"] = child  # type: ignore
        return super().substitute(_CaptionTemplate__mapping, **kwds)  # type: ignore

    def safe_substitute(
        self, __mapping: Mapping[str, object], **kwds: object
    ) -> str:
        """Overwrite the ``safe_substitute`` method.

        Depending on the value of ``self._short_caption``, the template is
        filled differently.

        Returns
        -------
        str
            The template with replaced values.

        """
        if self._short_caption:
            long_caption, short_caption = _CaptionTemplate__mapping["caption"]  # type: ignore
            _CaptionTemplate__mapping["short_caption"] = short_caption  # type: ignore
            _CaptionTemplate__mapping["long_caption"] = long_caption  # type: ignore
            _CaptionTemplate__mapping.pop("caption")  # type: ignore
        path = _CaptionTemplate__mapping["path"]  # type: ignore
        child = reformat_path(path)
        _CaptionTemplate__mapping["path"] = child  # type: ignore
        return super().safe_substitute(_CaptionTemplate__mapping, **kwds)  # type: ignore


class FigureTemplate(_CaptionTemplate):
    """A template class for figures.

    This template class provides an interface to LaTeX by
    generating use-ready LaTeX files which contain figures.

    """

    def __init__(self, short_caption: bool = False) -> None:
        """Init the FigureTemplate.

        Parameters
        ----------
        short_caption : bool, optional
            Determine if a short caption should be used,
            by default False.

        """

        if short_caption:
            template: str = (
                "\\begin{figure}[$position]\n"
                "\t\\centering\n"
                "\t\\includegraphics[width=$width\\textwidth]{$path}\n"
                "\t\\caption[$short_caption]{$long_caption}\n"
                "\t\\label{fig:$label}\n"
                "\\end{figure}\n"
            )
        else:
            template: str = (
                "\\begin{figure}[$position]\n"
                "\t\\centering\n"
                "\t\\includegraphics[width=$width\\textwidth]{$path}\n"
                "\t\\caption{$caption}\n"
                "\t\\label{fig:$label}\n"
                "\\end{figure}\n"
            )
        super().__init__(template, short_caption)


class TableTemplate(string.Template):
    """A template class for tables.

    This template class provides an interface to LaTeX by
    generating use-ready LaTeX files which contain tables.

    The tables itself are generated using the pandas
    ``to_latex`` method of the ``DataFrame`` class,
    see also [1].

    References
    ----------
    [1] https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.to_latex.html

    """

    def __init__(self) -> None:
        template: str = (
            "\\begingroup\n"
            "\\renewcommand{\\arraystretch}{$arraystretch}\n"
            "$data\n"
            "\\endgroup\n"
        )
        super().__init__(template)


class CodeTemplate(_CaptionTemplate):
    """A template class for pseudocode.

    This template class provides an interface to LaTeX by
    generating use-ready LaTeX files which contain pseudo code.
        
    """

    def __init__(self, short_caption: bool = False) -> None:
        """Init the CodeTemplate.

        Parameters
        ----------
        short_caption : bool, optional
            Determine if a short caption should be used,
            by default False.

        """
        if short_caption:
            template: str = (
                "\\begin{listing}[$position]\n"
                "\t\\inputminted{$language}{$path}\n"
                "\t\\caption[$short_caption]{$long_caption}\n"
                "\t\\label{lst:$label}\n"
                "\\end{listing}\n"
            )
        else:
            template: str = (
                "\\begin{listing}[$position]\n"
                "\t\\inputminted{$language}{$path}\n"
                "\t\\caption{$caption}\n"
                "\t\\label{lst:$label}\n"
                "\\end{listing}\n"
            )
        super().__init__(template, short_caption)

