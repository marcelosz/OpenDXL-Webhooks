#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""webhooks_server.py - 
  ***
  ***."""

__author__ = "Marcelo Souza"
__license__ = "GPL"

import sys, logging, argparse, textwrap
import requests, json, re, urllib3, time
import sys, logging, argparse, textwrap
import requests, json, re, urllib3, time
from app import application

# Enable logging, this will also direct built-in DXL log messages.
# See - https://docs.python.org/2/howto/logging-cookbook.html
log_formatter = logging.Formatter('%(asctime)s webhooks_server (%(name)s) %(levelname)s: %(message)s')
console_handler = logging.StreamHandler()
console_handler.setFormatter(log_formatter)
logger = logging.getLogger()
logger.addHandler(console_handler)

def main(argv):
    # parse the args
    arg_parser = create_arg_parser()
    args = arg_parser.parse_args()

    # set logging level
    set_logging_level(logger, args.loglevel)

    # read cfg file
    try:
        config = ConfigObj(args.configfile, raise_errors=True, file_error=True)
    except:
        # TODO - enhance error handling here 
        logger.error("Could not parse config file!")
        exit(1)

    application.run()

if __name__ == "__main__":
    try:
        main(sys.argv[1:])
    except KeyboardInterrupt:
        # TODO - gracefully exit
        logger.info("Caught keyboard interrupt signal. Exiting...")
        exit(0)
