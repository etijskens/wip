# -*- coding: utf-8 -*-

"""
# Command line interface wip.

Create projects, add components, documentation, ...
"""
from pathlib import Path
import sys

import click

import wiptools
from wiptools.wip.wip_add   import wip_add
from wiptools.wip.wip_bump  import wip_bump
from wiptools.wip.wip_build import wip_build
from wiptools.wip.wip_docs  import wip_docs
from wiptools.wip.wip_env   import wip_env
from wiptools.wip.wip_info  import wip_info
from wiptools.wip.wip_init  import wip_init
from wiptools.wip.wip_remote_repo  import wip_remote_repo

def wip_version():
    return f"wip CLI v{wiptools.__version__}"

@click.group(invoke_without_command=True)
@click.option('-v', '--verbosity', count=True
             , help="The verbosity of the program output."
             )
@click.option('--version'
             , help="Print the wiptools version number."
             , is_flag=True
             )
@click.option('--config', default=Path.home() / '.wiptools' / 'config.json'
             , type=Path
             , help='The location (path) of the config.file with developer information (name, e-mail address, '
                    'GitHub username, GitHub personal access token). If it does not exist, the application creates the '
                    'file, asks for missing the information and stores it in the file. If the file exists, it is kept '
                    'without modification (i.e. missing parameters supplied by the user are not stored).'
             )
@click.pass_context
def wip(ctx: click.Context, verbosity, version, config):
    """Command line interface wip.
    """
    if not ctx.invoked_subcommand:
        print(wip_version())

    if verbosity:
        print(wip_version())

@wip.command()
@click.argument('project_name')
@click.option('--python-version', default=''
             , help='The minimal Python version for the project.'
             )
@click.option('--description', '-d', default=''
             , help='A short description of project.'
             )
@click.option('--remote'
             , help="Create a remote GitHub repo with visibility 'public' (default) or 'private'. "
                    "If 'none' is specified no remote is created. This option is case-insensitive."
                    "The creation of a remote GitHub repo requires a GitHub username and a personal "
                    "access token with `repo` and `read:org` permissions."
             , default='public'
             )
@click.option('--md', is_flag=True
             , help='Add documentation templates in Markdown format to this project. (This is the default case).'
             )
@click.option('--rst', is_flag=True
             , help='Add documentation templates in restructuredText format to this project.'
             )
@click.pass_context
def init( ctx
        , project_name: str
        , python_version: str
        , description: str
        , remote: str
        , md: bool
        , rst: bool
        ):
    """Initialize a new project skeleton.

    Args:
        project_name: name of the project folder to create.
    """
    # allow only one documentation format
    if md:
        rst = False
    if rst:
        md = False

    assert ctx.params['md'] == md
    assert ctx.params['rst'] == rst

    wip_init(ctx)


@wip.command()
@click.pass_context
def env(ctx):
    """Check the environment for needed components."""
    wip_env(ctx)


@wip.command()
@click.option('--fmt', '-f', type=click.Choice(['md', 'rst']), default='md'
             , help="Documentation format to be used (md=Markdown (default), rst=restructuredText)."
             )
@click.pass_context
def docs(ctx: click.Context, fmt):
    """Add documentation to the project."""
    wip_docs(ctx)


@wip.command()
@click.argument('name')
@click.option('--py', is_flag=True
             , help='Add a Python submodule to the project.'
             )
@click.option('--cli', is_flag=True
             , help='Add a Python CLI (with a single command) to the project.'
             )
@click.option('--clisub', is_flag=True
             , help='Add a Python CLI with subcommands to the project.'
             )
@click.option('--cpp', is_flag=True
             , help='Add a C++ binary extension module to the project (building requires nanobind and CMake).'
             )
@click.option('--f90', is_flag=True
             , help='Add a Modern Fortran binary extension module to the project (building requires numpy.f2py and CMake).'
             )
@click.pass_context
def add(ctx: click.Context, name, py, cpp, f90, cli, clisub):
    """Add components, such as submodules and CLIs, to the project.

    Args:
        name: For submodules the name can contain a path to an already existion component relative to the package
            directory. CLI names must not contain a path, only a name.
    """
    wip_add(ctx)


@wip.command()
@click.option('--short', '-s', default=False, is_flag=True
             , help='List short project info (suppress project tree).'
             )
@click.pass_context
def info(ctx: click.Context, short):
    """List info about the project's structure."""

    wip_info(ctx)


@wip.command()
@click.argument('component', default='')
@click.option('--cpp', is_flag=True, default=False
             , help='Build all C++ binary extension modules.'
             )
@click.option('--f90', is_flag=True, default=False
             , help='Build all Modern Fortran binary extension modules.'
             )
@click.pass_context
def build(ctx: click.Context, component: str, f90: bool, cpp: bool):
    """Build binary extension modules.

    Args:
        component: Path to the component to build, relative to package directory.
    """

    wip_build(ctx)


@wip.command()
@click.option('--private', is_flag=True, default=False
             , help='Add a private remote GitHub repo, otherwise a public one.'
             )
@click.pass_context
def remote(ctx: click.Context, private: bool):
    """Add a remote GitHub repo."""

    wip_remote_repo(ctx)


@wip.command()
@click.argument('args', type=str, default='')
@click.pass_context
def bump(ctx: click.Context, args: str):
    """Bump2version wrapper.

    Args:
        args: a quoted str containing the bump2version arguments.
    """

    wip_bump(ctx)




if __name__ == "__main__":
    sys.exit(wip())  # pragma: no cover
