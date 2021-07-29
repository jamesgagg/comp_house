import copy
from pathlib import Path

from database import (database_exists,
                      create_database,
                      table_exists,
                      create_database_connection,
                      create_database_cursor)
from tables import (config_from_xml_file,
                    create_mysql_table,
                    load_data_into_mysql_table)



CONFIG_FILE = str(Path(__file__).parent / 'config.xml')



def main():
    config = config_from_xml_file(CONFIG_FILE)

    mysql_config = copy.deepcopy(config['mysql_config'])
    del mysql_config['database'] # databases can't be checked or created if a database is specified
    database_connection = create_database_connection(mysql_config)
    database_cursor = create_database_cursor(database_connection)

    if database_exists(config, database_cursor):
        print("'{}' database already exists.".format(config['database_name']))
    else:
        create_database(config, database_cursor)
    print()

    database_cursor.stop_cursor()
    database_connection.disconnect()

    database_connection = create_database_connection(config['mysql_config'])
    database_cursor = create_database_cursor(database_connection)

    for table in config['tables'].keys():
        if table_exists(table, database_cursor):
            print("'{}' table already exists.".format(table))
        else:
            create_mysql_table(config, table, database_connection, database_cursor)
            print("'{}' table has been created.".format(table))
            print("Populating '{}' table with data......".format(table))
            load_data_into_mysql_table(config, table, database_connection, database_cursor)
            print("Population of '{}' table has been completed".format(table))
            print()

    database_cursor.stop_cursor()
    database_connection.disconnect()



if __name__ == '__main__':
    main()
