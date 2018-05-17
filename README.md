# pendo-api
Some tools for interacting with the Pendo API to get and store Weave usage data

## Description

### manual_update_mysql.py, auto_update_mysql.py
Insert data from Pendo into a MySQL database.

### pendo_csv.py
Writes data from Pendo to a collection of csv files.

### schema.sql
Use to create a MySQL database that is appropriately formatted to be used with `auto_` and `manual_update_mysql.py`, with the table and column names referenced in those files.
It also contains the foreign keys describing the relationships between the tables and triggers for updating the `shortaccountId` columns (which are included only because of an issue with an older version of the Weave software which resulted in some users' account IDs being formatted to not contain dashes in the Pendo usage records.)

## Getting Started

### Prerequisites
To get data from Pendo you will need a valid Pendo API key.
To use `auto_` and `manual_update_mysql.py`, you will also need to have MySQL installed.
These tools all use the Python Requests library and `auto_` and `manual_update_mysql.py` use the PyMySQL library.
(I recommend installing the package manager [Homebrew](https://brew.sh/) if you haven't already and then using Homebrew to install the latest version of Python.
You can find a walkthrough of this process [here](http://docs.python-guide.org/en/latest/starting/install3/osx/).)

To install MySQL using Homebrew:
```bash
brew install mysql
```

To install Requests and PyMySQL using pip3:
```bash
pip3 install requests
pip3 install pymysql
```

### Usage
No matter which of these tools you are using, you will need to edit `config.py` and add your Pendo API key.

#### Creating the Pendo database in MySQL (for `auto_` and `manual_update_mysql.py`)
If you are using `auto_` and/or `manual_update_mysql.py`, you will first need to create a MySQL database named **Pendo** that is structured appropriately.
You can easily do this using the included file `schema.sql`.

```bash
mysql -u USERNAME -p < schema.sql
```

Just replace `USERNAME` with your MySQL username, and remember that depending on where you have saved `schema.sql`, you may need to specify its full path.

#### Using `auto_` and `manual_update_mysql.py`
In order to write to the MySQL database, you will need to edit `config.py` to include your MySQL credentials.
(If you used `schema.sql`, you can set `database = "Pendo"`.
Also if you are running MySQL locally, then set `host = "localhost"`.)

If you are using `manual_update_mysql.py`, you will need to add the first date for which you would like to retrieve data and the number of days' worth of data that you would like to retrieve.

For `auto_update_mysql.py`, your Pendo MySQL database will need at least one record in the each `_events` table.
Then running `auto_update_mysql.py` will insert any new records created since the latest date recorded in that table.

Both `auto_update_mysql.py` and `manual_update_mysql.py` will first update the lists of pages, features, and guides, adding any that are not already in the database.
Then they will update the accounts and visitors tables, similarly adding any new records and updating any that have changed.
Finally they will update the various events tables for each date in the requested range.

#### Using `pendo_csv.py`
To use `pendo_csv.py`, you will need to add the first date for which you would like to retrieve data and the number of days' worth of data that you would like to retrieve.
Running `pendo_csv.py` will then create a collection of csv files containing the data for all dates in the requested range.