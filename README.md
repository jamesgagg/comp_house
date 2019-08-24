# Companies House Data To MySQL Database

Python 3 code to create a MySQL database comprising UK company data. Two sources of data are imported to the database:
1. Free UK Companies House data from www.companieshouse.gov.uk
2. Free GPS and post code data from www.freemaptools.com  

## Requirements
1. MySQL (https://dev.mysql.com/downloads/installer/)
2. Python 3 (https://www.python.org/downloads/)

## Instructions
1. Clone or download this git repository
2. Download both of the data files and unzip them:
  * http://download.companieshouse.gov.uk/en_output.html (select the 'BasicCompanyDataAsOneFile-\<date\>.zip' file)
  * https://www.freemaptools.com/download/full-postcodes/ukpostcodes.zip
3. In the config.xml file from this repository: 
  * By default the name of the MySQL database to be created is 'companies_house'. This can be changed by inserting another name between the \<name\> tags in the parent \<Database\> section.
  * Add your MySQL username, password and host to the tags between the parent \<MySQL\> tags
  * Add the full path and filename for your unzipped 'BasicCompanyDataAsOneFile-\<date\>.csv between the \<source_csv\> tag in the parent \<ch_table\> section
  * Add the full path and filename for your unzipped 'ukpostcodes.csv between the \<source_csv\> tag in the parent \<pc_table\> section
4. Run the ch_main.py file from this repository. This will create the database and tables if they don't already exist. These will then be populated with the Companies House and FreeMapTools data. Its a lot of data so this can take a long time, i.e. over an hour.
