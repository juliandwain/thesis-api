# aerospace-thesis-api

This repository should serve as an interface from the aerospace-thesis-code repository to the aerospace-thesis repository.

## Auxiliary Files

### Check for Input Statements

- ``check_inputs.py``
  - checks every input statement in every .tex file and prints to the console if the .tex file does not exist

### Clean up Empty Directories

- ``cleanup.py``
  - cleans up empty directories
  - this file is called via the command line as follows

    ```properties
    python cleanup.py --delete 0
    ```

  - herein, the argument can either be ``0`` if the empty directories should only be given to the user as output (informational) or ``1`` if the empty directories should also be deleted

- ``cleanup.bat``
  - this file calls ``latexmk -c`` to clean up all LaTeX auxiliary files and also calls ``cleanup.py`` with arg ``1``

### Initialize Chapter Directories

- ``init_chapter_dir.py``
  - this file initializes empty chapter directories with sections and subsections as well as folders for possible figures, tables, or pseudo code files for each individual chapter/section/subsection
  - the folder structure for each chapter is defined in the ``chapter.json`` file located in the ``templates`` folder

