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

from ..common import CommandGroup, lowerize
from ..common import OPTION_TYPE_VALUE

_CMD_GROUP_FUNC_BODY = '''
    if (( CURRENT == 1 )); then
        _describe -t commands '{execname} command' _{prefix}_cmds || compadd "$@"
    else
        local curcontext="$curcontext"

        cmd="${{${{_{prefix}_cmds[(r)$words[1]:*]%%:*}}}}"

    if (( $#cmd )); then
            curcontext="${{curcontext%:*:*}}:{execname}-${{cmd}}:"

            _call_function ret _{prefix}_$cmd || _message 'no more arguments'
        else
            _message "unknown {execname} command: $words[1]"
        fi
        return ret
    fi
}}
'''

def _func_from_name(name):
    if name.startswith('file'):
        func = ":_files"
    elif name.startswith('dir'):
        func = ":_directories"
    elif name.startswith('iface'):
        func = ":_net_interfaces"
    elif name.startswith('url'):
        func = ":_urls"
    else:
        func = ''
    return func

class ZshCompletionGenerator(object):
    """Generates ZSH completion"""

    def _format_options(self, options):
        text = ""
        for opt in options:
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
            if opt.type == OPTION_TYPE_VALUE:
                if opt.metavar:
                    variable = opt.metavar.lower()
                    func = _func_from_name(variable)
                    value = '{}{}'.format(variable, func)
                else:
                    value = 'value'
                value = ":{}".format(value)
            else:
                value = ""
            text += " \\\n        {}{}{}'".format(name, help, value)
        return text

    def _format_arguments(self, execname, arguments):
        text = ""
        for index, arg in enumerate(arguments):
            if isinstance(arg, CommandGroup):
                fmt = " \\\n    '*::{} command:_{}_command'"
                text += fmt.format(execname, lowerize(execname))
            else:
                func = _func_from_name(arg.name)
                text += " \\\n        '{}:{}{}'".format(index + 1, arg.name, func)
        return text

    def _format_command(self, execname, command):
        funcname = "_{}_{}".format(lowerize(execname), command.name)
        text = "\n(( $+functions[{}] )) || {}()\n{{".format(funcname, funcname)
        text += "\n    _arguments -w -S -s"
        text += self._format_options(command.options)
        text += self._format_arguments(command.name, command.arguments)
        text += "\n}\n"
        return text

    def _format_command_group(self, execname, group):
        text = ""
        for cmd in group.choices:
            text += self._format_command(execname, cmd)
        prefix = lowerize(execname)
        funcname = "_{}_{}".format(prefix, group.name or "command")
        text += "\n(( $+functions[{}] )) || {}()\n{{".format(funcname, funcname)
        text += "\n    local -a _{}_cmds".format(prefix)
        text += "\n    _{}_cmds=(".format(prefix)
        for cmd in group.choices:
            text += "\n        \"{}:{}\"".format(cmd.name, cmd.help)
        text += "\n    )"
        text += _CMD_GROUP_FUNC_BODY.format(execname=execname,
                                            funcname=funcname,
                                            prefix=prefix)
        return text

    def generate(self, invocation):
        groups = filter(lambda a: isinstance(a, CommandGroup),
                        invocation.arguments)
        text = "#compdef {}\n".format(invocation.name)
        for group in groups:
            text += self._format_command_group(invocation.name, group)
        text += "\n_arguments -w -S -s"
        text += self._format_options(invocation.options)
        text += self._format_arguments(invocation.name, invocation.arguments)
        text += '\n\n# vim: ts=4 sts=4 sw=4 et ai\n'
        return text

# vim: ts=4 sts=4 sw=4 et ai
