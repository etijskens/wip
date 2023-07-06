# -*- coding: utf-8 -*-
import importlib
from platform import python_version
from packaging.version import Version
import re
from subprocess import run
from typing import Callable,Tuple

import click

import wiptools.messages as messages
from wiptools.utils import subprocess_run_cmds


fg = {
    0: 'red',
    1: 'green'
}

def wip_env(ctx: click.Context):
    """Check the current environment for necessary components."""

    print(("For a full functional `wip` the following commands and packages must be available in our environment:\n"))

    ok = True
    ok &= has_python('3.9')
    ok &= has_command( ['git', '--version'], '2.35',
        info="\nTo install see https://git-scm.com/book/en/v2/Getting-Started-Installing-Git.\n" \
             "  Needed for local and remote version control.\n" \
             "  Highly recommended.\n"
    )
    ok &= has_command( ['gh', '--version'], '2.31',
        info="\nTo install see https://cli.github.com/manual/installation.\n" \
             "  Enables `wip init` to create remote GitHub repositories.\n" \
             "  Highly recommended.\n"
    )
    ok &= has_command( ['bump2version', '-h'], '1.0',
        info="\nTo install: `python -m pip install bump2version --upgrade [--user]`\n" \
             "  Needed for version string management.\n" \
             "  Highly recommended.\n"
    )
    ok &= has_command( ['poetry', '--version'], '1.5',
        info="\nTo install: `python -m pip install poetry --upgrade [--user]`\n" \
             "  Needed for dependency management, publishing to PyPI.\n" \
             "  Highly recommended in development environments.\n"
    )
    ok &= has_command( ['mkdocs', '--version'], '1.4.3',
        info="\nTo install: `python -m pip install mkdocs --upgrade [--user]`\n" \
             "  Needed for documentation generation.\n" \
             "  Highly recommended on workstations, discouraged on HPC clusters.\n"
    )
    ok &= has_module('nanobind', '1.4',
        info="\nTo install: `python -m pip install nanobind --upgrade [--user]`\n" \
             "  Needed to construct C++ binary extension modules.\n"
    )
    ok &= has_module('numpy', '1.22',
        info="\nTo install: `python -m pip install numpy --upgrade [--user]`\n" \
             "  Needed to construct Modern Fortran binary extension modules (f2py is part of numpy).\n"
             "  Generally extremely useful for scientific computing, HPC, ... \n"
    )
    ok &= has_command( ['cmake', '--version'], '3.18',
        info="\nTo install see https://cmake.org/install/.\n" \
             "  Needed to build C++ and Modern Fortran binary extension modules.\n"
    )

    msg = "\nAll components are present." if ok else \
          "\nSome components are missing. This is only a problem is you are planning to use them.\n" \
          "If you are working on your own machine, you must install these components yourself.\n" \
          "If you are working on a HPC cluster, preferably load the corresponding LMOD modules. \n"

    click.secho(msg, fg = fg[ok])


def check_version(command: str, version: str, minimal: str, info: str = ""):
    if not info.startswith('\n'):
        info = '\n' + info
    ok = Version(version) >= Version(minimal)
    click.secho(f"{command}: v{version} {'(OK)' if ok else f': (not OK, {minimal=} ){info}'}", fg=fg[ok])
    return ok

def missing(what:str, minimal: str, info:str = ""):
    click.secho(f"{what} is missing in the current environment ({minimal=}')\n"
                f"{info}", fg =fg[False])
    return False

def has_python(minimal: str):
    """Python"""
    return check_version('Python', python_version(), minimal=minimal)

# From https://gist.github.com/jhorsman/62eeea161a13b80e39f5249281e17c39
semver = re.compile(r'^([0-9]+)\.([0-9]+)\.([0-9]+)(?:-([0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?(?:\+[0-9A-Za-z-]+)?$')

def extract_version(stdout: str) -> str:
    """Extract version string from output."""

    lines = stdout.split('\n')
    for line in lines:
        words = line.replace(')', '').split(' ')
        for word in words:
            if word.startswith('v'):
                word = word[1:]
            if re.match(semver, word):
                return word

    print(f"oops: {stdout=}")
    return '??? no version string found'

def has_command( command             : list
               , minimal             : str
               , info: str=''
               , extract_version     : Callable=extract_version
               ) -> bool:
    """Verify whether a command is avalaible, and if so if its version is <minimal> or higher."""
    try:
        cmd = ' '.join(command)
        completed_process = run(cmd, shell=True, capture_output=True, encoding='utf-8')
        if not completed_process.returncode:
            version = extract_version(completed_process.stdout)
            return check_version(
                command[0], version, minimal,
                info=info,
            )
    except FileNotFoundError:
        pass
    return missing(f"Command {command[0]}", minimal=minimal, info=info)

def extract_version_bump2version(stdout: str):
    """extract version from `bump2version -h` output."""
    lines = stdout.split('\n')
    for line in lines:
        if 'bumpversion:' in line:
            v = line.split(' ')[1][1:]
            return v


def has_module(module_name: str, minimal: str, info="", version_var='__version__') -> bool:
    try:
        m = importlib.import_module(module_name)
        version = eval(f"m.{version_var}")
        return check_version(module_name, version, minimal=minimal,
            info=info
        )
        return True
    except ModuleNotFoundError:
        return missing(f"Module numpy", minimal=minimal, info=info)
