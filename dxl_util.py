#!/usr/bin/env python
# -*- coding: UTF-8 -*-

__author__ = "Marcelo Souza"
__license__ = "GPL"

import conf_util

# DXL imports
from dxlclient.client import DxlClient
from dxlclient.client_config import DxlClientConfig
from dxlclient.message import Event

#
# DXL initialization
#
def dxl_init(dxl_config):
    # TODO - enhance error handling here
    # DxlClientConfig from DXL configuration file
    logger.info("Loading DXL config from: %s", dxl_config)
    dxl_config = DxlClientConfig.create_dxl_config_from_file(conf_util.cfg['DXL']['Config'])

#
# Connect to DXL and publish the observables as events
#
def dxl_publish(topic, payload):
    try:
        with DxlClient(dxl_config) as dxl_client:
            # Connect to DXL Broker
            logger.debug("Connecting to DXL broker...")
            dxl_client.connect()
            # TODO - handle possible connection errors
            logger.debug("Publishing message on topic %s.", topic)
            dxl_event = Event(topic)
            logger.debug("Msg payload: %s", payload)
            dxl_event.payload = str(payload_str).encode()
            dxl_client.send_event(dxl_event)
            logger.debug("Msg published to DXL fabric.")
    except Exception as e:
        logger.error("Could not initialize OpenDXL client ({0}).".format(e.message))
        return False
    return True