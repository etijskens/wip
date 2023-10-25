# Python package wiptools

Python project skeleton set up and management.

## Quick start

### Installation

```shell
> pip install [--user] wiptools
```

### Create a skeleton for a new project `foo`

`wip init foo`, will ask you to supply a brief project description, a minimal Python 
version and a documentation format. `wip init` will also ask you a few other items 
the first time. If you did not choose a documentation format, you can add one later 
with `wip docs --md`, e.g.
```shell
path/to/workspace > wip init foo

Project info needed:
Enter a short description for the project: [<project_short_description>]: a foo-lish project
Enter the minimal Python version [3.8]: 3.9

[[Expanding cookiecutter template `/Users/etijskens/software/dev/workspace/wiptools/wiptools/cookiecutters/project`...
]] (done Expanding cookiecutter template `/Users/etijskens/software/dev/workspace/wiptools/wiptools/cookiecutters/project`)
Add documentation templates? press
  [enter] for no,
  [m] for markdown format,
  [r] for restructuredText format []: m

[[Expanding cookiecutter template `/Users/etijskens/software/dev/workspace/wiptools/wiptools/cookiecutters/project-doc-md`...
]] (done Expanding cookiecutter template `/Users/etijskens/software/dev/workspace/wiptools/wiptools/cookiecutters/project-doc-md`)

[[Adding documentation for components ...
]] (done Adding documentation for components )

[[Creating a local git repo...

[[Running `git init --initial-branch=main` in directory /Users/etijskens/software/dev/ws-wip/foo...
Initialized empty Git repository in /Users/etijskens/software/dev/ws-wip/foo/.git/
]] (done Running `git init --initial-branch=main` in directory /Users/etijskens/software/dev/ws-wip/foo)

[[Running `git add *` in directory /Users/etijskens/software/dev/ws-wip/foo...
]] (done Running `git add *` in directory /Users/etijskens/software/dev/ws-wip/foo)

[[Running `git add .gitignore` in directory /Users/etijskens/software/dev/ws-wip/foo...
]] (done Running `git add .gitignore` in directory /Users/etijskens/software/dev/ws-wip/foo)

[[Running `git commit -m "Initial commit from wip init foo"` in directory /Users/etijskens/software/dev/ws-wip/foo...
[main (root-commit) fca0133] Initial commit from wip init foo
 11 files changed, 281 insertions(+)
 create mode 100644 .gitignore
...
]] (done Running `git commit -m "Initial commit from wip init foo"` in directory 
/Users/etijskens/software/dev/ws-wip/foo)
]] (done Creating a local git repo)

[[Creating a remote GitHub repo...

[[Running `gh auth login --with-token kwargs={'stdin': <_io.TextIOWrapper name='/Users/etijskens/.wiptools/etijskens.pat' mode='r' encoding='UTF-8'>, 'text': True}` in directory /Users/etijskens/software/dev/ws-wip/foo...
]] (done Running `gh auth login --with-token kwargs={'stdin': <_io.TextIOWrapper name='/Users/etijskens/.wiptools/etijskens.pat' mode='r' encoding='UTF-8'>, 'text': True}` in directory /Users/etijskens/software/dev/ws-wip/foo)

[[Running `gh repo create --source . --public --push` in directory /Users/etijskens/software/dev/ws-wip/foo...
✓ Created repository etijskens/foo on GitHub
✓ Added remote https://github.com/etijskens/foo.git
Enumerating objects: 17, done.
Counting objects: 100% (17/17), done.
Delta compression using up to 8 threads
Compressing objects: 100% (12/12), done.
Writing objects: 100% (17/17), 3.57 KiB | 1.19 MiB/s, done.
Total 17 (delta 0), reused 0 (delta 0), pack-reused 0
To https://github.com/etijskens/foo.git
 * [new branch]      HEAD -> main
branch 'main' set up to track 'origin/main'.
✓ Pushed commits to https://github.com/etijskens/foo.git
]] (done Running `gh repo create --source . --public --push` in directory /Users/etijskens/software/dev/ws-wip/foo)
]] (done Creating a remote GitHub repo)
path/to/workspace/foo
```



### Listing project info

Cd into th project (`cd foo`) and use `wip info`:

```shell
path/to/foo > wip info
Project    : foo
Version    : 0.0.0
Package    : foo
GitHub repo: "https://github.com/<your github username>/foo"
Home page  : "https://<your github username>.github.io/foo"
Location   : /Users/etijskens/software/dev/ws-wip/foo

Structure of Python package foo
  foo [Python module]
  └── __init__.py
```

### Add components

You can add Python submodules (`--py`), C++ binary extension modules (`--cpp`) or 
Modern Fortran binary extension modules (`--f90`), as well as CLIs with a single 
command (`--cli`) or with subcommands(`--clisub`):

```shell
path/to/foo > wip add foo_py --py
path/to/foo > wip add foo_cpp --cpp
path/to/foo > wip add foo_f90 --f90
path/to/foo > wip add foo_cli --cli
path/to/foo > wip add foo_clisub --clisub
path/to/foo > wip info
Project    : foofoo
Version    : 0.0.0
Package    : foofoo
GitHub repo: https://github.com/<your github username>/foo
Home page  : https://<your github username>.github.io/foo
Location   : /Users/etijskens/software/dev/workspace/wiptools/.test-workspace/foofoo

Structure of Python package foofoo
  foofoo [Python module]
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
To build the binary extension modules 
## Links

 - [Wiptools GitHub repository](https://github.com/etijskens/fp=)
 - [Wiptools homepage](https://etijskens.github.io/wiptools)
