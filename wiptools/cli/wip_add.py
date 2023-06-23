# -*- coding: utf-8 -*-
import os
from pathlib import Path
import shutil
import subprocess

import click
from cookiecutter.main import cookiecutter

import wiptools.messages as messages
import wiptools.utils as utils


def wip_add(ctx: click.Context):
    """Add submodules and CLIs."""

    cookiecutter_params = utils.read_wip_cookiecutter_json()

    project_path = Path.cwd()
    package_name = cookiecutter_params['package_name']
    submodule_path = project_path / package_name / ctx.params['submodule_path']
    submodule_name = submodule_path.name
    parent_module = submodule_path.parent.name
    parent_pypath = str(submodule_path.parent.relative_to(project_path)).replace(os.sep,'.') + '.'

    if not submodule_path.parent.is_dir():
        messages.error_message(f"The parent directory `{submodule_path.parent}` does not exist.")

    cookiecutter_params.update(
      { 'submodule_name' : submodule_name
      , 'parent_module'  : parent_module
      , 'parent_pypath'  : parent_pypath
      }
    )
    project_path = Path.cwd()

    template = str(utils.cookiecutters() / 'submodule-py')
    with messages.TaskInfo(f"Expanding cookiecutter template `{template}`"):
        cookiecutter( template=template
                    , extra_context=cookiecutter_params
                    , output_dir=submodule_path.parent
                    , no_input=True
                    , overwrite_if_exists=True
                    )

    template = str(utils.cookiecutters() / 'submodule-py-tests')
    output_dir = (project_path / 'tests' / submodule_path.relative_to(project_path / package_name))
    with messages.TaskInfo(f"Expanding cookiecutter template `{template}`"):
        cookiecutter( template=template
                    , extra_context=cookiecutter_params
                    , output_dir=output_dir
                    , no_input=True
                    , overwrite_if_exists=True
                    )
