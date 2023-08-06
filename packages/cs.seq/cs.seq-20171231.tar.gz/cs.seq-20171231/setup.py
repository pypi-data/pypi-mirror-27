#!/usr/bin/env python
from setuptools import setup
setup(
  name = 'cs.seq',
  description = 'Stuff to do with counters, sequences and iterables.',
  author = 'Cameron Simpson',
  author_email = 'cs@cskk.id.au',
  version = '20171231',
  url = 'https://bitbucket.org/cameron_simpson/css/commits/all',
  classifiers = ['Programming Language :: Python', 'Programming Language :: Python :: 2', 'Programming Language :: Python :: 3', 'Development Status :: 4 - Beta', 'Intended Audience :: Developers', 'Operating System :: OS Independent', 'Topic :: Software Development :: Libraries :: Python Modules', 'License :: OSI Approved :: GNU General Public License v3 (GPLv3)'],
  install_requires = ['cs.logutils'],
  keywords = ['python2', 'python3'],
  long_description = 'Presents:\n\n* Seq, a class for thread safe sequential integer generation.\n\n* seq(), a function to return such a number from a default global Seq instance.\n\n* the(), first(), last(), get0(): return the only, first, last or optional-first element of an iterable respectively.\n\n* TrackingCounter, a counting object with facilities for users to wait for it to reach arbitrary values.',
  package_dir = {'': 'lib/python'},
  py_modules = ['cs.seq'],
)
