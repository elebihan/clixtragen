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
Common classes and helpers.
"""

import re
from gettext import gettext as _

import os
import logging
from gettext import bindtextdomain, textdomain

__LOG_LEVELS = {
    'debug': logging.DEBUG,
    'info': logging.INFO,
    'warning': logging.WARNING,
    'error': logging.ERROR
}

try:
    value = os.environ.get('CLIXTRAGEN_LOG', 'warning').lower()
    __level = __LOG_LEVELS[value]
except:
    __level = logging.WARNING

__logger = logging.getLogger('clixtragen')
__logger.setLevel(__level)

def debug(message):
    """Log a debug message.

    The message will only be printed to standard output if the environment
    variable 'CLIXTRAGEN_LOG' is set to 'debug'.

    :param message: the message to be logged.
    :type message: str.
    """
    __logger.debug(message)

def start_yaml(indent, in_list):
    prefix = 4 * indent * ' '
    text = prefix
    if in_list:
        prefix += 2 * ' '
        text += '- '
    return prefix, text

class ProgramInvocation:
    """Stores information about invocation of aprogram"""
    def __init__(self):
        self.options = []
        self.arguments = []

    def to_yaml(self):
        text = 'options:\n'
        for o in self.options:
            text += o.to_yaml(1, True)
        text += 'arguments:\n'
        for a in self.arguments:
            text += a.to_yaml(1, True)
        return text

class Argument:
    """Stores information about an argument of the program"""
    def __init__(self):
        self.name = None
        self.help = None

    def to_yaml(self, indent=0, in_list=False):
        prefix, text = start_yaml(indent, in_list)
        text += "name: {}\n".format(self.name or '')
        text += prefix
        text += "help: {}\n".format(self.help or '')
        return text

class Option:
    """Stores information about an option of the program"""
    def __init__(self):
        self.short_name = None
        self.long_name = None
        self.help = None
        self.action = None
        self.metavar = None
        self.choices = []

    def to_yaml(self, indent=0, in_list=False):
        prefix, text = start_yaml(indent, in_list)
        text += "short_name: {}\n".format(self.short_name or '')
        text += prefix
        text += "long_name: {}\n".format(self.long_name or '')
        text += prefix
        text += "help: {}\n".format(self.help or '')
        text += prefix
        text += "metavar: {}\n".format(self.metavar or '')
        text += prefix
        text += 'choices:\n'
        for c in self.choices:
            text += c.to_yaml(indent + 1, True)
        return text

class CommandGroup(Argument):
    """Stores information about a group of commands"""
    def __init__(self):
        Argument.__init__(self)
        self.choices = []

    def to_yaml(self, indent=0, in_list=False):
        prefix, text = start_yaml(indent, in_list)
        text = Argument.to_yaml(self, indent, in_list)
        text += prefix
        text += 'choices:\n'
        for c in self.choices:
            text += c.to_yaml(indent + 1, True)
        return text

class Command:
    """Stores information about a command"""
    def __init__(self):
        self.name = None
        self.help = None
        self.options = []
        self.arguments = []

    def to_yaml(self, indent=0, in_list=False):
        prefix, text = start_yaml(indent, in_list)
        text += "name: {}\n".format(self.name or '')
        text += prefix
        text += "help: {}\n".format(self.help or '')
        text += prefix
        text += 'options:\n'
        for o in self.options:
            text += o.to_yaml(indent + 1, True)
        text += prefix
        text += 'arguments:\n'
        for a in self.arguments:
            text += a.to_yaml(indent + 1, True)
        return text

# vim: ts=4 sts=4 sw=4 et ai
