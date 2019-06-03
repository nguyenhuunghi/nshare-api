import requests, json, sys, os, time, datetime
from werkzeug.exceptions import HTTPException
from flask import Flask, abort, request, jsonify, Response, make_response
from flask_restful import Resource
from flask_restful.utils import cors
from utils import TRUE_WORDS, FALSE_WORDS, NONE_WORDS
from utils.api import add_assets, get_assets
from functools import wraps
from utils import auth

class Task(Resource):
    def __init__(self):
        self.key = 'task' 
        self.task = {
            'id': 'int',
            'field': 'int',
            'task': 'string'
        }

        # pgsql.init_db(__tablename__, columns)

    # @auth.requires_auth
    def get(self):
        sql = 'SELECT id, task, field FROM {}'.format(self.key)
        data = query_sql_fetchall(sql)
        tasks = []
        if data not in NONE_WORDS:
            for t in data:
                if t[2] == 'todo':
                    tasks.append({'id': t[0], 'task': t[1], 'field': t[2]})
        return jsonify({'task': tasks})

    def post(self):
        raw_data = request.get_json()
        if raw_data not in NONE_WORDS:
            sql = "INSERT INTO {} ({}, {}) VALUES ('{}', '{}');".format(self.key, 'task', 'field', raw_data['task'], 'todo')
            query_sql_fetchall(sql)
        return jsonify({'message': 'successful'}) 

    def put(self):
        raw_data = request.get_json()
        if raw_data not in NONE_WORDS:
            sql = "INSERT INTO \"{}\" ({}) VALUES ('{}')".format(str(raw_data['field']) + '-' + 'field', 'task', raw_data['task'])
            query_sql_fetchall(sql)
            field = None
            sql = 'SELECT field FROM "{}" WHERE id={}'.format(self.key, raw_data['task'])
            field = query_sql_fetchall(sql)
            if field and str(field) != str(raw_data['field']):
                if str(field) != 'todo':
                    sql = "DELETE FROM \"{}\" WHERE task={}".format(str(field) + '-' + 'field', raw_data['task'])
                    query_sql_fetchall(sql)
            sql = "UPDATE \"{}\" SET {}={} WHERE id='{}'".format(self.key, 'field', raw_data['field'], raw_data['task'])
            query_sql_fetchall(sql)
            tasks = get_field_by_id(str(raw_data['field']))
        return jsonify({'message': 'successful', 'task': tasks})

def get_task_by_id(id):
    task = None
    sql = 'SELECT task FROM {} WHERE id={}'.format('task', id)
    task = query_sql_fetchall(sql)
    if task in NONE_WORDS:
        task = ''
    return task

def get_field_by_id(id):
    data = None
    sql = 'SELECT task FROM "{}"'.format(str(id) + '-' + 'field')
    data = query_sql_fetchall(sql)
    tasks = []
    if data not in NONE_WORDS:
        for t in data:
            tasks.append({
                'id': t[0],
                'name': get_task_by_id(t[0])
            })
    return tasks

class Field(Resource):
    def __init__(self):
        self.key = 'field'
        self.field = {
            'id': 'int',
            'name': 'string'
        }
        try:
            create_table_sql(self.key, self.field)
        except:
            pass

    def get(self):
        data = None
        sql = 'SELECT id, name FROM {}'.format(self.key)
        data = query_sql_fetchall(sql)
        fields = []
        if data not in NONE_WORDS:
            for f in data:
                task = get_field_by_id(f[0])
                fields.append({'id': f[0], 'name': f[1], 'task': task})
        return jsonify({'field': fields})

    def post(self):
        raw_data = request.get_json()
        if raw_data not in NONE_WORDS:
            last_id = None
            sql = "INSERT INTO {} ({}) VALUES ('{}')".format(self.key, 'name', raw_data['field'])
            query_sql_fetchall(sql)
            sql = 'SELECT MAX(id) FROM {}'.format(self.key)
            last_id = query_sql_fetchall(sql)
            if last_id not in NONE_WORDS:
                create_table_sql('{}'.format(str(last_id) + '-'+ self.key), {'id': 'int', 'task': 'int'})
        return jsonify({'message': 'successful'})
