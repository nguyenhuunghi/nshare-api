import sys, os, json
from flask import Flask, jsonify, request
from flask_restful import Api, Resource, reqparse
from flask_cors import CORS, cross_origin
from api.user import User
from api.assets import Assets
from api.login import Login
from api.task import Task, Field
from api import blog, comment
from utils import auth

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'
# @app.errorhandler(auth.AuthError)
# def handle_auth_error(ex):
#     response = jsonify(ex.error)
#     response.status_code = ex.status_code
#     return response
# @auth.requires_auth
api = Api(app)
# Controller API
api.add_resource(User, '/user')
api.add_resource(Assets, '/assets')
api.add_resource(Login, '/login')
api.add_resource(Task, '/task')
api.add_resource(Field, '/field')
api.add_resource(blog.Item, '/blog/<string:id>', endpoint='blog_item')
api.add_resource(blog.Collection, '/blogs', endpoint='blog_collection')
api.add_resource(comment.Item, '/comment/<string:id>', endpoint='comment_item')
api.add_resource(comment.Collection, '/comments/<string:id>', endpoint='comment_collection')


if __name__ == '__main__':
    app.config["DEBUG"] = True 
    port = int(os.environ.get("PORT", 5000))
    app.run(host="127.0.0.1", port=port)