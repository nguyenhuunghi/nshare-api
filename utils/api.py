import sys, os, json, requests
from pgsql import conn, cur

client_id = 'bb4b7d38bb08bd6'
client_secret = 'ee015df68e84e93dc42fb594651639a14e48ae73'
access_token='2b9a7c6ce39556af0e56acc7abc2ba9af692a8c4'
expires_in='315360000'
token_type='bearer'
refresh_token='89ce098cb74c037800eb98c673ec560e5778daaf'
account_username='huunghi'
account_id='90815005'

def add_assets(file):
    # sotre image to imgur
    url = "https://api.imgur.com/3/image"
    headers = {
        'Content-type': 'multipart/form-data',
        'Authorization': 'Bearer {}'.format(access_token)
    }
    response = requests.request('POST', url, data=file, headers=headers)
    print response
    data = json.loads(response.text.encode('utf8'))
    return data

def get_assets():
    url = "https://api.imgur.com/3/account/me/images"
    headers = {'Authorization': 'Bearer {}'.format(access_token)}
    response = requests.request("GET", url, headers=headers)
    assets = json.loads(response.text.encode('utf8'))
    return assets
