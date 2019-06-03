import requests, json, sys, os, time, datetime
from imgurpython import ImgurClient
from werkzeug.exceptions import HTTPException
from flask import Flask, abort, request, jsonify, Response, make_response
from flask_restful import Resource
from flask_restful.utils import cors
from functools import wraps
from utils import auth, pgsql, TRUE_WORDS, FALSE_WORDS, NONE_WORDS

class User(Resource):
    __tablename__ = 'user' 

    columns = {
        'id': 'int',
        'full_name': 'string',
        'email': 'string',
        'password': 'string',
        'user_created': 'string',
        'token': 'string',
        'assets': 'string'
    }

    # pgsql.init_db(__tablename__, columns)

    # @auth.requires_auth
    def get(self):
        data = {'name': 'davidism'}
        return jsonify(data)

    def post(self):
        raw_data = request.get_json()
        if raw_data['email']:
            if verify_email(self.key, raw_data['email']) in FALSE_WORDS: return abort(401, 'Email already exist!')
            if verify_email(self.key, raw_data['email']) in NONE_WORDS: return abort(502, 'Bad Gateway!')
        if raw_data['password']:
            raw_data['password'] = hash_password(raw_data['password'])
            if raw_data['password'] == None: return abort(401, 'Password wrong!')
        user = {
            'full_name': raw_data['full_name'],
            'password': raw_data['password'],
            'email': raw_data['email'],
            'assets': raw_data['assets'],
            'user_created': str(time.time())
        }
        if pgsql.insert_table_sql(self.key, user) == False: return abort(500, 'Create a new account wrong!')
        try:
            cur.execute('SELECT id, full_name, email FROM _user WHERE email={};'.format(user['email']))
            user = cur.fetchone()
        except:
            user = None
        return abort(200, user)
