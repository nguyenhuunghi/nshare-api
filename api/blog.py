import requests, json, sys, os, time, datetime
#  import frameworks
from werkzeug.exceptions import HTTPException
from flask import Flask, abort, request, jsonify, Response, make_response
from flask_restful import Resource
# import utils
from utils import TRUE_WORDS, FALSE_WORDS, NONE_WORDS
from utils.api import add_assets, get_assets
from utils import auth, db, pgsql

class Blog(Resource):
    def __init__(self):
        self.__table__ = 'blog'
        self.__column__ = {
            'id': 'int',
            'date': 'string',
            'intro_text': 'string',
            'blog_text': 'string',
            'comments': 'array',
            'assets': 'string'
        }
        self.db = db.Database(self.__table__, self.__column__)
        
    # @auth.requires_auth

class Collection(Blog):
    def get(self):
        sql = 'SELECT id, date, intro_text FROM {}'.format(self.__table__);
        data = self.db.query(sql)
        blogs = []
        if not data or len(data) <= 0:
            return jsonify({'blogs': blogs})
        for d in data:
            blogs.append({'id': d[0], 'date': d[1], 'intro_text': d[2]})
        return jsonify({'blogs': blogs})

class Item(Blog):
    def get(self, id):
        sql = 'SELECT id, date, intro_text, blog_text, comments FROM {} WHERE id={}'.format(self.__table__, id);
        blog = {}
        data = self.db.query(sql)
        if data:
            for d in data:
                blog = {'id': d[0], 'date': d[1], 'intro_text': d[2], 'blog_text': d[3], 'comments': d[4]}
        return jsonify({'blog': blog})

