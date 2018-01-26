#!/usr/bin/env python3

import json
import logging


def start(args, mod):
    '''
    Start local version of Carbon Tool
    '''
    result = {}
    loglevel = logging.WARNING
    if args.verbose:
        loglevel = logging.DEBUG
    logging.basicConfig(level=loglevel, format='%(message)s')
    logger = logging.getLogger('local')
    result['self'] = ""
    results = mod.run(args=args, resultDict=result,
                      logger=logger)
    print(json.dumps(results, indent=4))
