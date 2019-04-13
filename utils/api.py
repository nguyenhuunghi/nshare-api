import sys, os, json, requests
from config import conn, cur, access_token
from flask import request, abort

def add_assets(file):
    # sotre image to imgur
    url = "https://api.imgur.com/3/image"
    headers = {
        'Content-type': 'multipart/form-data',
        'Authorization': 'Bearer {}'.format(access_token)
    }
    data = None
    links = []
    response = requests.request('POST', url, data=file, headers=headers)
    data = json.loads(response.text.encode('utf8'))
    if data['status'] != 200:
        return abort(400, 'Upload image failed!')
    link = data['data']['link']
    links.append(str(link))
    if not link:
        return abort(400, 'The assets not link!')
    return links

def get_assets():
    # get image from imgur
    url = "https://api.imgur.com/3/account/me/images"
    headers = {'Authorization': 'Bearer {}'.format(access_token)}
    response = requests.request("GET", url, headers=headers)
    assets = json.loads(response.text.encode('utf8'))
    return assets

def query_string(request):
    return request.query_string.split('&')
