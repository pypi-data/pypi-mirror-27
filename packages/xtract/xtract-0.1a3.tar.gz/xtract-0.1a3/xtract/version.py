"""
:py:mod:`xtract.version`

Version definition and formatting.


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

import datetime
import os
import subprocess

from collections import namedtuple


Version = namedtuple('Version', ['major', 'minor', 'patch', 'pre_release', 'sub'])


# Change the version here!
# * Use pre_release 'final' and sub 0 for stable
# * Use pre_release 'alpha' and sub 0 for development (instead of 'dev')
#
# Examples:
# (0,  1, 0, 'final', 0) -> '0.1.0'
# (42, 1, 3, 'final', 0) -> '42.1.3'
# (0,  1, 0, 'alpha', 0) -> '0.1.0.dev20170101133742'
# (0,  1, 0, 'alpha', 1) -> '0.1.0a1'
# (1,  0, 1, 'rc',    0) -> '1.0.1rc0'
# (1,  0, 1, 'rc',    2) -> '1.0.1rc2'
VERSION = Version(0, 1, 0, 'alpha', 3)


def get_version(version):
    """Return a PEP 440-compliant version."""
    assert len(version) == 5
    assert version[3] in ('alpha', 'beta', 'rc', 'final')

    parts = 2 if version[2] == 0 else 3
    main = '.'.join([str(p) for p in version[:parts]])

    sub = ''
    if version[3] == 'alpha' and version[4] == 0:
        timestamp = get_git_commit_timestamp()
        if timestamp:
            sub = '.dev{}'.format(timestamp)
    elif version[3] != 'final':
        mapping = {'alpha': 'a', 'beta': 'b', 'rc': 'rc'}
        sub = mapping[version[3]] + str(version[4])

    return main + sub


def get_git_commit_timestamp():
    """
    Return a numeric identifier of the latest git changeset.

    The result is the UTC timestamp of the changeset in YYYYMMDDHHMMSS format.
    This value isn't guaranteed to be unique, but collisions are very unlikely,
    so it's sufficient for generating the development version numbers.
    """
    repo_dir = os.path.dirname(os.path.abspath(__file__))
    git_log = subprocess.Popen(
        'git log --pretty=format:%ct --quiet -1 HEAD',
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        shell=True, cwd=repo_dir, universal_newlines=True,
    )
    timestamp = git_log.communicate()[0]
    try:
        timestamp = datetime.datetime.utcfromtimestamp(int(timestamp))
    except ValueError:
        return None
    return timestamp.strftime('%Y%m%d%H%M%S')


__version_info__ = VERSION
__version__ = get_version(__version_info__)
