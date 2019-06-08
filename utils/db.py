import sys, os

# Import libraries
import psycopg2
# import frameworks
from flask import abort
# import config, utils
from config import db_config

class Database:
    def __init__(self, table=None, columns=None):
        self.conn = self.conn(db_config)
        self.__table__ = table
        self.__column__ = columns
        self.map_fields = {
            'int': 'integer',
            'float': 'float',
            'string': 'varchar',
            'array': 'integer ARRAY',
            'string_array': 'varchar ARRAY'
        }
        self.init_db()

    def conn(self, db_config):
        print('Connecting to database')
        conn = psycopg2.connect(db_config)
        conn.autocommit = True
        return conn

    def execute(self, *args):
        cur = self.conn.cursor()
        try: cur.execute(*args)
        except Exception as e: 
            print('Error', e.message)
            return abort(400, 'Execute is wrong!')

    def query(self, *args):
        cur = self.conn.cursor()
        try: cur.execute(*args)
        except Exception as e: 
            print('Error', e.message )
            return abort(400, 'Execute is wrong!')
        return cur.fetchall()

    def query_one(self, *args):
        return self.query(*args)[0]

    def query_values(self, *args):
        result = self.query(*args) # result return like ('[(1,), (2, ), ...]')
        if result: return list(map(lambda r: r[0], result)) # lambda return a function and map return a object
        else: return abort(400, 'Database is wrong!')

    def query_value(self, *args):
        result = self.query_values(*args)
        return result and result[0]

    def init_db(self):
        if not self.__table__ or not self.__column__:
            return abort(400, 'Not found tables or columns!')
        fields = self.__column__.copy()
        if self.__table__ == 'user': self.__table__ = '_user'
        sql = "SELECT count(*) FROM information_schema.tables WHERE table_name = '{}'".format(self.__table__)
        count = self.query_value(sql)
        if count == 0:
            self.create_table(fields)
            return
        sql = "SELECT column_name, data_type FROM information_schema.columns WHERE table_name ='{}'".format(self.__table__);
        columns_query = self.query(sql)
        columns_exists = list(map(lambda r: r[0], columns_query)) # return a list of columns
        if columns_exists and len(columns_exists) > 0:
            self.add_column_table(columns_exists, fields)
            self.drop_column_table(columns_exists, fields)
        if columns_query and len(columns_query) > 0:
            self.modify_data_type_table(columns_query, fields)

    # Create a table with psotgresql
    def create_table(self, fields=None):
        new_fields = []
        if self.__table__ == 'user': self.__table__ = '_user'
        if not fields:
            return abort(400, 'Not found columns.')
        for field in fields:
            type_of_field = fields[field]
            if field == 'id':
                fields[field] = 'serial primary key'
            if type_of_field in self.map_fields and field != 'id':
                fields[field] = self.map_fields[type_of_field]
            new_fields.append(field + ' ' + fields[field])
        sql_field = ', '.join(new_fields)
        sql = 'CREATE TABLE "{}" ({});'.format(self.__table__, sql_field)
        return self.execute(sql)

    # add column into table.
    def add_column_table(self, columns_exists=None, fields=None):
        if not columns_exists or not fields:
            return
        new_fields = []
        # check field already in columns_exists yet?
        new_columns = [field for field in fields.keys() if field not in columns_exists]
        if not new_columns or len(new_columns) <= 0:
            return
        for field in new_columns:
            type_of_field = fields[field]
            if type_of_field in self.map_fields:
                fields[field] = self.map_fields[type_of_field]
            new_fields.append('ADD ' + field + ' ' + fields[field])
        sql_field = ', '.join(new_fields)
        sql = 'ALTER TABLE "{}" {};'.format(self.__table__, sql_field)
        return self.execute(sql)

    # drop column at the table
    def drop_column_table(self, columns_exists=None, fields=None):
        if self.__table__ or columns_exists and fields:
            columns_removed = [col for col in columns_exists if col not in fields.keys()]
            columns_have_to_remove = []
            if columns_removed and len(columns_removed) > 0:
                for col in columns_removed:
                    columns_have_to_remove.append('DROP COLUMN IF EXISTS {}'.format(col))
                sql_field = ', '.join(columns_have_to_remove)
                sql = 'ALTER TABLE {} {};'.format(self.__table__, sql_field)
                return self.execute(sql)

    # modify type of column at the table
    def modify_data_type_table(self, column_query=None, fields=None):
        if self.__table__ or column_query and fields:
            map_data_type = {
                'integer': 'int',
                'character varying': 'string',
                'ARRAY': 'array'
            }
            new_data_type = [field for field in column_query if map_data_type[field[1]] != fields[field[0]]]
            if new_data_type and len(new_data_type) > 0:
                for col, col_type in new_data_type:
                    sql_field = str(col) + ' TYPE ' + str(self.map_fields[fields[col]]) + ' USING ( ' + str(col) + '::' + str(self.map_fields[fields[col]]) + ' )'
                    sql = "ALTER TABLE {} ALTER COLUMN {};".format(self.__table__, sql_field)
                    self.execute(sql)

    def insert_table_sql(self, fields=None, values=None):
        new_values = []
        if self.__table__ or fields and values:
            if self.__table__ == 'user': self.__table__ = '_user'
            for field in fields:
                if field == 'id':
                    continue
                new_values.append("'" + values[field] + "'")
            sql_fields = ', '.join(fields)
            sql_values = ', '.join(new_values)
            sql = "INSERT INTO {} ({}) VALUES ({});".format(self.__table__, sql_fields, sql_values)
            return self.execute(sql)
        
    def update_table_sql(self, fields=None, values=None, condition=None):
        sql_value = ''
        new_values = []
        if not self.__table__:
            return abort(400, 'you have to table')
        if not condition:
            return abort(400, "you don't have condition")
        if self.__table__ == 'user': self.__table__ = '_user'
        if fields:
            for field in fields:
                if field == 'id':
                    continue
                new_values.append(field + '=' + "'" + values[field] + "'")
            sql_value = ','.join(new_values)
            sql = "UPDATE {} SET {} WHERE {}".format(self.__table__, sql_value, condition)
            return self.execute(sql)
