#!/usr/bin/env python
# -*- coding: UTF-8 -*-

__author__ = "Marcelo Souza"
__license__ = "GPL"

import sys, cherrypy, json
from conf_util import plugin_cfg
from opendxl_util.settings import opendxl_client

import logging
logger = logging.getLogger()

alerts = []
message = ""

#
# Common webapp parameters
#
webapp_conf = {
    '/' : {
        'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
        'request.method_with_bodies': True,
        'request.show_tracebacks': False
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
        if send_dxl_msg('NetworkMisuse', body):
            return "Ok"
        else:
            raise cherrypy.HTTPError(400, message)

@cherrypy.expose
class NetworkAttackHandler(object):
    @cherrypy.tools.accept(media='application/json')
    def POST(self):
        body = cherrypy.request.body.read()
        if send_dxl_msg('NetworkAttack', body):
            return "Ok"
        else:
            raise cherrypy.HTTPError(400, message)

def send_dxl_msg(alert_name, body):
    # TODO - add more error checks
    payload = ""
    json_body = ""
    #
    # parse the request body, if it is a JSON
    #
    try:
        json_body = json.loads(body)
        logger.debug("JSON Request Body: %s", json.dumps(json_body, indent=2,sort_keys=False))
    except Exception as e:
        message = "Error processing request. Could not parse JSON request body (%s)." % (e.message)
        logger.error(message)
        return False
    #
    # filter by 'search_name'
    #
    # - get only one item from the list 'alerts' with the name 'name'
    cur_alert = filter(lambda list : list['name'] == alert_name, alerts)
    search_name = cur_alert[0]['search_name']
    # - do the filter
    if not json_body['search_name'] == search_name:
        message = "Ignoring request ('search_name' does not match %s)." % search_name
        logger.info(message)
        return False
    # TODO - add option to publish only parts of the request body
    payload = json_body
    opendxl_client.publish(cur_alert[0]['topic'], payload)
    message = "Alert successfuly published to DXL bus!"
    logger.info(message)    
    return True    

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
                       'search_name': plugin_cfg['SplunkAlertAction'][name]['SearchName'], 
                       'topic': plugin_cfg['SplunkAlertAction'][name]['DXLMsgTopic'] })
        handler_obj = handlers[name]()
        cherrypy.tree.mount(handler_obj, route, webapp_conf)     
