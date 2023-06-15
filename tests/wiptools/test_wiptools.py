# -*- coding: utf-8 -*-

from pathlib import Path
import shutil
import sys

path = Path(__file__).parent.parent.parent
print(path)
sys.path.insert(0, str(path))

# import pytest
import wiptools
import wiptools.utils as utils

def empty_test_workspace():
    """return the path to an empty test workspace."""
    test_ws = (Path(wiptools.__file__).parent.parent / '.test-workspace').resolve()
    if test_ws.exists():
        shutil.rmtree(test_ws)

    test_ws.mkdir(exist_ok=True)

    return test_ws

def test_in_directory():
    
    with utils.in_directory(empty_test_workspace()):
        assert Path.cwd().name == '.test-workspace'
        foo_path = Path('foo')
        with open(foo_path, 'w') as f:
            f.write("blablabla")
        assert foo_path.is_file()
        foo_path = foo_path.resolve()
    assert foo_path.is_file()

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
