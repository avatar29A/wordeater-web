# WordEater RestFull API server

WordEater it's project what need to help you learn new foreign words 

# Requirements

- python 2.7 (https://www.python.org/downloads/)
- pip 
- MongoDB (https://www.mongodb.org/)
- Memcached (http://memcached.org/)

# Installation

- Clone project

```sh
git clone https://github.com/h-qub/wordeater-web/
```

- Install all requirements for python
```
pip install -r requirements
```
- Next, you can create new file with name 'settings.ini' and copy to all strings from settings.default.ini. And put it into **we-web** folder.

**For example settings.ini**
```ini
[DATABASE]
host=127.0.0.1
port=27017
db_name=we_db

[MEMCACHED]
host=127.0.0.1
port=11211

[LOGGER]
directory=C:\temp\wordeater\we.log

[APPLICATION]
cards_in_group_amount=10
version=0.1.0
session_expires=5184000
is_debug=0
```

# Run

- For what run application you need invoke next command:

```
$ python run.py
```

- If all is ok, you can see:

```
* Running on http://127.0.0.1:5050/ (Press CTRL+C to quit) 
```

- For test API open url:

```
http://127.0.0.1:5050/api/
```

# Test

Application contains functional tests. You may looking for they into tests folder.

All test you may run with help **nose test runner** (http://nose.readthedocs.org/).
