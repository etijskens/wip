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
@click.pass_context
def init( ctx
        , project_name: str
        , python_version: str
        , description: str
        ):
    """Initialize a new project.

    Args:
        project_name: name of the project to create.
    """

    return wip_init(ctx)


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
#eodf
