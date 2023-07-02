import sys

import click

def error_message(message: str, return_code:int = 1):
    """Print an error message and exit if return_code is non-zero."""
    click.secho(f"\nERROR: {message}", fg='red')
    if return_code:
        click.secho(f"ERROR: exiting ({return_code=})", fg='red')
        sys.exit(return_code)

def warning_message(message:str, return_code:int = 0):
    """Print a warning message."""
    click.secho(f"\nWARNING: {message}", fg='red')
    if return_code:
        click.secho(f"WARNING: exiting ({return_code=})", fg='red')
        sys.exit(return_code)

def info_message(message: str):
    click.secho(f"\n{message}", fg='green')

class TaskInfo:
    """Context manager class for printing a message before and after a task """
    def __init__(self, message: str, end_message:str = '', fg='bright_black', short=False):
        self.message = message
        self.end_message = end_message if end_message else message
        self.fg = fg
        self.short = short

    def __enter__(self):
        if self.short:
            click.secho(f"{self.message} ... ", fg=self.fg, nl=False)
        else:
            click.secho(f"\n[[{self.message} ...", fg=self.fg)

    def __exit__(self, exc_type, exc_value, exc_tb):
        if exc_value:
            if self.short:
                click.secho(f"FAILED!", fg='red')
            else:
                click.secho(f"]] (FAILED {self.end_message})", fg='red')
        else:
            if self.short:
                click.secho(f"done", fg=self.fg)
            else:
              click.secho(f"]] (done {self.end_message})", fg=self.fg)


def ask(question: str, type=str, default=None):
    """Ask a question and return the answer as `type`."""

    if default is None:
        answer = click.prompt(text=question, type=type)
    else:
        answer = click.prompt(text=question, default=default)

    return answer


def warn_for_python_before_3_8(minimal_python_version: str) -> bool:
    v = [ int(s) for s in minimal_python_version.split('.')]

    if v[0] <  3 \
    or (v[0] <= 3 and v[1] < 8):
        warning_message(f'The requested Python version ({minimal_python_version}) is incompatible with nanobind.\n'
                        f'Building C++ binary extensions will not be possible. Python 3.8 or later is needed.')

        try:
            if click.confirm("Continue?",default=False):
                return
            else:
                warning_message("Aborting.")
                sys.exit(1)
        except click.Abort:
            sys.exit(1)