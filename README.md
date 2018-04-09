# pendo-api
Some tools for interacting with the Pendo API

## Description

### update_mysql
Inserts data from Pendo into a MySQL database.

### pendo_csv
Writes data from Pendo to a collection of csv files.

### pages, guides, features
`pages.py` retrieves the names and IDs of all pages that are tracked on Pendo and writes them to a csv file.
`guides.py` and `features.py` are similar.

## Getting Started

### Prerequisites
To get data from Pendo you will need a valid Pendo API key.
These tools all use the Python Requests library and `update_mysql.py` uses the PyMySQL library.

```bash
pip3 install requests 
pip3 install pymysql
```

### Usage
To use `pages.py`, `guides.py`, `features.py`, and `pendo_csv.py`, you will only need to edit `config.py` to suit your needs.
In each of these cases, you will need to add your Pendo API key, and for `pendo_csv.py` you will need to add the first date for which you would like to retrieve data and the number of days' worth of data that you would like to retrieve.