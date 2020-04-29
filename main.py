#!/usr/bin/env python3

import argparse
#import server
import local
import core
import json
import time

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
        epilog='For more help, type main.py -h')
    
    mode_group = parser.add_mutually_exclusive_group(required=True)
    mode_group.add_argument('--list-mods', action='store_true',
                            help='List all avaiable modules')
    mode_group.add_argument('-s', '--server', action='store_true',
                            help='Launch server version of Carbon Date Tool')
    mode_group.add_argument('-l', '--local', metavar='{URI}',
                            help='Run Carbon Date Tool as a local application.'
                            ' Takes a URI as a parameter',
                            dest="local_uri")
   
    parser.add_argument('-t', '--timeout', type=int,
                        help='Set timeout for all modules in seconds',
                        default=300)
    parser.add_argument(
        '-v', '--verbose', action='store_true', help='Enable verbose output')
    
    modOpGroup = parser.add_mutually_exclusive_group()
    modOpGroup.add_argument('-a', '--all', action="store_true",
                            help='Load all modules (default)', dest='all')
    modOpGroup.add_argument(
        '-m', metavar='MODULE', help='Specify mode, only load given modules ',
        nargs='+')
    modOpGroup.add_argument(
        '-e', metavar='MODULE', help="Exclusive mode, load all modules except \
        the given modules", nargs='+')
    return parser


if __name__ == '__main__':
    '''
    If time.strptime is used before starting the threads, then no exception
    is raised (the issue may thus come from strptime.py not being imported in
    a thread safe manner). -- http://bugs.python.org/issue7980
    '''
    time.strptime("1995-01-01T12:00:00", '%Y-%m-%dT%H:%M:%S')
    parser = parserinit()
    args, unknown = parser.parse_known_args()

    # read system config
    fileConfig = open("config", "r")
    config = fileConfig.read()
    fileConfig.close()
    cfg = json.loads(config)
    # setup modules to load
    mod = core.ModuleManager()
    mod.loadModule(cfg, args)

    if args.list_mods:
        print('Available Modules (include system utilities)')
        print('====================================')
        for m in mod.modules:
            print(m)
        print('====================================')
    #elif args.server:
    #    server.start(args, cfg, mod)
    elif args.local_uri:
        local.start(args, mod)
