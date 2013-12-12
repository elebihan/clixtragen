==========
clixtragen
==========

Tool to generate helpers for a command line interpreter, such as ZSH
completion function.

Description
===========

`clixtragen(1)` generates helpers for a command line interpreter. It collects
information about the arguments of the program and its option by parsing its
source code.

It currently only supports Python scripts using ``argparse``.

Installation
============

To build and install for current user::

  $ PYTHONPATH=. ./setup.py sdist
  $ pip install --user dist/clixtragen*.tar.gz

To build and install globally (may require superuser privileges)::

  $ PYTHONPATH=. ./setup.py install

Usage
=====

To generate the ZSH completion for program `foo`::

  $ clixtragen foo /path/to/foo.py

License
=======

Released under the GNU General Public License v3 or later. See ``COPYING`` for
details.
