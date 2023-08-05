Generic storage module
=================

Project target create a simple module that can get file out of project.

For example , here is scenario. 

You are using some Google API in your project such as [Sheet API](#https://developers.google.com/sheets/api/)
and choice the [ServiceAccount](#https://developers.google.com/identity/protocols/OAuth2ServiceAccount) as authentication method

So you will got the JSON file which contain private-key , service-account email ...etc.
This file you don't want any other people known coz it contain sensitive information.

Moreover, you want build your project as a dockerized open-source project 
so that anyone can reproduce your application in own server.

So how would you deal with this JSON file ? Extract it to external storage 
and then let user input the external path as enviroment variable of your docker image 
is a grant idea

But how did you achieve the goal ? Most of external cloud storage need your code have some change accordingly .
For example, AWS S3 will need integrate `boto3` and Google cloud storage will need `google-cloud-storage` ...etc.

Then you project must have dependency to the external storage service. 
If you want to change the external storage service provider, you must have code change.

This is totally bad idea coz it has violate the **Open closed principle** .
You project did't open to change behaviour and close to code change.

This module is aim to provide the solution.
if user want use google-cloud-storage then he using environment like this
```bash
SECRET_STORAGE_STRATEGY=GCP
SECRET_CONFIG_FILE=gs://my-bucket/secret.txt
```

if user want use AWS S3 then he using environment like this
```bash
SECRET_STORAGE_STRATEGY=S3
SECRET_CONFIG_FILE=s3://my-bucket/secret.txt
```

In your project. You can just type
```python
import os
import generic_storage
storage_instance = generic_storage.get_storage(os.environ.get('SECRET_STORAGE_STRATEGY'))
secret_content = generic_storage.read(os.environ.get('SECRET_CONFIG_FILE'))
```   

Table of contents
=================
  * [Installation](#installation)
  * [Development](#development)
  * [Testing](#testing)
  * [Usage](#usage)
    * [Stored on local file system](#stored-on-local-file-system)
    * [Stored on AWS S3](#stored-on-aws-s3)

Installation
============
```bash
pip install secret_storage 
```

Development
============
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
py.test --cov=secret_storage
```

Usage
=====
Currently , `get_storage` function only accept 'Local' and 'S3'.  

Using local storage
-------------------------------------
```python
import generic_storage
storage_instance = generic_storage.get_storage('Local')
secret_content = generic_storage.read('./tests/fixtures/.env')
```

Using AWS S3
--------------------------
```python
import generic_storage
storage_instance = generic_storage.get_storage('S3')
secret_content = generic_storage.read('s3://your-bucket/your-key')
```
