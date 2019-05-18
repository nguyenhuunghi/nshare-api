import requests, json, sys, os, time, datetime
from werkzeug.exceptions import HTTPException
from flask import Flask, abort, request, jsonify, Response, make_response
from flask_restful import Resource
from flask_restful.utils import cors
from utils import TRUE_WORDS, FALSE_WORDS, NONE_WORDS
from config import conn, cur 
from utils.pgsql import create_table_sql, query_sql_fetchall, add_column_table_sql
from utils.api import add_assets, get_assets
from functools import wraps
from utils import auth

class Blog(Resource):
    key = 'blog' 
    blog = {
        'id': 'int',
        'date': 'string',
        'intro_text': 'string',
        'blog_text': 'string',
        'comments': 'array',
        'assets': 'array'
    }
    try: create_table_sql(key, blog)
    except: pass
    try: add_column_table_sql(key, blog)
    except: pass
    # @auth.requires_auth

class Collection(Blog):
    def get(self):
        sql = 'SELECT id, date, intro_text FROM {}'.format(self.key);
        blogs = []
        data = query_sql_fetchall(sql)
        if data:
            for d in data:
                blogs.append({'id': d[0], 'date': d[1], 'intro_text': d[2]})
        return jsonify({'blogs': blogs})

class Item(Blog):
    def get(self, id):
        sql = 'SELECT id, date, intro_text, blog_text, comments FROM {} WHERE id={}'.format(self.key, id);
        blog = {}
        data = query_sql_fetchall(sql)
        if data:
            for d in data:
                blog = {'id': d[0], 'date': d[1], 'intro_text': d[2], 'blog_text': d[3], 'comments': d[4]}
        return jsonify({'blog': blog})

    def post(self):
        return {}

    def put(self):
        return {}
