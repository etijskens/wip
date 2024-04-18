import os
from pathlib import Path
import wiptools

try:
    home = os.environ['VSC_HOME']
except KeyError:
    home = os.environ['HOME']
WORKSPACE = (Path(home) / 'workspace').resolve()


def test_get_project_dir():
    expected = WORKSPACE / 'wiptools'

    project_dir = wiptools.get_project_dir()
    print(f"{project_dir =}")
    assert project_dir == expected

    project_dir = wiptools.get_project_dir(__file__)
    print(f"{project_dir =}")
    assert project_dir == expected

    project_dir = wiptools.get_project_dir(project_dir)
    print(f"{project_dir =}")
    assert project_dir == expected

def test_get_project_dir_nested():
    p = Path(__file__).parent / 'a_nested_project_directory/some_directory/another_nested_project_directory/some_other_directory'
    project_dir = wiptools.get_project_dir(p)
    expected = Path(__file__).parent / 'a_nested_project_directory/some_directory/another_nested_project_directory'
    assert project_dir == expected

    top_project_dir = wiptools.get_project_dir(p,outer=True)
    expected = WORKSPACE / 'wiptools'
    assert project_dir == expected

    assert wiptools.get_project_dir(p,outer=True).parent == WORKSPACE

def test_get_workspace_dir():
    expected = WORKSPACE

    project_dir = wiptools.get_workspace_dir()
    print(f"{project_dir =}")
    assert project_dir == expected

    project_dir = wiptools.get_workspace_dir(__file__)
    print(f"{project_dir =}")
    assert project_dir == expected


# ==============================================================================
# The code below is for debugging a particular test in eclipse/pydev.
# (normally all tests are run with pytest)
# ==============================================================================
if __name__ == "__main__":
    the_test_you_want_to_debug = test_get_workspace_dir

    print(f"__main__ running {the_test_you_want_to_debug}")
    the_test_you_want_to_debug()
    print('-*# finished #*-')
# eof
