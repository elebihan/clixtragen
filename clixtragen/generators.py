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
collection of generators
"""

class ZshCompletionGenerator(object):
    """Generates ZSH completion"""

    def generate(self, progname, args, opts):
        text = "#compdef {}\n\n".format(progname)
        text += "local curcontext=\"$curcontext\" line state expl ret=1\n\n"
        text += "_arguments -C -s \\\n"
        for opt in opts:
            if opt.sname and opt.lname:
                name = "'({0.sname} {0.lname})'{{{0.sname},{0.lname}}}'"
            elif opt.sname:
                name = "'{0.sname}"
            elif opt.lname:
                name = "'{0.lname}"
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

        for index, arg in enumerate(args):
            text += "\t'{0}:{1}:->{1}' \\\n".format(index + 1, arg.name)
        text += "&& ret=0\n\n"

        if args:
            text += "case \"$state\" in\n"
            for arg in args:
                fmt = "\t({0.name})\n\t\t_message '{0.help}' && ret=0\n\t\t;;\n"
                text += fmt.format(arg)
            text += "esac\n\n"

        text += "return ret\n"
        return text

# vim: ts=4 sts=4 sw=4 et ai
