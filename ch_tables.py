'''Module containing table code'''

from datetime import datetime
import xml.etree.ElementTree as ET


class CHTable():
    """tables class"""
    
    def __init__(self, table_name, fields,
                 sql_create_table_input_str, 
                 sql_create_table_input_format,
                 sql_input_input_str, 
                 sql_input_input_format):
        '''initialisation'''
        self.table_name = table_name
        self.fields = fields
        self.sql_create_table_input_str = sql_create_table_input_str
        self.sql_create_table_input_format = sql_create_table_input_format
        self.sql_input_input_str = sql_input_input_str
        self.sql_input_input_format = sql_input_input_format

    def sql_create_table_str(self):
        '''create the string to pass to mysql to create the table'''
        table_creation_string = self.sql_create_table_input_str.format(
            *self.sql_create_table_input_format)
        return table_creation_string

    def sql_insert_data_str(self, data):
        '''inserts data into the table'''
        insert_string = self.sql_input_input_str.format(*self.sql_input_input_format + data)
        return insert_string



def double_braces_string(no_of_instances):
    '''creates a string of '{} {},\n' repeated 'no_of_instances' times '''
    return '{} {}, ' * no_of_instances


def fields_from_ch_xml_header_file(xml_file):
    '''get field information from the xml header file'''
    ch_tree = ET.parse(xml_file)
    ch_root = ch_tree.getroot()

    output_fields = [[ch_root.find('idfield').find('field').find('name').text, 
                      ch_root.find('idfield').find('field').find('type').text]]

    chfields = ch_root.find('other_fields').findall('field')

    for field in chfields:
        output_fields.append([field.find('name').text, field.find('type').text])
    
    return output_fields


def single_braces_string(no_of_instances):
    '''returns a number of pairs of braces defined by no_of_instances'''
    return ('{}, ' * (no_of_instances - 1)) + '{}'


def single_braces_quotes_string(no_of_instances):
    '''returns a number of pairs of braces defined by no_of_instances'''
    return ('\"{}\", ' * (no_of_instances - 1)) + '\"{}\"'


def initialise_chdata_object():
    '''initialise the companies house data object'''

    table_name = "ch_data"

    chdata_xml_file = 'ch_table_headers.xml'
    fields = fields_from_ch_xml_header_file(chdata_xml_file)

    sql_create_table_input_str = ('CREATE TABLE {} ' + 
                                  '({} {} AUTO_INCREMENT, ' +
                                  double_braces_string(len(fields) - 1) + 
                                  'PRIMARY KEY ({}))')

    sql_create_table_input_format = [table_name]
    sql_create_table_input_format += [item for sublist in fields for item in sublist]
    sql_create_table_input_format += [fields[0][0]]

    sql_input_input_str = ('INSERT INTO {} (' + 
                           single_braces_string(len(fields) - 1) + 
                           ') VALUES (' + 
                           single_braces_quotes_string(len(fields) - 1) +')')

    sql_input_input_format = [table_name]
    sql_input_input_format += [sublist[0] for sublist in fields][1:]

    return CHTable(table_name, fields,
                   sql_create_table_input_str,
                   sql_create_table_input_format,
                   sql_input_input_str,
                   sql_input_input_format)


def initialise_pcdata_object():
    '''initialise the postcode data object'''

    table_name = "pc_data"

    pcdata_xml_file = 'pc_table_headers.xml'
    fields = fields_from_ch_xml_header_file(pcdata_xml_file)

    sql_create_table_input_str = ('CREATE TABLE {} ' + 
                                  '({} {} AUTO_INCREMENT, ' +
                                  double_braces_string(len(fields) - 1) + 
                                  'PRIMARY KEY ({}))')

    sql_create_table_input_format = [table_name]
    sql_create_table_input_format += [item for sublist in fields for item in sublist]
    sql_create_table_input_format += [fields[0][0]]

    sql_input_input_str = ('INSERT INTO {} (' + 
                           single_braces_string(len(fields) - 1) + 
                           ') VALUES (' + 
                           single_braces_quotes_string(len(fields) - 1) +')')

    sql_input_input_format = [table_name]
    sql_input_input_format += [sublist[0] for sublist in fields][1:]

    return CHTable(table_name, fields,
                   sql_create_table_input_str,
                   sql_create_table_input_format,
                   sql_input_input_str,
                   sql_input_input_format)

