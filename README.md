# Companies House Data To MySQL Database

Python 3 code to create a MySQL database comprising UK company data. Two sources of data are imported to the database:
1. Free UK Companies House data from https://www.gov.uk/government/organisations/companies-house
2. Free post code vs GPS data from https://www.freemaptools.com

## Why
* Searches are very limited using the https://find-and-update.company-information.service.gov.uk/ site, e.g. you can't
currently search by things like outward postcodes, SIC codes, etc.
* The Companies House data doesn't contain any GPS data making it difficult to search by things like distance from a point.
* Importing the data above to MySQL gives a starting point for addressing the issues above and allows much greater flexibility
with querying the data.

## Requirements
1. MySQL (https://dev.mysql.com/downloads/installer/)
2. Python 3 (https://www.python.org/downloads/)
3. Python mysql-connector-python module (https://dev.mysql.com/doc/connector-python/en/connector-python-installation-binary.html)
4. Basic knowledge of these packages.

## Instructions
1. Clone or download this git repository.
2. Download both of the data files and unzip them:
   * http://download.companieshouse.gov.uk/en_output.html (select the 'BasicCompanyDataAsOneFile-\<date\>.zip' file)
   * https://www.freemaptools.com/download/full-postcodes/ukpostcodes.zip
3. In the repository config.xml file:
   * If required, change the name of the database to be created (by default it is 'companies_house'): To change the name change the text between the \<name\> tags in the parent \<Database\> section.
   * Add your MySQL username, password and host to the tags between the parent \<MySQL\> tags
   * Add the full path and filename for your unzipped 'BasicCompanyDataAsOneFile-\<date\>.csv between the \<source_csv\> tags in the parent \<companies\> section
   * Add the full path and filename for your unzipped 'ukpostcodes.csv between the \<source_csv\> tags in the parent \<postcodes\> section
4. Run the repository create.py file. This will create the database and tables if they don't already exist. These will then be populated with the Companies House and FreeMapTools data. Its a lot of data so this can take a long time, e.g. an hour or more.
5. Use Python/MySQL to query the data as required: sql_queries_to_csv_example.py gives an example of querying the data and saving the results to csv files.
