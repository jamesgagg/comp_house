import csv
from datetime import datetime
import xml.etree.ElementTree as ET



PROGRESS_STEP_ROWS = 100000



def double_braces_string(no_of_instances):
    return '{} {}, ' * no_of_instances


def single_braces_string(no_of_instances):
    return ('{}, ' * (no_of_instances - 1)) + '{}'


def single_braces_quotes_string(no_of_instances):
    return ('\"{}\", ' * (no_of_instances - 1)) + '\"{}\"'


def mysql_table_creation_string(table_name, headers):
    curly_braces_for_non_id_headers = double_braces_string(len(headers) - 1)

    sql_create_table_format = ''.join(['CREATE TABLE {} ',
                                       '({} {} AUTO_INCREMENT, ',
                                       curly_braces_for_non_id_headers,
                                       'PRIMARY KEY ({}))'])

    sql_create_table_values = [table_name]
    sql_create_table_values += [item for sublist in headers for item in sublist]
    sql_create_table_values += [headers[0][0]]

    table_creation_string = sql_create_table_format.format(*sql_create_table_values)

    return table_creation_string


def mysql_insert_record_format_string(headers):
    braces_for_column_names = single_braces_string(len(headers) - 1)
    braces_and_quotes_for_values = single_braces_quotes_string(len(headers) - 1)

    sql_insert_str_format = ''.join(['INSERT INTO {} (',
                                     braces_for_column_names,
                                     ') VALUES (',
                                     braces_and_quotes_for_values,
                                     ')'])
    return sql_insert_str_format


def make_strings_mysql_compatible(list_of_strings):

    for i in range(len(list_of_strings)):
        # the line directly below must come before the other replacements to avoid their
        # resultant escape characters being erroneously replaced
        list_of_strings[i] = list_of_strings[i].replace('\\', '\\\\')

        list_of_strings[i] = list_of_strings[i].replace('\'', '\\\'')
        list_of_strings[i] = list_of_strings[i].replace('"', '\\\"')
        list_of_strings[i] = list_of_strings[i].replace('%', '\\%')
        list_of_strings[i] = list_of_strings[i].replace('_', '\\_')

    return list_of_strings


def config_from_xml_file(config_file):
    config_tree = ET.parse(config_file)
    config_root = config_tree.getroot()

    config = {}
    config['mysql_user'] = config_root.find('MySQL').find('user').text
    config['mysql_password'] = config_root.find('MySQL').find('password').text
    config['mysql_host'] = config_root.find('MySQL').find('host').text
    config['database_name'] = config_root.find('Database').find('name').text

    config['tables'] = {}
    tables = config_root.find('Database').find('Tables')
    for table in tables:
        source_csv = table.find('source_csv').text
        headers_xml = table.find('headers_xml').text

        ignore_first_column = table.find('ignore_first_column').text
        if ignore_first_column.lower() == 'true':
            ignore_first_column = True
        elif ignore_first_column.lower() == 'false':
            ignore_first_column = False
        else:
            ignore_first_column = False

        table_tag = table.tag
        config['tables'][table_tag] = {'source_csv': source_csv,
                                       'headers_xml': headers_xml,
                                       'ignore_first_column': ignore_first_column}

    config['mysql_config'] = {'user': config['mysql_user'],
                              'database': config['database_name'],
                              'password': config['mysql_password'],
                              'host': config['mysql_host']}

    return config


def headers_from_xml_file(xml_file):
    xml_tree = ET.parse(xml_file)
    xml_root = xml_tree.getroot()

    id_header_name = xml_root.find('idfield').find('field').find('name').text
    id_header_type = xml_root.find('idfield').find('field').find('type').text

    headers = [[id_header_name, id_header_type]]

    non_id_headers = xml_root.find('other_fields').findall('field')

    for non_id_header in non_id_headers:
        header_name = non_id_header.find('name').text
        header_type = non_id_header.find('type').text

        headers.append([header_name, header_type])

    return headers


def create_mysql_table(config, table_name, database_connection, database_cursor):
    xml_file = config['tables'][table_name]['headers_xml']
    headers = headers_from_xml_file(xml_file)

    table_creation_string = mysql_table_creation_string(table_name, headers)

    database_cursor.execute(table_creation_string)
    database_connection.connection.commit()


def load_data_into_mysql_table(config, table_name, database_connection, database_cursor):
    filename = config['tables'][table_name]['source_csv']
    ignore_first_column = config['tables'][table_name]['ignore_first_column']

    xml_file = config['tables'][table_name]['headers_xml']
    headers = headers_from_xml_file(xml_file)

    sql_insert_str_format = mysql_insert_record_format_string(headers)

    sql_input_str_first_values = [table_name]
    sql_input_str_first_values += [sublist[0] for sublist in headers][1:]

    print(''.join(['Starting: ', datetime.now().strftime('%Y-%m-%d %H:%M:%S')]))
    with open(filename, encoding="Latin-1") as data_file:
        csv_reader = csv.reader(data_file)
        line_count = 0
        for row in csv_reader:
            if line_count > 0:
                mutable_row = row

                if ignore_first_column:
                    mutable_row = mutable_row[1:]

                mysql_compatible_values = make_strings_mysql_compatible(mutable_row)

                mysql_insert_string = sql_insert_str_format.format(
                    *sql_input_str_first_values + mysql_compatible_values)
                database_cursor.execute(mysql_insert_string)

                if (line_count % PROGRESS_STEP_ROWS) == 0:
                    database_connection.connection.commit()
                    print(''.join(['{:,}'.format(line_count),
                                   ' records added to the database @ ',
                                   datetime.now().strftime('%Y-%m-%d %H:%M:%S')]))

            line_count += 1

    database_connection.connection.commit()
    print(''.join(['Finished: ', datetime.now().strftime('%Y-%m-%d %H:%M:%S')]))
