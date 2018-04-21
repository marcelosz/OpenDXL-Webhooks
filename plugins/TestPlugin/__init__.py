#!/usr/bin/env python
# -*- coding: UTF-8 -*-

__author__ = "Marcelo Souza"
__license__ = "GPL"

import sys, cherrypy
#add parent path to import modules
sys.path.append("..")
import conf_util
import dxl_globals

import logging
logger = logging.getLogger()

@cherrypy.expose
class TestPlugin(object):

    @cherrypy.tools.accept(media='text/plain')

    def POST(self):
        #print("Request Headers: ", cherrypy.request.headers)
        body = cherrypy.request.body.read()
        print("Request Body: ", body)
        #global dxl_client
        #dxl_client.publish("/opendxl/webhooks/event/test", body)
        dxl_globals.dxl_client.publish("/opendxl/webhooks/event/test", "Test ok!")        
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
    cherrypy.tree.mount(TestPlugin(), '/webhooks/test', conf)