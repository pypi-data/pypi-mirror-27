Compander
=========

Simple context manager to wrap compression and uncompression of gzip and bzip2 files.

Example
-------

```
from compander import Compander

with Compander() as c:  # Default is bz2
    c.compress('uncompressed_file','compressed_file.bz2')

with Compander('bz2') as c:
    c.uncompress('compressed_file.bz2','uncompressed_file')

with Compander('gz') as c:
    c.compress('uncompressed_file','compressed_file.gz')

with Compander('gz') as c:
    c.uncompress('compressed_file.gz','uncompressed_file')
```

Testing
-------

* python setup.py test

Installation
------------

* python setup.py install

Development
-----------

* pip install -r requirements.txt
* python setup.py test
* python setup.py develop
