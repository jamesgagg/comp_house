'''Module containing database code'''

import mysql.connector
from mysql.connector import errorcode



class MysqlConnection():
    """MySQL connection object"""
    
    def __init__(self, config):
        '''initialise the MysqlConnection object'''
        self.config = config
        self.connection = None
        self.connected = False


    def __str__(self):
        '''prints all attributes and their values'''
        attributes = [
            "{key}='{value}'".format(key=key, value=self.__dict__[key])
            for key in self.__dict__
        ]

        return ', '.join(attributes)
        
        
    def connect(self):
        '''Tries to connect to MySQL using the supplied config, 
        returns the connection if successful, raises an error if not'''
        try:
            conn = mysql.connector.connect(**self.config)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Your user name or password is incorrect")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("The requested database does not exist")
            else:
                print(err)
            self.connection = None
            self.connected = False
        else:
            self.connection = conn
            self.connected = True


    def disconnect(self):
        '''disconnect the supplied connection'''
        self.connection.close()
        self.connection = None
        self.connected = False


class MysqlCursor():
    """MySQL cursor object"""

    def __init__(self, mysql_connection):
        '''object initialisation'''
        self.connection = mysql_connection
        self.cursor = None
        self.activecursor = False


    def __str__(self):
        '''prints all attributes and their values'''
        attributes = [
            "{key}='{value}'".format(key=key, value=self.__dict__[key])
            for key in self.__dict__
        ]

        return ', '.join(attributes)


    def start_cursor(self):
        '''create a cursor if the supplied connection is valid'''
        if isinstance(self.connection.connection, mysql.connector.connection_cext.CMySQLConnection):
            if self.connection.connection.is_connected():
                self.cursor = self.connection.connection.cursor()
                self.activecursor = True
        else:
            print('No connection was present, a cursor could not be created')
        

    def stop_cursor(self):
        '''close the supplied cursor'''
        self.cursor.close()
        self.cursor = None
        self.activecursor = False


    def execute(self, query):
        '''execute the supplied query'''
        self.cursor.execute(query)
        


def list_from_sql_query(mysql_cursor, query):
    '''return a list of the MySQL databases using the supplied cursor'''    
    mysql_cursor.execute(query)
    return [x[0] for x in mysql_cursor.fetchall()]


def check_db_exists(dbname, mysql_cursor):
    '''checks if the supplied database name is present via the 
    supplied cursor'''
    query = 'show databases'    
    return dbname in list_from_sql_query(mysql_cursor, query)


def check_table_exists(table_name, mysql_cursor):
    '''checks if the supplied database name is present via the 
    supplied cursor'''
    query = 'show tables'
    return table_name in list_from_sql_query(mysql_cursor, query)


def create_connection_cursor(ccs_config):
    '''Create connection and cursor'''
    ccs_connection = MysqlConnection(ccs_config)
    ccs_connection.connect()
    ccs_cursor = MysqlCursor(ccs_connection)
    ccs_cursor.start_cursor()
    return [ccs_connection, ccs_cursor]


def destroy_connection_cursor(cursor, connection):
    '''Destroy connection and cursor'''
    cursor.stop_cursor()
    connection.disconnect()


def mysqlconfig_from_config(config):
    '''creates a mysql compatible config from the program config'''
    return {
        'user': config['mysql_user'],
        'password': config['mysql_password'],
        'host': config['mysql_host']
        }


def create_fs_db(config):
    '''checks if the supplied database name is present via the 
    supplied cursor, creates it if it isn't 
    returns [x,y] where x is whether the db existed when the 
    function was called and y is if the db is now in existence'''
    mysql_config = mysqlconfig_from_config(config)

    f_connection, f_cursor = create_connection_cursor(mysql_config)
    
    if check_db_exists(config['database_name'], f_cursor.cursor):
        print('Database: \'' + config['database_name'] + '\' already exists.')
        return
    
    query = 'CREATE DATABASE ' + config['database_name']
    try:
        f_cursor.execute(query)
    except mysql.connector.errors.DatabaseError as error:
        print('Database: \'' + config['database_name'] + '\' could not be created.')
        print(error)
        return
    else:
        print('Database: \'' + config['database_name'] + '\' has been created.')
        return
    finally:
        destroy_connection_cursor(f_cursor, f_connection)
