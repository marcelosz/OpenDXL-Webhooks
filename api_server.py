from flask import Flask, request
from flask_restful import Resource, Api
import json

app = Flask(__name__)
api = Api(app)

class SplunkNetworkMisuse(Resource):
    def post(self):
        return {'result': 'OK'}, 200

api.add_resource(SplunkNetworkMisuse, '/splunk/alert/network/misuse')

if __name__ == '__main__':
    app.run(host='0.0.0.0')
