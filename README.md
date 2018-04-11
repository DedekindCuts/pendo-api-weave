# pendo-api
Some tools for interacting with the Pendo API

## Description

### manual_update_mysql, auto_update_mysql
Inserts data from Pendo into a MySQL database.

### pendo_csv
Writes data from Pendo to a collection of csv files.

## Getting Started

### Prerequisites
To get data from Pendo you will need a valid Pendo API key.
These tools all use the Python Requests library and `update_mysql.py` uses the PyMySQL library.

```bash
pip3 install requests 
pip3 install pymysql
```

### Usage
For each of these, you will only need to edit `config.py` to suit your needs.
You will need to add your Pendo API key, and for `pendo_csv.py` and `manual_update_mysql.py` you will need to add the first date for which you would like to retrieve data and the number of days' worth of data that you would like to retrieve.
For `auto_update_mysql.py`, you will need an existing MySQL database with at least one record in the `page_events` table.
Then `auto_update_mysql.py` will insert any new records created since the latest date recorded in that table.
Both `auto_update_mysql.py` and `manual_update_mysql.py` will first update the lists of pages, features, and guides, adding any that are not already in the database.
Then they will update the accounts and visitors tables, similarly adding any new records and updating any that have changed.
Finally they will update the various events tables for each date in the requested range.