"""
Copyright (C) 2016-2017 Mathias Stelzer

xtract is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

xtract is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
from __future__ import absolute_import, print_function, unicode_literals

import os

from io import open
from setuptools import setup, find_packages


__dirname__ = os.path.dirname(os.path.abspath(__file__))
module_dir = os.path.join(__dirname__, 'xtract')

__version__ = None
with open(os.path.join(module_dir, 'version.py'), encoding='utf8') as f:
    exec(f.read())


with open(os.path.join(__dirname__, 'README.rst'), encoding='utf8') as f:
    long_description = f.read()


setup(
    name='xtract',
    version=__version__,
    description='Library to (un)pack archives and (de)compress files',
    long_description=long_description,

    author='Mathias Stelzer',
    author_email='knoppo@rolln.de',
    url='https://rolln.de/knoppo/xtract',
    license='GNU GPLv3+',

    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    install_requires=[
        'python-magic'
    ],

    entry_points={
        "console_scripts": [
            'xtract = xtract.__main__:main'
        ]
    },

    zip_safe=False,

    keywords='xtract extract unpack pack archive compress decompress zip rar tar gz gzip bz bzip bz2 bzip2 xz'
             'magic python-magic',

    classifiers=[  # https://pypi.python.org/pypi?%3Aaction=list_classifiers
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        'Intended Audience :: Developers',

        'Topic :: System :: Archiving',
        'Topic :: System :: Archiving :: Compression',

        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',

        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)
