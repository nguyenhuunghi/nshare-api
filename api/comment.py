import requests, json, sys, os, time, datetime
from werkzeug.exceptions import HTTPException
from flask import Flask, abort, request, jsonify, Response, make_response
from flask_restful import Resource
from flask_restful.utils import cors
from utils import TRUE_WORDS, FALSE_WORDS, NONE_WORDS
from config import conn, cur 
from utils.pgsql import create_table_sql, query_sql, query_sql_not_data, add_column_table_sql, insert_table_sql, insert_sql
from utils.api import add_assets, get_assets
from functools import wraps
from utils import auth
from utils.api import query_string


class Comment(Resource):
    key = 'comment' 
    comment = {
        'id': 'int',
        'date': 'string',
        'comment_text': 'string',
        'assets': 'string_array'
    }
    try:
        create_table_sql('{}'.format(key + '_1'), comment)
    except:
        pass
    try:
        add_column_table_sql('{}'.format(key + '_1'), comment)
    except:
        pass

class Collection(Comment):
    def get(self, id):
        limit = request.query_string.split('=')[1]
        sql = 'SELECT id, date, comment_text, assets FROM {} ORDER BY id ASC LIMIT {}'.format(self.key + '_' + id, limit);
        data = query_sql(sql)
        comments = []
        if data:
            for val in data:
                comments.append({
                    'id': val[0], 
                    'date': val[1], 
                    'comment_text': val[2], 
                    'assets': val[3]
                })
        return jsonify({'comments': comments})
        

class Item(Comment):
    def get(self, id):
        sql = 'SELECT id, "date", comment_text, assets FROM {} WHERE id={}'.format(self.key, id)
        data = query_sql(sql)
        comment = {}
        if data:
            for val in data:
                comment = {
                    'id': val[0], 
                    'date': val[1], 
                    'comment_text': val[2], 
                    'assets': val[3]
                }
        return jsonify({'comment': comment})

    def post(self, id):
        raw_data = request.get_json()
        data = {}
        if raw_data:
            if raw_data['assets']:
                links = add_assets(raw_data['assets'])
                if links and links not in NONE_WORDS:
                    data['assets'] = links
            if raw_data.has_key('comment_text'):
                data['comment_text'] = raw_data['comment_text']
            data['date'] = str(int(time.time()))
        if not data:
            return abort(400, 'Can not insert a comment!')
        # insert_table_sql(self.key + '_' + id, data)
        fields = ', '.join(['date', 'comment_text', 'assets'])
        # values = (data['date'], data['comment_text'])
        sql = "INSERT INTO {} ({}) VALUES ('{}', '{}', ARRAY {});".format(self.key + '_' + id, fields, data['date'], data['comment_text'], data['assets'])
        query_sql_not_data(sql)
        return jsonify({'message': 'successful'})

    def put(self, id):
        raw_data = request.get_json()
        if raw_data and raw_data.has_key('comment_text') and raw_data.has_key('blog_id'):
            sql = "UPDATE {} SET {}='{}' WHERE id='{}';".format(self.key + '_' + str(raw_data['blog_id']), 'comment_text', str(raw_data['comment_text']), id)
            query_sql_not_data(sql)
        return jsonify({'message': 'successful'})

    def delete(self, id):
        raw_data = query_string(request)
        if raw_data:
            sql = 'DELETE FROM {} WHERE id={};'.format(self.key + '_' + str(raw_data[0].split('=')[1]), id)
            query_sql_not_data(sql)
        else:
            return abort(400, 'Something wrong')
        return jsonify({'message': 'successful'})
