#!/usr/bin/env python
from setuptools import setup
setup(
  name = 'cs.fileutils',
  description = 'convenience functions and classes for files and filenames/pathnames',
  author = 'Cameron Simpson',
  author_email = 'cs@cskk.id.au',
  version = '20171231.1',
  url = 'https://bitbucket.org/cameron_simpson/css/commits/all',
  classifiers = ['Programming Language :: Python', 'Programming Language :: Python :: 2', 'Programming Language :: Python :: 3', 'Development Status :: 4 - Beta', 'Intended Audience :: Developers', 'Operating System :: OS Independent', 'Topic :: Software Development :: Libraries :: Python Modules', 'License :: OSI Approved :: GNU General Public License v3 (GPLv3)'],
  install_requires = ['cs.deco', 'cs.env', 'cs.filestate', 'cs.lex', 'cs.logutils', 'cs.pfx', 'cs.py3', 'cs.range', 'cs.threads', 'cs.timeutils'],
  keywords = ['python2', 'python3'],
  package_dir = {'': 'lib/python'},
  py_modules = ['cs.fileutils'],
)
