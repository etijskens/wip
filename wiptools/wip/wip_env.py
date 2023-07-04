# -*- coding: utf-8 -*-

from  platform import python_version
import sys
from packaging.version import Version
from subprocess import run

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
    ok &= has_git('2.35')
    ok &= has_gh('2.31')
    ok &= has_bumpversion('1.0')
    ok &= has_nanobind('1.4')
    ok &= has_numpy('1.22')
    ok &= has_cmake('3.18')
    ok &= has_poetry('1.5')
    ok &= has_mkdocs('1.4.3')

    msg = "\nAll components are present." if ok else \
          "\nSome components are missing. This is only a problem is you are planning to use them.\n" \
          "If you are working on your own machine, you must install these components yourself.\n" \
          "If you are working on a HPC cluster, preferably load the corresponding modules. \n"

    click.secho(msg, fg = fg[ok])


def check_version(v: str, minimal: str, message: str, install_instructions: str = ""):
    ok = Version(v) >= Version(minimal)
    click.secho(f"{message} {'(OK)' if ok else f': {minimal=} (not OK){install_instructions}'}", fg=fg[ok])
    return ok

def missing(what:str, install_instructions:str = ""):
    click.secho(f"{what} is missing in the current environment.{install_instructions}", fg =fg[False])
    return False

def has_python(minimal: str):
    """Python"""
    return check_version(python_version(), minimal=minimal,
        message='python ' + sys.version.replace('\n',' '),
    )

def has_git(minimal: str):
    """git"""
    cmd = 'git'
    install_instructions = "\nTo install see https://git-scm.com/book/en/v2/Getting-Started-Installing-Git.\n" \
                           "Needed for local and remote version control.\n" \
                           "Highly recommended.\n"
    try:
        completed_proces = run(f"{cmd} --version", shell=True, capture_output=True)
        s = completed_proces.stdout.decode('utf-8')
        version = s.split(' ')[2]
        return check_version(
            version, minimal=minimal,
            message=s.replace('\n',' '),
            install_instructions=install_instructions
        )
    except FileNotFoundError:
        return missing(f"Command {cmd}", install_instructions=install_instructions)

def has_gh(minimal: str):
    """git CLI"""
    cmd = 'gh'
    install_instructions = "\nTo install see https://cli.github.com/manual/installation.\n" \
                           "Enables `wip init` to create remote GitHub repositories.\n" \
                           "Highly recommended.\n"
    try:
        completed_proces = run(f"{cmd} --version", shell=True, capture_output=True)
        s = completed_proces.stdout.decode('utf-8').replace('\n', ' ')
        version = s.split(' ')[2]
        return check_version(
            version, minimal=minimal,
            install_instructions=install_instructions,
            message=s
        )
    except FileNotFoundError:
        return missing(f"Command {cmd}", install_instructions=install_instructions)

def has_bumpversion(minimal: str):
    cmd = 'bumpversion'
    install_instructions = "\nTo install: `python -m pip install bump2version --upgrade [--user]`\n" \
                           "Needed for version string management.\n" \
                           "Highly recommended.\n"
    try:
        completed_process = run([cmd, '-h'], capture_output=True, )
        lines = completed_process.stdout.decode('utf-8').split('\n')
        for line in lines:
            if 'bumpversion:' in line:
                v = line.split(' ')[1][1:]
                return check_version(
                    v, minimal=minimal,
                    message=line,
                    install_instructions=install_instructions
                )

    except FileNotFoundError:
        return missing(f"Command {cmd}", install_instructions=install_instructions)


def has_nanobind(minimal: str):
    """"""
    install_instructions = "\nTo install: `python -m pip install nanobind --upgrade [--user]`\n" \
                           "Needed to construct C++ binary extension modules.\n"
    try:
        from nanobind import __version__ as nanobind_version
        return check_version(
            nanobind_version, minimal=minimal,
            message=f"nanobind {nanobind_version}",
            install_instructions=install_instructions
        )
    except ModuleNotFoundError:
        return missing(f"Module nanobind", install_instructions=install_instructions)

def has_numpy(minimal: str):
    """"""
    install_instructions = "\nTo install: `python -m pip install numpy --upgrade [--user]`\n" \
                           "Needed to construct Modern Fortran binary extension modules./n"
    try:
        from numpy import __version__ as numpy_version
        return check_version(
            numpy_version, minimal=minimal,
            message=f"numpy {numpy_version}",
            install_instructions=install_instructions
        )
    except ModuleNotFoundError:
        return missing(f"Module numpy", install_instructions=install_instructions)


def has_cmake(minimal: str):
    """cmake"""
    cmd = 'cmake'
    install_instructions = "\nTo install see https://cmake.org/install/.\n" \
                           "Needed to build C++ and Modern Fortran binary extension modules.\n"
    try:
        completed_proces = run(f"{cmd} --version", shell=True, capture_output=True)
        s = completed_proces.stdout.decode('utf-8')
        p = s.find('\n')
        s = s[:p]
        version = s.split(' ')[2]
        return check_version(
            version, minimal=minimal,
            message=s.replace('\n',' '),
            install_instructions=install_instructions
        )
    except FileNotFoundError:
        return missing(f"Command {cmd}", install_instructions=install_instructions)

def has_poetry(minimal: str):
    """"""
    cmd = 'poetry'
    install_instructions = "\nTo install: `python -m pip install poetry --upgrade [--user]`\n" \
                           "Needed for dependency management, publishing to PyPI.\n" \
                           "Recommended for virtual environments during development.\n"
    try:
        completed_proces = run(f"{cmd} --version", shell=True, capture_output=True)
        s = completed_proces.stdout.decode('utf-8').replace('\n', ' ')
        version = s.split(' ')[2][:-1]
        return check_version(version, minimal=minimal, message=s.replace('\n',' '))
    except FileNotFoundError:
        return missing(f"Command {cmd}", install_instructions=install_instructions)

def has_mkdocs(minimal: str):
    """"""
    cmd = 'mkdocs'
    install_instructions = "\nTo install: `python -m pip install mkdocs --upgrade [--user]`\n" \
                           "Needed for documentation generation.\n" \
                           "Highly recommended on workstations, discouraged on HPC clusters.\n"
    try:
        completed_proces = run(f"{cmd} --version", shell=True, capture_output=True)
        s = completed_proces.stdout.decode('utf-8')
        version = s.split(' ')[2]
        return check_version(version, minimal=minimal, message=s.replace('\n',' '))
    except FileNotFoundError:
        return missing(f"Command {cmd}", install_instructions=install_instructions)

