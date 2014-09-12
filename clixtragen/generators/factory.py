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

from .zsh import ZshCompletionGenerator
from .yaml import YamlGenerator
from gettext import gettext as _

class GeneratorFactory:
    """Factory which creates generators"""

    def __init__(self):
        self._generators = {
            'yaml': YamlGenerator,
            'zsh': ZshCompletionGenerator,
        }

    def create_generator(self, name):
        """Creates a generator from its name.

        :param name: name of the generator
        :type name: str

        :returns: an instance of the desired generator
        :rtype: :class:`yaprogen.generators.generator.Generator`
        """
        if name not in self._generators:
            raise RuntimeError(_('unknown generator'))
        klass = self._generators[name]
        return klass()

    @property
    def names(self):
        """Returns a list of the names of the available generators.

        :return: list of generator names
        :rtype: list of str
        """
        return self._generators.keys()

# vim: ts=4 sts=4 sw=4 et ai
