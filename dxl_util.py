#!/usr/bin/env python
# -*- coding: UTF-8 -*-

__author__ = "Marcelo Souza"
__license__ = "GPL"

# DXL imports
from dxlclient.client import DxlClient
from dxlclient.client_config import DxlClientConfig
from dxlclient.message import Event
import dxl_globals

import logging
logger = logging.getLogger()

class DXLClient:
    
    def __init__(self, cfg_file):
        self.dxl_config = None
        # TODO - enhance error handling here
        # DxlClientConfig from DXL configuration file
        logger.debug("Loading DXL config from: %s", cfg_file)
        try:
            self.dxl_config = DxlClientConfig.create_dxl_config_from_file(cfg_file)
        except Exception as e:
            logger.error("Could not read OpenDXL client config!")
	    return None

    def connect(self):
        try:
            self.dxl_client = DxlClient(self.dxl_config)
            logger.debug("Connecting to DXL broker...")
            self.dxl_client.connect()
            return True
        except Exception as e:
            logger.error("Could not connect OpenDXL client ({0}).".format(e.message))
            return False

    def publish(self, topic, payload_str):
        # TODO - handle possible errors
        logger.debug("Publishing message on topic %s.", topic)
        dxl_event = Event(topic)
        logger.debug("Msg payload: %s", payload_str)
        dxl_event.payload = str(payload_str).encode()
        self.dxl_client.send_event(dxl_event)
        logger.debug("Msg published to DXL fabric.")

#
# DXL init and connection - call this function first
#
def init(cfg_file):
    dxl_globals.dxl_client = DXLClient(cfg_file)
    if not dxl_globals.dxl_client.connect():
        return False
    return True
