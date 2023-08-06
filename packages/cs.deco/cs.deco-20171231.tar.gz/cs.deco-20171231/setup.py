#!/usr/bin/env python
from setuptools import setup
setup(
  name = 'cs.deco',
  description = 'Some decorator functions: @decorator, @cached.',
  author = 'Cameron Simpson',
  author_email = 'cs@cskk.id.au',
  version = '20171231',
  url = 'https://bitbucket.org/cameron_simpson/css/commits/all',
  classifiers = ['Programming Language :: Python', 'Programming Language :: Python :: 2', 'Programming Language :: Python :: 3', 'Development Status :: 4 - Beta', 'Intended Audience :: Developers', 'Operating System :: OS Independent', 'Topic :: Software Development :: Libraries :: Python Modules', 'License :: OSI Approved :: GNU General Public License v3 (GPLv3)'],
  install_requires = [],
  keywords = ['python2', 'python3'],
  long_description = '* @decorator: decorator for decorators to imbue them with optional keyword arguments.\n* @cache: decorator for functions to cache their return value subject to some change detection.',
  package_dir = {'': 'lib/python'},
  py_modules = ['cs.deco'],
)
