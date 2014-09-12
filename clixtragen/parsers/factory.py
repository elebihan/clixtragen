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

from .python import PythonParser
from gettext import gettext as _

class ParserFactory:
    """Factory which creates parsers"""

    def __init__(self):
        self._parsers = {
            'python': PythonParser,
        }

    def create_parser(self, name):
        """Creates a parser from its name.

        :param name: name of the parser
        :type name: str

        :returns: an instance of the desired parser
        :rtype: :class:`yaprogen.parsers.parser.Parser`
        """
        if name not in self._parsers:
            raise RuntimeError(_('unknown parser'))
        klass = self._parsers[name]
        return klass()

    @property
    def names(self):
        """Returns a list of the names of the available parsers.

        :return: list of parser names
        :rtype: list of str
        """
        return self._parsers.keys()

# vim: ts=4 sts=4 sw=4 et ai
