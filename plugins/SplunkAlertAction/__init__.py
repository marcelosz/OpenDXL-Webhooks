#!/usr/bin/env python
# -*- coding: UTF-8 -*-

__author__ = "Marcelo Souza"
__license__ = "GPL"

import sys, cherrypy
from conf_util import plugin_cfg
from opendxl_util.settings import opendxl_client

alerts = []

#
# Common webapp parameters
#
webapp_conf = {
    '/' : {
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
        body = cherrypy.request.body.read()
        try:
            json_body = json.loads(body)
            print("JSON Request Body: ", json.dumps(json_body, indent=2,sort_keys=False))
        except Exception as e: 
            print "Erro"
            dxl_client.publish("/opendxl/webhooks/event/status", "connected")
        return "OK"

@cherrypy.expose
class NetworkAttackHandler(object):
    @cherrypy.tools.accept(media='application/json')
    def POST(self):
        body = cherrypy.request.body.read()
        json_body = json.loads(body)
        print("JSON Request Body: ", json.dumps(json_body, indent=2,sort_keys=False))
        return "OK"

handlers = {'NetworkMisuse': NetworkMisuseHandler, 'NetworkAttack': NetworkAttackHandler}
#
# Initialization
#
def init():
    # NetworkMisuse handler
    for name in plugin_cfg['SplunkAlertAction']['Alerts']:
        route = plugin_cfg['SplunkAlertAction'][name]['Route']   
        alerts.append({'name': name, 
                       'route': route, 
                       'filter': plugin_cfg['SplunkAlertAction'][name]['SearchNameFilter'], 
                       'fields': plugin_cfg['SplunkAlertAction'][name]['AlertFields'],
                       'topic': plugin_cfg['SplunkAlertAction'][name]['DXLMsgTopic'] })
        handler_obj = handlers[name]()
        cherrypy.tree.mount(handler_obj, route, webapp_conf)
