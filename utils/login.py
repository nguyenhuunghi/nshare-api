import bcrypt

def do_the_login(user):
    cur.execute("select id, email, pass from _user")
    conn.commit()
    _users = cur.fetchall()
    user_data = {}
    msg = ''
    for _user in _users:
        user_data['id'] = _user[0]
        user_data['email'] = _user[1]
        user_data['password'] = _user[2]
        if user['email'] and user['email'] == user_data['email']:
            if user['password'] and bcrypt.checkpw(user['password'].encode('utf8'), user_data['password']):
                return True, user_data
            else:
                msg = 'Wrong password'
                return False, msg
        else:
            msg = 'Not found email'
            return False, msg

def login_success():
    cur.execute("select email from _user")
    conn.commit()
    _users = cur.fetchall()
    user_data = {}
    for _user in _users:
        user_data['email'] = _user[0]
    return user_data