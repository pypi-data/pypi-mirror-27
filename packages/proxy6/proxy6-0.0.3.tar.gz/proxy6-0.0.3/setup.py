#!/usr/bin/env python
# coding: utf8

from __future__ import print_function, unicode_literals

import os
import sys

from setuptools import setup, find_packages

sys.path.insert(0, 'proxy6')

from proxy6 import __version__

VERSION = __version__

sys.path.pop(0)

if os.path.exists('README.rst'):
    with open('README.rst') as fp:
        README = fp.read()
else:
    README = 'proxy6\n======\n\nA 2/3 compatible crawler http proxy pool.'

setup(
    name='proxy6',
    version=VERSION,
    description='A 2/3 compatible crawler http proxy pool.',
    long_description=README,
    license='MIT',
    author='xlzd',
    author_email='i@xlzd.me',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Environment :: Console',
        'Topic :: Internet',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    url='https://github.com/xlzd/proxy6',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'proxy6=proxy6:main',
        ],
    }
)
