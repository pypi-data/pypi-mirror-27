"""
:py:mod:`xtract.types`

Archive and compression classes.


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

from xtract.base import BaseArchiveType, BaseCompressionType
from xtract.utils import register_xtract


logger = logging.getLogger(__name__)


@register_xtract
class Rar(BaseArchiveType):
    """A class to represent the archive type: rar."""

    name = 'rar'
    extensions = [
        'rar'
    ]
    mimetypes = [
        'application/rar',
        'application/x-rar'
    ]

    def get_unpack_command(self, source, destination):
        """Unpack the given rar archive to the given destination."""
        return "unrar x -o+ {} {}".format(source, destination)

    def get_pack_command(self, source_root, source_files, destination):
        """Pack the given source to a rar archive at the given destination."""
        return "rar a -r -ep1 {} {}".format(destination, ' '.join(source_files)), source_root


def rar(*args, **kwargs):
    return Rar().pack(*args, **kwargs)


@register_xtract
class Zip(BaseArchiveType):
    """A class to represent the archive type: zip."""

    name = 'zip'
    extensions = [
        'zip',
        'egg',
        'whl',
        'jar'
    ]
    mimetypes = [
        'application/zip',
        'application/x-zip',
    ]

    def get_unpack_command(self, source, destination):
        """Unpack the given zip archive to the given destination."""
        return "unzip -o {} -d {}".format(source, destination)

    def get_pack_command(self, source_root, source_files, destination):
        """Pack the given source to a zip archive at the given destination."""
        return "zip -r {} {}".format(destination, ' '.join(source_files)), source_root


def zip(*args, **kwargs):
    return Zip().pack(*args, **kwargs)


@register_xtract
class Tar(BaseArchiveType):
    """A class to represent the archive type: tar."""

    name = 'tar'
    extensions = [
        'tar'
    ]
    mimetypes = [
        "application/tar",
        "application/x-tar",
    ]

    def get_unpack_command(self, source, destination):
        """Unpack the given tar archive to the given destination."""
        return "tar --overwrite -C {} -xf {}".format(destination, source)

    def get_pack_command(self, source_root, source_files, destination):
        """Pack the given source to a tar archive at the given destination."""
        return "tar -C {} -cf {} {}".format(source_root, destination, ' '.join(source_files))


def tar(*args, **kwargs):
    return Tar().pack(*args, **kwargs)


@register_xtract
class GZip(BaseCompressionType):
    """A class to represent the archive type: gzip."""

    name = 'gzip'
    extensions = [
        'gz'
    ]
    mimetypes = [
        "application/gzip",
        "application/x-gzip",
    ]


def gzip(*args, **kwargs):
    return GZip().compress(*args, **kwargs)


@register_xtract
class XZ(BaseCompressionType):
    """A class to represent the archive type: xz."""

    name = 'xz'
    extensions = [
        'xz',
        'lzma',
        'txz',
        'tlz'
    ]
    mimetypes = [
        "application/xz",
        "application/x-xz",
    ]


def xz(*args, **kwargs):
    return XZ().compress(*args, **kwargs)


@register_xtract
class BZip2(BaseCompressionType):
    """A class to represent the archive type: bzip2."""

    name = 'bzip2'
    extensions = [
        'bz2',
        'bz',
        'tbz2',
        'tbz',
        'bzip2',
        'bzip',
    ]
    mimetypes = [
        "application/bzip",
        "application/bzip2",
        "application/x-bzip",
        "application/x-bzip2",
    ]


def bzip2(*args, **kwargs):
    return BZip2().compress(*args, **kwargs)
