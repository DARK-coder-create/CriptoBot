from flask import Flask
from flask_restful import Api

from class_request import Request

from config import *

app = Flask(__name__)
api = Api(app)

api.add_resource(Request, '/request')

if __name__ == '__main__':
    app.run(host=ip, port=port, debug=False)