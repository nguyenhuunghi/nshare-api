import requests, json, sys, os, time, datetime
# import frameworks
from werkzeug.exceptions import HTTPException
from flask import Flask, abort, request, jsonify, Response, make_response
from flask_restful import Resource
from flask_restful.utils import cors
from functools import wraps
# import utils
from utils import pgsql, api, auth, db, TRUE_WORDS, FALSE_WORDS, NONE_WORDS

class Comment(Resource):
    def __init__(self):
        self.__table__ = 'comment'
        self.__column__ = {
            'id': 'int',
            'blog_id': 'string',
            'date_created': 'string',
            'comment_text': 'string',
            'assets': 'string',
            'reply_comment': 'string'
        }
        self.db = db.Database(self.__table__, self.__column__)

class Collection(Comment):
    def get(self, blog_id):
        self.__table__ = self.__table__ + '_' + blog_id
        sql = 'SELECT id, date, comment_text, assets FROM {} ORDER BY id ASC'.format(self.__table__);
        data = self.db.query(sql)
        comments = []
        if not data or len(data) <= 0:
            return jsonify({'comments': comments})
        for val in data:
            comments.append({
                'id': val[0], 
                'date': val[1], 
                'comment_text': val[2], 
                'assets': val[3]
            })
        return jsonify({'comments': comments})
        
class Item(Comment):
    def post(self, id):
        raw_data = request.get_json()
        data = {}
        if raw_data:
            if raw_data.has_key('assets') and raw_data.get('assets', None):
                link = add_assets(raw_data['assets']) 
                if link: data['assets'] = link
                else: data['assets'] = ''
            else:
                data['assets'] = ''
            if raw_data.has_key('comment_text'):
                data['comment_text'] = raw_data['comment_text']
            else:
                raw_data['comment_text'] = ''
            data['date_created'] = str(int(time.time()))
        if not data:
            return abort(400, 'Can not insert a comment!')
        fields = ['date_created', 'comment_text', 'assets']
        self.db.insert_table_sql(self.__tablename__, fields, data)
        return jsonify({'message': 'successful'})

    def put(self, comment_id):
        raw_data = request.get_json()
        if raw_data and raw_data.has_key('comment_text') and raw_data.has_key('blog_id'):
            raw_data['date_created'] =  str(int(time.time()))
            fields = ['date_created', 'comment_text']
            condition = 'id={}'.format(comment_id)
            self.db.update_table_sql(self.__tablename__, fields, raw_data, condition)
        return jsonify({'message': 'successful'})

    def delete(self, comment_id):
        raw_data = api.query_string(request)
        if raw_data:
            sql = 'DELETE FROM {} WHERE id={};'.format(self.__tablename__, comment_id)
            self.db.execute(conn, sql)
        else:
            return abort(400, 'Something wrong')
        return jsonify({'message': 'successful'})

class ReplyComment(Comment):
    def post(self, comment_id):
        raw_data = request.get_json()
        data = {}
        if not raw_data:
            return abort(400, 'Something wrong')
        if raw_data.has_key('assets') and raw_data.get('assets', None):
            link = add_assets(raw_data['assets']) 
            if link: data['assets'] = link
            else: data['assets'] = ''
        else:
            data['assets'] = ''
        if raw_data.has_key('comment_text'):
            data['comment_text'] = raw_data['comment_text']
        else:
            raw_data['comment_text'] = ''
        data['date_created'] = str(int(time.time()))
        if not data:
            return abort(400, 'Can not insert a comment!')
        fields = ['date_created', 'comment_text', 'assets']
        self.db.insert_table_sql(self.__tablename__, fields, data)
        return jsonify({'message': 'successful'})
        
