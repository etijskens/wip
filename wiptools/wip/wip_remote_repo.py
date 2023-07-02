# -*- coding: utf-8 -*-

from pathlib import Path

import click

import wiptools.messages as messages
import wiptools.utils as utils


def wip_remote_repo(ctx:click.Context):
    """Add a remote Github repo."""

    # Retrieve github_username
    cookiecutter_params = utils.read_wip_cookiecutter_json()
    github_username = cookiecutter_params['github_username']

    remote_visibility = 'private' if ctx.params['private'] else 'public'

    add_remote(github_username, remote_visibility)


def add_remote(github_username:str, remote_visibility: str):
    """Add a remote GitHub repo."""
    if not github_username:
        messages.warning_message("A GitHub username must be supplied to create remote GitHub repositories.")
        return

    # Find .pat file (personal access token)
    pat_file = utils.pat(github_username)
    if not pat_file.is_file():
        messages.error_message(f"No personal access token (PAT) for `github.com/{github_username}` found at \n"
                               f"`{pat_file}`. (A PAT is needed to access your GitHub account).\n"
                               f"The remote GitHub repo `github.com/{github_username}/{utils.PROJECT_PATH.name}` cannot be created."
                               )

    # Create remote GitHub repo:
    with messages.TaskInfo('Creating a remote GitHub repo'):
        with open(pat_file) as fd_pat:
            cmds = [
                ('gh auth login --with-token', {'stdin': fd_pat, 'text': True}),
                f'gh repo create --source . --{remote_visibility} --push'
            ]
            utils.subprocess_run_cmds(cmds, message2=f" in project folder {utils.PROJECT_PATH.name}")
