'''main program'''

import xml.etree.ElementTree as ET
import ch_mysql
import ch_tables



def main_program():
    '''main program'''

    #load configuration settings
    ch_config = ch_tables.get_config_from_file()

    #create table objects
    ch_data_table = ch_tables.initialise_chdata_object()
    pc_data_table = ch_tables.initialise_pcdata_object()

    #create database it if it doesn't already exist
    ch_mysql.create_fs_db(ch_config)

    #create a connection and cursor
    config_w_db = ch_mysql.mysqlconfig_from_config(ch_config)
    config_w_db['database'] = ch_config['database_name']
    _, ch_cursor = ch_mysql.create_connection_cursor(config_w_db)

    #check if ch data table exists, create and populate it if it doesn't
    if ch_mysql.check_table_exists(ch_config['ch_table_name'], ch_cursor.cursor):
        print('Table: \'' + ch_config['ch_table_name'] + '\' already exists')
    else:
        ch_tables.create_table(ch_config, ch_data_table)
        print('Table: \'' + ch_config['ch_table_name'] + '\' has been created')
        print('Populating table....')
        ch_tables.populate_ch_table(ch_config, ch_data_table)

    #check if pc data table exists, create and populate it if it doesn't
    if ch_mysql.check_table_exists(ch_config['pc_table_name'], ch_cursor.cursor):
        print('Table: \'' + ch_config['pc_table_name'] + '\' already exists')
    else:
        ch_tables.create_table(ch_config, pc_data_table)
        print('Table: \'' + ch_config['pc_table_name'] + '\' has been created')
        print('Populating table....')
        ch_tables.populate_pc_table(ch_config, pc_data_table)

  

if __name__ == '__main__':
    main_program()
