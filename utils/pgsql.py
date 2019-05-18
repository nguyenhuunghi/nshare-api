from config import conn, cur
from utils import TRUE_WORDS, FALSE_WORDS, NONE_WORDS
from flask import abort

def create_table_sql(table_name, field_table=None):
    fields = None
    if field_table:
        fields = field_table.copy()
    sql_field = ''
    new_fields = []
    map_fields = {
        'int': 'int',
        'float': 'float',
        'string': 'varchar',
        'array': 'integer ARRAY',
        'string_array': 'varchar ARRAY'
    }
    if table_name == 'user':
        table_name = '_user'
    if fields:
        for field in fields:
            type_of_field = fields[field]
            if field == 'id':
                fields[field] = 'serial primary key'
            if type_of_field in map_fields and field != 'id':
                fields[field] = map_fields[type_of_field]
            new_fields.append(field + ' ' + fields[field])
        sql_field = ', '.join(new_fields)
        sql = 'CREATE TABLE "{}" ({});'.format(table_name, sql_field)
        query_sql(sql)
    return

def add_column_table_sql(table_name, field_table=None):
    fields = None
    if field_table:
        fields = field_table.copy()
    new_fields = []
    map_fields = {
        'int': 'int',
        'float': 'float',
        'string': 'varchar',
        'array': 'integer ARRAY',
        'string_array': 'varchar ARRAY'
    }
    if table_name == 'user':
        table_name = '_user'
    sql = "SELECT column_name FROM information_schema.columns WHERE table_name='{}'".format(table_name);
    column_query = query_sql_fetchall(sql)
    if fields:
        # find columns alreay exists in table
        columns_already_exists = [val for cols in column_query for val in cols]
        # check field already in columns_already_exists yet?
        new_columns = [field for field in fields if field not in columns_already_exists] 
        if len(new_columns) > 0:
            for field in new_columns:
                type_of_field = fields[field]
                if field == 'id':
                    fields[field] = 'serial primary key'
                if type_of_field in map_fields and field != 'id':
                    fields[field] = map_fields[type_of_field]
                new_fields.append('ADD ' + field + ' ' + fields[field])
            sql_field = ', '.join(new_fields)
            sql = 'ALTER TABLE "{}" {};'.format(table_name, sql_field)
            query_sql(sql)
    return

def modify_data_type_table_sql(table_name, field_table=None):
    fields = None
    if field_table:
        fields = field_table.copy()
    new_fields = []
    if table_name == 'user':
        table_name = '_user'
    sql = "SELECT column_name, data_type FROM information_schema.columns WHERE table_name='{}'".format(table_name);
    column_query = query_sql_fetchall(sql)
    map_data_type = {
        'integer': 'int',
        'character varying': 'string',
        'ARRAY': 'array'
    }
    if fields:
        new_data_type = [field for field in column_query if map_data_type[field[1]] != fields[field[0]]]
        map_fields = {
            'int': 'int',
            'float': 'float',
            'string': 'varchar',
            'array': 'integer ARRAY',
            'string_array': 'varchar ARRAY'
        }
        if len(new_data_type) > 0:
            for col, col_type in new_data_type:
                new_fields.append(str(col) + ' TYPE ' + str(map_fields[fields[col]]))
            sql_field = ', '.join(new_fields)
            sql = "ALTER TABLE {} ALTER COLUMN {};".format(table_name, sql_field)
            query_sql(sql)
    return

def insert_table_sql(table_name=None, fields=None, values=None):
    sql_fields = ''
    sql_values = ''
    new_values = []
    if table_name and fields and values:
        if table_name == 'user':
            table_name = '_user'
        for field in fields:
            if field != 'id':
                new_values.append("'" + values[field] + "'")
        sql_fields = ', '.join(fields)
        sql_values = ', '.join(new_values)
        sql = "INSERT INTO {} ({}) VALUES ({});".format(table_name, sql_fields, sql_values)
        query_sql(sql)
    return

def update_table_sql(table_name=None, fields=None, values=None, field_condition=None, value_condition=None):
    sql_value = ''
    new_values = []
    if table_name in NONE_WORDS:
        return abort(400, 'you have to table_name')
    if field_condition in NONE_WORDS or value_condition in NONE_WORDS:
        return abort(400, 'you have to field_condition and value_condition')
    if table_name == 'user':
        table_name = '_user'
    for field in fields:
        if field != 'id':
            new_values.append(field + '=' + "'" + values[field] + "'")
    sql_value = ','.join(new_values)
    sql = "UPDATE {} SET {} WHERE {}='{}'".format(table_name, sql_value, field_condition, value_condition)
    query_sql(sql)

def query_sql_fetchall(sql):
    try:
        cur.execute(sql)
        conn.commit()
    except: conn.rollback()
    data = cur.fetchall()
    if not data:
        return None
    return data

def query_sql_fetchone(sql):
    try:
        cur.execute(sql)
        conn.commit()
    except: conn.rollback()
    data = cur.fetchone()
    if not data:
        return None
    return data

def insert_sql(sql, values):
    try:
        cur.execute(sql, values)
        conn.commit()
    except: conn.rollback()

def query_many_sql(sql, values):
    try:
        cur.executemany(sql, values)
        conn.commit()
    except: conn.rollback()

def query_sql(sql):
    try:
        cur.execute(sql)
        conn.commit()
    except: conn.rollback()


