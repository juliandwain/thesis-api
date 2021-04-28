# -*- coding: utf-8 -*-

import json
import pathlib
import shutil
import unittest

from api import ENCODING, TEX_FILE
from api.tools.maintenance import Maintainer


class TestMaintainer(unittest.TestCase):
    def setUp(self) -> None:
        self.thesis_dir = pathlib.Path("./tests/data")
        self.chapter_dir = self.thesis_dir / "chapters/"
        self.thesis_dir.mkdir(parents=True, exist_ok=True)
        self.chapter_dir.mkdir(parents=True, exist_ok=True)

        self.maint = Maintainer(self.thesis_dir)
        template = self.thesis_dir / "chapter.json"
        with template.open(mode="r", encoding=ENCODING) as file:
            self.data = json.load(file)

    def tearDown(self) -> None:
        shutil.rmtree(self.chapter_dir)

    def test_check_inputs(self):
        self.maint.init_chapter_dir(
            self.data["chapter"],
            self.data["sections"],
            self.data["subsections"],
        )
        self.maint.check_inputs(self.thesis_dir)
        assert self.maint.counter == 0

    def test_create_ftc(self):
        typ = (
            {"figs": True, "tabs": True, "code": True},
            {"figs": True, "tabs": True, "code": False},
            {"figs": True, "tabs": False, "code": False},
            {"figs": False, "tabs": True, "code": True},
            {"figs": False, "tabs": False, "code": True},
            {"figs": False, "tabs": True, "code": False},
            {"figs": True, "tabs": False, "code": True},
            {"figs": False, "tabs": False, "code": False},
        )
        for t in typ:
            self.maint.create_ftc(self.chapter_dir, t)
            for k, v in t.items():
                assert (
                    f := self.chapter_dir / k
                ).exists() == v, f"{f} {'exists' if f.exists() else 'does not exist'} even though it {'should not' if not v else 'should'}!"
                if f.exists():
                    shutil.rmtree(f)

    def test_init_chapter(self):
        self.maint.init_chapter_dir(
            self.data["chapter"],
            self.data["sections"],
            self.data["subsections"],
        )

        def check_files(path: pathlib.Path, m=self.maint, t=self.thesis_dir):
            for child in path.iterdir():
                if child.is_dir():
                    if any(child.iterdir()):
                        check_files(child)
                else:
                    if TEX_FILE in child.parts[-1]:
                        for inp in m.find_input(child):
                            assert (
                                n := t.resolve() / inp
                            ).exists(), (
                                f"Expected {n} to exists but it does not!"
                            )

        check_files(self.chapter_dir)


if __name__ == "__main__":
    unittest.main()