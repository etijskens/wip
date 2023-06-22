# -*- coding: utf-8 -*-
from pathlib import Path
import shutil
import subprocess

import click
from cookiecutter.main import cookiecutter

from wiptools.cli.wip_add_project_doc import wip_add_project_doc
import wiptools.messages as messages
import wiptools.utils as utils

def wip_init(ctx: click.Context) -> int:
    """Actual body of wip subcommand `wip init ...`.

    Returns:
        0 if successful, exits with non-zero return code otherwise.
    """
    if ctx.parent.params['verbosity']:
        click.echo(f"wip init {ctx.params['project_name']}")

    project_name = ctx.params['project_name']
    project_path = Path(project_name)
    if project_path.is_file():
        messages.error_message(f"A file with name '{project_name}' exists already.")
    if project_path.is_dir():
        messages.error_message(f"A directory with name '{project_name}' exists already.")

    cookiecutter_params = utils.get_config(
        ctx.parent.params['config']
      , needed={ 'full_name'      : { 'question': 'Enter your full name'}
               , 'email_address'  : { 'question': 'Enter your email address'}
               , 'github_username': { 'question': 'Enter your GitHub username (leave empty if no remote repos needed)'
                                    , 'default' : ''}
               }
    )

    github_username = cookiecutter_params['github_username']
    if github_username:
        pat_standard_location = Path.home() / '.wiptools' / f'{github_username}.pat'
        if not pat_standard_location.is_file():
            while True:
                pat_location = messages.ask(question=f'Enter location of personal access token for github.com/{github_username}\n'
                                                     f'(i.e. a directory containing file `{github_username}.pat`)'
                                           )
                if not pat_location.strip():
                    messages.error_message('Interrupted.', return_code=0)
                    break
                pat_location = Path(pat_location).expanduser()
                if pat_location.is_dir():
                    pat_location = pat_location / f'{github_username}.pat'
                    if pat_location.is_file():
                        shutil.copy(pat_location, pat_standard_location)
                        break
                    else:
                        continue

    click.secho("\nProject info needed:", fg='green')
    project_short_description = ctx.params['description'] if ctx.params['description'] else messages.ask(
        'Enter a short description for the project:', default='<project_short_description>'
    )
    minimal_python_version = ctx.params['python_version'] if ctx.params['python_version'] else messages.ask(
        'Enter the minimal Python version', default='3.8'
    )

    cookiecutter_params.update(
      { 'project_name' : project_name
      , 'package_name' : utils.pep8_module_name(project_name)
      , 'project_short_description': project_short_description
      , 'minimal_python_version': minimal_python_version
      }
    )
    with messages.TaskInfo("Expanding cookiecutters"):
        template = str(utils.cookiecutters() / 'project')
        print(f'Expanding template: {template}')
        cookiecutter( template=template
                    , extra_context=cookiecutter_params
                    , output_dir=Path.cwd()
                    , no_input=True
                    )

    with utils.in_directory(project_path):
        # Create local git repo:
        with messages.TaskInfo('Creating a local git repo'):
            completed_process = subprocess.run(['git', 'init', '--initial-branch=main'])
            if completed_process.returncode:
                messages.error_message('Failing git command.')

            completed_process = subprocess.run(['git', 'add', '*'])
            if completed_process.returncode:
                messages.error_message('Failing git command.')

            completed_process = subprocess.run(['git', 'add', '.gitignore'])
            if completed_process.returncode:
                messages.error_message('Failing git command.')

            completed_process = subprocess.run(['git', 'commit', '-m', f'"Initial commit from `wip init {project_name}`"'])
            if completed_process.returncode:
                messages.error_message('Failing git command.')

        # Verify necessary conditions for creating a remote GitHub repo :
        remote_visibility = ctx.params['remote_visibility'].lower()
        if not remote_visibility in ['public', 'private', 'none']:
            messages.error_message(
                f"ERROR: --remote={remote_visibility} is not a valid option. Valid options are:\n"
                f"       --remote=public\n"
                f"       --remote=private\n"
                f"       --remote=none\n"
            )
        if remote_visibility.lower() != 'none':
            if not github_username:
                messages.error_message("A GitHub username must be supplied to create remote GitHub repositories.")

            # Find .pat file (personal access token)
            pat_file = utils.pat(github_username)
            if not pat_file.is_file():
                messages.error_message(f"No personal access token (PAT) for `github.com/{github_username}` found at \n"
                                       f"`{pat_file}`. (A PAT is needed to access your GitHub account).\n"
                                       f"The remote GitHub repo `github.com/{github_username}/{project_name}` cannot be created."
                                      )

            # Create remote GitHub repo:
            with messages.TaskInfo('Creating a remote GitHub repo'):
                with open(pat_file) as fd_pat:
                    cmd = ['gh', 'auth', 'login', '--with-token']
                    completed_process = subprocess.run(cmd, stdin=fd_pat, text=True)
                    if completed_process.returncode:
                        messages.error_message('gh: authentication failed.')

                    cmd = ['gh', 'repo', 'create', '--source', '.', f'--{remote_visibility}', '--push']
                    completed_process = subprocess.run(cmd)
                    if completed_process.returncode:
                        messages.error_message(f'gh: Creating remote repo `https://github.com/{github_username}/{project_name}` failed.')

    if ctx.params['doc_md']:
        wip_add_project_doc(ctx)

    return 0