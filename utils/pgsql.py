from config import conn, cur

def create_table_sql(table_name, fields):
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
    for field in fields:
        type_of_field = fields[field]
        if field == 'id':
            fields[field] = 'serial primary key'
        elif type_of_field in map_fields and field != 'id':
            fields[field] = map_fields[type_of_field]
        new_fields.append(field + ' ' + fields[field])
    sql_field = ', '.join(new_fields)
    sql = 'CREATE TABLE "{}" ({});'.format(table_name, sql_field)
    query_sql_not_data(sql)

def add_column_table_sql(table_name, fields):
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
    sql = "SELECT column_name FROM information_schema.columns WHERE table_name='{}'".format(table_name);
    columns_query = query_sql(sql)
    columns_already_exists = [val for cols in columns_query for val in cols]
    new_columns = [field for field in fields if field not in columns_already_exists] 
    for field in new_columns:
        type_of_field = fields[field]
        if field == 'id':
            fields[field] = 'serial primary key'
        elif type_of_field in map_fields and field != 'id':
            fields[field] = map_fields[type_of_field]
        new_fields.append('ADD ' + field + ' ' + fields[field])
    sql_field = ', '.join(new_fields)
    sql = 'ALTER TABLE "{}" {};'.format(table_name, sql_field)
    query_sql_not_data(sql)

def insert_table_sql(table_name, values):
    sql_field = ''
    sql_value = ''
    new_fields = []
    new_values = []
    if table_name == 'user':
        table_name = '_user'
    for value in values:
        if value != 'id':
            new_fields.append(value)
            # except list
            if type(values[value]) == list:
                new_values.append(ARRAY[values[value]])
            else:
                new_values.append("'" + values[value] + "'")
    sql_field = ', '.join(new_fields)
    sql_value = ', '.join(new_values)
    sql = "INSERT INTO {} ({}) VALUES ({});".format(table_name, sql_field, sql_value)
    query_sql_not_data(sql)

def update_table_sql(table_name, values, places):
    sql_value = ''
    new_values = []
    if table_name == 'user':
        table_name = '_user'
    for value in values:
        if value != 'id':
            new_values.append(value + '+' + "'" + values[value] + "'")
    sql_value = ', '.join(new_values)
    sql = 'UPDATE TABLE {} SET {} WHERE {}'.format(table_name, sql_value, places)
    query_sql_not_data(sql)

def query_sql(sql):
    try:
        cur.execute(sql)
        conn.commit()
    except:
        conn.rollback()
    data = cur.fetchall()
    return data

def insert_sql(sql, values):
    try:
        cur.execute(sql, values)
        conn.commit()
    except:
        conn.rollback()

def query_many_sql(sql, values):
    try:
        cur.executemany(sql, values)
        conn.commit()
    except:
        conn.rollback()

def query_sql_not_data(sql):
    try:
        cur.execute(sql)
        conn.commit()
    except:
        conn.rollback()


