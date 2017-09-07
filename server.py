#!/usr/bin/env python3
import json
import time
import os
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
            url = self.get_argument('url')
        except Exception:
            self.set_status(400)
            return

        logger = logging.getLogger('server')

        realIP = self.request.remote_ip
        print(self.request.headers)
        if self.request.headers.get("X-Real-IP"):
            realIP = self.request.headers.get("X-Real-IP")
        if self.request.headers.get("X-Forwarded-For"):
            realIP = self.request.headers.get("X-Forwarded-For")

        logger.log(45, 'Get request from %s' % (realIP))
        logger.log(45, 'URI Requested: %s' % (url))
        fileConfig = open("config", "r")
        config = fileConfig.read()
        fileConfig.close()
        cfg = json.loads(config)

        parser = argparse.ArgumentParser(
            description='server version of Carbon Date Tool')
        parser.add_argument('-a', '--all', action="store_true")
        parser.add_argument('-e', metavar='MODULE')
        parser.add_argument('url', help='The url to look up')
        parser.add_argument('-t', '--timeout', type=int,
                            help='Set timeout for all modules', default=300)
        parser.add_argument('-v', '--verbose',
                            action='store_true', help='Enable verbose output')

        args = parser.parse_args(['-a', url])

        result = {}
        modLoader = core.ModuleManager()
        modLoader.loadModule(cfg, args)
        self.run_background(modLoader.run, self.on_complete,
                            args=args, resultDict=result, logger=logger)

    def on_complete(self, res):
        resultDict = {}
        resultDict["self"] = (self.request.protocol +
                              "://" + self.request.host + self.request.uri)
        resultDict.update(res)

        r = OrderedDict(resultDict)
        self.write(json.dumps(r, sort_keys=False,
                              indent=2, separators=(',', ': ')))
        self.set_header("Content-Type", "application/json")
        self.set_header("Access-Control-Allow-Origin", "*")

        logger.log(45, 'Request from %s is done.' % (self.request.remote_ip))
        self.finish()

    def run_background(self, func, callback, *args, **kwargs):
        self.ioloop = tornado.ioloop.IOLoop.instance()

        def _callback(result):
            self.ioloop.add_callback(lambda: callback(result))
        _workers.apply_async(func, args, kwargs, _callback)


if __name__ == '__main__':
    '''
    If time.strptime is used before starting the threads, then no exception
    is raised (the issue may thus come from strptime.py not being imported in
    a thread safe manner). -- http://bugs.python.org/issue7980
    '''
    time.strptime("1995-01-01T12:00:00", '%Y-%m-%dT%H:%M:%S')

    fileConfig = open("config", "r")
    config = fileConfig.read()
    fileConfig.close()
    jsonFile = json.loads(config)
    ServerIP = jsonFile["ServerIP"]
    ServerPort = jsonFile["ServerPort"]

    ip_env = os.getenv('CD_Server_IP')
    port_env = os.getenv('CD_Server_port')
    if ip_env is not None:
        logging.warning(
            'Server.py: Server IP detected in environment variable, overwite \
             local config values.')
        ServerIP = int(ip_env)
    if port_env is not None:
        logging.warning(
            'Server.py: Server Port number detected in environment variable, \
            overwite local config values.')
        ServerPort = int(port_env)

    # initialize logger
    logging.basicConfig(level=int(os.environ.get("LOGLV", logging.ERROR)),
                        format='%(asctime)s [%(levelname)s]%(funcName)s : '
                        '%(message)s',
                        handlers=[logging.FileHandler("logs/carbonServer.log"),
                                  logging.StreamHandler()])
    logger = logging.getLogger('server')
    logging.addLevelName(45, "Server")
    # initialize server
    app = tornado.web.Application([
        (r"/cd", CarbonDateServer),
        (r'/(.*)', tornado.web.StaticFileHandler,
         {'path': 'docs', "default_filename": "index.html"})
    ])
    app.listen(int(os.environ.get("PORT", ServerPort)))
    logger.log(45, 'Server started.')
    try:
        tornado.ioloop.IOLoop.current().start()
    except KeyboardInterrupt:
        print("Closing Server!")
