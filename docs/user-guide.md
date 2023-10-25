# User guide

The work horse of `wiptools` is the `wip` CLI. You can ask `wip` for help:

```shell
> wip --help
Usage: wip [OPTIONS] COMMAND [ARGS]...

  Command line interface wip.

...
```

as well as its subcommands:

```shell  
> wip info --help
Usage: wip info [OPTIONS]

  List info about the project's structure.

...
```

Wip relies on a bunch of other tools. You can test your environment for their presence and 
version compliance with `wip env`:

```shell
> wip env
For full `wip` functionality the following commands and packages must be available in our envirionment:

python 3.9.5 (default, Sep 20 2021, 16:33:56)  [Clang 12.0.5 (clang-1205.0.22.9)] (OK)
git version 2.35.1  (OK)
gh version 2.31.0 (2023-06-20) https://github.com/cli/cli/releases/tag/v2.31.0  (OK)
bumpversion: v1.0.1 (using Python v3.9.5) (OK)
nanobind 1.4.0 (OK)
numpy 1.25.0 : minimal='2.22' (not OK)
cmake version 3.21.2 (OK)
Poetry (version 1.5.1)  (OK)
mkdocs, version 1.4.3 from /Users/etijskens/software/dev/workspace/wiptools/.venv/lib/python3.9/site-packages/mkdocs (Python 3.9)  (OK)
```

## Create a new project skeleton 

You create a new project skeleton by executing `wip init <project_name>`. This will create a 
project folder `project_name` in the current working directory.

Before `wip` can create a new project skeleton, some developer specific and project specific 
information must be provided. 

### Developer info - GitHub access

!!! tip
    Checkout [Prerequisites][prerequisites] before using `wip`.

As the developer info is typically the same for many projects, it is stored in a `config.json` 
file. It contains your **name**, your **e-mail address**, and your **GitHub username**. Here is 
an example `config.json` file:

```json
{
  "full_name": "Bert Tijskens",
  "email_address": "engelbert.tijskens@uantwerpen.be",
  "github_username": "etijskens"
}
```

The default location of the `config.json` file is `$HOME/.wiptools`, but you can store it 
wherever you like, or with a different name, in case you need to deal with several sets of 
developer info, e.g. if you have work-related as well as personal projects, which are 
maintained on different GitHub accounts or with a different e-mail address.  In that case
use the `--config` flag to pass a config file other than the default one:

```shell
> wip init <project_name> --config=path/to/another_config.json [options]
```

If the config file does not exist, which is typically the case the first time you execute 
`wip init`, `wip` prompts you to supply your name, your e-mail address and your GitHub username,
and creates a new file to store the supplied info. If, on the other hand, the file exists, but has 
missing fields, the user is also prompted to supply them, but the file is **not** updated. When a 
new GitHub username is supplied, `wip` also prompts the user to supply a **GitHub personal access token**. This is a 
kind of password for accessing your GitHub account. It enables `wip` to automatically create a 
remote GitHub repository to store and backup you work. The personal access tokens you provide are 
always copied to `$HOME/.wiptools/github_{github_username}.pat`, where `github_username` is taken 
from the corresponding field in the `config.json` file. 

When you create a new project `wip` automatically creates a remote GitHub repository for 
the project. This is highly recommended, as this gets you a secure backup of your code 
(and all its prior versions) on a remote machine. The only effort needed is that you commit
and push your code regularly to the remote repo. 

