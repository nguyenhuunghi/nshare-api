import sys, os, json, requests
from flask_restful import Resource
from flask import request, Response, abort, jsonify
from utils.api import add_assets
from utils import FALSE_WORDS
from utils.pgsql import create_table_sql, insert_table_sql, add_column_table_sql

class Assets(Resource):
    key = 'assets'
    assets = {
        'id': 'int',
        'link': 'string',
        'deletehash': 'string',
        'datetime': 'string'
    }
    try: create_table_sql(key, assets)
    except: pass
    try: add_column_table_sql(key, assets)
    except: pass
    try: modify_data_type_table_sql('{}'.format(key + '_1'), comment)
    except: pass

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
        
        