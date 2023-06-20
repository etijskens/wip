import sys

import click

def error_message(message, return_code = 1):
    """Print an error message and exit if return_code is non-zero."""
    click.secho(f"ERROR: {message}", fg='red')
    if return_code:
        click.secho(f"ERROR: exiting ({return_code=})", fg='red')
        sys.exit(return_code)


def ask(question, type=str, default=None):
    """Ask a question and return the answer as a type object."""

    if default is None:
        answer = click.prompt(text=question, type=type)
    else:
        answer = click.prompt(text=question, default=default)

    return answer

