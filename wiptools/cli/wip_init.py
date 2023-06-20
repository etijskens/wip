# -*- coding: utf-8 -*-
import json
from pathlib import Path
import subprocess

import click
from cookiecutter.main import cookiecutter

import wiptools.messages as messages
import wiptools.utils as utils


def wip_init(ctx: click.Context) -> int:
    """Actual body of wip subcommand `wip init ...`.

    Returns:
        0 if successful, non-zero otherwise
    """
    if ctx.parent.params['verbosity']:
        click.echo(F"wip init {ctx.params['project_name']}")

    project_name = ctx.params['project_name']
    project_path = Path(project_name)
    if project_path.is_file():
        messages.error_message(f"A file with name '{project_name}' exists already.")
    if project_path.is_dir():
        messages.error_message(f"A directory with name '{project_name}' exists already.")

    cookiecutter_params = utils.get_config(
        ctx.parent.params['config']
      , needed={ 'full_name'      : { 'question': 'Enter your full name'}
               , 'email_address'  : { 'question': 'Enter your email address'}
               , 'github_username': { 'question': 'Enter your GitHub username (leave empty if no remote repos needed)'
                                    , 'default' : ''}
               }
    )

    no_github_username = not bool(cookiecutter_params['github_username'])

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

    # Perform initial git commit:
    completed_process = subprocess.run(['git', 'commit', '-a', '-m', '"Initial commit"'])
    if completed_process.returncode:
        messages.error_message('Failing git command.')

    # Create remote GitHub repo if requested:
    remote = ctx.params['remote'].lower()
    if not remote in ['public','private', 'none', 'None']:
        messages.error_message(
            f"ERROR: --remote={remote} is not a valid option. Valid options are:\n"
            f"       --remote=public\n"
            f"       --remote=private\n"
            f"       --remote=none\n"
        )
    if remote.lower() != 'none':
        if no_github_username:
            messages.error_message("A GitHub username must be supplied to create remote GitHub repositories.")


    return return_code