!!! Note
    If you do not already have a GitHub account, create one at [Signing up for a new GitHub account](https://docs.github.com/en/get-started/signing-up-for-github/signing-up-for-a-new-github-account)and create a (classic) personal access token following [these instructions](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-personal-access-token-classic). When creating a GitHub personal access token for use with wip, make sure that you check the scopes `repo` and `read:org`.

!!! Note
    Wip will automatically create a local git repository and a remote public GitHub repo 
    for you project (if you have provided a GitHub username and a personal access token 
    (see[Developer info](#developer-info)). Use `--remote=private|none` to 
    create a private GitHub repo, or no remote repo at all.

### Project info

For every project you create, `wip` will ask you to supply 

- a brief project description, which can be left empty, and
- a minimal Python version.

!!! Note
    After creating the project skeleton, you must `cd` into your project folder to 
    apply other wip commands.

!!! Note
    If you choose to not create a remote GitHub repo (e.g. because you have no 
    internet connection), you can always add it later with `wip init_remote [--private]`.
) 

## Listing project info

Cd into the project folder (`cd foo`) and use `wip info`:

```shell
path/to > wip init FOO 
...
path/to > cd FOO
path/to/FOO > wip info --pkg --dev
Project    : FOO: <project_short_description>
Version    : 0.0.0
Package    : foo
GitHub repo: --
Home page  : --
Location   : /Users/etijskens/software/dev/workspace/.test-wip/FOO
docs format: none

Developer info:
  author         : Bert Tijskens
  e-mail         : engelbert.tijskens@uantwerpen.be
  GitHub username: etijskens

Structure of Python package foo
  foo [Python module]
  └── __init__.py
```

Note that wip translates the project name `FOO` in to the PEP compliant package name
`foo`, converting to lowercase (and replacing hyphens with underscores).

## Add components

You can add Python submodules (`--py`), C++ binary extension modules (`--cpp`) or 
Modern Fortran binary extension modules (`--f90`), as well as CLIs with a single 
command (`--cli`) or with subcommands(`--clisub`):

```shell
path/to/FOO > wip add foo_py --py
path/to/FOO > wip add foo_cpp --cpp
path/to/FOO > wip add foo_f90 --f90
path/to/FOO > wip add foo_cli --cli
path/to/FOO > wip add foo_clisub --clisub
path/to/FOO > wip info --pkg 
Project    : FOO: the foo package
Version    : 0.0.0
Package    : foo
GitHub repo: https://github.com/<your github username>/foo
Home page  : https://<your github username>.github.io/foo
Location   : /Users/etijskens/software/dev/workspace/wiptools/.test-workspace/foofoo
docs format: none

Structure of Python package foofoo
  foo [Python module]
  ├── __init__.py
  ├── foo_cli [CLI]
  │   └── __main__.py
  ├── foo_clisub [CLI]
  │   └── __main__.py
  ├── foo_cpp [C++ binary extension module]
  │   ├── foo_cpp.cpp
  │   └── foo_cpp.md
  ├── foo_f90 [Modern Fortran binary extension module]
  │   ├── foo_f90.f90
  │   └── foo_f90.md
  └── foo_py [Python module]
      └── __init__.py
```

Python submodules can contain other Python submodules, as well as binary extension
modules. You only need to preceed the module name with the path (relative to the 
package folder), e.g. to add a C++ binary extension module to the `foo_py` submodule:

```shell
path/to/FOO > wip add foo_py/bar --cpp
...
path/to/FOO > wip info
...
Structure of Python package foo
  foo [Python module]
  ├── __init__.py
  ...
  └── foo_py [Python module]
      ├── __init__.py
      └── bar [C++ binary extension module]
          ├── bar.cpp
          └── bar.md
```

To build the binary extension modules use the `wip build` command. This builds all
binary extension modules and installs them in the parent of the submodule folder. 
Hence, they can be imported using the path you specified when you added it. E.g. a
client script could import these modules as:

```python
import foo            # the foo package
import foo.foo_cpp    # the foo_cpp submodule (C++ binary extension) 
import foo.foo_f90    # the foo_f90 submodule (Fortran binary extension)
import foo.foo_py     # the foo_py submodule
import foo.foo_py.bar # the bar subsubmodule in the foo_py submodule
``` 

I the build process was successful, will see some dynamic libraries in the directory 
tree. On Linux and MacOS these have the `.so` (shared objecrt) extension and `.dll` 
On Windows. The middle part depends on the Python distribution the binary extension 
was built against, and on the operating system. 

```python
Structure of Python package foo
  foo [Python module]
  ├── __init__.py
  ├── foo_cli [CLI]
  │   └── __main__.py
  ├── foo_clisub [CLI]
  │   └── __main__.py
  ├── foo_cpp.cpython-39.darwin.so
  ├── foo_cpp [C++ binary extension module]
  │   ├── foo_cpp.cpp
  │   └── foo_cpp.md
  ├── foo_f90.cpython-39.darwin.so
  ├── foo_f90 [Modern Fortran binary extension module]
  │   ├── foo_f90.f90
  │   └── foo_f90.md
  └── foo_py [Python module]
      ├── __init__.py
      └── bar.cpython-39.darwin.so
      └── bar [C++ binary extension module]
          ├── bar.cpp
          └── bar.md
```

You can build a single binary extension by specifiyng its path:

```python
path/to/FOO > wip build foo_py/bar
```
or build all C++/Fortran binary extensions using `wip build --cpp|--f90`.

## Documentation

For small projects, we recommend writing down the documentation in `README.md`. 
Larger projects with submodules or CLIs are more conveniently documented with 
[mkdocs](https://mkdocs.org), using the [Markdown](https://www.markdownguide.org) 
format, or [sphinx](https//www.sphinx-doc.org/) using the 
[restructuredText](https://www.sphinx-doc.org/en/master/usage/restructuredtext/index.html). 
When creating a new project, wip asks for a documentation format. If you choose none, 
you can always add the necessary documentation templates running `wip docs [--md|--rst]`.

!!! Tip
    Learn documenting your project with mkdocs [here]
    (https://realpython.com/python-project-documentation-with-mkdocs/).

## Version management

Wip relies on [bump2version](https://pypi.org/project/bump2version/) for version 
management. Newly created project have a `bumpversion.cfg` file. The `bumpversion` 
command can directly be used, e.g.: `bump[2]version major|minor|patch|release`. 
There is also a wip subcommand `wip bump` that wraps the `bumpversion` command and 
lists information about the previous and the new version:

```shell
path/to/FOO > bumpversion patch
path/to/FOO > wip bump patch

[[Running `bump2version patch`` in directory 'foo' ...
]] (done Running `bump2version patch`)

foo v0.0.1-dev -> v0.0.2-dev

path/to/FOO > wip bump release

[[Running `bump2version release`` in directory 'foo' ...
]] (done Running `bump2version release`)

foo v0.0.2-dev -> v0.0.2

> wip bump minor

[[Running `bump2version minor`` in directory 'foo' ...
]] (done Running `bump2version minor`)

foo v0.0.2 -> v0.1.0-dev
```

## Publishing on PyPI

When your code is published on [PyPI](https://pypi.org/) users can effortlessly install it with
`pip install your-package`. Dependencies are automatically installed as well.

Wip relies on [poetry](https://python-poetry.org) for publishing to [PyPI](https://pypi.org/).
To be able to publish on PyPI, you must

1. [Create an account on PyPI](https://pypi.org/account/register/).
2. Log in on your account, and go to `account settings`. Scroll down and hit `Add API token`. 
3. Choose a token name, _e.g._ `poetry-publishing-on-pypi`, and select a scope, _e.g._ 
   `Entire account (all projects)` to use the token for publishing all your projects. 
4. Hit `Add token` to generate a new token, and copy the token.
5. Finally, add your API token to Poetry with this command
   `poetry config pypi-token.pypi your-api-token` (paste the copied token for `your-api-token`).

Now you can publish your code as below:

```shell
(wiptools-py3.9) ~/workspace/wiptools > poetry publish --build
Building wiptools (1.2.0-dev)
  - Building sdist
  - Built wiptools-1.2.0.dev0.tar.gz
  - Building wheel
  - Built wiptools-1.2.0.dev0-py3-none-any.whl

Publishing wiptools (1.2.0-dev) to PyPI
 - Uploading wiptools-1.2.0.dev0-py3-none-any.whl 100%
 - Uploading wiptools-1.2.0.dev0.tar.gz 100%
```

!!! Note
    You can publish a version of your code only once to PyPI. If you want to publish an 
    update, you must `bump2version` your code first. 