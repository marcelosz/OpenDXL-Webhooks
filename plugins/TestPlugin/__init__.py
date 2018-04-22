#!/usr/bin/env python
# -*- coding: UTF-8 -*-

__author__ = "Marcelo Souza"
__license__ = "GPL"

import sys, cherrypy
from conf_util import plugin_cfg
from opendxl_util.settings import opendxl_client

import logging
logger = logging.getLogger()

@cherrypy.expose
class TestPlugin(object):
    @cherrypy.tools.accept(media='text/plain')
    def POST(self):
        #print("Request Headers: ", cherrypy.request.headers)
        body = cherrypy.request.body.read()
        logger.debug("Request body: %s", body)
        opendxl_client.publish(plugin_cfg['TestPlugin']['DXLMsgTopic'], body)
        return "OK"
        
def init():
    conf = {
        '/': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'request.method_with_bodies': True,
            'tools.sessions.on': True,
            'tools.response_headers.on': True,
            'tools.response_headers.headers': [('Content-Type', 'text/plain')],
        }
    }
    cherrypy.tree.mount(TestPlugin(), plugin_cfg['TestPlugin']['Route'], conf)