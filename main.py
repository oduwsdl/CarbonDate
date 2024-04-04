#!/usr/bin/env python3

import argparse
import server
import local
import core
import gui
import json
import time
import tkinter as tk

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
    mode_group.add_argument('--gui', help='Activate the tkinter implementation.',
                            action='store_true')
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
            
#FORMATTING FUNCTION FOR THE TKINTER ENTRY BOX 
def on_entry_click(event):
    """function that gets called whenever entry is clicked"""
    if nameE.get() == 'https://www.cs.odu.edu':
        nameE.delete(0, "end") # delete all the text in the entry
        nameE.insert(0, '') #Insert blank for user input
        nameE.config(fg = 'black')
def on_focusout(event):
    if nameE.get() == '':
        nameE.insert(0, 'https://www.cs.odu.edu')
        nameE.config(fg = 'grey')

def passArgs(args, mod, name):
    args.local_uri = name 

    local.start(args, mod)


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
    elif args.server:
        server.start(args, cfg, mod)
    elif args.local_uri:
        local.start(args, mod)
    elif args.gui: 
        root = tk.Tk()
        root.title('CarbonDate')
        nameL = tk.Label (root, text="URL")
        nameL.grid(column = 0, row = 0, sticky = "W")

        nameE = tk.Entry(root, bd = 5, width = 25)
        nameE.insert(0, 'https://www.cs.odu.edu/')
        nameE.config(fg = 'grey')
        nameE.bind('<FocusIn>', on_entry_click)
        nameE.bind('<FocusOut>', on_focusout)
        nameE.grid(column = 1, row = 0, sticky = "W")
        s = tk.Button(root, text="Start", command = lambda : passArgs(args, mod, str(nameE.get())))
        s.grid(column = 2, row = 0, pady = 5)
        root.mainloop()

        
    #    gui = gui.Gui()
    #    gui.mainloop()
