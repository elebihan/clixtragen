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

"""
collection of source file parsers
"""

import re
from gettext import gettext as _

class ProgArgument:
    """Stores information about an argument of the program"""
    __slots__ = ['name', 'help', 'metavar']

class ProgOption:
    """Stores information about an option of the program"""
    __slots__ = ['sname', 'lname', 'help', 'metavar', 'action']

class PythonParser(object):
    """Parses a Python file."""

    def parse_file(self, filename):
        args = []
        opts = []
        with open(filename) as f:
            text = f.read()
        text = re.sub(r'help=_\((.+)\)', r'help=\1', text)
        for m in re.findall(r'add_argument\(([-\'\",\w\n\s=]+)\)', text):
            info = {}
            for item in [x.strip() for x in m.split(',')]:
                fields = [f.strip('\'\"') for f in item.split('=')]
                if len(fields) == 1:
                    s = fields[0]
                    if s.startswith('--'):
                        info['lname'] = s
                    elif s.startswith('-'):
                        info['sname'] = s
                    else:
                        info['name'] = s
                elif len(fields) == 2:
                    info[fields[0]] = fields[1]
            if 'name' in info:
                arg = ProgArgument()
                arg.name = info.get('name')
                arg.help = info.get('help', None)
                arg.metavar = info.get('metavar', None)
                args.append(arg)
            else:
                opt = ProgOption()
                opt.sname = info.get('sname', None)
                opt.lname = info.get('lname', None)
                opt.action = info.get('action', None)
                opt.help = info.get('help', None)
                opt.metavar = info.get('metavar', None)
                opts.append(opt)
        return args, opts

# vim: ts=4 sts=4 sw=4 et ai
