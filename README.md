# Companies House Data To MySQL Database

Python 3 code to create a MySQL database comprising UK company data. Two sources of data are imported to the database:
1. Free UK Companies House data
2. Free GPS and post code data from www.freemaptools.com  

## Requirements
1. MySQL (https://dev.mysql.com/downloads/installer/)
2. Python 3 (https://www.python.org/downloads/)

## Instructions
1. Download both of the data files and unzip them:
  * http://download.companieshouse.gov.uk/en_output.html (select the 'BasicCompanyDataAsOneFile-\<date\>.zip' file)
  * https://www.freemaptools.com/download/full-postcodes/ukpostcodes.zip
2. In the config.xml file: 
  * Add your MySQL username, password and host
  * Add the full path and filename for your unzipped 'BasicCompanyDataAsOneFile-<date>.csv to the 
