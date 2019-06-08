import sys, os, json, requests
from config import access_token, account_username
from flask import request, abort

def add_assets(file):
    # sotre image to imgur
    url = "https://api.imgur.com/3/image"
    headers = {
        'Content-type': 'multipart/form-data',
        'Authorization': 'Bearer {}'.format(access_token)
    }
    data = None
    link = None
    response = requests.request('POST', url, data=file, headers=headers)
    data = json.loads(response.text.encode('utf8'))
    if data['status'] != 200:
        return abort(400, 'Upload image failed!')
    link = data['data']['link']
    if not link:
        return abort(400, 'Upload image failed without link!')
    data = data['data']
    data['datetime'] = str(data['datetime'])
    insert_table_sql('assets', ['link', 'deletehash', 'datetime'], data)
    return link

def get_assets():
    # get image from imgur
    url = "https://api.imgur.com/3/account/me/images"
    headers = {'Authorization': 'Bearer {}'.format(access_token)}
    response = requests.request("GET", url, headers=headers)
    assets = json.loads(response.text.encode('utf8'))
    return assets

def delete_assets(deleteHash):
    url = "https://api.imgur.com/3/account/{}/image/{}".format(account_username, deleteHash)
    headers = {'Authorization': 'Bearer {}'.format(access_token)}
    response = requests.request("DELETE", url, headers=headers)
    response = json.loads(response.text.encode('utf8'))
    return response
    
def query_string(request):
    _query = request.query_string
    if _query and type(_query) != str:
        _query = _query.decode('utf-8')
    else: return None