def create_table(config, table_object):
    '''Create a table in the database from a python table object'''
    mysql_config = ch_mysql.mysqlconfig_from_config(config)
    mysql_config['database'] = config['database_name']

    f_connection, f_cursor = ch_mysql.create_connection_cursor(mysql_config)
    f_cursor.execute(table_object.sql_create_table_str())
    f_connection.connection.commit()
    ch_mysql.destroy_connection_cursor(f_cursor, f_connection)


def populate_ch_table(config, ch_data_table):
    '''populate the companies house database table with data from the csv'''
    ch_csv_file = config['ch_table_source']

    mysql_config = ch_mysql.mysqlconfig_from_config(config)
    mysql_config['database'] = config['database_name']

    f_connection, f_cursor = ch_mysql.create_connection_cursor(mysql_config)

    with open(ch_csv_file, encoding="Latin-1") as fch:
        print('Start time: ' + datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        file_line = fch.readline()
        line_count = 1
        while file_line:
            if line_count > 1:
                #remove the first and last double quotes so the fields 
                #can be delimited by ","
                processed_line = file_line[1:-2]

                #turn the line in a list using "," delimiter
                processed_line = processed_line.strip().split('\",\"')

                #replace any remaining double quotes or single quotes with mysql 
                #compatible escaped characters
                for i, _ in enumerate(processed_line):
                    processed_line[i] = processed_line[i].replace('\\', "\\\\")
                    processed_line[i] = processed_line[i].replace('\"', "\\\"")
                    processed_line[i] = processed_line[i].replace('\'', "\'\'")
                
                query = ch_data_table.sql_insert_data_str(processed_line)
                f_cursor.execute(query)
            
            file_line = fch.readline()
            line_count += 1
            
            if (line_count % 100000) == 0:
                f_connection.connection.commit()
                print(str(line_count) + ' records added to the database, ' + 
                      datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    f_connection.connection.commit()
    ch_mysql.destroy_connection_cursor(f_cursor, f_connection)


def populate_pc_table(config, pc_data_table):
    '''populate the postcode table with data from the csv file'''
    pc_csv_file = config['pc_table_source']

    mysql_config = ch_mysql.mysqlconfig_from_config(config)
    mysql_config['database'] = config['database_name']

    f_connection, f_cursor = ch_mysql.create_connection_cursor(mysql_config)

    with open(pc_csv_file, encoding="Latin-1") as fpc:
        print('Start time: ' + datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        file_line = fpc.readline()
        
        line_count = 1
        while file_line:
            if line_count > 1:
                #we don't need the id so throw everything away before and including
                #the first comma
                processed_line = file_line.split(',', 1)[1]

                #turn the line in a list using "," delimiter
                processed_line = processed_line.strip().split(',')
                
                query = pc_data_table.sql_insert_data_str(processed_line)
                f_cursor.execute(query)
            
            file_line = fpc.readline()
            line_count += 1
            
            if (line_count % 100000) == 0:
                f_connection.connection.commit()
                print(str(line_count) + ' records added to the database, ' + 
                      datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    f_connection.connection.commit()
    ch_mysql.destroy_connection_cursor(f_cursor, f_connection)


def get_config_from_file():
    '''loads the program configuration from the config.xml file'''
    config_tree = ET.parse('config.xml')
    config_root = config_tree.getroot()

    config = {}
    config['mysql_user'] = config_root.find('MySQL').find('user').text
    config['mysql_password'] = config_root.find('MySQL').find('password').text
    config['mysql_host'] = config_root.find('MySQL').find('host').text
    config['database_name'] = config_root.find('Database').find('name').text
    config['ch_table_name'] = config_root.find('Database').find('ch_table').find('name').text
    config['ch_table_source'] = config_root.find('Database').find('ch_table') \
                                .find('source_csv').text
    config['pc_table_name'] = config_root.find('Database').find('pc_table').find('name').text
    config['pc_table_source'] = config_root.find('Database').find('pc_table') \
                                .find('source_csv').text

    return config
