==========
clixtragen
==========

--------------------------
Generate helpers for a CLI
--------------------------

:Author: Eric Le Bihan <eric.le.bihan.dev@free.fr>
:Copyright: 2013 Eric Le Bihan
:Manual section: 1

SYNOPSIS
========

clixtragen [OPTIONS] <executable name> <source file>

DESCRIPTION
===========

`clixtragen(1)` generates helpers for a command line interpreter, such as ZSH
completion function.

OPTIONS
=======

-f LANGUAGE, --from LANGUAGE    set input language (default python)
-g, --list-generators           print list of available generators and exit
-o FILE, --output FILE          set output filename
-p, --list-parsers              print list of available parsers and exit
-t FORMAT, --to FORMAT          set output format (default YAML)

.. vim: ft=rst
