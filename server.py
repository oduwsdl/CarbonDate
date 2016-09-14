#!/usr/bin/env python3
import json
import time
import os,sys, traceback
import datetime
from collections import OrderedDict

import tornado.web
import tornado.ioloop
import core
import argparse
import logging
from multiprocessing.pool import ThreadPool

_workers = ThreadPool(50)

class CarbonDateServer(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(self):
        try:
            url=self.get_argument('url')
        except Exception as e:
            self.set_status(400)
            return

        logger=logging.getLogger('server')
        logger.log(45,'Get request from %s'%(self.request.remote_ip))
        fileConfig = open("config", "r")
        config = fileConfig.read()
        fileConfig.close()
        cfg = json.loads(config)

        parser=argparse.ArgumentParser(description='server version of Carbon Date Tool')
        parser.add_argument('-a', '--all', action="store_true")
        parser.add_argument('-e', metavar='MODULE')
        parser.add_argument('url', help='The url to look up')
        parser.add_argument('-t','--timeout' , type=int, help='Set timeout for all modules',default=300)
        parser.add_argument('-v','--verbose' , action='store_true', help='Enable verbose output')

        args=parser.parse_args(['-a',url])

        result=[]
        modLoader=core.ModuleManager()
        modLoader.loadModule(cfg,args)
        self.run_background(modLoader.run,self.on_complete,args=args,resultArray=result,logger=logger)
        

    def on_complete(self, res):
        #resultArray=modLoader.run(args=args,resultArray=result,logger=logger)
        resultArray=res
        resultArray.insert(0,('self',self.request.protocol + "://" + self.request.host + self.request.uri))
        r= OrderedDict(resultArray)
        self.write(json.dumps(r, sort_keys=False, indent=2, separators=(',', ': ')))
        self.set_header("Content-Type", "application/json")
        self.set_header("Access-Control-Allow-Origin", "*")

        logger.log(45,'Request from %s is done.'%(self.request.remote_ip))
        self.finish()

    def run_background(self, func, callback, *args, **kwargs):
        self.ioloop = tornado.ioloop.IOLoop.instance()

        def _callback(result):
            self.ioloop.add_callback(lambda: callback(result))
        _workers.apply_async(func, args, kwargs, _callback)
    



if __name__ == '__main__':
    #fix for none-thread safe strptime
    #If time.strptime is used before starting the threads, then no exception is raised (the issue may thus come from strptime.py not being imported in a thread safe manner). -- http://bugs.python.org/issue7980
    time.strptime("1995-01-01T12:00:00", '%Y-%m-%dT%H:%M:%S')

    fileConfig = open("config", "r")
    config = fileConfig.read()
    fileConfig.close()
    jsonFile = json.loads(config)
    ServerIP = jsonFile["ServerIP"]
    ServerPort = jsonFile["ServerPort"]
    
    ip_env=os.getenv('CD_Server_IP')
    port_env=os.getenv('CD_Server_port')
    if ip_env is not None:
            print('Server.py: Server IP detected in environment variable, overwite local config values.')
            ServerIP=int(ip_env)
    if port_env is not None:
            print('Server.py: Server Port number detected in environment variable, overwite local config values.')
            ServerPort=int(port_env)

    #initialize logger
    logging.basicConfig(level=int(os.environ.get("LOGLV",logging.ERROR)),format='<%(name)s><<%(asctime)s>>[%(levelname)s]%(funcName)s : %(message)s')
    logger=logging.getLogger('server')
    logging.addLevelName(45, "Server")
    #initialize server
    app=tornado.web.Application([
            (r"/cd",CarbonDateServer),
            (r'/(.*)', tornado.web.StaticFileHandler, {'path': 'docs', "default_filename": "index.html"})
        ])
    app.listen(int(os.environ.get("PORT",ServerPort)))
    print('Server started.')
    tornado.ioloop.IOLoop.current().start()
  
  
  
  
  
