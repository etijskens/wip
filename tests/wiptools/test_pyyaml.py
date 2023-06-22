# -*- coding: utf-8 -*-

"""Tests of pyyaml module, more exploration than testing actually"""

from pathlib import Path
import yaml
import shutil
import sys

path = Path(__file__).parent.parent.parent
# print(path)
sys.path.insert(0, str(path))

def test_read_yaml():
    conf = yaml.safe_load(Path('mkdocs.yml').read_text())
    print(f'{conf=}')


# ==============================================================================
# The code below is for debugging a particular test in eclipse/pydev.
# (normally all tests are run with pytest)
# ==============================================================================
if __name__ == "__main__":
    the_test_you_want_to_debug = test_read_yaml

    print(f"__main__ running {the_test_you_want_to_debug}")
    the_test_you_want_to_debug()
    print('-*# finished #*-')
