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



