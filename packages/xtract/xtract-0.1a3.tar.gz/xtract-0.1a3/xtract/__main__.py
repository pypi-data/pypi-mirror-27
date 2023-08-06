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

import argparse
import logging
import sys

from xtract.utils import xtract, FileTypeNotSupported
from xtract.version import __version__


DESCRIPTION = """\
xtract wraps various other archiving and compression tools. It tries
to determine the required tool by checking the file's magic (mimetype)
header and if that fails its filename suffix.
"""


logger = logging.getLogger(__name__)


def get_parser():
    kwargs = {
        'prog': 'xtract',
        'description': DESCRIPTION
    }
    parser = argparse.ArgumentParser(**kwargs)
    parser.add_argument('source',
                        help='The file to unpack/decompress')
    parser.add_argument('destination',
                        nargs='?',
                        help='The destination directory (or file, if source is compressed file)')

    parser.add_argument('-V', '--version',
                        action='version',
                        version='xtract {}'.format(__version__))

    parser.add_argument('-o', '--overwrite',
                        action='store_true',
                        help='Overwrite the destination if it exists')

    parser.add_argument('-a', '--all',
                        action='store_true',
                        help='Unpack/Decompress until the filetype is not supported anymore')

    parser.add_argument('--keep-intermediate',
                        action='store_true',
                        help='Keep intermediate files when using the --all switch. This switch is ignored otherwise.')
    return parser


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]

    parser = get_parser()

    args = parser.parse_args(argv)

    try:
        path = xtract(args.source,
                      destination=args.destination,
                      overwrite=args.overwrite,
                      all=args.all,
                      keep_intermediate=args.keep_intermediate)
    except FileTypeNotSupported:
        print('Filetype is not supported:', args.source)
        sys.exit(2)

    print(path)


if __name__ == '__main__':
    main()
