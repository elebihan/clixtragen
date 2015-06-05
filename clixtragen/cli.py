#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# clixtragen - generates helpers for a command line interpreter
#
# Copyright (C) 2013 Eric Le Bihan
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the
# Free Software Foundation, Inc.,
# 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#

import sys
import argparse
import logging
from gettext import gettext as _
from clixtragen import __version__
from clixtragen.utils import setup_i18n
from clixtragen.parsers.python import PythonParser
from clixtragen.generators.zsh import ZshCompletionGenerator

logging.basicConfig()

setup_i18n()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--version',
                        action='version',
                        version=__version__)
    parser.add_argument('-y', '--yaml',
                        action='store_true',
                        dest='as_yaml',
                        default=False,
                        help=_('print program invocation as YAML and exit'))
    parser.add_argument('execname',
                        help=_('name of the executable'))
    parser.add_argument('filename',
                        help=_('source file to parse'))
    parser.add_argument('-o', '--output',
                        metavar='FILE',
                        help=_('set output filename'))

    args = parser.parse_args()

    parser = PythonParser()
    invocation = parser.parse_file(args.filename)
    invocation.name = args.execname

    if args.as_yaml:
        print(invocation.to_yaml().strip())
        sys.exit(0)

    generator = ZshCompletionGenerator()
    text = generator.generate(invocation)

    if args.output:
        with open(args.output, 'w') as f:
            f.write(text)
    else:
        print(text, end='')

# vim: ts=4 sts=4 sw=4 et ai
