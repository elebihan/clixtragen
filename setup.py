#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# clixtragen - generates helpers for a command line interpreter
#
# Copyright (c) 2013 Eric Le Bihan <eric.le.bihan.dev@free.fr>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

from setuptools import setup, find_packages
from disthelpers import extract_messages, init_catalog, update_catalog
from disthelpers import build, build_catalog, build_man
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
      keywords=['command line', 'code generator'],
      install_requires=['docutils >= 0.11'],
      packages=find_packages(),
      scripts=['scripts/clixtragen'],
      data_files=[],
      include_package_data=True,
      author='Eric Le Bihan',
      author_email='eric.le.bihan.dev@free.fr',
      cmdclass={'build': build,
                'build_man': build_man,
                'extract_messages': extract_messages,
                'init_catalog': init_catalog,
                'update_catalog': update_catalog,
                'build_catalog': build_catalog})

# vim: ts=4 sts=4 sw=4 sta et ai
