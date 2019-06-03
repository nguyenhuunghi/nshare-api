import sys, os, json, requests
from flask_restful import Resource
from flask import request, Response, abort, jsonify
from utils.api import add_assets
from utils import pgsql, db, FALSE_WORDS

class Assets(Resource):
    __table__ = 'assets'
    __column__ = {
        'id': 'int',
        'link': 'string',
        'deletehash': 'string',
        'datetime': 'string'
    }
    # pgsql.init_db(__tablename__, columns)

class Item(Assets):
    def post(self):
        data = request.get_json()
        response = add_assets(data['image'].split(',')[1])
        if response['status'] != 200:
            return abort(400, 'Upload image failed!')
        link = response['data']['link']
        data['link'] = link
        if data['image']: del data['image']
        # if insert_table_pg(self.key, data) in FALSE_WORDS:
        #     return abort(401, 'Upload image failed!')
        return jsonify(data)
        
        