'''example queries for the database'''

import csv
import ch_mysql
import ch_tables


def query_to_csv(query, cursor, results_path, filename):
    '''process an SQL query and save the results as a csv file'''
    cursor.execute(query)
    mysql_list = cursor.cursor.fetchall()

    fields = ch_tables.fields_from_ch_xml_header_file('ch_table_headers.xml')
    fields = [field[0] for field in fields]

    with open((results_path + filename), 'w', newline='', encoding='Latin-1') as out:
        csv_out = csv.writer(out)
        csv_out.writerow(fields)
        for result in mysql_list:
            csv_out.writerow(result)


def sic_like(code_list):
    '''create mysql 'like' string for supplied sic code list'''
    out_string = []
    for code in code_list:
        temp_string = [
            'SICCode_SicText_' + str(i) + ' LIKE \'' + code + '%\''
            for i in range(1, 5)
        ]

        temp_string = ' OR '.join(temp_string)
        out_string.append(temp_string)
    out_string = '(' + ' OR '.join(out_string) + ')'
    return out_string


def postcodes_like(postcode_list):
    '''create mysql 'like' string for supplied postcode list'''
    out_string = [
        'RegAddress_PostCode LIKE \'' + postcode + '%\''
        for postcode in postcode_list
    ]

    out_string = '(' + ' OR '.join(out_string) + ')'
    return out_string    


def query_001(results_path, cursor):
    '''Postcodes within 3 miles of LE16, active companies'''
    filename = '3Miles_Active.csv'
    postcode_list = ['LE16', 'LE17', 'LE8', 'LE94', 'NN14', 'NN6']
    sic_list = ['58290', '62011', '62012', '62020', '62090', '63110', '63990']

    query = ('SELECT * FROM ch_data ' +
             'WHERE ' +
             'Accounts_AccountCategory <> \'DORMANT\' AND ' +
             postcodes_like(postcode_list) + ' AND ' + 
             'CompanyStatus = \'Active\' AND ' +  
             sic_like(sic_list))
    query_to_csv(query, cursor, results_path, filename)


def query_002(results_path, cursor):
    '''Postcodes within 20 miles of LE16, active companies'''
    filename = '20Miles_Active.csv'
    postcode_list = ['CV11', 'CV12', 'CV2', 'CV21', 'CV22', 'CV23', 'CV7', 'CV8', 
                     'LE1', 'LE10', 'LE12', 'LE13', 'LE14', 'LE15', 'LE16', 'LE17', 
                     'LE18', 'LE19', 'LE2', 'LE21', 'LE3', 'LE4', 'LE41', 'LE5', 
                     'LE55', 'LE6', 'LE67', 'LE7', 'LE8', 'LE87', 'LE9', 'LE94', 
                     'LE95', 'NN1', 'NN10', 'NN11', 'NN12', 'NN14', 'NN15', 'NN16', 
                     'NN17', 'NN18', 'NN2', 'NN29', 'NN3', 'NN4', 'NN5', 'NN6', 
                     'NN7', 'NN8', 'NN9', 'NN99', 'PE8', 'PE9']
    sic_list = ['62012', '62020']
    query = ('SELECT * FROM ch_data ' +
             'WHERE ' +
             'Accounts_AccountCategory <> \'DORMANT\' AND ' +
             postcodes_like(postcode_list) + ' AND ' + 
             'CompanyStatus = \'Active\' AND ' +  
             sic_like(sic_list))
    query_to_csv(query, cursor, results_path, filename)


def main_program():
    '''entry point of the code'''
    ch_config = ch_tables.get_config_from_file()
    mysql_config = ch_mysql.mysqlconfig_from_config(ch_config)
    mysql_config['database'] = ch_config['database_name']
    _, cursor = ch_mysql.create_connection_cursor(mysql_config)

    results_path = ('')

    query_001(results_path, cursor)
    query_002(results_path, cursor)


if __name__ == '__main__':
    main_program()
