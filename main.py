#!/usr/bin/env python3

import argparse
import os
import sys
import shlex

logo = ('''
 _____       ___   _____    _____   _____   __   _   _____       ___   _____   _____
/  ___|     /   | |  _  \  |  _  \ /  _  \ |  \ | | |  _  \     /   | |_   _| | ____|
| |        / /| | | |_| |  | |_| | | | | | |   \| | | | | |    / /| |   | |   | |__
| |       / / | | |  _  /  |  _  { | | | | | |\   | | | | |   / / | |   | |   |  __|
| |___   / /  | | | | \ \  | |_| | | |_| | | | \  | | |_| |  / /  | |   | |   | |___
\_____| /_/   |_| |_|  \_\ |_____/ \_____/ |_|  \_| |_____/ /_/   |_|   |_|   |_____|

''')


def parserinit():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=logo + 'Integrated interface for Carbon Date Tool',
        epilog="For more help about running locally, type main.py -lh")
    modeGroup = parser.add_mutually_exclusive_group(required=True)
    modeGroup.add_argument('-s', '--server', action="store_true",
                           help="Launch server of Carbon Date Tool")
    modeGroup.add_argument('-l', '--local', action="store_true",
                           help="Run Carbon Date Tool as a local application")
    modeGroup.add_argument('-lh', action='store_true',
                           help='Manual of running locally')
    return parser


if __name__ == '__main__':
    parser = parserinit()
    args, unknown = parser.parse_known_args()
    if args.server:
        os.system('./server.py')
    elif args.local:
        arg_str = ""
        for a in sys.argv[2:]:
            arg_str += (' ' + shlex.quote(a))
        os.system('./local.py%s' % (arg_str))
    elif args.lh:
        os.system('./local.py -h')
