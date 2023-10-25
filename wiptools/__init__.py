# -*- coding: utf-8 -*-

"""
# Python package wiptools

Common tools between the CLIs
"""

__version__ = "1.3.2-dev"

def version():
    return f"wiptools v{__version__}"

COMPONENT_TYPES = {
    'py' : 'Python module',
    'cpp': 'C++ binary extension',
    'f90': 'Modern Fortran binary extension',
    'cli': 'CLI'
}

DOCUMENTATION_FORMATS = {
    'md' : 'Markdown',
    'rst': 'restructuredText',
    ''   : 'none'
}
