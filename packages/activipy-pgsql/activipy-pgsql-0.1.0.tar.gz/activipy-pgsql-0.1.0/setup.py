"""This file is part of the activitypub_server package

Copyright (c) 2017 Mark Shane Hayden
Copyright (c) 2017 Coalesco Digital Systems Inc.

See the COPYRIGHT.txt file in the root directory of the package source for
full copyright notice

Distribution granted under the terms of EITHER GPLv3+ OR Apache v2

See LICENSE_*.txt files in the root directory for full license terms.
"""

from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Use the README file as the Long Description
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='activipy-pgsql',

    version='0.1.0',

    description='A PostgreSQL Environment for Activipy',
    long_description=long_description,

    url='https://src.coalesco.ca/w3c-social/activipy_pgsql',

    author='Coalesco Digital Systems Inc. - Mark Shane Hayden',
    author_email='mhayden@coalesco.ca',

    license='Apache Software License 2.0, GPLv3+',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Communications',
        'Topic :: Software Development :: Libraries',
        'License :: OSI Approved :: Apache Software License',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Programming Language :: Python :: 3',
    ],

    keywords='activitystream postgresql environment',

    package_dir={'activipy.pgsql': '.'},
    packages=[
        'activipy.pgsql',
        'activipy.pgsql.tests',
    ],

    install_requires=['activipy', 'psycopg2'],

    extras_require={
        'dev': ['check-manifest'],
        'test': ['coverage'],
    },

    entry_points="""
    """
)
