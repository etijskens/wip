# -*- coding: utf-8 -*-

"""
# Python package wiptools

Common tools between the CLIs
"""

__version__ = "1.3.3"

import copy
from pathlib import Path
import json

def version():
    return f"wiptools v{__version__}"


def is_project_dir(path: Path) -> bool:
    return (path / 'wip-cookiecutter.json').is_file()


def get_project_dir(p: Path = None, outer: bool = False) -> Path:
    """Return the innermost or outermost project directory containing Path `p`.
    
    Args:
        p (Path, optional): Defaults to `None`, in which case the current working
            directory is used.
        outer (bool, optional): if `False` return the innermost project directory of `p`
            is returned. Otherwise, the outermost project directory is returned.

    Returns: Path to the innermost or outermost project directory containing `p`.

    Raises:
        ValueError: if the `p` is not inside a project directory.
    """
    p_ = Path.cwd() if p is None else Path(p)
    outer_project_dir = None
    if p_.is_file():
        p_ = p_.parent
    # Look for wip-cookiecutter.json
    while True:
        if is_project_dir(p_):
            if outer:
                outer_project_dir = p_
                p_ = p_.parent
            else:
                return p_
        else:
            p_ = p_.parent
            if p_ == Path('/'):
                if outer and outer_project_dir is not None:
                    return outer_project_dir
                else:
                    raise ValueError(f"Path `{p_}` is not inside a project directory")

def get_workspace_dir(p: Path = None) -> Path:
    """Convenience method that obtains the workspace directory containing Path `p`.
    This is the parent of the inner project directory."""
    return get_project_dir(p, outer=True).parent


# global stuff
COMPONENT_TYPES = {
    'py' : 'Python module',
    'cpp': 'C++ binary extension',
    'f90': 'Modern Fortran binary extension',
    'cli': 'CLI'
}

DOCUMENTATION_FORMATS = {
    'md' : 'Markdown',
    'rst': 'restructuredText',
    ''   : 'none'
}
