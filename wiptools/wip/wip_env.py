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
          "Otherwise, if you are working on a HPC cluster, you must load the corresponding modules."

    click.secho(msg, fg = fg[ok])


def check_version(v: str, minimal: str, message: str):
    ok = Version(v) >= Version(minimal)
    click.secho(f"{message} {'(OK)' if ok else f': {minimal=} (not OK)'}", fg=fg[ok])
    return ok

def missing(what):
    click.secho(f"{what} is missing in the current environment.", fg =fg[False])
    return False

def has_python(minimal: str):
    """Python"""
    return check_version(python_version(), minimal=minimal, message='python ' + sys.version.replace('\n',' '))

def has_git(minimal: str):
    """git"""
    cmd = 'git'
    try:
        completed_proces = run(f"{cmd} --version", shell=True, capture_output=True)
        s = completed_proces.stdout.decode('utf-8')
        version = s.split(' ')[2]
        return check_version(version, minimal=minimal, message=s.replace('\n',' '))
    except FileNotFoundError:
        return missing(f"Command {cmd}")

def has_gh(minimal: str):
    """git CLI"""
    cmd = 'gh'
    try:
        completed_proces = run(f"{cmd} --version", shell=True, capture_output=True)
        s = completed_proces.stdout.decode('utf-8').replace('\n', ' ')
        version = s.split(' ')[2]
        return check_version(version, minimal=minimal, message=s)
    except FileNotFoundError:
        return missing(f"Command {cmd}")

def has_bumpversion(minimal: str):
    cmd = 'bumpversion'
    try:
        completed_process = run([cmd, '-h'], capture_output=True, )
        lines = completed_process.stdout.decode('utf-8').split('\n')
        for line in lines:
            if 'bumpversion:' in line:
                v = line.split(' ')[1][1:]
                return check_version(v, minimal=minimal, message=line)

    except FileNotFoundError:
        return missing(f"Command {cmd}")


def has_nanobind(minimal: str):
    """"""
    try:
        from nanobind import __version__
        return check_version(__version__, minimal=minimal, message=f"nanobind {__version__}")
    except ModuleNotFoundError:
        return missing(f"Module nanobind")

def has_numpy(minimal: str):
    """"""
    try:
        from numpy import __version__
        return check_version(__version__, minimal=minimal, message=f"numpy {__version__}")
    except ModuleNotFoundError:
        return missing(f"Module numpy")


def has_cmake(minimal: str):
    """git"""
    cmd = 'cmake'
    try:
        completed_proces = run(f"{cmd} --version", shell=True, capture_output=True)
        s = completed_proces.stdout.decode('utf-8')
        p = s.find('\n')
        s = s[:p]
        version = s.split(' ')[2]
        return check_version(version, minimal=minimal, message=s.replace('\n',' '))
    except FileNotFoundError:
        return missing(f"Command {cmd}")

def has_poetry(minimal: str):
    """"""
    cmd = 'poetry'
    try:
        completed_proces = run(f"{cmd} --version", shell=True, capture_output=True)
        s = completed_proces.stdout.decode('utf-8').replace('\n', ' ')
        version = s.split(' ')[2][:-1]
        return check_version(version, minimal=minimal, message=s.replace('\n',' '))
    except FileNotFoundError:
        return missing(f"Command {cmd}")

def has_mkdocs(minimal: str):
    """"""
    cmd = 'mkdocs'
    try:
        completed_proces = run(f"{cmd} --version", shell=True, capture_output=True)
        s = completed_proces.stdout.decode('utf-8')
        version = s.split(' ')[2]
        return check_version(version, minimal=minimal, message=s.replace('\n',' '))
    except FileNotFoundError:
        return missing(f"Command {cmd}")

