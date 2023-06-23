# -*- coding: utf-8 -*-
import json
from pathlib import Path
import subprocess

import click

import wiptools.messages as messages
from wiptools.tree import tree
import wiptools.utils as utils


def wip_info(ctx: click.Context):
    """get info about the project's structure."""

    cookiecutter_params = utils.read_wip_cookiecutter_json()

    project_path = Path.cwd()
    package_name = cookiecutter_params['package_name']

    style_kwargs = {'fg': 'cyan'}
    click.secho("Package structure", **style_kwargs)
    prefix = '  '
    package_tree = tree(project_path / package_name, prefix='  ', **style_kwargs)

    click.echo(f'{prefix}{package_name} ' + click.style('[python package]', **style_kwargs))
    for line in package_tree:
        print(line)

