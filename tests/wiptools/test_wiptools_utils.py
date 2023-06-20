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
from random import randint

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


def random_element_from_str(s: str) -> str:
    r = randint(0,len(s)-1)
    if r >= len(s):
        print( f"oops {r=}>={len(s)=}")
    assert r < len(s)
    c = s[r]
    return c

def test_verify_project_name():
    az = 'abcdefghijklmnopqrstuwxyz'
    azAZ = az+az.upper()
    numbers = '0123456789'
    other = '-_'
    azAZnumbersother = azAZ+numbers+other

    for i in range(100):
        s = random_element_from_str(azAZ)
        length = randint(0,10)
        for j in range(length):
            s += random_element_from_str(azAZnumbersother)
        assert utils.verify_project_name(s)

    for i in range(100):
        s = random_element_from_str(numbers+other+'!@#$%^&*()_+-=§±,./<>?;:[]{}')
        length = randint(0,10)
        for j in range(length):
            s += random_element_from_str(azAZnumbersother)
        assert not utils.verify_project_name(s)

    for i in range(100):
        s = random_element_from_str(azAZ)
        length = randint(0, 10)
        for j in range(length):
            s += random_element_from_str(azAZnumbersother+" ")
        assert  utils.verify_project_name(s) ==  (' ' not in s)

# def test_pep8_module_name():


# ==============================================================================
# The code below is for debugging a particular test in eclipse/pydev.
# (normally all tests are run with pytest)
# ==============================================================================
if __name__ == "__main__":
    the_test_you_want_to_debug = test_verify_project_name

    print(f"__main__ running {the_test_you_want_to_debug}")
    the_test_you_want_to_debug()
    print('-*# finished #*-')
# eof
