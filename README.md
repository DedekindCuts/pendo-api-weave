# pendo-api
Some tools for interacting with the Pendo API

## Description

### update_mysql
Inserts data from Pendo into a MySQL database.

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
