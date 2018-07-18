# seeddms

Python library to access the SeedDMS REST API. Written against version 5.1.8.

Install
-------

```
virtualenv venv
source venv/bin/activate
pip install git+https://github.com/jvzantvoort/seeddms.git
```

Example use
-----------

Configuration file: `~/.seeddms-cli.conf` 

Example content:

```ini

[main]
baseurl = http://localhost/seeddms/restapi/index.php
username = admin
password = admin
targetfolder = DMS
```

Example code:

```python

import seeddms

config = seeddms.Config()

sdms = seeddms.SeedDMS(baseurl = config.baseurl,
                       username = config.username,
                       password = config.password,
                       targetfolder = config.targetfolder)
sdms.do_login()

for row in sdms.get_categories():
    print row.get('name')

```

Testing
-------

For testing I use a forked and updates (docker-seeddms
image)[https://github.com/jvzantvoort/docker-seeddms] That provides
the imterface to which the functions connect.
