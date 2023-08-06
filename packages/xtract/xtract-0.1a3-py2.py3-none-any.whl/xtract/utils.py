"""
:py:mod:`xtract.utils`

The :func:`xtract.utils.xtract` utility and random utilities used in :py:mod:`xtract`.


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

import logging
import magic
import os
import shutil
import subprocess
import sys

if sys.version_info[0] < 3:
    IsADirectoryError = IOError


logger = logging.getLogger(__name__)


class FileTypeNotSupported(Exception):
    """The given file type is not supported."""

    pass


TYPES = []


def register_xtract(cls):
    """Register xtract type class."""
    TYPES.append(cls)
    return cls


def get_file_type(path, types=TYPES):
    """Get the magic mimetype and return according file extension."""
    if os.path.exists(path):
        try:
            mime = magic.from_file(path, mime=True)
        except IsADirectoryError:
            return
        for cls in types:
            if cls().has_mimetype(mime):
                return cls
    for cls in types:
        if cls().check_extension(path):
            return cls


def _xtract(source, destination, overwrite, delete_source, types):
    cls = get_file_type(source, types=types)

    if cls is None:
        raise FileTypeNotSupported(source)

    return cls().xtract(source, destination=destination, overwrite=overwrite, delete_source=delete_source)


def xtract(source, destination=None, overwrite=False, all=False, keep_intermediate=False, types=TYPES):
    final_destination = destination
    first_cycle = True
    while True:
        destination = None
        delete_source = not first_cycle and not keep_intermediate
        overwrite_current = not all and overwrite
        try:
            destination = _xtract(source, destination, overwrite_current, delete_source, types)
        except FileTypeNotSupported as e:
            if first_cycle:
                raise e
            break
            # if not all:
            #     raise e
            # if not first_cycle:
            #     break
        source = destination
        if not all:
            break
        first_cycle = False

    if final_destination:
        if os.path.exists(final_destination):
            if not overwrite:
                return source
        try:
            shutil.move(source, final_destination)
        except shutil.Error:
            pass
        else:
            source = final_destination
    return source


xtract.register = register_xtract


def delete_path(path):
    """Delete a file or directory (recursive)."""
    try:
        os.unlink(path)
    except IsADirectoryError:
        shutil.rmtree(path)


def run(cmd, cwd=None, log=True):
    """Run the given command as a subprocess."""
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=cwd)

    stdout, stderr = p.communicate()

    stdout = stdout.strip().decode()
    if stdout and log:
        logger.debug('Command output: {}'.format(stdout))

    stderr = stderr.strip().decode()
    if stderr and log:
        logger.error('Command error: {}'.format(stderr))

    if p.returncode:
        raise subprocess.CalledProcessError(p.returncode, cmd, output=stdout, stderr=stderr)
