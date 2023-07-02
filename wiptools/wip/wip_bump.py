# -*- coding: utf-8 -*-

from pathlib import Path

import click

import wiptools.messages as messages
import wiptools.utils as utils


def wip_bump(ctx: click.Context):
    """Bump2version wrapper."""

    cookiecutter_params = utils.read_wip_cookiecutter_json()
    project_name = cookiecutter_params['project_name']

    old_version = utils.read_pyproject_toml()['tool']['poetry']['version']
    command = f"bump2version {ctx.params['args']}"
    utils.subprocess_run_cmds(command,
        message2 = f" in project folder `{project_name}`"
    )

    new_version = utils.read_pyproject_toml()['tool']['poetry']['version']
    messages.info_message(f"{project_name} v{old_version} -> v{new_version}")