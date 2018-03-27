from flask import Flask, request
from flask_restful import Resource, Api
import json

application = Flask(__name__)
api = Api(application)

class SplunkNetworkMisuse(Resource):
    def post(self):
        return {'result': 'OK'}, 200

api.add_resource(SplunkNetworkMisuse, '/api/splunk/network-misuse')

#if __name__ == '__main__':
#    application.run(host='0.0.0.0')