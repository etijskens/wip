# -*- coding: utf-8 -*-
import json
from pathlib import Path
from typing import Callable

import click

from wiptools import DOCUMENTATION_FORMATS
import wiptools.messages as messages
import wiptools.utils as utils
from wiptools.wip.wip_docs import get_documentation_format
from wiptools.wip.wip_env import wip_env


def wip_info(ctx: click.Context):
    """List project info."""

    cookiecutter_params = utils.read_wip_cookiecutter_json()

    project_path = Path.cwd()
    package_name = cookiecutter_params['package_name']

    # project version
    toml = utils.read_pyproject_toml()
    version     = toml['tool']['poetry']['version']
    repository  = toml['tool']['poetry']['repository']
    homepage    = toml['tool']['poetry']['homepage']
    description = toml['tool']['poetry']['description']
    print(
        f"Project    : {project_path.name}: {description}\n"
        f"Version    : {version}\n"
        f"Package    : {package_name}\n"
        f"GitHub repo: {'--' if not repository else repository}\n"
        f"Home page  : {'--' if not homepage else homepage}\n"
        f"Location   : {project_path}\n"
        f"docs format: {DOCUMENTATION_FORMATS[get_documentation_format()]}\n"
    )

    # developer info
    if ctx.params['dev']:
        print(
            f"Developer info:\n"
            f"  author         : {cookiecutter_params['full_name']}\n"
            f"  e-mail         : {cookiecutter_params['email_address']}\n"
            f"  GitHub username: {cookiecutter_params['github_username']}\n"
        )

    # Package structure
    if ctx.params['pkg']:
        click.secho(f"Structure of Python package {package_name}", fg='bright_blue')
        paths = DisplayablePath.make_tree(
            project_path / package_name
          , criteria=criteria
        )
        for path in paths:
            click.echo('  ' + path.displayable())

    # Run environment check
    if ctx.params['env']:
        wip_env(ctx)

def criteria(path: Path):
    if path.is_dir():
        return path.name != '__pycache__' and path.name != '_cmake_build'
    else:
        return path.suffix in ['.py', '.cpp', '.f90', '.md', 'rst', '.so']


class DisplayablePath:
    """Class for printing the tree structure of a python package.

    Adapted from https://stackoverflow.com/questions/9727673/list-directory-tree-structure-in-python.
    """
    display_filename_prefix_middle = '├──'
    display_filename_prefix_last = '└──'
    display_parent_prefix_middle = '    '
    display_parent_prefix_last = '│   '

    def __init__(self, path: Path, parent_path: Path, is_last: bool):
        self.path = Path(str(path))
        self.parent = parent_path
        self.is_last = is_last
        if self.parent:
            self.depth = self.parent.depth + 1
        else:
            self.depth = 0

    @property
    def displayname(self):
        if self.path.is_dir():
            component_string = utils.component_string(self.path)
            return click.style(component_string, fg='blue')

        if self.is_shared_object():
            dot = self.path.name.find('.')
            stem = self.path.name[:dot]
            sufx = self.path.name[dot:]
            return click.style(stem, fg='blue') + click.style(sufx, fg='cyan')

        return click.style(self.path.name, fg='cyan')

    def is_shared_object(self):
        return self.path.suffix in ('.so', '.dll', '.dylib')

    @classmethod
    def make_tree( cls,
        root: Path,
        parent: Path=None,
        is_last: bool=False,
        criteria: Callable=None
    ):
        """Create a generator that produces a tree structure of a python package."""
        root = Path(str(root))
        criteria = criteria or cls._default_criteria

        displayable_root = cls(root, parent, is_last)
        yield displayable_root

        children = sorted(
            list(path for path in root.iterdir() if criteria(path)),
            key=lambda s: str(s).lower()
        )
        count = 1
        for path in children:
            is_last = count == len(children)
            if path.is_dir():
                yield from cls.make_tree(path,
                                         parent=displayable_root,
                                         is_last=is_last,
                                         criteria=criteria)
            else:
                yield cls(path, displayable_root, is_last)
            count += 1

    @classmethod
    def _default_criteria(cls, path: Path):
        return True

    def displayable(self):
        if self.parent is None:
            return self.displayname

        _filename_prefix = (self.display_filename_prefix_last
                            if self.is_last
                            else self.display_filename_prefix_middle)

        parts = ['{!s} {!s}'.format(_filename_prefix,
                                    self.displayname)]

        parent = self.parent
        while parent and parent.parent is not None:
            parts.append(self.display_parent_prefix_middle
                         if parent.is_last
                         else self.display_parent_prefix_last)
            parent = parent.parent

        return ''.join(reversed(parts))
