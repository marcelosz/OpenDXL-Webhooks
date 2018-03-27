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

def create_arg_parser():
    """
    Parses command line arguments.
    
    Returns:
        An ArgumentParser object.
    """

    epilog = """\
       This script works as ***.
       """
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter,
                                     epilog=textwrap.dedent(epilog))
    #parser.add_argument("filter_query", help="Query used to filter desired observables (confidence, type, time window, ...).", metavar="FILTER_QUERY")
    parser.add_argument("-c", "--configfile", help="Configuration file.", default="/etc/***/server.conf")
    parser.add_argument("-d", "--dryrun", help="***.", action='store_true', default=False)
    parser.add_argument("-l", "--loglevel", help="Logging level (DEBUG, INFO or ERROR).", default="INFO")
    parser.add_argument("-p", "--pprint", help="Pretty print exported observables to STDOUT.", action='store_true', default=False)
    parser.add_argument("-s", "--singleshot", help="Single shot mode (***).", action='store_true', default=False)
    parser.add_argument("-t", "--time", help="Polling time (in seconds).", default=60)    

    return parser

def set_logging_level(lg, level):
    """
    Set the level of verbosity of a logger instance.
    """
    # Configure logging level
    if level == 'DEBUG':
        lg.setLevel(logging.DEBUG)
    elif level == 'INFO':
        lg.setLevel(logging.INFO)
    elif level == 'WARNING':
        lg.setLevel(logging.WARNING)   
    else:
        lg.setLevel(logging.ERROR)

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
