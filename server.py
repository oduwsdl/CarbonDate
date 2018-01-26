#!/usr/bin/env python3
import json
import os
from collections import OrderedDict

import tornado.web
import tornado.ioloop
import logging
from multiprocessing.pool import ThreadPool

_workers = ThreadPool(50)
# initialize logger
logging.basicConfig(level=int(os.environ.get("LOGLV", logging.ERROR)),
                    format='%(asctime)s [%(levelname)s]%(funcName)s : '
                    '%(message)s',
                    handlers=[logging.FileHandler("logs/carbonServer.log"),
                              logging.StreamHandler()])
logger = logging.getLogger('server')
logging.addLevelName(45, "Server")


class CarbonDateServer(tornado.web.RequestHandler):
    def initialize(self, args, modLoader):
        self.args = args
        self.modLoader = modLoader

    @tornado.web.asynchronous
    def get(self, req):
        try:
            url = self.request.uri[4:]
        except Exception:
            self.set_status(400)
            return

        logger = logging.getLogger('server')

        realIP = self.request.remote_ip
        if self.request.headers.get("X-Real-IP"):
            realIP = self.request.headers.get("X-Real-IP")
        if self.request.headers.get("X-Forwarded-For"):
            realIP = self.request.headers.get("X-Forwarded-For")

        logger.log(45, 'Get request from %s' % (realIP))
        logger.log(45, 'URI Requested: %s' % (url))

        result = {}
        self.run_background(self.modLoader.run, self.on_complete,
                            args=self.args, resultDict=result, logger=logger,
                            url=url)

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


def start(args, config, mod):
    '''
    Start server version of Carbon Tool
    '''
    ServerPort = config["ServerPort"]
    port_env = os.getenv('CD_Server_port')
    if port_env is not None:
        logging.warning(
            'Server.py: Server Port number detected in environment variable, \
            overwite local config values.')
        ServerPort = int(port_env)

    # initialize server
    app = tornado.web.Application([
        (r"/cd/(.*)", CarbonDateServer, dict(args=args, modLoader=mod)),
        (r'/(.*)', tornado.web.StaticFileHandler,
         {'path': 'docs', "default_filename": "index.html"})
    ])
    app.listen(int(os.environ.get("PORT", ServerPort)))
    logger.log(45, 'Server started.')
    try:
        tornado.ioloop.IOLoop.current().start()
    except KeyboardInterrupt:
        print("Closing Server!")
