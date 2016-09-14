#!/usr/bin/env python3

from checkForModules import checkForModules
import json
import time
import os,sys, traceback
import datetime

import core
import argparse
import logging

def cd(modLoader,args):
    result=[]
    #read system config
    fileConfig = open("config", "r")
    config = fileConfig.read()
    fileConfig.close()
    cfg = json.loads(config)
    loglevel=logging.WARNING
   
    
    modLoader.loadModule(cfg,args)

    if args.mode=='dev' :
        if args.lm:
            print('Available Modules (include system utilities)')
            print('====================================')
            for m in modLoader.getAvailableModules():
                print(m)
            print('====================================')
            print()
        else:
            if args.ak is not None:
                cfg[args.ak[0]]=args.ak[1]
                print("\"%s\" is now set to \"%s\"" %(args.ak[0], cfg[args.ak[0]]))
                json.dump(cfg, open('config','w'), sort_keys=True, indent=4, separators=(',', ': '))
            if args.rk is not None:
                try:
                    cfg.pop(args.rk)
                    json.dump(cfg, open('config','w'), sort_keys=True, indent=4, separators=(',', ': '))
                except Exception as e:
                    print('local.py: No such key: %s'%e)
            if args.lk:
                print(json.dumps(cfg, sort_keys=True, indent=4, separators=(',', ': ')))
    elif args.mode=='search':
        if args.verbose:
            loglevel=logging.DEBUG
        logging.basicConfig(level=loglevel,format='%(message)s')
        logger=logging.getLogger('local')
        modLoader.run(args=args,resultArray=result,logger=logger)
        os._exit(0)


    

##### script entry ######
if __name__ == '__main__':

    #init argparse
    parser=argparse.ArgumentParser(description='Local version of Carbon Date Tool')
    sub_parsers=parser.add_subparsers(dest = 'mode',help='Working mode')
    #main search service
    search_parser=sub_parsers.add_parser('search',  help = 'Search (normal) mode of carbon tool')
    modOpGroup=search_parser.add_mutually_exclusive_group()
    modOpGroup.add_argument('-a', '--all', action="store_true", help='Load all modules (default)',dest='all')
    modOpGroup.add_argument('-m',  metavar='MODULE', help='Specify mode, only load given modules ', nargs='+')
    modOpGroup.add_argument('-e', metavar='MODULE', help="Exclusive mode, load all modules except the given modules", nargs='+')

    search_parser.add_argument('url', help='The url to look up')

    search_parser.add_argument('-t','--timeout' , type=int, help='Set timeout for all modules',default=300)
    search_parser.add_argument('-v','--verbose' , action='store_true', help='Enable verbose output')

    #sub command parser for dev mod
    
    dev_parser=sub_parsers.add_parser('dev', help = 'Dev mode of carbon tool, for system configuration')
    dev_parser.add_argument('-lm',action="store_true" , help="List all the module available in the system")
    dev_parser.add_argument('-ak', metavar=('KEY','VALUE'), nargs=2,help = 'Add/update api key, system configuration, etc')
    dev_parser.add_argument('-rk', metavar='KEY', help = 'Remove configuration key pair')    
    dev_parser.add_argument('-lk', action='store_true', help='List all the configuration key-value pair (Environment value will overwrite certain value during runtime)')


    args=parser.parse_args()

    mod=core.ModuleManager()
    time.strptime("1995-01-01T12:00:00", '%Y-%m-%dT%H:%M:%S')
    cd(mod,args)
  
  
  
