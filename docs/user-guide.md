# User guide

The work hors of `wiptools` is the `wip` CLI.

## Developer info

Wip stores your name, and e-mail adress, and optionally also your GitHub username
(see [signing up for a new GitHub account](https://docs.github.
com/en/get-started/signing-up-for-github/signing-up-for-a-new-github-account))
and a GitHub personal access token (check 
[this](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-personal-access-token-classic)
for details). The latter is used to automatically create a remote repository for a 
new project. Wip will ask you for missing info and remember it.

!!! Note 
    When creating a GitHub personal access token for use with wip, make sure that 
    you check the scopes `repo` and `read:org`.

Wip builds on other tools. You can test your environment for their presence with 
`wip env`.

## Create a new skeleton 

Use the command `wip init <project_name>`. This will create the project in the folder 
`project_name`. Wip will ask you to supply 

- a brief project description, 
- a minimal Python version, and
- a documentation generation format (none, Markdown, or restructuredText) 

Wip will automatically create a local git repositoy and a remote public GitHub repo 
for you project (if you have provided a GitHub username and a personal access token 
(see[Developer info](#developer-info)). Use `--remote-visibility=private|none` to 
create a private GitHub repo, or no remote repo at all. 

!!! Note
    After creating the project skeleton, you must `cd` into your project folder to 
    apply other wip commands.

!!! Tip
    If your work requires different developer info can specify a config file: 
    `wip init --config=personal-config.json`. If the file exists, it will retrieve 
    the developer info from it, otherwise it will ask for new developer info and 
    save it in the file. The default configuration file is in 
    `$HOME/.wiptools/config.json`. Personal access tokens for GitHub are also stored 
    there.

!!! Note
    If you choose to not create a remote GitHub repo (e.g. because you have no 
    internet connection), you can always add it later with `wip remote [--private]`.
) 


## Listing project info

Cd into the project folder (`cd foo`) and use `wip info`:

```shell
path/to > wip init FOO
...
path/to > cd FOO
path/to/FOO > wip info
Project    : FOO
Version    : 0.0.0
Package    : foo
GitHub repo: "https://github.com/<your github username>/foo"
Home page  : "https://<your github username>.github.io/foo"
Location   : /Users/etijskens/software/dev/ws-wip/foo

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
path/to/FOO > wip info
Project    : FOO
Version    : 0.0.0
Package    : foo
GitHub repo: https://github.com/<your github username>/foo
Home page  : https://<your github username>.github.io/foo
Location   : /Users/etijskens/software/dev/workspace/wiptools/.test-workspace/foofoo

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
format, or [sphinx](https//sphinx-doc.org) using the 
[restructuredText](https://www.sphinx-doc.org/en/master/usage/restructuredtext/index.html). 
When creating a new project, wip asks for a documentation format. If you choose none, 
you can always add the necessary documentation templates running `wip docs [--md|--rst]`

## Version management

Wip relies on [bump2version](https://pypi.org/project/bump2version/) for version 
management. Newly created project have a `bumpversion.cfg` file. The `bumpversion` 
command can directly be used, e.g.: `bump[2]version major|minor|patch|release`. 
There is also a wip subcommand `wip bump` that wraps the `bumpversion` command and 
lists information about the previous and the new version:

```shell
path/to/FOO > bumpversion patch
path/to/FOO > wip bump patch

[[Running `bump2version patch`` in directory 'oops' ...
]] (done Running `bump2version patch`)

oops v0.0.1-dev -> v0.0.2-dev

path/to/FOO > wip bump release

[[Running `bump2version release`` in directory 'oops' ...
]] (done Running `bump2version release`)

oops v0.0.2-dev -> v0.0.2

> wip bump minor

[[Running `bump2version minor`` in directory 'oops' ...
]] (done Running `bump2version minor`)

oops v0.0.2 -> v0.1.0-dev
```

## Links

 - [Wiptools GitHub repository](https://github.com/etijskens/fp=)
 - [Wiptools homepage](https://etijskens.github.io/wiptools)
