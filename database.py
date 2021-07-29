import mysql.connector
from mysql.connector import errorcode



class MysqlConnection():
    def __init__(self, config):
        self.config = config
        self.connection = None
        self.connected = False


    def __str__(self):
        attributes = []
        for key in self.__dict__:
            attributes.append("{key}='{value}'".format(key=key, value=self.__dict__[key]))
        return ', '.join(attributes)


    def connect(self):
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
        self.connection.close()
        self.connection = None
        self.connected = False


class MysqlCursor():
    def __init__(self, mysql_connection):
        self.connection = mysql_connection
        self.cursor = None
        self.activecursor = False


    def __str__(self):
        attributes = []
        for key in self.__dict__:
            attributes.append("{key}='{value}'".format(key=key, value=self.__dict__[key]))
        return ', '.join(attributes)


    def start_cursor(self):
        if isinstance(self.connection.connection,
                      mysql.connector.connection_cext.CMySQLConnection):
            if self.connection.connection.is_connected():
                self.cursor = self.connection.connection.cursor()
                self.activecursor = True
        else:
            print('No connection was present, a cursor could not be created')


    def stop_cursor(self):
        self.cursor.close()
        self.cursor = None
        self.activecursor = False


    def execute(self, query):
        self.cursor.execute(query)



def list_from_sql_query(database_cursor, query):
    database_cursor.execute(query)
    mysql_list = [x[0] for x in database_cursor.cursor.fetchall()]
    return mysql_list


def database_exists(config, database_cursor):
    database_name = config['database_name']

    query = 'show databases'

    return database_name in list_from_sql_query(database_cursor, query)


def table_exists(table_name, database_cursor):
    query = 'show tables'
    return table_name in list_from_sql_query(database_cursor, query)


def create_database_connection(mysql_config):
    connection = MysqlConnection(mysql_config)
    connection.connect()
    return connection


def create_database_cursor(database_connection):
    cursor = MysqlCursor(database_connection)
    cursor.start_cursor()
    return cursor


def create_database(config, database_cursor):
    query = 'CREATE DATABASE ' + config['database_name']

    try:
        database_cursor.execute(query)
    except mysql.connector.errors.DatabaseError as error:
        print('Database: \'' + config['database_name'] + '\' could not be created.')
        print(error)
        return
    else:
        print('Database: \'' + config['database_name'] + '\' has been created.')
        return
