# Companies House Data To MySQL Database

Python 3 code to create a MySQL database comprising UK company data. Two sources of data are imported to the database:
1. Free UK Companies House data as seen at https://beta.companieshouse.gov.uk/
2. Free post code vs GPS data from https://www.freemaptools.com  

## Why
* Searches are very limited using the https://beta.companieshouse.gov.uk/ site, e.g. you can't currently search by things like SIC codes
* The Companies House data doesn't contain any GPS data making it difficult to search by things like distance from a point 
* Importing the data above to MySQL addresses the issues above and allows much greater flexibility with querying the data.  

## Requirements
1. MySQL (https://dev.mysql.com/downloads/installer/)
2. Python 3 (https://www.python.org/downloads/)
3. Python mysql-connector-python module (https://dev.mysql.com/doc/connector-python/en/connector-python-installation-binary.html)
4. Basic knowledge of these packages.

## Instructions
1. Clone or download this git repository
2. Download both of the data files and unzip them:
   * http://download.companieshouse.gov.uk/en_output.html (select the 'BasicCompanyDataAsOneFile-\<date\>.zip' file)
   * https://www.freemaptools.com/download/full-postcodes/ukpostcodes.zip
3. In the repository config.xml file: 
   * Change the name of the database to be created, if required (by default it is 'companies_house'): To change the name change the text between the \<name\> tags in the parent \<Database\> section.
   * Add your MySQL username, password and host to the tags between the parent \<MySQL\> tags
   * Add the full path and filename for your unzipped 'BasicCompanyDataAsOneFile-\<date\>.csv between the \<source_csv\> tag in the parent \<ch_table\> section
   * Add the full path and filename for your unzipped 'ukpostcodes.csv between the \<source_csv\> tag in the parent \<pc_table\> section
4. Run the repository ch_main.py file. This will create the database and tables if they don't already exist. These will then be populated with the Companies House and FreeMapTools data. Its a lot of data so this can take a long time, e.g. over an hour.
5. Use Python/MySQL to query the data as required: ch_sql_queries_to_csv_example.py gives an example of querying the data and saving the results to a csv file.
