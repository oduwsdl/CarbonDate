from checkForModules import checkForModules
import json
import time
import os,sys, traceback
import datetime

import tornado.web
import tornado.ioloop

import core
import argparse


class CarbonDateServer(tornado.web.RequestHandler):

    def get(self):
        try:
            url=self.get_argument('url')
        except Exception, e:
            self.set_status(400)
            return

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
        r=modLoader.run(args=args,resultArray=result)
        self.write(r)

        
    



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
   

    app=tornado.web.Application([
        (r"/search",CarbonDateServer)])
    app.listen(ServerPort)
    #str(ServerIP),
    tornado.ioloop.IOLoop.current().start()
  
  
  
  
  





