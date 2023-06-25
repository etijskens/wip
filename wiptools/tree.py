# -*- coding: utf-8 -*-
# after https://stackoverflow.com/questions/9727673/list-directory-tree-structure-in-python
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
            #  if the directory contains a
            #    - .py file
            #    - .cpp file
            #    - .f90 file
            #    we keep it.
            for pattern in ['*.py', '*.cpp', '*.f90']:
                if list(item.glob(pattern)):
                    keep.append(item)
        else:
            if str(item).endswith('.py' ) \
            or str(item).endswith('.cpp') \
            or str(item).endswith('.f90') \
            or str(item).endswith('.md' ) \
            or str(item).endswith('.rst'):
                keep.append(item)
    contents = keep

    # contents each get pointers that are ├── with a final └── :
    pointers = [tee] * (len(contents) - 1) + [last]
    for pointer, path in zip(pointers, contents):
        s = prefix + pointer + path.name
        if path.is_dir():
            if list(path.glob('*.cpp')):
                s += click.style(' [C++ binary extension module]', **style_kwargs)
            elif list(path.glob('*.f90')):
                s += click.style(' [Modern Fortran binary extension module]', **style_kwargs)
            elif list(path.glob('__init__.py')):
                s += click.style(' [python module]', **style_kwargs)
            elif list(path.glob('__main__.py')):
                s += click.style(' [CLI]', **style_kwargs)
            else:
                s += click.style(' [???]', **style_kwargs)
        yield s

        if path.is_dir(): # extend the prefix and recurse:
            extension = branch if pointer == tee else space
            # i.e. space because last, └── , above so no more |
            yield from tree(path, prefix=prefix+extension, **style_kwargs)
