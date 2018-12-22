import sys, os, json, requests
from functools import wraps
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

# Format error message and append status code
class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


@app.errorhandler(AuthError)
def handle_auth_error(ex):
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response

def get_token_auth_header():
    """ Obtains to acess token from the Authorization header
    """
    auth = request.header.get('Authorization', None)
    if not auth:
        raise AuthError({
            'code': 'authorization_header_missing',
            'description': 'Authorization header is expected'
        }, 401)

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        # token = get_token_auth_header()
        token = 'asda21311asda1131'
        if not token:
            print 'AuthError'
            # raise AuthError({
            #     'code': 'authorization_header_missing',
            #     'description': 'Authorization header is expected'
            # }, 401)
    return decorated

@app.route('/api/public')
@cross_origin(headers=['Content-Type', 'Authorization'])
def public():
    response = "Hello from a public endpoint! You need to be authenticated to see this."
    return jsonify(message=response)

@app.route('/api/private')
@cross_origin(headers=['Content-Type', 'Authorization'])
@requires_auth
def private():
    response = "Hello from a private endpoint! You need to be authenticated to see this."
    return jsonify(message=response)

# Controller API
api.add_resource(User, '/user')
api.add_resource(Assets, '/assets')
api.add_resource(Login, '/login')


if __name__ == '__main__':
    app.config["DEBUG"] = True 
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)