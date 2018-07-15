import sys, os, json, requests
from flask import Flask, jsonify, redirect, url_for, render_template, request, abort, Response
from werkzeug.wrappers import BaseRequest
from werkzeug.exceptions import HTTPException, NotFound
from werkzeug.http import HTTP_STATUS_CODES
from flask_cors import CORS, cross_origin
from login import do_the_login, login_success
from home import get_phone
from pgsql import cur, conn

app = Flask(__name__)
cors = CORS(app)
app.config["DEBUG"] = True

# class PaymentRequired(HTTPException):
#     code = 404
#     description = 'not found'

# HTTP_STATUS_CODES[404] = 'Not found' 

@cross_origin()
@app.route('/', methods=['GET'])
def home(name=None):
    return '''<h1>Distant Reading Archive</h1>
            <p>A prototype API for distant reading of science fiction novels.</p>'''

@app.route('/phones', methods=['GET'])
def get_phones():
    data = get_phone()
    return jsonify(data)

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        user = {}
        user['email'] = request.form['email']
        user['password'] = request.form['password']
        result = do_the_login(user)
        if result[0] == True:
            if result[1]:
                data = {
                    'data': result[1]
                }
                return jsonify(data)
        elif result[0] == False:
            return Response(result[1], status=404)
        else:
            return abort(400)
    else:
        email = login_success()
        if email:
            return jsonify({'data':email})
        else:
            return abort(400)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="127.0.0.1", port=port)