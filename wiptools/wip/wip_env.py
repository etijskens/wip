# -*- coding: utf-8 -*-

from  platform import python_version
import sys
from packaging.version import Version
from subprocess import run

import click

import wiptools.messages as messages
from wiptools.utils import subprocess_run_cmds

def wip_env(ctx: click.Context):
    """Check the current environment for necessary components."""

    print(("For full `wip` functionality the following commands and packages must be available in our envirionment:\n"))

    has_python('3.9')
    has_git('2.35')
    has_gh('2.31')
    has_bumpversion('1.0')
    has_nanobind('1.4')
    has_numpy('2.22')
    has_cmake('3.18')
    has_poetry('1.5')
    has_mkdocs('1.4.3')


fg = {
    0: 'red',
    1: 'green'
}

def check_version(v: str, minimal: str, message: str):
    ok = Version(v) >= Version(minimal)
    click.secho(f"{message} {'(OK)' if ok else f': {minimal=} (not OK)'}", fg=fg[ok])

def missing(what):
    click.secho(f"{what} is missing in the current environment.", fg =fg[False])

def has_python(minimal: str):
    """Python"""
    check_version(python_version(), minimal=minimal, message='python ' + sys.version.replace('\n',' '))

def has_git(minimal: str):
    """git"""
    cmd = 'git'
    completed_proces = run(f"{cmd} --version", shell=True, capture_output=True)
    if completed_proces.returncode:
        missing(f"Command {cmd}")
    else:
        s = completed_proces.stdout.decode('utf-8')
        version = s.split(' ')[2]
        check_version(version, minimal=minimal, message=s.replace('\n',' '))

def has_gh(minimal: str):
    """git CLI"""
    cmd = 'gh'
    completed_proces = run(f"{cmd} --version", shell=True, capture_output=True)
    if completed_proces.returncode:
        missing(f"Command {cmd}")
    else:
        s = completed_proces.stdout.decode('utf-8').replace('\n', ' ')
        version = s.split(' ')[2]
        check_version(version, minimal=minimal, message=s)

def has_bumpversion(minimal: str):
    cmd = 'bumpversion'
    completed_process = run([cmd, '-h'], capture_output=True)
    if completed_process.returncode:
        missing(f"Command {cmd}")
    else:
        lines = completed_process.stdout.decode('utf-8').split('\n')
        for line in lines:
            if 'bumpversion:' in line:
                v = line.split(' ')[1][1:]
                check_version(v, minimal=minimal, message=line)
                break


def has_nanobind(minimal: str):
    """"""
    try:
        from nanobind import __version__
        check_version(__version__, minimal=minimal, message=f"nanobind {__version__}")
    except ModuleNotFoundError:
        missing(f"Module nanobind")

def has_numpy(minimal: str):
    """"""
    try:
        from numpy import __version__
        check_version(__version__, minimal=minimal, message=f"numpy {__version__}")
    except ModuleNotFoundError:
        missing(f"Module numpy")


def has_cmake(minimal: str):
    """git"""
    cmd = 'cmake'
    completed_proces = run(f"{cmd} --version", shell=True, capture_output=True)
    if completed_proces.returncode:
        missing(f"Command {cmd}")
    else:
        s = completed_proces.stdout.decode('utf-8')
        p = s.find('\n')
        s = s[:p]
        version = s.split(' ')[2]
        check_version(version, minimal=minimal, message=s.replace('\n',' '))

def has_poetry(minimal: str):
    """"""
    cmd = 'poetry'
    completed_proces = run(f"{cmd} --version", shell=True, capture_output=True)
    if completed_proces.returncode:
        missing(f"Command {cmd}")
    else:
        s = completed_proces.stdout.decode('utf-8').replace('\n', ' ')
        version = s.split(' ')[2][:-1]
        check_version(version, minimal=minimal, message=s.replace('\n',' '))

def has_mkdocs(minimal: str):
    """"""
    cmd = 'mkdocs'
    completed_proces = run(f"{cmd} --version", shell=True, capture_output=True)
    if completed_proces.returncode:
        missing(f"Command {cmd}")
    else:
        s = completed_proces.stdout.decode('utf-8')
        version = s.split(' ')[2]
        check_version(version, minimal=minimal, message=s.replace('\n',' '))

