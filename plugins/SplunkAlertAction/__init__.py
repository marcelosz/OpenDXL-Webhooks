#!/usr/bin/env python
# -*- coding: UTF-8 -*-

__author__ = "Marcelo Souza"
__license__ = "GPL"

import cherrypy

@cherrypy.expose
class SplunkAlertAction(object):

    @cherrypy.tools.accept(media='application/json')

    def POST(self):
        print("Request Headers: ", cherrypy.request.headers)
        print("Request Body: ", cherrypy.request.body.read())
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
  cherrypy.tree.mount(SplunkAlertAction(), '/webhooks/splunk/network-misuse', conf)