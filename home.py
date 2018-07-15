from pgsql import cur, conn

def get_phone():
    cur.execute("select name from phone")
    conn.commit()
    phones = cur.fetchall()
    data = []
    for phone in phones:
        data.append(phone[0])
    return data