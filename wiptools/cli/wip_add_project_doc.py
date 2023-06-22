# -*- coding: utf-8 -*-
from pathlib import Path
import shutil
import subprocess

import click
from cookiecutter.main import cookiecutter

import wiptools.messages as messages
import wiptools.utils as utils


def wip_add_project_doc(ctx: click.Context):
    """"""
    cookiecutter_params = utils.read_wip_cookiecutter_json()

    template = 'project-doc-md'  if ctx.params['doc'] == 'md'  else \
               'project-doc-rst' if ctx.params['doc'] == 'rst' else None
    if template:
        template = utils.cookiecutters() / template

    with messages.TaskInfo(f"Expanding cookiecutter template `{template}`"):
        cookiecutter( template=template
                    , extra_context=cookiecutter_params
                    , output_dir=Path.cwd()
                    , no_input=True
                    )

