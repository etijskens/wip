# -*- coding: utf-8 -*-

import os
from pathlib import Path
import shutil
import subprocess

import click
from cookiecutter.main import cookiecutter

import wiptools.messages as messages
import wiptools.utils as utils


def wip_docs(ctx: click.Context):
    """Add project documentation"""

    cookiecutter_params = utils.read_wip_cookiecutter_json()
    package_name = cookiecutter_params['package_name']

    # Verify that the project is not already configured for documentation generation:
    docs_path = Path.cwd() / 'docs'
    docs_format = 'markdown'         if (docs_path / 'index.md' ).is_file() else \
                  'restructuredText' if (docs_path / 'index.rst').is_file() else ''
    if docs_format:
        messages.warning_message( f"Project {cookiecutter_params['project_name']} is already configured \n"
                                  f"for documentation generation ({docs_format} format)."
                                )
        return

    if ctx.params['md'] and ctx.params['rst']:
        messages.warning_message(f"Both '--md' and '--rst' specified: ignoring '--rst'.")

    docs_format = 'md'  if ctx.params['md' ] else \
                  'rst' if ctx.params['rst'] else \
                  None

    if not docs_format:
        messages.warning_message("No documentation format specified")
        return # nothing to do.

    # for the time being...
    if docs_format == 'rst':
        messages.error_message("RestructuredText documentation generation is not yet implemented")

    # top level documentation template -----------------------------------------------------------
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

    # iterate over all components and add them to `docs/api-reference.md`
    utils.iter_components(Path.cwd() / cookiecutter_params['package_name'], apply=add_component_documentation(package_name=package_name))

class add_component_documentation:
    def __init__(self, package_name):
        self.project_path = Path.cwd()
        self.path_to_api_refence_md = self.project_path / 'docs' / 'api-reference.md'
    def __call__(self, path_to_component: Path, component_type: str):
        if component_type == 'py':
            with self.path_to_api_refence_md.open(mode='a') as fp:
                p = str(path_to_component.relative_to(self.project_path)).replace(os.sep, '.')
                fp.write(f'\n\n::: {p}')

        # not sure what to do here
        # elif component_type == 'py'\
        # or component_type == 'cli':
        #     with self.path_to_api_refence_md.open(mode='a') as fp:
        #         p = path_to_component.relative_to(self.project_path)
        #         fp.write(f'\n\n::: {p}')

        # also not sure what to do with CLI components
