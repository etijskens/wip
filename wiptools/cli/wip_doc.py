# -*- coding: utf-8 -*-
from pathlib import Path
import shutil
import subprocess

import click
from cookiecutter.main import cookiecutter

import wiptools.messages as messages
import wiptools.utils as utils


def wip_doc(ctx: click.Context):
    """Add project documentation"""

    cookiecutter_params = utils.read_wip_cookiecutter_json()

    # Verify that the project is not already configured for documentation generation:
    docs_path = Path.cwd() / 'docs'
    docs_format = 'markdown'         if (docs_path / 'index.md' ).is_file() else \
                  'restructuredText' if (docs_path / 'index.rst').is_file() else ''
    if docs_format:
        messages.warning_message( f"Project {cookiecutter_params['project_name']} is already configured \n"
                                  f"for documentation generation ({docs_format} format)."
                                )
        return

    docs_format = 'md'  if ctx.params['md' ] else \
                  'rst' if ctx.params['rst'] else ''

    if not docs_format:
        messages.warning_message("No documentation format specified")
        return # nothing to do.

    if docs_format == 'rst':
        messages.error_message("RestructuredText documentation generation is not yet implemented")

    # top level documentation template

    template = 'project-doc-md'  if docs_format == 'md'  else \
               'project-doc-rst' if docs_format == 'rst' else None
    if template:
        template = str(utils.cookiecutters() / template)

    with messages.TaskInfo(f"Expanding cookiecutter template `{template}`"):
        cookiecutter( template=template
                    , extra_context=cookiecutter_params
                    , output_dir=Path.cwd().parent
                    , no_input=True
                    , overwrite_if_exists=True
                    )

