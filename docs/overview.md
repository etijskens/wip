# About

Wiptools is a collection of tools for setting up a Python project skeleton and 
managing it. 

I wrote Wiptools (and its predecessors `micc` and 
[micc2](https://github.com/etijskens/et-micc2)) because with every new Python project I 
found myself loosing time looking up and fixing the nitty-gritty details for setting
up a remote GitHub repo, creating C++ binary extension modules or a CLI with subcommands, 
setting up documentation, and many more. If you start new projects on a regular basis 
using the same project skeleton and tools every time significantly improves productivity.    

It also turned out very useful for the [Parallel Programming course](https://etijskens.github.io/wetppr/),
especially the ability to easily prototype and test in Python and provide performant C++ or 
Fortran as replacement modules.

Wiptools provides:

- a project skeleton
- automatic creation of a git repository (locally, as well as remotely on github.com)
- integration with [poetry](https://python-poetry.org/) for dependency management 
  and virtual environments, publishing on [PyPI](https://pypi.org)
- version management with [bump2version](https://github.com/c4urself/bump2version)
- adding subcomponents 
    - Python (sub)modules
    - binary extension modules in C++ with [nanobind](https://nanobind.readthedocs.io/en/latest/))
      and Fortran with [f2py](https://numpy.org/doc/stable/f2py/)
    - command line interfaces with [click](https://click.palletsprojects.com/en/), 
      single command and with subcommands
- test templates for all added components and [pytest](https://docs.pytest.org/) integration
- documentation generation with [mkdocs](https://www.mkdocs.org) or 
  [sphinx](https://www.sphinx-doc.org/en/master/) (to be implemented)

## Links

 - [Wiptools GitHub repository](https://github.com/etijskens/wiptools)
 - [Wiptools homepage](https://etijskens.github.io/wiptools)
