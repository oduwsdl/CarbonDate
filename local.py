from checkForModules import checkForModules
import json
import time
import os,sys, traceback
import datetime

from cdHtmlMessages import *

import core
import argparse

def cd(modLoader,args):
    result=[]
    #read system config
    fileConfig = open("config", "r")
    config = fileConfig.read()
    fileConfig.close()
    cfg = json.loads(config)
   
    
    modLoader.loadModule(cfg,args)

    if args.lm:
        print 'Available Modules (include system utilities)'
        print '===================================='
        for m in modLoader.getAvailableModules():
            print m
        print '===================================='
        print
    else:
        modLoader.run(args=args,resultArray=result)
        os._exit(0)


    

##### script entry ######
if __name__ == '__main__':

    #init argparse
    parser=argparse.ArgumentParser(description='Local version of Carbon Date Tool')
    modOpGroup=parser.add_mutually_exclusive_group()
    modOpGroup.add_argument('-a', '--all', action="store_true", help='Load all modules (default)',dest='all')
    modOpGroup.add_argument('-m',  help='Specify mode, only load given modules ', nargs='+')
    modOpGroup.add_argument('-e', help="Exclusive mode, load all modules except the given modules", nargs='+')

    sysModeGrp=parser.add_mutually_exclusive_group(required=True)
    sysModeGrp.add_argument('-lm',action="store_true" , help="List all the module available in the system")
    sysModeGrp.add_argument('-url', help='The url to look up')

    parser.add_argument('-t','--timeout' , type=int, help='Set timeout for all modules',default=300)
    parser.add_argument('-v','--verbose' , action='store_true', help='Enable verbose output')

    

    args=parser.parse_args()

    mod=core.ModuleManager()
    time.strptime("1995-01-01T12:00:00", '%Y-%m-%dT%H:%M:%S')
    cd(mod,args)
  
  
  





