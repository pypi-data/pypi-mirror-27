Diamond-Patterns
================

**Diamond-Patterns** are scaffolds for knowledge work.  Use patterns to go faster.

The patterns currently included with Diamond-Patterns are:

- **analysis**: An R project suitable for data analysis
- **ansible**: A linux system configuration container
- **article**: A LaTeX article with sections and graphics
- **blog**: A blog based on Jekyll with auto-generating git hooks
- **book**: A LaTeX book
- **presentation**: An HTML5 presentation
- **python**: A Python package
- **website**: A website based on Jekyll

Installation
------------

UNIX
^^^^

Install on Linux, BSD, or OS X.  Supports system-wide installation and python virtual environments.

::

    pip install diamond-patterns

OS X
^^^^

Install system-wide with Homebrew.

::

    brew install https://raw.github.com/iandennismiller/diamond-patterns/master/etc/diamond-patterns.rb

Windows
^^^^^^^

Diamond-patterns installs system-wide with Administrator privileges.
All you need is Python.

::

    start-process powershell –verb runAs
    easy_install -U mr.bob==0.1.2
    pip install diamond-patterns

Usage
-----

To list all of the available patterns:

::

    diamond list

To create an `article` based on Diamond-Patterns, try the following:

::

    mkdir ~/Documents/my-article
    cd ~/Documents/my-article
    diamond --skel article scaffold

Resources
---------

- `Documentation <http://diamond-patterns.readthedocs.io/>`_
- `GitHub Project Page <http://github.com/iandennismiller/diamond-patterns>`_
- `Python Project on PyPi <http://pypi.python.org/pypi/Diamond-Patterns>`_
