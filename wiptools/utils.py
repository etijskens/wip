from contextlib import contextmanager
import os
from pathlib import Path

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
