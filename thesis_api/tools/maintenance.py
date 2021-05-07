# -*- coding: utf-8 -*-

import pathlib
import re
import shutil
import string
from typing import Any, Iterable, Union

from .. import LATEX_CONFIG_DIC, get_logger
from .template_strings import (
    ChapterTemplate,
    InputTemplate,
    SectionTemplate,
    SubsectionTemplate,
)

LOGGER = get_logger(__name__, stream=False)
PATTERN = re.compile("(?<=input{).*?(?=})")


class Maintainer(object):
    def __init__(self, thesis_dir: pathlib.Path) -> None:
        """Init the class.

        Parameters
        ----------
        thesis_dir : pathlib.Path
            The path to the thesis directory.
        
        """
        self._thesis_dir: pathlib.Path = thesis_dir
        self._chapter_dir: pathlib.Path = thesis_dir / "chapters"
        self._main_file: pathlib.Path = thesis_dir / "main.tex"
        self._counter: int = 0
        # save the template classes
        self._chapter_template: string.Template = ChapterTemplate()
        self._sec_template: string.Template = SectionTemplate()
        self._subsec_template: string.Template = SubsectionTemplate()
        self._input_template: string.Template = InputTemplate()
        super().__init__()

    @property
    def counter(self) -> int:
        """Counter for files which are included in \\input statements
        but do not exist.

        Returns
        -------
        int
            The number of times this is true.

        """
        return self._counter

    def check_inputs(self, child: pathlib.Path) -> None:
        """Recursivley check ``child`` for ``\\input`` statements.

        Parameters
        ----------
        child : pathlib.Path]
            The file which should be checked for input statements.
        
        """
        for child_ in child.iterdir():
            if child_.is_dir():
                if any(child_.iterdir()):
                    self.check_inputs(child_)
            else:
                if LATEX_CONFIG_DIC["tex_file"] in child_.parts[-1]:
                    for inp in self.find_input(child_):
                        if not (
                            p := self._thesis_dir.resolve() / inp
                        ).exists():
                            self._counter += 1
                            LOGGER.warning(
                                f"File {p} is included in {child_.resolve()} but does not exist!\n"
                            )
                        else:
                            LOGGER.debug(
                                f"File {p} is included in {child_.resolve()} and exists!\n"
                            )

    def check_main(self):
        """Check the ``main.tex`` file for all input statements.

        This function checks 2 cases:

        1) The input statements in the ``main.tex`` file and if the
            corresponding files exist.
        2) The chapter tex files in the chapters directory and if
            they are included in the ``main.tex`` file, and if not,
            then they are written to the corresponding place.
            
        """
        temp = self._main_file.read_text(encoding=LATEX_CONFIG_DIC["encoding"])
        inputs_re = list(PATTERN.finditer(temp))
        inputs_p = [pathlib.Path(p.group(0)) for p in inputs_re]
        for p_in in inputs_p:
            path = (self._thesis_dir / p_in).resolve()

            if path.exists():
                LOGGER.debug(
                    f"{path} exists and is included in {self._main_file.resolve()}!\n"
                )
            else:
                LOGGER.warning(
                    f"{path} does not exist but is included in {self._main_file.resolve()}!\n"
                )
            for p_glob in self._chapter_dir.glob("chapter*/*.tex"):
                if p_glob == p_in:
                    pass

    def cleanup(self, child: pathlib.Path, delete: bool = False) -> None:
        """Cleanup empty folders.

        Parameters
        ----------
        child : pathlib.Path
            The directory which is checked.
        delete : bool, optional
            Determine if empty folders should be deleted or only printed
            to console for user notification, by default False.

        """
        for child_ in child.iterdir():
            if child_.is_dir():
                if any(child_.iterdir()):
                    self.cleanup(child_, delete)
                else:
                    LOGGER.debug(f"{child_} is empty!")
                    if delete:
                        LOGGER.debug(f"{child_} is deleted since {delete=}!\n")
                        shutil.rmtree(child_)
                    else:
                        LOGGER.debug(
                            f"{child_} is not deleted since {delete=}!\n"
                        )
            else:
                continue

    def create_ftc(self, path: pathlib.Path, typ: dict) -> None:
        """Create the figs, tabs, and/or code directories.

        Parameters
        ----------
        path : pathlib.Path
            The path in which the ftc-directories should be created.
        typ : dict
            A dictionary containing information abouth which
            of the directories should be created at a given level.

        """
        for k, v in typ.items():
            temp_path = path / k
            if v:
                try:
                    temp_path.mkdir(parents=True, exist_ok=False)
                except FileExistsError:
                    LOGGER.debug(f"Folder {temp_path} already exists.")
            else:
                LOGGER.debug(
                    f"Folder {temp_path} was not created because it was set to {v}."
                )

    def create_subfolder(self, data: dict[str, Any]):
        typ: str = next(iter(data))
        num: str = str(data.pop(typ, 10))
        period: str = typ + num
        for t in ["num_sections", "num_subsections"]:
            try:
                num_s = data.pop(t, 0)
                break
            except KeyError:
                continue

    def find_input(self, path: pathlib.Path) -> Iterable[pathlib.Path]:
        """Find all ``\\input`` statements in a given file.

        Parameters
        ----------
        path : pathlib.Path
            The file which should be examined.

        Yields
        ------
        Iterable[pathlib.Path]
            The corresponding path within the ``input`` statement.

        """
        temp = path.read_text(encoding=LATEX_CONFIG_DIC["encoding"])
        for p in PATTERN.finditer(temp):
            yield pathlib.Path(p.group(0))

    def init_chapter_dir(
        self,
        chapter: dict[str, Union[bool, int]],
        sections: list[dict[str, Union[bool, int]]],
        subsections: dict[str, list[dict[str, Union[bool, int]]]],
    ) -> None:
        """Init an empty chapter directory structure.

        Parameters
        ----------
        chapter : dict[str, Union[bool, int]]
            The description for the chapter top level, this is a dict:

            * "chapter": int, the chapter number.
            * "num_sections": int, the number of sections.
            * "figs": bool, whether there are figures on the chapter level.
            * "tabs": bool, whether there are tables on the chapter level.
            * "code": bool, whether there are pseudo codes
                on the chapter level.

        sections : list[dict[str, Union[bool, int]]]
            The discription of the sections, this is a list of
            dicts where each dict contains the following values:

            * "section": int, the section number.
            * "num_subsections": int, the number of subsections.
            * "figs": bool, whether there are figures on the section level.
            * "tabs": bool, whether there are tables on the section level.
            * "code": bool, whether there are pseudo codes
                on the section level.

        subsections : dict[str, list[dict[str, Union[bool, int]]]]
            The description of the subsections, this is a dictionary
            where each key corresponds to the subsection number and the value
            is a list of dictionaries containing the following values:

            * "subsection": int, the subsection number.
            * "figs": bool, whether there are figures on the subsection level.
            * "tabs": bool, whether there are tables on the subsection level.
            * "code": bool, whether there are pseudo codes
                on the subsection level.

        Raises
        ------
        e
            TODO

        Notes
        -----
        For convenience, there is a ``chapter.json`` file located in the
        templates folder in this api which can be easily adapted and read
        into a dictionary, see the examples section.
        This function is only useful for initializing an empty chapter
        directory.

        Examples
        --------
        >>> import json
        >>> import pathlib
        >>> template = pathlib.Path("PATH/TO/TEMPLATE)
        >>> with template.open(mode="r", encoding="utf-8") as file:
        >>>     data = json.load(file)
        >>> self.init_chapter_dir(
        >>>     data["chapter"], data["sections"], data["subsections"]   
        >>> )

        """
        # get the type of folder to create
        chapter_type = next(iter(chapter))
        # self.create_subfolder(chapter)
        # get the chapter number
        chapter_num = str(chapter.pop("chapter", 10))
        # define the chapter
        chapter_ = chapter_type + chapter_num
        # get the number of sections in the chapter
        num_sections = chapter.pop("num_sections", 0)
        # test if the number of sections aligns with the number of sections given
        assert num_sections == (
            n := len(sections)
        ), f"Number of sections does not match!\nExpected: {num_sections}, Got: {n}!"
        chapter_path = self._chapter_dir / chapter_
        try:
            chapter_path.mkdir(parents=True, exist_ok=False)
        except FileExistsError as e:
            LOGGER.critical(
                f"{chapter_path} already exists!\nMaybe you want to create a new chapter?\n"
            )
            raise e
        chapter_file = chapter_path / (chapter_ + LATEX_CONFIG_DIC["tex_file"])
        # create the chapter directories
        self.create_ftc(chapter_path, chapter)
        # open the chapter template
        chapter_template_str = self._chapter_template.substitute(
            title=chapter_, label=chapter_
        )
        if num_sections != 0:
            sec_path = chapter_path / "sections"
            sec_path.mkdir(parents=True, exist_ok=True)
            for section in sections:
                sec_type = next(iter(section))
                sec_num = str(section.pop("section", 10))
                sec_ = sec_type + sec_num
                num_subsections = section.pop("num_subsections", 10)
                assert num_subsections == (
                    n := len(subsections[sec_num])
                ), f"Number of subsections does not match!\nExpected: {num_subsections}, Got: {n}!"
                sec_dir = sec_path / sec_
                sec_dir.mkdir(parents=True, exist_ok=True)
                sec_file = sec_dir / (sec_ + LATEX_CONFIG_DIC["tex_file"])
                # open the section template
                sec_template_str = self._sec_template.substitute(
                    title=f"{chapter_}-{sec_}", label=f"{chapter_}-{sec_}",
                )
                # create the section directories
                self.create_ftc(sec_dir, section)
                chapter_template_str += self._input_template.substitute(
                    {"path": sec_file}
                )
                if num_subsections != 0:
                    subsec_path = sec_dir / "subsections"
                    subsec_path.mkdir(parents=True, exist_ok=True)
                    for subsection in subsections[str(sec_num)]:
                        subsec_type = next(iter(subsection))
                        subsec_num = str(subsection.pop("subsection", 10))
                        subsec_ = subsec_type + subsec_num
                        subsec_dir = subsec_path / subsec_
                        subsec_dir.mkdir(parents=True, exist_ok=True)
                        subsec_file = subsec_dir / (
                            subsec_ + LATEX_CONFIG_DIC["tex_file"]
                        )
                        # create the subsection latex file
                        subsec_template_str = self._subsec_template.substitute(
                            title=f"{chapter_}-{sec_}-{subsec_}",
                            label=f"{chapter_}-{sec_}-{subsec_}",
                        )
                        self.tex_file(
                            subsec_file, subsec_template_str,
                        )
                        # create the subsection directories
                        self.create_ftc(subsec_dir, subsection)
                        sec_template_str += self._input_template.substitute(
                            {"path": subsec_file}
                        )
                else:
                    LOGGER.debug(f"No Subsections created in {sec_dir}!")
                # create the section latex file
                self.tex_file(sec_file, sec_template_str)

        else:
            LOGGER.debug(f"No Sections created in {chapter_path}!")
        # create the chapter latex file
        self.tex_file(chapter_file, chapter_template_str)

    def tex_file(self, path: pathlib.Path, temp: str) -> None:
        """Create the template LaTeX file.

        Parameters
        ----------
        path : pathlib.Path
            The file which should be created.
        temp : str
            The content to write to the file.

        Notes
        -----
        - This function uses the templates provided from ``open_template``.
        - If the file already exists, then a notification is printed.

        """
        if not path.exists():
            path.write_text(temp, encoding=LATEX_CONFIG_DIC["encoding"])
        else:
            LOGGER.debug(f"File {path} already exists.")
