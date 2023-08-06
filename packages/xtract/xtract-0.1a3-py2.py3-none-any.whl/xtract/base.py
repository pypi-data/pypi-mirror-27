"""
:py:mod:`xtract.base`

Base classes for archive and compression types.


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

import magic
import logging
import os
import sys

from xtract.utils import run, delete_path


logger = logging.getLogger(__name__)


if sys.version_info[0] < 3:
    FileExistsError = OSError


class BaseFileType(object):
    """Archive type base class."""

    #: Name for this archive type
    name = NotImplemented

    #: List of possible file suffix.
    #: The first entry is considered default and used when packing new archives
    extensions = []

    #: Suffix that will be appended to extracted filename if original
    #: file has none
    unknown_suffix = '-xtract'

    #: List of possible mime types
    mimetypes = []

    def __repr__(self):
        """Return the objects python representation."""
        return '<{} {}>'.format(self.__class__.__name__, self.name)

    def __str__(self):
        """Return the objects string representation."""
        return str(self.name)

    def get_extensions(self):
        """Make sure extensions start with a dot and yield them."""
        for extension in self.extensions:
            if not extension.startswith('.'):
                extension = '.' + extension
            yield extension

    @property
    def default_extension(self):
        """Return the first extension as default."""
        return next(self.get_extensions())

    def check_extension(self, path):
        """Check whether the path ends with an archive suffix."""
        for extension in self.get_extensions():
            if path.endswith(extension):
                return extension

    def remove_extension(self, path):
        """Remove the extension from the given path and return it."""
        extension = self.check_extension(path)
        if extension is None:
            return
        return path[:-len(extension)]

    def has_mimetype(self, mimetype):
        return mimetype in self.mimetypes

    def check_mimetype(self, path):
        mime = magic.from_file(path, mime=True)
        return self.has_mimetype(mime)

    def clean_destination(self, destination, overwrite):
        if not os.path.exists(destination):
            return
        if not overwrite:
            raise FileExistsError(destination)
        delete_path(destination)

    def run_cmd(self, cmd):
        cwd = None
        if isinstance(cmd, tuple):
            cmd, cwd = cmd
        run(cmd, cwd)

    ##########################################################################
    # xtract

    def get_xtract_default_destination(self, source):
        destination = self.remove_extension(source)
        if destination is None:
            destination = source + self.unknown_suffix
        return destination

    def get_xtract_destination(self, source, destination=None):
        if destination is None:
            return self.get_xtract_default_destination(source)
        if not os.path.isdir(destination):
            return destination
        basename = os.path.basename(self.get_xtract_default_destination(source))
        return os.path.join(destination, basename)

    def xtract(self, source, destination=None, overwrite=False, delete_source=False):
        destination = self.get_xtract_destination(source, destination)
        self.clean_destination(destination, overwrite)

        self.pre_xtract(source, destination)

        cmd = self.get_xtract_command(source, destination)
        self.run_cmd(cmd)

        if delete_source:
            delete_path(source)

        return destination

    def pre_xtract(self, source, destination):
        pass

    def get_xtract_command(self, source, destination):
        raise NotImplementedError

    ##########################################################################
    # insert

    def get_insert_default_destination(self, source):
        return source + self.default_extension

    def get_insert_destination(self, source, destination=None):
        if destination is None:
            return self.get_insert_default_destination(source)
        if not os.path.isdir(destination):
            if not destination.endswith(self.default_extension):
                destination += self.default_extension
            return destination
        basename = os.path.basename(self.get_insert_default_destination(source))
        return os.path.join(destination, basename)


class BaseArchiveType(BaseFileType):

    def unpack(self, source, destination=None, overwrite=False):
        return self.xtract(source, destination=destination, overwrite=overwrite)

    def pre_unpack(self, source, destination):
        try:
            os.makedirs(destination)
        except OSError:
            pass

    def pre_xtract(self, *args, **kwargs):
        return self.pre_unpack(*args, **kwargs)

    def get_unpack_command(self, source, destination):
        raise NotImplementedError

    def get_xtract_command(self, *args, **kwargs):
        return self.get_unpack_command(*args, **kwargs)

    def pack(self, source_root, source_files=None, destination=None, overwrite=False, delete_source=False):
        original_source_root = source_root
        if source_files is None:
            source_root = os.path.dirname(source_root)
            source_files = os.path.basename(original_source_root)
            if destination is None:
                destination = source_root
        destination = self.get_insert_destination(original_source_root, destination)

        source_files = self.get_source_files(source_root, source_files)

        self.clean_destination(destination, overwrite)

        self.pre_pack(source_root, source_files, destination)

        cmd = self.get_pack_command(source_root, source_files, destination)
        self.run_cmd(cmd)

        if delete_source:
            delete_path(original_source_root)

        return destination

    def get_source_files(self, source_root, source_files):
        if not isinstance(source_files, (tuple, list)):
            source_files = [source_files]
        for path in source_files:
            if os.path.isabs(path):
                yield os.path.relpath(path, source_root)
            else:
                yield path

    def pre_pack(self, source_root, source_files, destination):
        pass

    def get_pack_command(self, source_root, source_files, destination):
        raise NotImplementedError


class BaseCompressionType(BaseFileType):

    def decompress(self, source, destination=None, overwrite=False):
        return self.xtract(source, destination=destination, overwrite=overwrite)

    def pre_decompress(self, source, destination):
        try:
            os.makedirs(os.path.dirname(destination))
        except OSError:
            pass

    def pre_xtract(self, *args, **kwargs):
        return self.pre_decompress(*args, **kwargs)

    def get_decompress_command(self, source, destination):
        """Return command to decompress the given file to the given destination."""
        return "{} --decompress -c {} > {}".format(self.name, source, destination)

    def get_xtract_command(self, *args, **kwargs):
        return self.get_decompress_command(*args, **kwargs)

    def compress(self, source, destination=None, overwrite=False, delete_source=False):
        destination = self.get_insert_destination(source, destination)

        self.clean_destination(destination, overwrite)

        self.pre_compress(source, destination)

        cmd = self.get_compress_command(source, destination)
        self.run_cmd(cmd)

        if delete_source:
            delete_path(source)

        return destination

    def pre_compress(self, source, destination):
        pass

    def get_compress_command(self, source, destination):
        """Return command to compress the given file to the given destination."""
        path, filename = os.path.split(source)
        return "{} -c {} > {}".format(self.name, filename, destination), path
