#!/usr/bin/env python
# -*- coding: UTF-8 -*-

__author__ = "Marcelo Souza"
__license__ = "GPL"

import cherrypy
import conf_util

alerts = []

#
# Common webapp parameters
#
webapp_conf = {
    '/webhooks/splunk' : {
        'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
        'request.method_with_bodies': True,
    }
}

#
# Handler classes
#
@cherrypy.expose
class NetworkMisuseHandler(object):
    
    @cherrypy.tools.accept(media='application/json')

    def POST(self):
        #print(cherrypy.request.request_line)
        print("Request Headers: ", cherrypy.request.headers)
        print("Request Body: ", cherrypy.request.body.read())
        return "OK"

@cherrypy.expose
class NetworkAttack(object):

    @cherrypy.tools.accept(media='text/plain')

    def POST(self, length=8):
        print("Request Headers: ", cherrypy.request.headers)
        #body = cherrypy.request.body.read()
        print("Request Body: ", cherrypy.request.body.read())
    	#dxl_util.dxl_init()
        return "OK"

#
# Initialization
#
def init():
    # NetworkMisuse handler
    name = 'NetworkMisuse'
    route = conf_util.plugin_cfg['SplunkAlertAction'][name]['Route']    
    alerts.append({'name': name, 
                   'route': route, 
                   'filter': conf_util.plugin_cfg['SplunkAlertAction'][name]['SearchNameFilter'], 
                   'fields': conf_util.plugin_cfg['SplunkAlertAction'][name]['AlertFields'],
                   'topic': conf_util.plugin_cfg['SplunkAlertAction'][name]['DXLMsgTopic']
                  })    
    cherrypy.tree.mount(NetworkMisuseHandler(), route, webapp_conf)
    # NetworkAttack handler
    name = 'NetworkAttack'
    route = conf_util.plugin_cfg['SplunkAlertAction'][name]['Route']    
    alerts.append({'name': name, 
                   'route': route, 
                   'filter': conf_util.plugin_cfg['SplunkAlertAction'][name]['SearchNameFilter'], 
                   'fields': conf_util.plugin_cfg['SplunkAlertAction'][name]['AlertFields'],
                   'topic': conf_util.plugin_cfg['SplunkAlertAction'][name]['DXLMsgTopic']
                  })    
    cherrypy.tree.mount(NetworkAttack(), route, webapp_conf)
