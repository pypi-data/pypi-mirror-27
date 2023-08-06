#!/usr/bin/env python
from setuptools import setup
setup(
  name = 'cs.debug',
  description = 'Assorted debugging facilities.',
  author = 'Cameron Simpson',
  author_email = 'cs@cskk.id.au',
  version = '20171231',
  url = 'https://bitbucket.org/cameron_simpson/css/commits/all',
  classifiers = ['Programming Language :: Python', 'Programming Language :: Python :: 2', 'Programming Language :: Python :: 3', 'Development Status :: 4 - Beta', 'Intended Audience :: Developers', 'Operating System :: OS Independent', 'Topic :: Software Development :: Libraries :: Python Modules', 'License :: OSI Approved :: GNU General Public License v3 (GPLv3)'],
  install_requires = ['cs.logutils', 'cs.obj', 'cs.pfx', 'cs.py.func', 'cs.py.stack', 'cs.py3', 'cs.seq', 'cs.x'],
  keywords = ['python2', 'python3'],
  long_description = '* Lock, RLock, Thread: wrappers for threading facilties; simply import from here instead of there\n\n* thread_dump, stack_dump: dump thread and stack state\n\n* @DEBUG: decorator to wrap functions in timing and value debuggers\n\n* @trace: decorator to report call and return from functions\n\n* @trace_caller: decorator to report caller of function\n\n* TracingObject: subclass of cs.obj.Proxy that reports attribute use',
  package_dir = {'': 'lib/python'},
  py_modules = ['cs.debug'],
)
