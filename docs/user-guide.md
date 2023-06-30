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


### Listing project info

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

### Add components

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
Structure of Python package foofoo
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
Structure of Python package foofoo
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
or build all C++/Fortran binary extensions `wip build --cpp|--f90`.

## Links

 - [Wiptools GitHub repository](https://github.com/etijskens/fp=)
 - [Wiptools homepage](https://etijskens.github.io/wiptools)
