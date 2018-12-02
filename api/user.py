import requests, json, sys, os, time, datetime
from imgurpython import ImgurClient
from werkzeug.exceptions import HTTPException
from flask import Flask, abort, request, jsonify, Response, make_response
from flask_restful import Resource
from flask_restful.utils import cors
from utils import TRUE_WORDS, FALSE_WORDS, NONE_WORDS
from utils.login import do_the_login, login_success
from utils.pgsql import conn, cur, create_table_pg, insert_table_pg, update_table_pg
from utils.api import add_assets, get_assets
from utils.user import hash_password, verify_email


class User(Resource):

    key = 'user' 

    user = {
        'id': 'int',
        'full_name': 'string',
        'email': 'string',
        'password': 'string',
        'user_created': 'string',
        'token': 'string',
        'assets': 'string'
    }

    try:
        create_table_pg(key,user)
    except:
        pass

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
        if insert_table_pg(self.key, user) == False: return abort(500, 'Create a new account wrong!')
        try:
            cur.execute('SELECT id, full_name, email FROM _user WHERE email={};'.format(user['email']))
            user = cur.fetchone()
        except:
            user = None
        return abort(200, user)
