# -*- coding: utf-8 -*-
import json
from pathlib import Path

import click
from cookiecutter.main import cookiecutter

import wiptools.messages as messages
import wiptools.utils as utils


def wip_init(ctx: click.Context) -> int:
    """Function called by `wip init ...`.

    Returns:
        0 if successful, non-zero otherwise
    """
    return_code = 0
    if ctx.parent.params['verbosity']:
        click.echo(F"wip init {ctx.params['project_name']}")

    project_name = ctx.params['project_name']
    project_path = Path(project_name)
    if project_path.is_file():
        return_code = 1
        messages.error_message(f"A file with name '{project_name}' exists already.")
    if project_path.is_dir():
        return_code = 1
        messages.error_message(f"A directory with name '{project_name}' exists already.")

    cookiecutter_params = utils.get_config(
        ctx.parent.params['config']
      , needed={ 'full_name'      : { 'question': 'Enter your full name'}
               , 'email_address'  : { 'question': 'Enter your email address'}
               , 'github_username': { 'question': 'Enter your GitHub username (leave empty if no remote repos needed)'
                                    , 'default' : ''}
               }
    )
    click.secho("\nProject info needed:", fg='green')
    project_short_description = ctx.params['description'] if ctx.params['description'] else messages.ask(
        'Enter a short description for the project:', default='<project_short_description>'
    )
    minimal_python_version = ctx.params['python_version'] if ctx.params['python_version'] else messages.ask(
        'Enter the minimal Python version', default='3.8'
    )

    cookiecutter_params.update(
      { 'project_name' : project_name
      , 'package_name' : utils.pep8_module_name(project_name)
      , 'project_short_description': project_short_description
      , 'minimal_python_version': minimal_python_version
      }
    )

    cookiecutter( template=str(utils.cookiecutters() / 'project')
                , extra_context=cookiecutter_params
                , output_dir=Path.cwd()
                , no_input=True
                )

    return return_code