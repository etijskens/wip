# -*- coding: utf-8 -*-
import json
from pathlib import Path
import subprocess

import click

import wiptools.messages as messages
from wiptools.tree import tree
import wiptools.utils as utils


def wip_build(ctx: click.Context):
    """build binary extensions"""

    cookiecutter_params = utils.read_wip_cookiecutter_json()
    build = BuildBinaryExtension(cookiecutter_params)

    component = ctx.params['component']
    if component:
        with messages.TaskInfo(f"Building binary extension"):
            build(component)
    else:
        # iterate over all components and add them to `docs/api-reference.md`
        with messages.TaskInfo(f"building all binary extensions"):
            utils.iter_components(
                Path(cookiecutter_params['project_path']) / cookiecutter_params['package_name'],
                apply=build
            )


class BuildBinaryExtension:
    """A Functor for building binary extension modules."""
    def __init__(self, cookiecutter_params):
        self.cookiecutter_params = cookiecutter_params

    def __call__(self, path_to_component: Path):
        """Build this component's binary extension module."""
        component_type = utils.component_type(path_to_component)

        if component_type == 'cpp':
            self.build_cpp(path_to_component)

        elif component_type == 'f90':
            self.build_f90(path_to_component)

    def build_cpp(self, path_to_component):
        """Build C++ module."""
        with messages.TaskInfo(f"Building C++ binary extension `{path_to_component.relative_to(self.cookiecutter_params['project_path'])}`"):
            pass

    def build_f90(self, path_to_component):
        """Build f90 module."""
        with messages.TaskInfo(f"Building Modern Fortran binary extension "
                               f"`{path_to_component.relative_to(self.cookiecutter_params['project_path'])}`"):
            pass
