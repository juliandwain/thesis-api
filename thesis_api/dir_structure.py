# -*- coding: utf-8 -*-

__doc__ = """
"""

import functools
import pathlib
import re
import string
from typing import Any, Optional, Union

from . import LATEX_CONFIG_DIC, get_logger
from .tools.template_strings import (
    FigureTemplate,
    SiUnitxTemplate,
    TableTemplate,
)

LOGGER = get_logger(__name__)
"""logging.Logger: The module level logger.
"""


def format_table(number: Union[int, float], unit: Optional[str] = None) -> str:
    r"""Format numbers in tables.

    When writing a pandas DataFrame to a LaTeX table,
    this function can be used to wrap the columns specified
    (columns containing numbers) in \num or \SI from siunitx.

    Parameters
    ----------
    number : Union[int, float]
        The number from the DataFrame.
    unit : Optional[str], optional
        The corresponding unit, by default None.

    Returns
    -------
    str
        A LaTeX siuntix string.

    Notes
    -----
    The ``unit`` parameter can often be neglected since one can write the unit
    of the column (since most entries in columns have the same unit)
    within the column's respective header.

    """
    temp = SiUnitxTemplate(unit)
    if unit:
        temp_str: str = temp.substitute(num=number, unit=unit)
    else:
        temp_str: str = temp.substitute(num=number)
    return temp_str


