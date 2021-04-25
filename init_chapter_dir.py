# -*- coding: utf-8 -*-

__doc__ = """Initialize a chapter directory with template files.
"""

import json
import pathlib
import string

from conf import ENCODING, TEX_FILE, get_logger
from api.tools import ChapterTemplate, SectionTemplate, SubsectionTemplate

# import string

LOGGER = get_logger(__name__)

TEMPLATE_FOLDER = pathlib.Path("./templates")
# INPUT_TEMPLATE_ = string.Template()
INPUT_TEMPLATE = string.Template("\n\\input{$path}\n")


def open_template(typ: str) -> string.Template:
    """Open a LaTeX template defined by ``typ``.

    Parameters
    ----------
    typ : str
        The type of LaTeX template to open.

    Returns
    -------
    string.Template
        The template.

    """
    if typ == "chapter":
        return ChapterTemplate()
    elif typ == "section":
        return SectionTemplate()
    elif typ == "subsection":
        return SubsectionTemplate()
    else:
        raise NotImplementedError


def tex_file(path: pathlib.Path, temp: str) -> None:
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
        with path.open(mode="w", encoding=ENCODING, newline="\n") as file:
            file.write(temp)
    else:
        LOGGER.debug(f"File {path} already exists.")


def create_ftc(path: pathlib.Path, typ: dict) -> None:
    """Create the figs, tabs, and/or code directories.

    Parameters
    ----------
    path : pathlib.Path
        The path in which the ftc-direcotires should be created.
    typ : dict
        A dictionary containing information abouth which of the directories
        should be created at a given level.

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


def create(
    path: pathlib.Path, chapter: dict, sections: list, subsections: dict,
) -> None:
    """Create a chapter template directory.

    Parameters
    ----------
    path : pathlib.Path
        The path in which the chapter should be created.
    chapter : dict
        The chapter configuration dict.
    sections : list
        The section configuration list.
    subsections : dict
        The subsection configuration dict.

    """
    # get the type of folder to create
    chapter_type = next(iter(chapter))
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
    chapter_path = path / chapter_
    try:
        chapter_path.mkdir(parents=True, exist_ok=False)
    except FileExistsError as e:
        LOGGER.critical(
            f"{chapter_path} already exists!\nMaybe you want to create a new chapter?\n"
        )
        raise e
    chapter_file = chapter_path / (chapter_ + TEX_FILE)
    # create the chapter directories
    create_ftc(chapter_path, chapter)
    # open the chapter template
    chapter_template = open_template(chapter_type)
    chapter_template_str = chapter_template.substitute(
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
            sec_file = sec_dir / (sec_ + TEX_FILE)
            # open the section template
            sec_template = open_template(sec_type)
            sec_template_str = sec_template.substitute(
                title=f"{chapter_}-{sec_}", label=f"{chapter_}-{sec_}",
            )
            # create the section directories
            create_ftc(sec_dir, section)
            chapter_template_str += INPUT_TEMPLATE.substitute(
                path=f"{sec_file}".replace("\\", "/")
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
                    subsec_file = subsec_dir / (subsec_ + TEX_FILE)
                    # open the subsection template
                    subsec_template = open_template(subsec_type)
                    # create the subsection latex file
                    subsec_template_str = subsec_template.substitute(
                        title=f"{chapter_}-{sec_}-{subsec_}",
                        label=f"{chapter_}-{sec_}-{subsec_}",
                    )
                    tex_file(
                        subsec_file, subsec_template_str,
                    )
                    # create the subsection directories
                    create_ftc(subsec_dir, subsection)
                    sec_template_str += INPUT_TEMPLATE.substitute(
                        path=f"{subsec_file}".replace("\\", "/")
                    )
            else:
                LOGGER.debug(f"No Subsections created in {sec_dir}!")
            # create the section latex file
            tex_file(sec_file, sec_template_str)

    else:
        LOGGER.debug(f"No Sections created in {chapter_path}!")
    # create the chapter latex file
    tex_file(chapter_file, chapter_template_str)


def main() -> None:
    """Main function.
    """
    chapters = pathlib.Path("./chapters")
    chapter_info = pathlib.Path("./templates/chapter.json")
    with chapter_info.open(mode="r", encoding=ENCODING) as file:
        data = json.load(file)
    create(
        chapters, data["chapter"], data["sections"], data["subsections"],
    )


if __name__ == "__main__":
    main()
