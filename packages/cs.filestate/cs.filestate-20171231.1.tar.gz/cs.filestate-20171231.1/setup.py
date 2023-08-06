#!/usr/bin/env python
from setuptools import setup
setup(
  name = 'cs.filestate',
  description = 'Trivial FileState class used to watch for file changes.',
  author = 'Cameron Simpson',
  author_email = 'cs@cskk.id.au',
  version = '20171231.1',
  url = 'https://bitbucket.org/cameron_simpson/css/commits/all',
  classifiers = ['Programming Language :: Python', 'Programming Language :: Python :: 2', 'Programming Language :: Python :: 3', 'Development Status :: 4 - Beta', 'Intended Audience :: Developers', 'Operating System :: OS Independent', 'Topic :: Software Development :: Libraries :: Python Modules', 'License :: OSI Approved :: GNU General Public License v3 (GPLv3)'],
  install_requires = [],
  keywords = ['python2', 'python3'],
  long_description = 'This is used to watch for size or modification time changes,\n    or to notice when a file path no longer points at the same file.',
  package_dir = {'': 'lib/python'},
  py_modules = ['cs.filestate'],
)
