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

from distutils.core import setup
from disthelpers import build, build_trans, build_man, install_data
from clixtragen import __version__

setup(name='clixtragen',
      version=__version__,
      description='Generates helpers for a CLI',
      long_description='''
      This tool generates helpers for a command line interpreter,
      such as ZSH completion function.
      ''',
      license='GPLv3+',
      url='https://github.com/elebihan/clixtragen/',
      platforms=['linux'],
      classifiers=('Programming Language :: Python :: 3',
                   'Intended Audience :: Developers',
                   'Natural Language :: English',
                   'Development Status :: 2 - Pre-Alpha',
                   'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',),
      requires=['docutils (>=0.11)'],
      packages=['clixtragen', 'clixtragen/generators', 'clixtragen/parsers'],
      scripts=['scripts/clixtragen'],
      data_files=[('share/man/man1', ['build/man/man1/clixtragen.1'])],
      author='Eric Le Bihan',
      author_email='eric.le.bihan.dev@free.fr',
      cmdclass = {'build': build,
                  'build_man': build_man,
                  'build_trans': build_trans,
                  'install_data': install_data})

# vim: ts=4 sts=4 sw=4 sta et ai
