#!/usr/bin/env python
# -*- coding: UTF-8 -*-

__author__ = "Marcelo Souza"
__license__ = "GPL"

# DXL imports
from dxlclient.client import DxlClient
from dxlclient.client_config import DxlClientConfig
from dxlclient.message import Event
import logging

logger = logging.getLogger()

#
# DXL config initialization
#
def config_init(cfg_file):
    # TODO - enhance error handling here
    # DxlClientConfig from DXL configuration file
    logger.info("Loading DXL config from: %s", cfg_file)
    return DxlClientConfig.create_dxl_config_from_file(cfg_file)

#
# DXL broker connection
#
def connect(dxl_config):
    try:
        dxl_client = DxlClient(dxl_config)
        logger.debug("Connecting to DXL broker...")
        dxl_client.connect()
        return dxl_client
    except Exception as e:
        logger.error("Could not initialize OpenDXL client ({0}).".format(e.message))
        return None

#
# Send message via DXL
#
def publish(dxl_client, topic, payload_str):
    # TODO - handle possible errors
    logger.debug("Publishing message on topic %s.", topic)
    dxl_event = Event(topic)
    logger.debug("Msg payload: %s", payload_str)
    dxl_event.payload = str(payload_str).encode()
    dxl_client.send_event(dxl_event)
    logger.debug("Msg published to DXL fabric.")
