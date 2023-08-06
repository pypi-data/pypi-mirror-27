#!/usr/bin/env python
from setuptools import setup
setup(
  name = 'cs.app.mklinks',
  description = 'Tool for finding and hardlinking identical files.',
  author = 'Cameron Simpson',
  author_email = 'cs@cskk.id.au',
  version = '20171228',
  url = 'https://bitbucket.org/cameron_simpson/css/commits/all',
  classifiers = ['Programming Language :: Python', 'Programming Language :: Python :: 2', 'Programming Language :: Python :: 3', 'Development Status :: 4 - Beta', 'Intended Audience :: Developers', 'Operating System :: OS Independent', 'Topic :: Software Development :: Libraries :: Python Modules', 'License :: OSI Approved :: GNU General Public License v3 (GPLv3)'],
  entry_points = {'console_scripts': ['mklinks = cs.app.mklinks:main']},
  install_requires = ['cs.fileutils', 'cs.logutils', 'cs.pfx', 'cs.py.func'],
  keywords = ['python2', 'python3'],
  long_description = 'Mklinks walks supplied paths looking for files with the same content,\nbased on a cryptographic checksum of their content. It hardlinks\nall such files found, keeping the newest version.\n\nUnlike some rather naive tools out there, mklinks only compares\nfiles with other files of the same size, and is hardlink aware - a\npartially hardlinked tree is processed efficiently and correctly.',
  package_dir = {'': 'lib/python'},
  py_modules = ['cs.app.mklinks'],
)
