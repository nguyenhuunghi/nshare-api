import sys, os, json
# import framoworks
from flask import Flask, request
from flask_restful import Api
from flask_cors import CORS, cross_origin
# import config
from config import app_config
# import api and utils
from api.user import User
from api.login import Login
from api.task import Task, Field
from api import blog, comment, assets

class Createapp:
    def create_app(env_name):
        # app initliazation
        app = Flask(__name__)
        CORS(app, resources={r"/*": {"origins": "*"}})
        app.config.from_object(app_config[os.getenv('FLASK_ENV')])
        print('create_app')
        @app.route('/', methods=['GET'])
        def index():
            return 'Congratulations'
        return app

env_name = os.getenv('FLASK_ENV')
app = Createapp.create_app(env_name)
api = Api(app)
# resource API
api.add_resource(User, '/user')
api.add_resource(Login, '/login')
api.add_resource(Task, '/task')
api.add_resource(Field, '/field')
api.add_resource(assets.Item, '/assets')
api.add_resource(blog.Item, '/blog/<string:id>', endpoint='blog_item')
api.add_resource(blog.Collection, '/blogs', endpoint='blog_collection')
api.add_resource(comment.Item, '/comment/<string:id>', endpoint='comment_item')
api.add_resource(comment.Collection, '/comments/<string:blog_id>', endpoint='comment_collection')
api.add_resource(comment.ReplyComment, '/comment/<string:id>/reply_comment', endpoint='reply_comment')


if __name__ == '__main__':
    # run app
    app.run()
