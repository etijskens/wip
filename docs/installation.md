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

```shell
> wip env 
For a full functional `wip` the following commands and packages must be available in our environment:

Python: v3.10.4 (OK)
Command git is missing in the current environment.
To install see https://git-scm.com/book/en/v2/Getting-Started-Installing-Git.
  Needed for local and remote version control.
  Highly recommended.
  
Command gh is missing in the current environment.
To install see https://cli.github.com/manual/installation.
  Enables `wip init` to create remote GitHub repositories.
  Highly recommended.

Command bump2version is missing in the current environment.
To install: `python -m pip install bump2version --upgrade [--user]`
  Needed for version string management.
  Highly recommended.

poetry: v1.1.13 : minimal='1.5' (not OK)
To install: `python -m pip install poetry --upgrade [--user]`
  Needed for dependency management, publishing to PyPI.
  Recommended for virtual environments during development.

Command mkdocs is missing in the current environment.
To install: `python -m pip install mkdocs --upgrade [--user]`
  Needed for documentation generation.
  Highly recommended on workstations, discouraged on HPC clusters.

Module numpy is missing in the current environment.
To install: `python -m pip install nanobind --upgrade [--user]`
  Needed to construct C++ binary extension modules.

Module numpy is missing in the current environment.
To install: `python -m pip install numpy --upgrade [--user]`
  Needed to construct Modern Fortran binary extension modules./n
Command cmake is missing in the current environment.
To install see https://cmake.org/install/.
  Needed to build C++ and Modern Fortran binary extension modules.


Some components are missing. This is only a problem is you are planning to use them.
If you are working on your own machine, you must install these components yourself.
If you are working on a HPC cluster, preferably load the corresponding LMOD modules.

vsc20170@login1@vaughan [678] ~
>
```

## Installing on a HPC cluster (Linux)

On a HPC cluster software is installed in a central location, where users do not have write 
access. Hence, they must install their tools somewhere in their own file systems. In line with
general Linux expectations, we recommend  `~/.local`. Adding Python packages to a centrally 
installed Python distribution is achieved by pointing the `PYTHONUSERBASE` environment variable 
to this location and adding its `bin` folder to your `PATH`:

```shell
# in .bashrc
export PYTHONUSERBASE='path/to/my/homedir/.local/'
export PATH="$PATH:path/to/my/homedir/.local/bin/"
```

Now one can `pip install` packages with the `--user` flag. This works fine, even when working 
with different Python distributions. Installed CLIs will end up in `.local/bin/`, while packages 
installed using python 3.10, _e.g._, will end up in `.local/lib/python3.10/site-packages`. 

!!! Note "Note for VSC users"
    Use the `$VSC_DATA` file system for storing your `.local/` installations. `$VSC_HOME` is too 
    small for that purpose, and the `$VSC_SCRATCH` file system is not suitable for storing lots 
    of small files. (you might need to provide the expanded version of `$VSC_DATA`).



