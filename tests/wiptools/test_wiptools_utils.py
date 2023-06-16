# -*- coding: utf-8 -*-

"""Tests of wiptools.utils"""

from pathlib import Path
import shutil
import sys

path = Path(__file__).parent.parent.parent
# print(path)
sys.path.insert(0, str(path))
from tempfile import TemporaryDirectory
# import pytest
import wiptools
import wiptools.utils as utils


def test_in_directory():
    with TemporaryDirectory(dir=Path.cwd()) as tmp:
        with utils.in_directory(tmp):
            assert Path.cwd().name == Path(tmp).name
            foo_path = Path('foo')
            with open(foo_path, 'w') as f:
                f.write("blablabla")
            assert foo_path.is_file()
            foo_path = foo_path.resolve()
        assert foo_path.is_file()

    # print(f"{tmp=}")
    assert Path(tmp).is_dir() == False


# ==============================================================================
# The code below is for debugging a particular test in eclipse/pydev.
# (normally all tests are run with pytest)
# ==============================================================================
if __name__ == "__main__":
    the_test_you_want_to_debug = test_in_directory

    print(f"__main__ running {the_test_you_want_to_debug}")
    the_test_you_want_to_debug()
    print('-*# finished #*-')
# eof
