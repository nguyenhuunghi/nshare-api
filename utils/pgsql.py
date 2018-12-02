import psycopg2

conn = psycopg2.connect("host='ec2-54-197-253-122.compute-1.amazonaws.com' dbname='df3192mkr3k3ch' user='egtavjsibewktj' password='51fa705edf6ebe7f7e7e3f2223b9768386741a7d91bc731931820e2c7dc8f95d'")
cur = conn.cursor()

def create_table_pg(table_name, fields):
    sql_field = ''
    new_fields = []
    map_fields = {
        'int': 'int',
        'float': 'float',
        'string': 'varchar'
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
    cur.execute('CREATE TABLE {} ({});'.format(table_name, sql_field))
    conn.commit()

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
        print 'INSERT INTO {} ({}) VALUES ({});'.format(table_name, sql_field, sql_value)
        cur.execute('INSERT INTO {} ({}) VALUES ({});'.format(table_name, sql_field, sql_value))
        conn.commit()
    except Exception as e:
        print e.message
        return False

def update_table_pg(table_name, values, places):
    sql_value = ''
    new_values = []
    if table_name == 'user':
        table_name = '_user'
    for value in values:
        if value != 'id':
            new_values.append(value + '+' + "'" + values[value] + "'")
    sql_value = ', '.join(new_values)
    cur.execute('UPDATE TABLE {} SET {} WHERE {}'.format(table_name, sql_value, places))
    conn.commit()

