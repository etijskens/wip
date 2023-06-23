# -*- coding: utf-8 -*-
import fnmatch
from pathlib import Path
from typing import List

import click


# prefix components:
space =  '    '
branch = '│   '
# pointers:
tee =    '├── '
last =   '└── '


def tree(dir_path: Path, prefix: str='', **style_kwargs):
    """A recursive generator, given a directory Path object
    will yield a visual tree structure line by line
    with each line prefixed by the same characters

    """
    contents = list(dir_path.iterdir())
    keep = []
    for item in contents:
        if item.is_dir() and str(item) != '__pycache__': # ignore __pycache__
            # only if the directory contains a .py file we keep it.
            if list(item.glob('*.py')):
                keep.append(item)
        else:
            if str(item).endswith('.py'):
                keep.append(item)
    contents = keep

    # contents each get pointers that are ├── with a final └── :
    pointers = [tee] * (len(contents) - 1) + [last]
    for pointer, path in zip(pointers, contents):
        s = prefix + pointer + path.name
        if path.is_dir():
            s += click.style(' [python module]', **style_kwargs)
        yield s

        if path.is_dir(): # extend the prefix and recurse:
            extension = branch if pointer == tee else space
            # i.e. space because last, └── , above so no more |
            yield from tree(path, prefix=prefix+extension, **style_kwargs)
