#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import ast
from setuptools import find_packages, setup

_version_re = re.compile(r'__version__\s+=\s+(.*)')

with open('point/__init__.py', 'rb') as f:
    version = str(ast.literal_eval(_version_re.search(
        f.read().decode('utf-8')
    ).group(1)))

setup(
    name='point',
    version=version,
    description='python print utility.',
    author='Tsuyoshi Tokuda',
    url='https://github.com/tokuda109/point.py',
    license='MIT',
    packages=find_packages(),
    install_requires=[
        'six==1.11.0',
    ],
    extras_require={
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