class Chapter(object):
    def __init__(
        self,
        filename: str,
        chapter_dir: pathlib.Path,
        location: str,
        typ: str,
    ) -> None:
        r"""Init the class.

        Parameters
        ----------
        filename : str
            The name of the data under which it should be saved.
        chapter_dir : pathlib.Path
            The chapter directory.
        location : str
            The location in which the data should be saved. This is a string,
            e.g.,

            * "chapter3\nsection3".
            * "chapter4\nsection2\nsubsection1".
            * "chapter1\n".

        typ : str
            The type of data which should be saved.
            This can be either of the following:

            * "figs".
            * "tabs".
            * "code".

        """
        # save the chapter directory
        self._chapter_dir: pathlib.Path = chapter_dir
        # save the location where it should be saved
        self._location: list[str] = (
            location.lower().replace(" ", "").split("\n")
        )
        # define a template string with the LaTeX input command
        self._inputstr = string.Template("\n\\input{$path}\n")
        # get the filename
        self._filename = filename
        # get the file format
        self._fmt: str = filename.split(".")[-1].lower()
        # get the corresponding folder
        self._folder: str = typ.lower()

    def __str__(self) -> str:
        """String representation of ``self``.

        Returns
        -------
        str
            The class as string.

        """
        msg: str = f"|-{self._chapter_dir.resolve()}\n"
        for i, loc in enumerate(self._location, start=1):
            msg += "|" + i * "--" + f">{loc}\n"
        i += 1
        msg += "|" + i * "--" + f">{self._folder}\n"
        i += 1
        msg += "|" + i * "--" + f">{self._filename}\n"
        return msg

    def _construct_path(self) -> pathlib.Path:
        """Construct the path in which the file should be saved.

        Returns
        -------
        pathlib.Path
            The path within the chapters folder where
            the figure should be saved.

        """
        folders: tuple = (
            "",
            "sections/",
            "subsections/",
        )
        path: str = ""
        for folder, loc in zip(folders, self._location):
            path += folder + loc + "/"
        goal_dir: pathlib.Path = self._chapter_dir / path
        return goal_dir

    def _fill_template(
        self,
        fname: pathlib.Path,
        template_str: string.Template,
        template_desc: dict[str, Union[float, str, bool]],
    ) -> None:
        """Fill the LaTeX template.

        Parameters
        ----------
        fname : pathlib.Path
            The file which should be created based on ``template_str``.
        template_str : string.Template
            The template string.
        template_desc : dict[str, Union[float, str, bool]]
            The fields to write to the template.

        """
        template = template_str.substitute(template_desc)
        fname.write_text(template, encoding=LATEX_CONFIG_DIC["encoding"])

    def save_fig(
        self, fig: Any, fig_desc: dict[str, Union[float, str, bool]],
    ) -> None:
        r"""Save a result to a figure.

        Parameters
        ----------
        fig : Union[matplotlib.figure.Figure, plotly.graph_objs._figure.Figure]
            The figure which should be saved.
        fig_desc : dict[str, Union[float, str, bool]]
            The discription of the figure, see also [1].
            The most important args are:

            * "width": The width of the figure, float.
            * "caption": Tuple (full_caption, short_caption), which results in
                ``\caption[short_caption]{full_caption}``;
                if a single string is passed, no short caption will be set.
            * "label": The LaTeX label to be placed inside ``\label{}``
                in the output.
                This is used with ``\(c)ref{}`` in the main ``.tex`` file.
            * "position": The LaTeX positional argument for tables,
                to be placed after ``\begin{}`` in the output.

        Raises
        ------
        TypeError
            If the ``fig`` argument is neither of type
            ``matplotlib.figure.Figure`` nor of type
            ``plotly.graph_objs._figure.Figure``.

        References
        ----------
        [1] https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.to_latex.html

        """
        # construct the corresponding path
        goal_dir: pathlib.Path = self._construct_path()
        # get the folder and filename for the child directory
        child_folder = goal_dir / self._folder
        if not child_folder.exists():
            child_folder.mkdir(parents=True, exist_ok=True)
        child_filename = child_folder / self._filename
        child_filename_tex = child_folder / self._filename.replace(
            self._fmt, "tex"
        )
        t = type(fig)
        # check if t is of type matplotlib figure
        if t.__module__ == (mm := "matplotlib.figure"):
            fig.savefig(
                child_filename,
                dpi=600,
                orientation="portrait",
                format=self._fmt,
            )
        # check if t is of type plotly figure
        elif t.__module__ == (mp := "plotly.graph_objs._figure"):
            try:
                from kaleido.scopes.plotly import PlotlyScope  # type: ignore

                scope = PlotlyScope(
                    plotlyjs="https://cdn.plot.ly/plotly-latest.min.js",
                    # plotlyjs="/path/to/local/plotly.js",
                )
                with child_filename.open(mode="wb") as file:
                    file.write(scope.transform(fig, format=self._fmt))
            except ImportError:
                LOGGER.debug(
                    f"Kaleido is not installed, falling back to plotly save."
                )
                fig.write_image(f"{child_filename}")
        else:
            raise TypeError(
                f"fig is neither from matplotlib module {mm} nor from plotly module {mp}!"
            )
        fig_desc["fname"] = f"{child_filename}".replace("\\", "/")
        # fill the tex template
        if isinstance(fig_desc["caption"], tuple):
            short = True
        else:
            short = False
        self._fill_template(
            child_filename_tex, FigureTemplate(short_caption=short), fig_desc
        )
        # get the tex filename for the parent
        parent_filename_tex = list(goal_dir.glob("*.tex"))[0]
        self.update(parent_filename_tex, child_filename_tex)

    def save_tab(
        self,
        data: Any,
        data_desc: dict[str, Union[str, tuple]],
        format_cols: Optional[dict[str, Optional[str]]] = None,
        latex_args: dict[str, Union[float, str, bool, list[str]]] = {},
    ) -> None:
        r"""Save a result to a table.

        Parameters
        ----------
        data : pandas.DataFrame
            The data which should be saved as a table.
        data_desc : dict[str, Union[str, tuple]]
            The discription of the figure, see also [1].
            The most important args are:

            * "width": The width of the figure, float.
            * "caption": Tuple (full_caption, short_caption), which results in
                ``\caption[short_caption]{full_caption}``;
                if a single string is passed, no short caption will be set.
            * "label": The LaTeX label to be placed inside ``\label{}``
                in the output.
                This is used with ``\(c)ref{}`` in the main ``.tex`` file.
            * "position": The LaTeX positional argument for tables,
                to be placed after ``\begin{}`` in the output.

        format_cols : Optional[dict[str, Optional[str]]], optional
            A dictionary which maps columns to the
            ``format_table`` function which formats floats for LaTeX,
            by default None.
        latex_args : dict[str, Union[float, str, bool, list[str]]], optional
            A dict of arguments specific for LaTeX, by default {}.
            The arguments can be:

                * "arraystretch": float
                    The amount of spacing within the table.
                    If no value is given, then the default value of 1.8
                    is used.
                * "column_type": Optional[Union[str, list[str]]]
                    The column type, this can either be:

                    * a string with standard LaTeX table measures, e.g., "llr",
                        "ccc", "lSSS", etc.
                    * a list of strings containing user-defined measures, e.g.,
                        ["p{3cm}", p{4.5cm}"], etc.
                    * None, which will then use the default settings provided
                        by pandas.

                    If no value is given this is set to None.

                * "top_caption": bool
                    Determine whether the caption should be placed above the table
                    or below.
                    If no value is given this is set to False.


        References
        ----------
        [1] https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.to_latex.html

        """
        # construct the corresponding path
        goal_dir: pathlib.Path = self._construct_path()
        # get the folder and filename for the child directory
        child_folder = goal_dir / self._folder
        if not child_folder.exists():
            child_folder.mkdir(parents=True, exist_ok=True)
        child_filename = child_folder / self._filename
        if format_cols:
            formatters = {
                key: functools.partial(format_table, unit=value)
                for key, value in format_cols.items()
            }
        else:
            formatters = format_cols
        # save the table to the file
        data_str: str = data.to_latex(
            formatters=formatters, escape=False, index=False, **data_desc,
        )  # returns a string since buf is None, see [1]
        if not latex_args:
            latex_args["arraystretch"] = LATEX_CONFIG_DIC["arraystretch"]
        # fill the tex template
        n = data.shape[-1]
        column_type: Optional[Union[str, list[str]]] = latex_args.pop(
            "column_type", None
        )
        top_caption: bool = latex_args.pop("top_caption", False)
        data_str = self._rewrite_table(data_str, n, column_type, top_caption)
        latex_args["data"] = data_str
        self._fill_template(child_filename, TableTemplate(), latex_args)
        # get the tex filename for the parent
        parent_filename_tex = list(goal_dir.glob("*.tex"))[0]
        self.update(parent_filename_tex, child_filename)

    def _rewrite_table(
        self,
        data: str,
        num_data: int,
        column_type: Optional[Union[str, list[str]]],
        top_caption: bool,
    ) -> str:
        """Rewrite the LaTeX table generated by pandas.

        Parameters
        ----------
        data : str
            The LaTeX table as string generated by pandas.
        num_data : int
            The number of columns.
        column_type : Optional[Union[str, list[str]]]
            The column type, this can either be:

                * a string with standard LaTeX table measures, e.g., "llr",
                    "ccc", "lSSS", etc.
                * a list of strings containing user-defined measures, e.g.,
                    ["p{3cm}", p{4.5cm}"], etc.
                * None, which will then use the default settings provided
                    by pandas.

        top_caption : bool
            Determine whether the caption should be placed above the table
            or below.

        Returns
        -------
        str
            The LaTeX representation of the table.

        Raises
        ------
        AssertionError
            If the number of column measures does not match the
            number of data columns.

        Notes
        -----
        - Passing the LaTeX table measure "S" requires the siunitx package,
            see [1].
        - When using user-defined measures, the user is warned if the width
            of the table exceeds the width of the scrbook class.

        References
        ----------
        [1] http://ctan.math.utah.edu/ctan/tex-archive/macros/latex/contrib/siunitx/siunitx.pdf
        [2] https://stackoverflow.com/questions/11339210/how-to-get-integer-values-from-a-string-in-python
        [3] https://stackoverflow.com/questions/4703390/how-to-extract-a-floating-number-from-a-string

        """
        col_re = re.compile("(?<=tabular}{).*?(?=})")
        if column_type:
            assert (
                n := len(column_type)
            ) == num_data, f"The number of columns {n} does not match the number of columns in the data {num_data}!"
            if isinstance(column_type, list):
                table_width: float = sum(
                    [
                        float(re.search(r"[-+]?\d*\.?\d+|\d+", w).group())
                        for w in column_type
                    ]
                )
                if table_width > (w := LATEX_CONFIG_DIC["scrbook_width"]):
                    LOGGER.warning(
                        f"The table width {table_width}cm exceeds the limits by scrbook {w}cm!\n"
                    )
                column_type_: str = "".join(column_type)
            else:
                column_type_: str = column_type
            data = col_re.sub(column_type_, data)
        if not top_caption:
            temp = data.split("\n")
            cap = temp[2]  # the caption is always at 3rd place
            label = temp[3]  # the label is always at 4th place
            del temp[2]  # delete the values
            del temp[2]  # delete the values
            temp.insert(-2, cap)  # insert the caption at the bottom
            temp.insert(-2, label)  # insert the label at the bottom
            data = "\n".join(temp)
        return data

    def update(self, parent: pathlib.Path, child: pathlib.Path,) -> None:
        """Update the result.

        If the result is newly created but should still be located
        in the same file, then only the figure is updated but
        the path in the file stays the same.

        Parameters
        ----------
        parent : pathlib.Path
            The parent file in which the figure is included.
        child : pathlib.Path
            The figure file which is included in the parent.

        """
        # if only the figure should be updated but not the parent and the corresponding input
        for i, part in enumerate(child.parts):
            if part == "chapters":
                # child is not unbound since the for loop breaks
                child_ = "/".join(child.parts[i:])
                break
        string_ = self._inputstr.substitute(path=child_)  # type: ignore
        with parent.open(
            mode="r+", encoding=LATEX_CONFIG_DIC["encoding"]
        ) as file:
            temp: str = file.read()
            if string_ in temp:
                LOGGER.debug(f"{string_} is already in {parent}!\n")
            else:
                LOGGER.debug(
                    f"{string_} is appended to the end of {parent}!\n"
                )
                file.write(string_)
