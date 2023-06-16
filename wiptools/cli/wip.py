# -*- coding: utf-8 -*-

"""
# Command line interface wip.

Create projects, add components, documentation, ...
"""
from pathlib import Path
import sys
from types import SimpleNamespace

import click

import wiptools
import wiptools.messages as messages

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
@click.pass_context
def main(ctx, verbosity, version):
    """Command line interface wip.
    """
    if not ctx.invoked_subcommand:
        if version:
            print(wip_version())

    if verbosity:
        print(wip_version())

    # store global options in ctx.obj
    ctx.obj = SimpleNamespace(verbosity=verbosity)


@main.command()
@click.argument('project_name')
@click.pass_context
def init( ctx
        , project_name: str
        ):
    """Initialize a new project.

    Args:
        project_name: name of the project to create.
    """
    if ctx.obj.verbosity:
        click.echo(F"wip init {project_name}")

    project_path = Path(project_name)
    if project_path.is_file():
        messages.error_message(f"A file with name '{project_name}' exists already.")
    if project_path.is_dir():
        messages.error_message(f"A directory with name '{project_name}' exists already.")

    # project_path.mkdir(exist_ok=False)

    return 0

if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
#eodf
