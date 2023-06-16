import click

def error_message(message):
    click.secho(f"ERROR: {message}", fg='red')