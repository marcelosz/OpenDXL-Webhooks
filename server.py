#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""server.py - 
  ***
  ***."""

__author__ = "Marcelo Souza"
__license__ = "GPL"

import cherrypy

@cherrypy.expose
class SplunkNetworkMisuse(object):

    @cherrypy.tools.accept(media='text/plain')

    def POST(self, length=8):
        print("Request Headers: ", cherrypy.request.headers)
        #body = cherrypy.request.body.read()
        print("Request Body: ", cherrypy.request.body.read())
        return "OK"

#if __name__ == "__main__":
#    try:
#        main(sys.argv[1:])
#    except KeyboardInterrupt:
#        # TODO - gracefully exit
#        logger.info("Caught keyboard interrupt signal. Exiting...")
#        exit(0)

if __name__ == '__main__':
    cherrypy.config.update({'server.socket_host': '0.0.0.0',
                            'server.socket_port': 8001,})
    conf = {
        '/': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'request.method_with_bodies': True,
            'tools.sessions.on': True,
            'tools.response_headers.on': True,
            'tools.response_headers.headers': [('Content-Type', 'text/plain')],
        }
    }
    cherrypy.quickstart(SplunkNetworkMisuse(), '/webhooks/splunk/network-misuse', conf)