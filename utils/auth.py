import sys, os, json, requests
from functools import wraps
from flask import request

# Format error message and append status code
class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


def get_token_auth_header():
    """ Obtains to acess token from the Authorization header
    """
    auth = request.headers.get('Authorization', None)
    if not auth:
        raise AuthError({
            'code': 'authorization_header_missing',
            'description': 'Authorization header is expected'
        }, 401)
    parts = auth.split()
    if parts[0].lower() != 'bearer':
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header must start with Bearer'
        }, 401)     
    elif len(parts) == 1:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Token not found'
        }, 401)
    elif len(parts) > 2:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header must be Bearer token'
        }, 401)
    token = parts[1]
    
    return token

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = get_token_auth_header()
        if not token:
            raise AuthError({
                'code': 'authorization_header_missing',
                'description': 'Authorization header is expected'
            }, 401)
        return f(*args, **kwargs)
    return decorated

# @app.route('/api/public')
# @cross_origin(headers=['Content-Type', 'Authorization'])
# def public():
#     response = "Hello from a public endpoint! You need to be authenticated to see this."
#     return jsonify(message=response)

# @app.route('/api/private')
# @cross_origin(headers=['Content-Type', 'Authorization'])
# def private():
#     response = "Hello from a private endpoint! You need to be authenticated to see this."
#     return jsonify(message=response)

