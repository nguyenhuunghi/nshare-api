import requests, json, sys, os, time, datetime
from werkzeug.exceptions import HTTPException
from flask import Flask, abort, request, jsonify, Response, make_response
from flask_restful import Resource
from flask_restful.utils import cors
from utils import TRUE_WORDS, FALSE_WORDS, NONE_WORDS
from config import conn, cur 
from utils.pgsql import create_table_pg, query_sql 
from utils.api import add_assets, get_assets
from functools import wraps
from utils import auth

class Comment(Resource):
    key = 'comment' 
    comment = {
        'id': 'int',
        'date': 'string',
        'comment_text': 'string',
    }
    try:
        create_table_pg(key, comment)
    except:
        pass

class Item(Comment):
    def get(self, id):
        sql = 'SELECT id, date, comment_text FROM {} WHERE id={}'.format(self.key, id);
        comments = []
        data = query_sql(sql)
        if data not in NONE_WORDS:
            for d in data:
                comments.append({'id': d[0], 'date': d[1], 'comment_text': d[2]})
        return jsonify({'comments': comments})

    def post(self):
        return {}

    def put(self):
        return {}
