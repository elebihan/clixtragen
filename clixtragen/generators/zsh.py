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
ZSH completion generator
"""

class ZshCompletionGenerator(object):
    """Generates ZSH completion"""

    def generate(self, invocation):
        text = "#compdef {}\n\n".format(invocation.name)
        text += "local curcontext=\"$curcontext\" line state expl ret=1\n\n"
        text += "_arguments -C -s \\\n"
        for opt in invocation.options:
            if opt.short_name and opt.long_name:
                name = "'({0.short_name} {0.long_name})'{{{0.short_name},{0.long_name}}}'"
            elif opt.short_name:
                name = "'{0.short_name}"
            elif opt.long_name:
                name = "'{0.long_name}"
            else:
                raise RuntimeError('invalid option')
            name = name.format(opt)
            if opt.help:
                help = "[{}]".format(opt.help)
            else:
                help = ""
            if not opt.action:
                if opt.metavar:
                    value = opt.metavar.lower()
                    if value.startswith('file'):
                        value += ":_files"
                    elif value.startswith('dir'):
                        value += ":_directories"
                    elif value.startswith('iface'):
                        value += ":_net_interfaces"
                    elif value.startswith('url'):
                        value += "_urls"
                else:
                    value = 'value'
                value = ":{}".format(value)
            else:
                value = ""
            text += "\t{}{}{}' \\\n".format(name, help, value)

        for index, arg in enumerate(invocation.arguments):
            text += "\t'{0}:{1}:->{1}' \\\n".format(index + 1, arg.name)
        text += "&& ret=0\n\n"

        if invocation.arguments:
            text += "case \"$state\" in\n"
            for arg in invocation.arguments:
                fmt = "\t({0.name})\n\t\t_message '{0.help}' && ret=0\n\t\t;;\n"
                text += fmt.format(arg)
            text += "esac\n\n"

        text += "return ret\n"
        return text

# vim: ts=4 sts=4 sw=4 et ai
