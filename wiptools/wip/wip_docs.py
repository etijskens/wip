# -*- coding: utf-8 -*-

import os
from pathlib import Path
import shutil
import subprocess

import click
from cookiecutter.main import cookiecutter

import wiptools.messages as messages
import wiptools.utils as utils


formats = {
    'md': 'Markdown',
    'rst': 'restructuredText'
}
def wip_docs(ctx: click.Context):
    """Add project documentation"""

    cookiecutter_params = utils.read_wip_cookiecutter_json()
    package_name = cookiecutter_params['package_name']

    # Verify that the project is not already configured for documentation generation:
    docs_path = Path.cwd() / 'docs'
    fmt = 'md'  if (docs_path / 'index.md' ).is_file() else \
          'rst' if (docs_path / 'index.rst').is_file() else ''
    if fmt:
        messages.warning_message( f"Project {cookiecutter_params['project_name']} is already configured \n"
                                  f"for documentation generation ({formats[fmt]} format)."
                                )
        return

    fmt = ctx.params['fmt']

    # for the time being...
    if fmt == 'rst':
        messages.error_message("RestructuredText documentation generation is not yet implemented")

    # top level documentation template -----------------------------------------------------------
    template = f'project-doc-{fmt}'
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
    with messages.TaskInfo(f"Adding documentation for components "):
        utils.iter_components(
            Path.cwd() / cookiecutter_params['package_name'],
            apply=AddComponentDocumentationMarkdown(cookiecutter_params)
        )

class AddComponentDocumentationMarkdown:
    """A Functor for adding Markdowndocumentation generation skeleton."""
    def __init__(self, cookiecutter_params):
        self.cookiecutter_params = cookiecutter_params
        self.project_path = Path(self.cookiecutter_params['project_path'])
        self.path_to_api_refence_md = self.project_path / 'docs' / 'api-reference.md'

    def __call__(self, path_to_component: Path):
        """Add documentation generation skeleton for this component."""
        component_type = utils.component_type(path_to_component)
        messages.info_message(f"Adding documentation templates for {component_type}: {path_to_component.relative_to(self.project_path)}")
        if component_type == 'py':
            self.add_docs_py(path_to_component)
        elif component_type == 'cli':
            self.add_docs_cli(path_to_component)
        elif component_type == 'cp':
            self.add_docs_cpp(path_to_component)
        elif component_type == 'f90':
            self.add_docs_f90(path_to_component)

    def add_docs_py(self, path_to_component):
        """Add documentation generation skeleton for a python module."""
        with messages.TaskInfo(f"Adding `{path_to_component.relative_to(self.project_path)}` documentation (Python module)."):
            with self.path_to_api_refence_md.open(mode='a') as fp:
                p = str(path_to_component.relative_to(self.project_path)).replace(os.sep, '.')
                fp.write(f'\n\n::: {p}')

    def add_docs_cli(self, path_to_component):
        """Add documentation generation skeleton for a CLI."""
        with messages.TaskInfo(f"Adding `{path_to_component.relative_to(self.project_path)}` documentation (CLI)."):
            messages.warning_message("to be implemented!\n")
    def add_docs_cpp(self, path_to_component):
        """Add documentation generation skeleton for a C++ module"""
        with messages.TaskInfo(f"Adding `{path_to_component.relative_to(self.project_path)}` documentation (C++)."):
            messages.warning_message("to be implemented!\n")

    def add_docs_f90(self, path_to_component):
        """Add documentation generation skeleton for a Fortran module"""
        with messages.TaskInfo(f"Adding `{path_to_component.relative_to(self.project_path)}` documentation (Modern Fortran)."):
            messages.warning_message("to be implemented!\n")
