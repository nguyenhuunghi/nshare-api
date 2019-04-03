import sys, os, json, requests
from datetime import datetime, timedelta
from flask_restful import Resource
from flask import Flask, request, abort, jsonify
from utils.pgsql import conn, cur
from utils import TRUE_WORDS, FALSE_WORDS, NONE_WORDS, JWT_SECRET, JWT_ALGORITHM,  auth
from utils.user import hash_password
import bcrypt, jwt

class Login(Resource):
    def check_email_login(self, email=None):
        if email is None:
            return False
        sql = "SELECT count(*) FROM {} WHERE email='{}';".format('_user', email)
        try:
            conn.commit()
        except:
            pass
        cur.execute(sql)
        if cur.fetchone()[0] > 0:
            return True
        return False

    def check_password(self, pwd=None, email=None):   
        if pwd is None or email is None:
            return False
        sql = "SELECT password FROM {} WHERE email='{}';".format('_user', email)
        try:
            conn.commit()
        except:
            pass
        cur.execute(sql)
        passwords = [x for x in cur.fetchone()][0]
        pwd = pwd.encode(encoding='UTF-8',errors='strict')
        if bcrypt.hashpw(pwd, passwords) == passwords:
            return True
        return False        
    
    def post(self):
        raw_data = request.get_json()
        if raw_data['email'] not in NONE_WORDS:
            check_email_login = self.check_email_login(raw_data['email'])
            if check_email_login in NONE_WORDS:
                return abort(401, 'The database wrong!')
            if check_email_login not in TRUE_WORDS:
                return abort(400, 'Your email is not correct!')
        if raw_data['password'] not in NONE_WORDS:
            check_password = self.check_password(raw_data['password'], raw_data['email'])
            if check_password in NONE_WORDS:
                return abort(401, 'The database wrong!')
            if check_password not in TRUE_WORDS:
                return abort(400, 'Your password is not correct!')
        sql = "SELECT id FROM {} WHERE email='{}';".format('_user', raw_data['email'])
        try:
            conn.commit()
        except:
            pass
        cur.execute(sql)
        user = cur.fetchall()[0]
        payload = {
            'user_id': user[0]
        }
        jwt_token = jwt.encode(payload, JWT_SECRET, JWT_ALGORITHM)
        return jsonify({'token': jwt_token.decode('utf-8')})

