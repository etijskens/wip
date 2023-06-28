# About

Wiptools is a collection of tools for setting up a Python project skeleton and 
managing it. 

I wrote Wiptools (and its predecessors `micc` and 
[micc2](https://github.com/etijskens/et-micc2)) because I found myself with every new
Python project loosing time looking up and fixing the nitty-gritty details for setting
up a remote GitHub repo, creating C++ binary extension modules or a CLI with subcommands, 
setting up documentation, and many more. If you start new projects on a regular basis 
using the same project skeleton and tools every time significantly improves productivity.    

Wiptools provides:

- a project skeleton
- automatic local and remote git repo creation
- integration with [poetry](https://python-poetry.org/) for dependency management 
  and virtual environments, publishing on [PyPI](https://pypi.org)
- version management with [bump2version](https://github.com/c4urself/bump2version)
- adding subcomponents 
  - Python (sub)modules
  - binary extension modules in C++ with [nanobind](https://nanobind.readthedocs.io/en/latest/))
    and Fortran with [f2py](https://numpy.org/doc/stable/f2py/)
  - command line interfaces with [click](https://click.palletsprojects.com/en/), 
    single command and with subcommands
- documentation generation with [mkdocs](https://www.mkdocs.org) or 
  [sphinx](https://www.sphinx-doc.org/en/master/) (to be implemented)
