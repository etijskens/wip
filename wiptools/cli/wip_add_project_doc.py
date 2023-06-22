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
    template = 'project-doc-md'  if ctx.params['doc'] == 'md'  else \
               'project-doc-rst' if ctx.params['doc'] == 'rst' else None
    if template:
        template = utils.cookiecutters() / template

    co