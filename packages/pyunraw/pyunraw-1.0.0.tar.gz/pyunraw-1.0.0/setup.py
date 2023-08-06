#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import os

from setuptools import setup, find_packages, Extension
from setuptools.command.install import install as _install

here = os.path.abspath(os.path.dirname(__file__))

# Get the long description from the relevant file
with open(os.path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='pyunraw',
    version='1.0.0',
    description='A CPython implementation of dcraw',
    long_description=long_description,
    url='https://launchpad.net/pyunraw',
    author='Vincent Vande Vyvre',
    author_email='vincent.vandevyvre@oqapy.eu',
    license='GPL-3',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Multimedia :: Graphics',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: C',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython'
    ],
    keywords='raw image dcraw digital photo',
    packages = find_packages('src'),
    package_dir = {'': 'src'},
    package_data={'':['src/*.c']},
    install_requires=[],
    ext_modules=[
        Extension('_pyunraw',
            ['src/pyunrawmodule-9-28.c'],
            include_dirs=[],
            library_dirs=[],
            libraries=['jasper',
                      'lcms2',
                      'jpeg'],
            )
    ],
)
