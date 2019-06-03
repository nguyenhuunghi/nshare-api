import sys, os, json
from utils import NONE_WORDS
import bcrypt

def verify_email(table_name, email):
    if table_name == 'user':
        table_name = '_user'
    cur.execute('SELECT email FROM {};'.format(table_name))
    emails_created = cur.fetchall()
    print 'emails_created', emails_created
    if emails_created in NONE_WORDS: return None
    else:
        emails_created = [item[0] for item in emails_created]
        if email in emails_created: return False

def hash_password(pw):
    pw = pw.encode(encoding='UTF-8',errors='strict')
    hashed = bcrypt.hashpw(pw, bcrypt.gensalt())
    if hashed:
        return hashed
    return None

