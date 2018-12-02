import sys, os, json, requests
from flask import Flask, jsonify, redirect, url_for, render_template, request, abort, Response
from flask_restful import Api, Resource, reqparse
from werkzeug.wrappers import BaseRequest
from werkzeug.exceptions import HTTPException, NotFound
from werkzeug.http import HTTP_STATUS_CODES
from flask_cors import CORS, cross_origin
from api.user import User
from api.assets import Assets
from api.login import Login

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'
api = Api(app)

api.add_resource(User, '/user')
api.add_resource(Assets, '/assets')
api.add_resource(Login, '/login')

if __name__ == '__main__':
    app.config["DEBUG"] = True 
    port = int(os.environ.get("PORT", 5000))
    app.run(host="127.0.0.1", port=port)