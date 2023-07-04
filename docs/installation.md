# Installation

## Installing on a workstation

`Wiptools` is published on [PyPI](https://pypi.org/), and hence it can be installed with its 
dependencies as:

```shell
> pip install wiptools
```

This installs the bare `wip`. Because `wip` relies on quite a bit of other tools, installing al its
dependencies may waste quite a bit of resources, especially on clusters. For that reason the user
is responsible for installing them - if needed. The `wip env` command lists which tools are 
available in the current environment and which not, what they are used for and how they can be 
installed.

## Installing on a HPC cluster

HPC cluster administrators, typically, prefer that users do not install software components. 
Most tools used by `wip` will be available through LMOD modules and are made available with
`module load` commands. Python modules that are not available must be installed with 
`python -m pip install <package> --user`. The installation location must be chosen by exporting
the `PYTHONUSERBASE` environment variable:

```shell
> export PYTHONUSERBASE=$VSC_DATA/.local
```