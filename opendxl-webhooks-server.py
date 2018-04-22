#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""opendxl-webhooks-server.py - 
  OpenDXL Webhooks Server is a simple HTTP server that can handle Webhooks (HTTP requests) and 
  interact with McAfee OpenDXL bus based on those Webhooks.
"""

__author__ = "Marcelo Souza"
__license__ = "GPL"

import sys, logging, argparse, textwrap, os
import tokenize
import cherrypy
from configobj import ConfigObj, ConfigObjError
import conf_util
import opendxl_util.settings
import opendxl_util

# Enable logging, this will also direct built-in DXL and CherryPy log messages.
# See - https://docs.python.org/2/howto/logging-cookbook.html
log_formatter = logging.Formatter('%(asctime)s ows (%(name)s) %(levelname)s: %(message)s')
console_handler = logging.StreamHandler()
console_handler.setFormatter(log_formatter)
logger = logging.getLogger()
logger.addHandler(console_handler)
logging.getLogger("cherrypy").propagate = False

def create_arg_parser():
    """
    Parses command line arguments.
    
    Returns: 
        An ArgumentParser object.
    """

    epilog = """\
       This script works as a Webhooks server and an OpenDXL client at the same time. HTTP requests can be handled
       through a pluggable architecture where OpenDXL events or services interactions can take place.
       """
    #epilog = sys.modules[__name__].__doc__
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter,
                                     epilog=textwrap.dedent(epilog))
    #parser.add_argument("filter_query", help="Query used to filter desired observables (confidence, type, time window, ...).", metavar="FILTER_QUERY")
    parser.add_argument("-c", "--configfile", help="Configuration file.", default="/etc/opendxl-webhooks/server.conf")
    #parser.add_argument("-d", "--dryrun", help="***.", action='store_true', default=False)
    parser.add_argument("-l", "--loglevel", help="Logging level (DEBUG, INFO or ERROR). Dafault is INFO.", default="INFO")
    #parser.add_argument("-p", "--pprint", help="Pretty print exported observables to STDOUT.", action='store_true', default=False)

    return parser

# Plugin
if sys.version_info[0] < 3:
    import imp
else:
    import importlib

def init_plugins(path):
    """
    Get list of plugins, load and initialize them.
    """
    PluginsMainModule = "__init__"
    possiblePlugins = os.listdir(path)
    for i in possiblePlugins:
        module = None
        location = os.path.join(path, i)
        full_file_name = location + os.sep + "/__init__.py"
        logger.debug("Trying to load plugin %s...", i)
        if not os.path.isdir(location) or not PluginsMainModule + ".py" in os.listdir(location):
            # TODO - add error msg here
            continue
        if sys.version_info[0] < 3:
	        module = imp.load_source(i, full_file_name)
        else:
            spec = importlib.util.spec_from_file_location(i, full_file_name)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
        # TODO - enhance error handling here            
        # map and call plugin's init() function
        init = getattr(module, 'init')
        init()
    return True 

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

    logger.info("Starting OpenDXL-Webhooks server...")
    # read main cfg file
    conf_util.cfg = conf_util.read_cfg(args.configfile)
    if not conf_util.cfg:
        logger.error("Error reading main config file!")
        exit(1)
    # read plugins cfg file
    conf_util.plugin_cfg = conf_util.read_cfg(conf_util.cfg['Server']['PluginsConfig'])
    if not conf_util.cfg:
        logger.error("Error reading plugins config file!")
        exit(1)
    # set DXL config var
    conf_util.dxl_cfg = conf_util.cfg['DXL']['Config']

    #
    # init and connect DXL client
    # 
    logger.info("Initializing and connecting OpenDXL client...")
    if not opendxl_util.init(conf_util.dxl_cfg):
        exit(1)
    opendxl_util.send_status_msg("OpenDXL-Webhooks-Server client connected.")
    logger.info("OpenDXL client connected!")

    #
    # get plugins and execute their initializers
    #
    logger.info("Loading plugins...")
    init_plugins(conf_util.cfg['Server']['PluginsDir'])
    logger.info("Plugins loaded!")

    #
    # setup and run the CherryPy app
    #
    logger.info("Starting HTTP server...")
    enable_log_to_screen = False
    if conf_util.cfg['Server']['CherryPyLoggerEnable'] in ['true', 'True', 'yes', 'Yes']:
        enable_log_to_screen = True
    cherrypy.config.update({'server.socket_host': conf_util.cfg['Server']['BindAddress'],
                            'server.socket_port': int(conf_util.cfg['Server']['BindPort']),
                            'log.screen': enable_log_to_screen
                            })
                      
    cherrypy.engine.start()
    cherrypy.engine.block()

if __name__ == "__main__":
    main(sys.argv[1:])
