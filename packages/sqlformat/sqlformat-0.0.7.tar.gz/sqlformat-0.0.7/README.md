SQL format module
=================

Project target create a simple module support 
dynamic inject variable to sql statement and
batch execute SQL statement

Table of contents
=================
  * [Installation](#installation)
  * [Development](#development)
  * [Testing](#testing)
  * [Term](#term)
    * [Procedure](#procedure)
    * [Buffer](#buffer)
  * [Usage](#usage)
    * [Stored on local file system](#stored-on-local-file-system)
    * [Stored on AWS S3](#stored-on-aws-s3)

Installation
============
```bash
pip3 install sqlformat
```

Development
===========
Project is using [pipenv](https://github.com/kennethreitz/pipenv) to manage dependency

So in order to get started, install pipenv first.
```bash
pip3 install pipenv
# Or if you are mac user
brew install pipenv
``` 

After install pipenv, you can setup this repo by following command
```bash
pipenv --three install
```

Testing
=======
Following command will execute all test and shown the code coverage report
```bash
pipenv shell
py.test --cov=sqlformat
```

Term
====
Procedure
---------
A json array contain list file that contain sql statement to be execute

Example: [Sample procedure](tests/fixture/procedure/sample.json)

Statement variable
------
A place holder to used for inject value on run-time, it using [Standard python string format](https://docs.python.org/3.6/library/string.html#format-specification-mini-language). 
So any feature supported by `"".format()` will worked on statement variable

Example: [Sample statement with variable](tests/fixture/sql/hello01.sql)

Usage
=====
Stored on local file system
-------------------------------------
```python
from sqlformat import SQLBatch
from sqlformat import LocalStorageStrategy
from sqlformat import ResultBufferStrategy

sql_batch = SQLBatch(LocalStorageStrategy(), ResultBufferStrategy())
sql_batch.result_persistence('/tmp/hello.txt')
sql_batch.add_procedure('./tests/fixture/procedure/sample.json', {
    "keyword": {
        "foo": "10",
        "bar": "20"
    }
})
statements = sql_batch.get_statements() # Will contain both hello01 & hello02.sql
print(statements) #Statement contain {foo}, {bar} will replace to 10 & 20
```

Stored on AWS S3
--------------------------
```python
import boto3

from sqlformat import SQLBatch
from sqlformat import AWSStorageStrategy
from sqlformat import ResultBufferStrategy

s3_client = boto3.resource('s3')

sql_batch = SQLBatch(AWSStorageStrategy(s3_client), ResultBufferStrategy())
sql_batch.result_persistence('/tmp/hello.txt')
sql_batch.add_procedure('s3://dng-misc/procedure/sample.json', {
    "keyword": {
        "foo": "10",
        "bar": "20"
    }
})
statements = sql_batch.get_statements() # Will contain both hello01 & hello02.sql
print(statements) #Statement contain {foo}, {bar} will replace to 10 & 20
```