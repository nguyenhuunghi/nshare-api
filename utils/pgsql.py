from config import conn, cur

def create_table_pg(table_name, fields):
    sql_field = ''
    new_fields = []
    map_fields = {
        'int': 'int',
        'float': 'float',
        'string': 'varchar',
        'array': 'integer ARRAY'
    }
    if table_name == 'user':
        table_name = '_user'
    for field in fields:
        type_of_field = fields[field]
        if field == 'id':
            fields[field] = 'serial primary key'
        elif type_of_field in map_fields and field != 'id':
            fields[field] = map_fields[type_of_field]
        new_fields.append(field + ' ' + fields[field])
    sql_field = ', '.join(new_fields)
    try:
        cur.execute('CREATE TABLE "{}" ({});'.format(table_name, sql_field))
        conn.commit()
    except Exception as e:
        conn.rollback()

def insert_table_pg(table_name, values):
    sql_field = ''
    sql_value = ''
    new_fields = []
    new_values = []
    if table_name == 'user':
        table_name = '_user'
    for value in values:
        if value != 'id':
            new_fields.append(value)
            new_values.append("'" + values[value] + "'")
    sql_field = ', '.join(new_fields)
    sql_value = ', '.join(new_values)
    try:
        cur.execute('INSERT INTO {} ({}) VALUES ({});'.format(table_name, sql_field, sql_value))
        conn.commit()
    except Exception as e:
        conn.rollback()

def update_table_pg(table_name, values, places):
    sql_value = ''
    new_values = []
    if table_name == 'user':
        table_name = '_user'
    for value in values:
        if value != 'id':
            new_values.append(value + '+' + "'" + values[value] + "'")
    sql_value = ', '.join(new_values)
    try:
        cur.execute('UPDATE TABLE {} SET {} WHERE {}'.format(table_name, sql_value, places))
        conn.commit()
    except:
        conn.rollback()

def query_sql(sql):
    try:
        cur.execute(sql)
        conn.commit()
    except:
        conn.rollback()
    if 'INSERT' or 'UPDATE' not in sql:
        return cur.fetchall()

