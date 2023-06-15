# -*- coding: utf-8 -*-
"""
# Command line interface wip.

Create projects, add components, documentation, ...
"""
from pathlib import Path
import sys
from types import SimpleNamespace

import click


@click.group()
@click.option('-v', '--verbosity', count=True
             , help="The verbosity of the program output."
             , default=1
             )
@click.pass_context
def main(ctx, verbosity):
    """Command line interface wip.
    """
    # store global options in ctx.obj
    ctx.obj = SimpleNamespace(verbosity=verbosity)

    click.echo(f"running wip")


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
    click.echo("running wip init")
    project_path = Path(project_name)
    if project_path.is_file():
        raise FileExistsError(f"A file with name '{project_name}' exists already.")
    if project_path.is_dir():
        raise FileExistsError(f"A directory with name '{project_name}' exists already.")

    project_path.mkdir(exist_ok=False)

    return 0

if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
#eodf
