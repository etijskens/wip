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


    flag_py     = ctx.params['py']
    flag_cpp    = ctx.params['cpp']
    flag_f90    = ctx.params['f90']
    flag_cli    = ctx.params['cli']
    flag_clisub = ctx.params['clisub']
    nflags_set = flag_py + flag_cpp + flag_f90 + flag_cli + flag_clisub
    if nflags_set > 1:
        messages.error_message(
            "It is illegal to specify more than one component flags\n"
            "(--py|--cpp|--f90|--cli|--clisub"
        )

    cookiecutter_params = utils.read_wip_cookiecutter_json()
    project_path = Path.cwd()
    package_name = cookiecutter_params['package_name']
    component = ctx.params['component']

    if flag_py or flag_cpp or flag_f90:

        module_path = project_path / package_name / component
        module_name = module_path.name
        parent_module = module_path.parent.name
        parent_pypath = str(module_path.parent.relative_to(project_path)).replace(os.sep,'.') + '.'

        if not module_path.parent.is_dir():
            messages.error_message(f"The parent directory `{module_path.parent}` does not exist.")

        cookiecutter_params.update(
          { 'module_name' : module_name
          , 'parent_module'  : parent_module
          , 'parent_pypath'  : parent_pypath
          }
        )

        template = str(utils.cookiecutters() / 'module-py' ) if flag_py  else \
                   str(utils.cookiecutters() / 'module-cpp') if flag_cpp else \
                   str(utils.cookiecutters() / 'module-f90')

        with messages.TaskInfo(f"Expanding cookiecutter template `{template}`"):
            cookiecutter( template=template
                        , extra_context=cookiecutter_params
                        , output_dir=module_path.parent
                        , no_input=True
                        , overwrite_if_exists=True
                        )

        template = str(utils.cookiecutters() / 'module-py-tests' ) if flag_py  else \
                   str(utils.cookiecutters() / 'module-cpp-tests') if flag_cpp else \
                   str(utils.cookiecutters() / 'module-f90-tests')

        with messages.TaskInfo(f"Expanding cookiecutter template `{template}`"):
            cookiecutter( template=template
                        , extra_context=cookiecutter_params
                        , output_dir=(project_path / 'tests' / module_path.relative_to(project_path / package_name))
                        , no_input=True
                        , overwrite_if_exists=True
                        )

    elif flag_cli or flag_clisub:

        cli_path = project_path / package_name / 'cli' / component
        cli_name = cli_path.name
        # parent_module = cli_path.parent.name
        # parent_pypath = str(module_path.parent.relative_to(project_path)).replace(os.sep,'.') + '.'

        cli_path.parent.mkdir(parents=True, exist_ok=True)

        cookiecutter_params.update(
            {'cli_name': cli_name}
        )

        template = str(utils.cookiecutters() / 'cli'   ) if flag_cli else \
                   str(utils.cookiecutters() / 'clisub')

        with messages.TaskInfo(f"Expanding cookiecutter template `{template}`"):
            cookiecutter(template=template
                         , extra_context=cookiecutter_params
                         , output_dir=cli_path.parent
                         , no_input=True
                         , overwrite_if_exists=True
                         )

        template = str(utils.cookiecutters() / 'cli-tests') if flag_cli else \
                   str(utils.cookiecutters() / 'clisub-tests')

        with messages.TaskInfo(f"Expanding cookiecutter template `{template}`"):
            cookiecutter(template=template
                         , extra_context=cookiecutter_params
                         , output_dir=(project_path / 'tests' / cli_path.relative_to(project_path / package_name))
                         , no_input=True
                         , overwrite_if_exists=True
                         )
