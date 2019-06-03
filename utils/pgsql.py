# from config import conn
# from utils import TRUE_WORDS, FALSE_WORDS, NONE_WORDS
# from flask import abort
# import db

# map_fields = {
#     'int': 'integer',
#     'float': 'float',
#     'string': 'varchar',
#     'array': 'integer ARRAY',
#     'string_array': 'varchar ARRAY'
# }

# def init_db(table_name=None, columns=None):
#     if not table_name and not columns:
#         return
#     fields = columns.copy()
#     if table_name == 'user':
#         table_name = '_user'
#     sql = "SELECT count(*) FROM information_schema.tables WHERE table_name = '{}'".format(table_name)
#     count = db.query_value(conn, sql)
#     if int(count) == 0:
#         create_table(table_name, fields)
#         return
#     sql = "SELECT column_name, data_type FROM information_schema.columns WHERE table_name='{}'".format(table_name);
#     columns_query = db.query(conn, sql)
#     columns_exists = map(lambda r: r[0], columns_query)
#     if columns_exists and len(columns_exists) > 0:
#         add_column_table(table_name, columns_exists, fields)
#         drop_column_table(table_name, columns_exists, fields)
#     if columns_query and len(columns_query) > 0:
#         modify_data_type_table(table_name, columns_query, fields)

# def create_table(table_name=None, fields=None):
#     new_fields = []
#     if table_name == 'user':
#         table_name = '_user'
#     if fields:
#         for field in fields:
#             type_of_field = fields[field]
#             if field == 'id':
#                 fields[field] = 'serial primary key'
#             if type_of_field in map_fields and field != 'id':
#                 fields[field] = map_fields[type_of_field]
#             new_fields.append(field + ' ' + fields[field])
#         sql_field = ', '.join(new_fields)
#         sql = 'CREATE TABLE "{}" ({});'.format(table_name, sql_field)
#         return db.execute(conn, sql)

# def add_column_table(table_name=None, columns_exists=None, fields=None):
#     if table_name and columns_exists and fields:
#         new_fields = []
#         # check field already in columns_exists yet?
#         new_columns = [field for field in fields.keys() if field not in columns_exists]
#         if new_columns and len(new_columns) > 0:
#             for field in new_columns:
#                 type_of_field = fields[field]
#                 if type_of_field in map_fields:
#                     fields[field] = map_fields[type_of_field]
#                 new_fields.append('ADD ' + field + ' ' + fields[field])
#             sql_field = ', '.join(new_fields)
#             sql = 'ALTER TABLE "{}" {};'.format(table_name, sql_field)
#             return db.execute(conn, sql)

# def drop_column_table(table_name=None, columns_exists=None, fields=None):
#     if table_name and columns_exists and fields:
#         columns_removed = [col for col in columns_exists if col not in fields.keys()]
#         columns_have_to_remove = []
#         if columns_removed and len(columns_removed) > 0:
#             for col in columns_removed:
#                 columns_have_to_remove.append('DROP COLUMN IF EXISTS {}'.format(col))
#             sql_field = ', '.join(columns_have_to_remove)
#             sql = 'ALTER TABLE {} {};'.format(table_name, sql_field)
#             return db.execute(conn, sql)

# def modify_data_type_table(table_name=None, column_query=None, fields=None):
#     if table_name and column_query and fields:
#         map_data_type = {
#             'integer': 'int',
#             'character varying': 'string',
#             'ARRAY': 'array'
#         }
#         new_data_type = [field for field in column_query if map_data_type[field[1]] != fields[field[0]]]
#         if new_data_type and len(new_data_type) > 0:
#             for col, col_type in new_data_type:
#                 sql_field = str(col) + ' TYPE ' + str(map_fields[fields[col]]) + ' USING ( ' + str(col) + '::' + str(map_fields[fields[col]]) + ' )'
#                 sql = "ALTER TABLE {} ALTER COLUMN {};".format(table_name, sql_field)
#                 db.execute(conn, sql)

# def insert_table_sql(table_name=None, fields=None, values=None):
#     new_values = []
#     if table_name and fields and values:
#         if table_name == 'user':
#             table_name = '_user'
#         for field in fields:
#             if field == 'id':
#                 continue
#             new_values.append("'" + values[field] + "'")
#         sql_fields = ', '.join(fields)
#         sql_values = ', '.join(new_values)
#         sql = "INSERT INTO {} ({}) VALUES ({});".format(table_name, sql_fields, sql_values)
#         return db.execute(conn, sql)
    
# def update_table_sql(table_name=None, fields=None, values=None, condition=None):
#     sql_value = ''
#     new_values = []
#     if not table_name:
#         return abort(400, 'you have to table_name')
#     if not condition:
#         return abort(400, 'you dont have condition')
#     if table_name == 'user':
#         table_name = '_user'
#     if fields:
#         for field in fields:
#             if field == 'id':
#                 continue
#             new_values.append(field + '=' + "'" + values[field] + "'")
#         sql_value = ','.join(new_values)
#         sql = "UPDATE {} SET {} WHERE {}".format(table_name, sql_value, condition)
#         return db.execute(conn, sql)
