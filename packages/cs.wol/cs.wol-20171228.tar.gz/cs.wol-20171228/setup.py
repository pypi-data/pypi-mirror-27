#!/usr/bin/env python
from setuptools import setup
setup(
  name = 'cs.wol',
  description = 'Tool for sending a wake on LAN (WOL) packet out a specific interface to a specific MAC address.',
  author = 'Cameron Simpson',
  author_email = 'cs@cskk.id.au',
  version = '20171228',
  url = 'https://bitbucket.org/cameron_simpson/css/commits/all',
  classifiers = ['Programming Language :: Python', 'Programming Language :: Python :: 2', 'Programming Language :: Python :: 3', 'Development Status :: 4 - Beta', 'Intended Audience :: Developers', 'Operating System :: OS Independent', 'Topic :: Software Development :: Libraries :: Python Modules', 'License :: OSI Approved :: GNU General Public License v3 (GPLv3)'],
  entry_points = {'console_scripts': ['wol = cs.wol:main']},
  install_requires = [],
  keywords = ['python2', 'python3'],
  long_description = 'Every WOL tool I have seen takes IP addresses and (a) infers the\noutbound NIC from the routing table (directly or naively) and (b)\ndoes not provide control for specifying the outbound NIC. I needed\na tool to wake devices on a specific NIC, which do not have IP\naddresses, or do not have known IP addresses.',
  package_dir = {'': 'lib/python'},
  py_modules = ['cs.wol'],
)
