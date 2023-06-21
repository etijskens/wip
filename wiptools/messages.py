import sys

import click

def error_message(message, return_code = 1):
    """Print an error message and exit if return_code is non-zero."""
    click.secho(f"\nERROR: {message}", fg='red')
    if return_code:
        click.secho(f"ERROR: exiting ({return_code=})", fg='red')
        sys.exit(return_code)

class TaskInfo:
    """Context manager class for printing a message before and after a task """
    def __init__(self,message: str):
        self.message = message
    def __enter__(self):
        click.secho(f"\n[[{self.message}...", fg='cyan')
    def __exit__(self, exc_type, exc_value, exc_tb):
        click.secho(f"]] (done {self.message})", fg='cyan')


def ask(question, type=str, default=None):
    """Ask a question and return the answer as `type`."""

    if default is None:
        answer = click.prompt(text=question, type=type)
    else:
        answer = click.prompt(text=question, default=default)

    return answer

