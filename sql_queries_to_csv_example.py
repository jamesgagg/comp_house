import csv
from pathlib import Path

import database
import tables
import create



COMPANIES_HOUSE_TABLE = 'companies'
SIC_CODE_ENTRIES_PER_DATABASE_RECORD = 4
OUTPUT_FILE_PATH = Path(__name__).parent



def sql_query_to_csv(config, query, database_cursor, csv_output_file):
    '''process an SQL query and save the results as a csv file'''
    database_cursor.execute(query)
    database_records = database_cursor.cursor.fetchall()

    company_table_headers = config['tables'][COMPANIES_HOUSE_TABLE]['headers_xml']
    headers = tables.headers_from_xml_file(company_table_headers)
    headers = [header[0] for header in headers]

    with open((csv_output_file), 'wt', newline='', encoding='Latin-1') as output_file:
        csv_writer = csv.writer(output_file)

        csv_writer.writerow(headers)

        for database_record in database_records:
            csv_writer.writerow(database_record)


def create_sql_like_from_sic_codes(sic_code_list):
    '''create mysql 'like' string for supplied sic code list'''
    output_string = []
    for sic_code in sic_code_list:
        sic_string = []
        for i in range(1, SIC_CODE_ENTRIES_PER_DATABASE_RECORD + 1):
            string_to_append = ''.join(['SICCode_SicText_', str(i), ' LIKE \'', sic_code, '%\''])
            sic_string.append(string_to_append)

        sic_string = ' OR '.join(sic_string)

        output_string.append(sic_string)

    output_string = ''.join(['(', ' OR '.join(output_string), ')'])

    return output_string


def create_sql_like_from_incomplete_postcode(postcode_list):
    '''create mysql 'like' string for supplied postcode list'''
    output_string = []
    for postcode in postcode_list:
        output_string.append(''.join(['RegAddress_PostCode LIKE \'', postcode, '%\'']))

    output_string = ''.join(['(', ' OR '.join(output_string), ')'])

    return output_string


def query_001(config, database_cursor):
    '''Postcodes within 3 miles of LE16, active companies, specified SICs'''
    filename = '3Miles_Active.csv'
    postcode_list = ['LE16', 'LE17', 'LE8', 'LE94', 'NN14', 'NN6']
    sic_list = ['58290', '62011', '62012', '62020', '62090', '63110', '63990']

    query = ('SELECT * FROM companies ' +
             'WHERE ' +
             'Accounts_AccountCategory <> \'DORMANT\' AND ' +
             create_sql_like_from_incomplete_postcode(postcode_list) + ' AND ' +
             'CompanyStatus = \'Active\' AND ' +
             create_sql_like_from_sic_codes(sic_list))

    output_file = str(OUTPUT_FILE_PATH / filename)

    sql_query_to_csv(config, query, database_cursor, output_file)


def query_002(config, database_cursor):
    '''Postcodes within 20 miles of LE16, active companies, specified SICs'''
    filename = '20Miles_Active.csv'
    postcode_list = ['CV11', 'CV12', 'CV2', 'CV21', 'CV22', 'CV23', 'CV7', 'CV8',
                     'LE1', 'LE10', 'LE12', 'LE13', 'LE14', 'LE15', 'LE16', 'LE17',
                     'LE18', 'LE19', 'LE2', 'LE21', 'LE3', 'LE4', 'LE41', 'LE5',
                     'LE55', 'LE6', 'LE67', 'LE7', 'LE8', 'LE87', 'LE9', 'LE94',
                     'LE95', 'NN1', 'NN10', 'NN11', 'NN12', 'NN14', 'NN15', 'NN16',
                     'NN17', 'NN18', 'NN2', 'NN29', 'NN3', 'NN4', 'NN5', 'NN6',
                     'NN7', 'NN8', 'NN9', 'NN99', 'PE8', 'PE9']
    sic_list = ['62012', '62020']
    query = ('SELECT * FROM companies ' +
             'WHERE ' +
             'Accounts_AccountCategory <> \'DORMANT\' AND ' +
             create_sql_like_from_incomplete_postcode(postcode_list) + ' AND ' +
             'CompanyStatus = \'Active\' AND ' +
             create_sql_like_from_sic_codes(sic_list))

    output_file = str(OUTPUT_FILE_PATH / filename)

    sql_query_to_csv(config, query, database_cursor, output_file)


def main():
    '''entry point of the code'''
    config = tables.config_from_xml_file(create.CONFIG_FILE)

    database_connection = database.create_database_connection(config['mysql_config'])
    database_cursor = database.create_database_cursor(database_connection)

    query_001(config, database_cursor)
    query_002(config, database_cursor)



if __name__ == '__main__':
    main()
