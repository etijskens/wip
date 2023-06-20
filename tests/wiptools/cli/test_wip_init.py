# -*- coding: utf-8 -*-

"""Tests for `wip init`."""

from pathlib import Path
import subprocess
import sys

path = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(path))

import pytest

from helpers import run_wip, test_workspace
import wiptools.utils as utils


def test_init_project_name_exists():
    with utils.in_directory(test_workspace(clear=True)):
        foo_path = Path('foo')
        with open(foo_path, 'w') as f:
            f.write("blablabla")

        result = run_wip(['init', 'foo'], assert_exit_code=False)
        pytest.raises(FileExistsError)

        foo2_path = Path('foo2')
        foo2_path.mkdir()
        result = run_wip(['init', 'foo2'], assert_exit_code=False)
        pytest.raises(FileExistsError)


def test_init_project_name_does_not_exist():
    # test with no config file given
    with utils.in_directory(test_workspace(clear=True)):
        project = 'foo'
        result = run_wip( ['-vv', '--config', '.wip/config.json', 'init', project]
                        , stdin='bert tijskens\n'
                                'engelbert.tijskens@uantwerpen.be\n'
                                '\n'                        # default github_username
                                'foo description\n'         #
                                '\n'
                        , assert_exit_code=False)
        project_path = Path(project)
        assert project_path.is_dir()

        # run the tests for the project
        with utils.in_directory(project_path):
            completed_process = subprocess.run(['pytest', 'tests'])
            assert completed_process.returncode == 0

        project = 'bar'
        result = run_wip( ['-vv', '--config', '.wip/config.json', 'init', project]
                        , assert_exit_code=False)
        project_path = Path(project)
        assert project_path.is_dir()

        # run the tests for the project
        with utils.in_directory(project_path):
            completed_process = subprocess.run(['pytest', 'tests'])
            assert completed_process.returncode == 0



# ==============================================================================
# The code below is for debugging a particular test in eclipse/pydev.
# (normally all tests are run with pytest)
# ==============================================================================
if __name__ == "__main__":
    the_test_you_want_to_debug = test_init_project_name_does_not_exist

    print(f"__main__ running {the_test_you_want_to_debug}")
    the_test_you_want_to_debug()
    print('-*# finished #*-')
# eof
