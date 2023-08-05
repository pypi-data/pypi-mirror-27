SQL format module
=======

Project target create a simple module support 
dynamic inject variable to sql statement and
batch execute SQL statement

Table of contents
=================
  * [Installation](#installation)
  * [Term](#term)
    * [Procedure](#procedure)
    * [Buffer](#buffer)
  * [Usage](#usage)
    * [Stored on local file system](#stored-on-local-file-system)
    * [Stored on AWS S3](#stored-on-aws-s3)

Installation
============
```bash
virtualenv env3
source env3/bin/activate
```

Term
====
Procedure
---------
A file which is json array contain list of SQL statement to be execute

Buffer
------
A temp table used to save result of statement.


Usage
=====
Stored on local file system
-------------------------------------
```python
from sqlformat.models.SQLBatch import SQLBatch
from sqlformat.storage.LocalStorageStrategy import LocalStorageStrategy
from sqlformat.buffer.ResultBufferStrategy import ResultBufferStrategy

sql_batch = SQLBatch(LocalStorageStrategy(), ResultBufferStrategy())
sql_batch.result_persistence('/tmp/hello.txt')
sql_batch.add_procedure('./tests/fixture/procedure/sample.json', {
    "keyword": {
        "foo": "10",
        "bar": "20"
    }
})
statements = sql_batch.get_statements()
print(statements) #Statement contain {foo}, {bar} will replace to 10 & 20
```

Stored on AWS S3
--------------------------
```python
import boto3

from sqlformat.models.SQLBatch import SQLBatch
from sqlformat.storage.AWSStorageStrategy import AWSStorageStrategy
from sqlformat.buffer.ResultBufferStrategy import ResultBufferStrategy

s3_client = boto3.resource('s3')

sql_batch = SQLBatch(AWSStorageStrategy(s3_client), ResultBufferStrategy())
sql_batch.result_persistence('/tmp/hello.txt')
sql_batch.add_procedure('s3://dng-misc/procedure/sample.json', {
    "keyword": {
        "foo": "10",
        "bar": "20"
    }
})
statements = sql_batch.get_statements()
print(statements) #Statement contain {foo}, {bar} will replace to 10 & 20
```