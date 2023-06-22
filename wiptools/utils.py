from contextlib import contextmanager
import json
import os
from pathlib import Path
import re
from typing import Union

import click

import wiptools.messages as messages

@contextmanager
def in_directory(path):
    """Context manager for changing the current working directory while the body of the
    context manager executes.
    """
    previous_dir = Path.cwd()
    os.chdir(path) # the str method takes care of when path is a Path object
    try:
        yield Path.cwd()
    finally:
        os.chdir(previous_dir)


def cookiecutters():
    """Return the path to the cookiecutter templates"""
    return Path(__file__).parent / 'cookiecutters'

def pat(github_username):
    """Return the personal access token for github.com/{github_username} from the standard location."""
    return Path.home() / '.wiptools' / f'{github_username}.pat'

def verify_project_name(project_name: str) -> bool:
    """Project names must start with a char, and contain only chars, digits, underscores and dashes.

    Args:
        project_name: name of the current project
    """
    p = re.compile(r"\A[a-zA-Z][a-zA-Z0-9_-]*\Z")
    return bool(p.match(project_name))


def pep8_module_name(module_name: str)->str:
    """Convert a module name to a PEP8 compliant module name.

    Conversion implies:

    * -> lowercase
    * dash -> underscore

    If the conversion is not possible, the function exits with a non-zero exit code.

    This function is typically called to convert a project name to a PE8 compliant module name.

    Args:
        module_name to be converted

    Returns:
        PEP8 compliant version of module_name.
    """

    pep8_name = module_name\
        .lower()\
        .replace('-', '_')

    p = re.compile(r"\A[a-z][a-z0-9_]*\Z")
    if not bool(p.match(pep8_name)):
        messages.error_message(f"Module name '{module_name}' could not be made PEP8 compliant.")

    return pep8_name


def get_config(config_path: Path, needed: dict = {}) -> dict:
    """Get cookiecutter parameters from a config file and prompt for missing parameters.

    Args:
        config_path: path to config file. If it does not exist, the user is prompted for all needed parameters
            and the answers are saved to config_path.

        needed: (key, kwargs) pairs. Each key is the name of a needed parameter, and kwargs is a dict passed as
            messages.ask(**kwargs) to prompt the user for parameters missing from the config file in config_path.

    Returns:
         a dictionary with (cookiecutter_parameter_name, value) pairs.
    """

    save = False
    if config_path.is_file():
        with open(config_path) as f:
            config = json.load(f)
    else:
        config = {}
        if config_path:
            save = True

    header = False
    for cookiecutter_parameter, kwargs in needed.items():
        if not cookiecutter_parameter in config:
            if not header:
                click.secho("\nDeveloper info needed:")
                header = True
            config[cookiecutter_parameter] = messages.ask(**kwargs)

    if save:
        config_path.parent.mkdir(parents=True)
        with open(config_path, mode='w') as f:
            json.dump(config, f, indent=2)

    return config

def read_wip_cookiecutter_json() -> dict:
    """Read the `wip-cookiecutter.json` file. Exits if missing.

    This function also serves as a test that the current working directory is a wip project directory.
    """
    try:
        with open(Path.cwd() / 'wip-cookiecutter.json') as fp:
            return json.load(fp)
    except FileNotFoundError:
        messages.error_message(f"Current working directory does not contain a `wip-cookiecutter.json` file.\n"
                               f"Not a wip project?")