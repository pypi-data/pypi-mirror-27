#!/usr/bin/python

# -*- coding: utf-8 -*-

#
# Copyright (C) 2015-2018 Red Hat, Inc.
#    This copyrighted material is made available to anyone wishing to use,
#  modify, copy, or redistribute it subject to the terms and conditions of
#  the GNU General Public License v.2.
#
#    This application is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#    General Public License for more details.
#
# Authors:
#    Guy Streeter <guy.streeter@gmail.com>
#


from __future__ import print_function
import sys
import os
import errno

if sys.version_info[0] == 3:
    _pythonver = '3'
else:
    _pythonver = '2'

_package_name = 'python' + _pythonver + '-libnuma'
__author = 'Guy Streeter'
__author_email = 'guy.streeter@gmail.com'
__license = 'GPLv2+'
__version = '2.3.2'
__description = 'Python' + _pythonver + ' bindings for libnuma'
__URL = 'https://gitlab.com/guystreeter/python-libnuma'
__classifiers = [
    'Environment :: Other Environment',
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)',
    'Operating System :: POSIX :: Linux',
    'Programming Language :: Python',
    'Topic :: System :: Systems Administration',
    ]

from setuptools import setup, command
from distutils.command.build import build
from distutils.extension import Extension
from Cython.Distutils import build_ext
from babel.messages.frontend import compile_catalog as _compile_catalog
from babel.messages.frontend import init_catalog as _init_catalog

try:
    datadir = os.environ['DATADIR']
except:
    datadir = 'share'

try:
    docdir = os.environ['LICENSEDIR']
except KeyError:
    docdir = os.path.join(datadir, 'doc', _package_name)

data_files = [
    (docdir, ['COPYING', 'LICENSE']),
]

install_requires = None


class CompileMyCatalog(_compile_catalog, object):
    def initialize_options(self):
        super(CompileMyCatalog, self).initialize_options()
        self.domain = _package_name


class InitMyCatalog(_init_catalog, object):
    def initialize_options(self):
        super(InitMyCatalog, self).initialize_options()
        self.domain = _package_name


class all_build(build):
    sub_commands = [
        ('compile_catalog', None),
        ('build_ext', None),
        ] + build.sub_commands

in_dir = 'translations/locale'
if os.path.exists(in_dir):
    for lang in os.listdir(in_dir):
        src_file = os.path.join(in_dir, lang)
        if os.path.isdir(src_file):
            src_file = os.path.join(src_file,
                                    'LC_MESSAGES',
                                    _package_name+'.mo')
            install_path = os.path.join(datadir,
                                        'locale',
                                        lang,
                                        'LC_MESSAGES',)
            data_files.append((install_path, [src_file]))

setup(name=_package_name,
      version=__version,
      description=__description,
      author=__author,
      author_email=__author_email,
      license=__license,
      classifiers=__classifiers,
      long_description=__description,
      url=__URL,
      data_files=data_files,
      install_requires=install_requires,
      cmdclass={'build_ext': build_ext,
                'build': all_build,
                'compile_catalog': CompileMyCatalog,
                'init_catalog': InitMyCatalog,
                },
      ext_modules=[
          Extension('libnuma', ['src/libnuma.pyx'],
                    libraries=['numa'])
      ]
      )
