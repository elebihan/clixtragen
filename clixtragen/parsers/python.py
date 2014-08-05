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
Python source code parser.
"""

import ast
import re
from gettext import gettext as _
from ..common import ProgramInvocation, Argument, Option
from ..common import CommandGroup, Command
from ..common import debug

def _debug(message):
    debug("python parser: {}".format(message))

class ArgparseNode:
    """An node in a tree storing information about argparse parser.

    :param name: name of the node.
    :type name: str.
    """
    def __init__(self, name):
        self.name = name
        self.data = None
        self.children = []

    def search_child(self, name):
        """Searches for a child node by its name.

        If several children have the same name, the last child is returned.

        :param name: name of the node.
        :type name: str.
        """
        if self.name == name:
            return self
        candidates = [c for c in self.children if c.name == name]
        if candidates:
            return candidates[-1]
        for child in self.children:
            node = child.search_child(name)
            if node:
                return node
        return None

def convert_node_to_invocation(node):
    """Converts an ArgparseNode to a ProgramInvocation"""
    pi = ProgramInvocation()
    for child in node.children:
        if isinstance(child.data, CommandGroup):
            for gchild in child.children:
                command = convert_node_to_command(gchild)
                child.data.choices.append(command)
            pi.arguments.append(child.data)
        elif isinstance(child.data, Argument):
            pi.arguments.append(child.data)
        elif isinstance(child.data, Option):
            pi.options.append(child.data)
    return pi

def convert_node_to_command(node):
    """Converts an ArgparseNode to a Command"""
    cmd = node.data
    for child in node.children:
        if isinstance(child.data, Argument):
            cmd.arguments.append(child.data)
        elif isinstance(child.data, Option):
            cmd.options.append(child.data)
    return cmd

STATE_IDLE = 0
STATE_PARSE_CALL_FUNC = 1
STATE_PARSE_CALL_KW = 2
STATE_PARSE_CALL_ARG = 3
(CALL_ARG_TYPE_REF, CALL_ARG_TYPE_NUM, CALL_ARG_TYPE_STR) = range(0, 3)

def format_call_arg(arg):
    if arg[0] == CALL_ARG_TYPE_STR:
        return "'{}'".format(arg[1])
    else:
        return arg[1]

def format_call_kw(kw):
    if kw[0] == CALL_ARG_TYPE_STR:
        fmt = "{}='{}'"
    else:
        fmt = "{}={}"
    return fmt.format(kw[1], kw[2])

def sanitize_args(args):
    return [v for t, v in args if t == CALL_ARG_TYPE_STR]

def sanitize_keywords(keywords):
    items = [(n, v) for t, n, v in keywords if t == CALL_ARG_TYPE_STR]
    return dict(items)

def create_argument(args, keywords):
    args = sanitize_args(args)
    keywords = sanitize_keywords(keywords)
    if args[0].startswith('-'):
        o = Option()
        o.metavar = keywords.get('metavar', None)
        for a in args:
            if a.startswith('--'):
                o.long_name = a
            elif a.startswith('-'):
                o.short_name = a
        _debug("Created option '{}'".format(o))
    else:
        o = Argument()
        o.name = args[0]
        _debug("Created argument '{}'".format(o))
    o.help = keywords.get('help', None)
    return o

def create_command_group(args, keywords):
    args = sanitize_args(args)
    keywords = sanitize_keywords(keywords)
    grp = CommandGroup()
    grp.name = keywords.get('dest', None)
    grp.help = keywords.get('help', None)
    return grp

def create_command(args, keywords):
    args = sanitize_args(args)
    keywords = sanitize_keywords(keywords)
    cmd = Command()
    cmd.name = args[0]
    cmd.help = keywords.get('help', None)
    _debug("Created command '{}'".format(cmd))
    return cmd

class Call:
    """Stores information about a Python function call."""
    def __init__(self):
        self.args = []
        self.keywords = []
        self.cur_kw = None
        self.obj = None
        self.attr = None

    def __str__(self):
        text = ""
        if self.obj:
            text += "{0.obj}"
            if self.attr:
                text += "."
        if self.attr:
            text += "{0.attr}"
        text = text.format(self) + "("
        text += ", ".join(map(format_call_arg, self.args))
        if self.keywords:
            if self.args:
                text += ", "
            text += ", ".join(map(format_call_kw, self.keywords))
        return text + ")"

class ArgparseVisitor(ast.NodeVisitor):
    """Visits an AST, gathering information on calls to argparse module."""
    def __init__(self):
        ast.NodeVisitor.__init__(self)
        self.state = STATE_IDLE
        self.call = None
        self.dest = None
        self.root = None
        self.calls = []

    def visit_Str(self, node):
        if self.state == STATE_PARSE_CALL_ARG:
            self.call.args.append((CALL_ARG_TYPE_STR, node.s))
        elif self.state == STATE_PARSE_CALL_KW:
            self.call.keywords.append((CALL_ARG_TYPE_STR, self.call.cur_kw, node.s))

    def visit_Num(self, node):
        if self.state == STATE_PARSE_CALL_ARG:
            self.call.args.append((CALL_ARG_TYPE_NUM, node.n))
        elif self.state == STATE_PARSE_CALL_KW:
            self.call.keywords.append((CALL_ARG_TYPE_NUM, self.call.cur_kw, node.n))

    def visit_Name(self, node):
        if isinstance(node.ctx, ast.Load):
            if self.state == STATE_PARSE_CALL_FUNC:
                self.call.obj = node.id
            elif self.state == STATE_PARSE_CALL_ARG:
                self.call.args.append((CALL_ARG_TYPE_REF, node.id))
            elif self.state == STATE_PARSE_CALL_KW:
                self.call.keywords.append((CALL_ARG_TYPE_REF, self.call.cur_kw, node.id))
        elif isinstance(node.ctx, ast.Store):
            self.dest = node.id

    def visit_Attribute(self, node):
        if isinstance(node.ctx, ast.Load):
            if self.state == STATE_PARSE_CALL_FUNC:
                self.call.attr = node.attr
                self.visit(node.value)

    def visit_Call(self, node):
        if self.state != STATE_IDLE:
            return
        call = Call()
        self.calls.append(self.call)
        self.call = call

        self.state = STATE_PARSE_CALL_FUNC
        self.visit(node.func)

        self.state = STATE_PARSE_CALL_ARG
        for arg in node.args:
            self.visit(arg)

        self.state = STATE_PARSE_CALL_KW
        for kw in node.keywords:
            self.call.cur_kw = kw.arg
            self.visit(kw)
        if node.starargs:
            self.visit(node.starargs)
        if node.kwargs:
            self.visit(node.kwargs)

        self.state = STATE_IDLE

        self.process_call()

        self.call = self.calls.pop()

    def visit_Assign(self, node):
        if len(node.targets) > 1:
            return
        self.visit(node.targets[0])
        self.visit(node.value)

    def visit_Expr(self, node):
        self.visit(node.value)

    def process_call(self):
        _debug("Processing call '{}'".format(self.call))
        if self.call.attr == 'ArgumentParser':
            self.add_parser(self.dest)
        elif self.call.attr == 'add_subparsers':
            self.add_subparsers(self.call.obj,
                                self.dest,
                                self.call.args,
                                self.call.keywords)
        elif self.call.attr == 'add_argument':
            self.add_argument(self.call.obj,
                              self.call.args,
                              self.call.keywords)
        elif self.call.attr == 'add_parser':
            self.add_subparser(self.call.obj,
                               self.dest,
                               self.call.args,
                               self.call.keywords)
        else:
            _debug("Skipped call")

    def add_parser(self, name):
        _debug("Adding new parser '{}'".format(name))
        self.root = ArgparseNode(name)

    def add_subparsers(self, parent, name, args, keywords):
        _debug("Adding new subparsers '{}' to '{}'".format(name, parent))
        child = ArgparseNode(name)
        child.data = create_command_group(args, keywords)
        node = self.root.search_child(parent)
        node.children.append(child)

    def add_argument(self, name, args, keywords):
        _debug("Adding new argument/option to '{}'".format(name))
        child = ArgparseNode(None)
        child.data = create_argument(args, keywords)
        node = self.root.search_child(name)
        node.children.append(child)

    def add_subparser(self, parent, name, args, keywords):
        _debug("Adding new subparser '{}' to '{}'".format(name, parent))
        child = ArgparseNode(name)
        child.data = create_command(args, keywords)
        node = self.root.search_child(parent)
        node.children.append(child)

def ungettextize(text):
    sanitized = re.sub(r'help=_\((.+)\)', r'help=\1', text)
    return re.sub(r'metavar=_\((.+)\)', r'metavar=\1', sanitized)

class PythonParser(object):
    """Parses a Python file."""

    def parse_file(self, filename):
        with open(filename) as f:
            root = ast.parse(ungettextize(f.read()))
            visitor = ArgparseVisitor()
            visitor.visit(root)
            return convert_node_to_invocation(visitor.root)

# vim: ts=4 sts=4 sw=4 et ai
