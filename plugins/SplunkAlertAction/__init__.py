#!/usr/bin/env python
# -*- coding: UTF-8 -*-

__author__ = "Marcelo Souza"
__license__ = "GPL"

import sys, cherrypy, json
import conf_util
#add parent path to import modules
sys.path.append("..")

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
        json_body = json.loads(body)
        print("JSON Request Body: ", json.dumps(json_body, indent=2,sort_keys=False))
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
    for name in conf_util.plugin_cfg['SplunkAlertAction']['Alerts']:
        route = conf_util.plugin_cfg['SplunkAlertAction'][name]['Route']   
        alerts.append({'name': name, 
                       'route': route, 
                       'filter': conf_util.plugin_cfg['SplunkAlertAction'][name]['SearchNameFilter'], 
                       'fields': conf_util.plugin_cfg['SplunkAlertAction'][name]['AlertFields'],
                        'topic': conf_util.plugin_cfg['SplunkAlertAction'][name]['DXLMsgTopic'] })
        handler_obj = handlers[name]()
        cherrypy.tree.mount(handler_obj, route, webapp_conf)