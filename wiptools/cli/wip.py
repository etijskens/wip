# -*- coding: utf-8 -*-

"""
# Command line interface wip.

Create projects, add components, documentation, ...
"""
from pathlib import Path
import sys

import click

import wiptools
import wiptools.messages as messages
from wiptools.cli.wip_init import wip_init
from wiptools.cli.wip_env  import wip_env

def wip_version():
    return f"wip CLI v{wiptools.__version__}"

@click.group(invoke_without_command=True)
@click.option('-v', '--verbosity', count=True
             , help="The verbosity of the program output."
             )
@click.option('--version'
             , help="print wiptools version."
             , is_flag=True
             )
@click.option('--config', default=Path.home() / '.wip' / 'config.json', type=Path
             , help='location of config.file. If it does not exist, the config file is '
                    'created, otherwise it is kept without modification (i.e. missing '
                    'parameters are not stored).'
             )
@click.pass_context
def main(ctx, verbosity, version, config):
    """Command line interface wip.
    """
    # wip.main arguments are retrieved from ctx.parent.params
    # wip.some.subcommand arguments are retrieved from ctx.params

    if not ctx.invoked_subcommand:
        if version:
            print(wip_version())

    if verbosity:
        print(wip_version())

@main.command()
@click.argument('project_name')
@click.option('--python-version', default=''
             , help='minimal Python version'
             )
@click.option('--description', '-d', default=''
             , help='short description of project'
             )
@click.option('--remote-visibility'
             , help="Option for creating a remote GitHub repo with visibility `public` (default) or `private`. "
                    "If `none` is specified no remote is created. The option is case-insensitive."
             , default='public'
             )
@click.option('--md', is_flag=True
             , help='Add documentation templates (markdown format) to this project. (This is the default case).'
             )
@click.option('--rst', is_flag=True
             , help='Add documentation templates (restructuredText format) to this project.'
             )
@click.pass_context
def init( ctx
        , project_name: str
        , python_version: str
        , description: str
        , remote_visibility: str
        , md: bool
        , rst: bool
        ):
    """Initialize a new project.

    The creation of a remote GitHub repo requires a GitHub username and
    a personal access token with `repo` and `read:org` permissions.

    Args:
        project_name: name of the project to create.
    """
    # allow only one documentation format
    if md:
        rst = False
    if rst:
        md = False

    assert ctx.params['md'] == md
    assert ctx.params['rst'] == rst

    wip_init(ctx)


@main.command()
@click.pass_context
def env(ctx):
    """Check the environment for needed components."""
    wip_env(ctx)

@main.command()
@click.option('--md', is_flag=True
             , help='Add documentation templates (markdown format) to this project. (This is the default case).'
             )
@click.option('--rst', is_flag=True
             , help='Add documentation templates (restructuredText format) to this project.'
             )
@click.pass_context
def docs(ctx):
    """Add documentation to the project."""



if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
