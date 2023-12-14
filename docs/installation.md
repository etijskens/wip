# Installation

## Prerequisites

In order to make full use of wiptools, it is higly recommended to first create a github account for storing your work with `git` version controlled. If you do not already have a GitHub account,

* create one at [Signing up for a new GitHub account](https://docs.github.com/en/get-started/signing-up-for-github/signing-up-for-a-new-github-account), and 

* create a (classic) personal access token following [these instructions](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-personal-access-token-classic). This is a kind of password for accessing your github repositories. When creating a GitHub personal access token for use with wiptools, make sure that you check the scopes `repo` and `read:org`. Store the access token in a file and remember its location.

## Installing on a workstation

`Wiptools` is Python CLI published on [PyPI](https://pypi.org/). To install, make sure that you have Python 3.9 or later and run:

```shell
> pip install wiptools
```

!!! Tip
    Consider installing in a virtual environment if you need to deal with different Python versions. To learn about Python virtual environments, checkout [this primer](https://realpython.com/python-virtual-environments-a-primer/).

This installs the bare `wip`. Because `wip` relies on quite a bit of other tools, installing al its
dependencies may waste quite a bit of resources, especially on clusters. For that reason the user
is responsible for installing them - if needed. The `wip env` command lists which tools are 
available in the current environment and which not, what they are used for and how they can be 
installed. Here is the output from `wip env` if all components are missing.

```shell
> wip env
For a full functional `wip` the following commands and packages must be available in your environment:

Python: v3.10.4 (OK)

Command git is missing in the current environment (minimal=v2.35).
To install see https://git-scm.com/book/en/v2/Getting-Started-Installing-Git.
  Needed for local and remote version control.
  Highly recommended.

Command gh is missing in the current environment (minimal=v2.31).
To install see https://cli.github.com/manual/installation.
  Enables `wip init` to create remote GitHub repositories.
  Highly recommended.

Command bump2version is missing in the current environment (minimal=v1.0).
To install: `python -m pip install bump2version --upgrade [--user]`
  Needed for version string management.
  Highly recommended.

Command poetry is missing in the current environment (minimal=v1.5).
To install: `python -m pip install poetry --upgrade [--user]`
  Needed for dependency management, publishing to PyPI.
  Highly recommended in development environments.

Command mkdocs is missing in the current environment (minimal=v1.4.3).
To install: `python -m pip install mkdocs --upgrade [--user]`
  Needed for documentation generation.
  Highly recommended on workstations, discouraged on HPC clusters.

Module nanobind is missing in the current environment (minimal=v1.4).
To install: `python -m pip install nanobind --upgrade [--user]`
  Needed to construct C++ binary extension modules.

Module numpy is missing in the current environment (minimal=v1.22).
To install: `python -m pip install numpy --upgrade [--user]`
  Needed to construct Modern Fortran binary extension modules (f2py is part of numpy).
  Generally extremely useful for scientific computing, HPC, ...

Command cmake is missing in the current environment (minimal=v3.18).
To install see https://cmake.org/install/.
  Needed to build C++ and Modern Fortran binary extension modules.

Some components are missing. This is only a problem is you are planning to use them.
If you are working on your own machine, you must install these components yourself.
If you are working on a HPC cluster, preferably load the corresponding LMOD modules.
```

## Installing on a HPC cluster (Linux)

On a HPC cluster software is installed in a central location, where users do not have write access. Users can, however, pip install additional Python packages by adding the `--user` flag. This installs the package by default under `~/.local`. _E.g._

```shell
> python --version
Python 3.10.4
> pip install --user wiptools
...
```

will install wiptools in `~/.local/lib/python3.10/site-packages`. On VSC clusters, however, the home directory is in the `$VSC_HOME` file system, which is rather small (<10GB) and therefor not suited for local installations. It is therefor recommended change the default `--user` installation location by setting the `PYTHONUSERBASE` environment variable. If you are on a VSC cluster, _e.g._ Vaughan, `$VSC_DATA` is the preferred file system for this. Therfor, add the following lines to your `.bashrc` file:

```shell
export PYTHONUSERBASE=$VSC_DATA/.local/
export PATH="$PATH:$PYTHONUSERBASE/bin/"
```

The first line ensures that `> pip install --user wiptools` will install wiptools in `$VSC_DATA/.local/lib/python3.10/site-packages` (when using Python 3.10, as above). The second line ensures that, if the package installs some CLIs, your shell will be able to find them. Wiptools indeed comes with a CLI `wip`:

```shell
> echo $VSC_DATA 
/data/antwerpen/201/vsc20170
> echo $PYTHONUSERBASE 
/data/antwerpen/201/vsc20170/.local
> which wip
/data/antwerpen/201/vsc20170/.local/bin/wip
```

As an alternative to using pip's `--user` flag, you can install wiptools in a virtual environment. To learn about Python virtual environments, checkout [this primer](https://realpython.com/python-virtual-environments-a-primer/).