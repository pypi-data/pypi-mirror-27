"""
:py:mod:`xtract`

(un)pack archives and (de)compress files.

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
from .utils import FileTypeNotSupported, xtract
from .types import (
    BZip2,
    GZip,
    Rar,
    Tar,
    XZ,
    Zip,
)


__all__ = (
    'xtract',
    'FileTypeNotSupported',
    'BZip2',
    'GZip',
    'Rar',
    'Tar',
    'XZ',
    'Zip',
)
