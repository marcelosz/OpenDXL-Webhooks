#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""server.py - 
  ***
  ***."""

__author__ = "Marcelo Souza"
__license__ = "GPL"

import sys, logging, argparse, textwrap, os, importlib
import tokenize
import dxl_util
import cherrypy
#import requests, json, re, urllib3, time

# Enable logging, this will also direct built-in DXL and CherryPy log messages.
# See - https://docs.python.org/2/howto/logging-cookbook.html
log_formatter = logging.Formatter('%(asctime)s opendxl_webhooks_server (%(name)s) %(levelname)s: %(message)s')
console_handler = logging.StreamHandler()
console_handler.setFormatter(log_formatter)
logger = logging.getLogger()
logger.addHandler(console_handler)
logging.getLogger('cherrypy').propagate = False

# Config
from configobj import ConfigObj, ConfigObjError
config = None

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
    parser.add_argument("-c", "--configfile", help="Configuration file.", default="/etc/opendxl-webhooks/server.conf")
    #parser.add_argument("-d", "--dryrun", help="***.", action='store_true', default=False)
    parser.add_argument("-l", "--loglevel", help="Logging level (DEBUG, INFO or ERROR).", default="INFO")
    #parser.add_argument("-p", "--pprint", help="Pretty print exported observables to STDOUT.", action='store_true', default=False)

    return parser

# Plugin
PluginsMainModule = "__init__"
def get_plugins(path):
    """
    Get plugins.
    """
    # get plugins
    plugins = []
    possiblePlugins = os.listdir(path)
    for i in possiblePlugins:
        location = os.path.join(path, i)
        full_file_name = (location + "\__init__.py")
        if not os.path.isdir(location) or not PluginsMainModule + ".py" in os.listdir(location):
            # TODO - add error msg here
            continue
        spec = importlib.util.spec_from_file_location(i, full_file_name)
        plugins.append({"name": i, "full_file_name": full_file_name, "spec": spec})
    return plugins

def load_plugin(plugin):
    """
    Load plugin.
    """    
    spec = plugin["spec"]
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def main(argv):
    # parse the args
    arg_parser = create_arg_parser()
    args = arg_parser.parse_args()

    # set logging level
    level = args.loglevel
    if level == 'DEBUG':
        logger.setLevel(logging.DEBUG)
    elif level == 'INFO':
        logger.setLevel(logging.INFO)
    elif level == 'WARNING':
        logger.setLevel(logging.WARNING)   
    else:
        logger.setLevel(logging.ERROR)    

    # read cfg file
    try:
        config = ConfigObj(args.configfile, raise_errors=True, file_error=True)
    except:
        # TODO - enhance error handling here 
        logger.error("Could not parse config file!")
        exit(1)

    logger.info("Starting OpenDXL-Webhooks server...")        

    # get plugins and execute their initializers
    for i in get_plugins(config['Server']['PluginsDir']):
        logger.debug("Loading plugin %s...", i["name"])
        plugin = load_plugin(i)
        # map and call plugin's init() function
        init = getattr(plugin, 'init')
        init()

    # setup and run the CherryPy app
    cherrypy.config.update({'server.socket_host': config['Server']['BindAddress'],
                            'server.socket_port': int(config['Server']['BindPort']),
                            'log.screen': config['Server']['CherryPyLoggerEnable'] in ['true', 'True', 'yes', 'Yes'],
                            })
    cherrypy.engine.start()
    cherrypy.engine.block()

if __name__ == "__main__":
    main(sys.argv[1:])