=======
Summary
=======

kylin_client is a api client for kylin.
It currently supports the versions from **2.6
to 3.6** (users of Python 2.4 and 2.5 may use
`2.1.3 <https://pypi.python.org/pypi?name=psutil&version=2.1.3&:action=files>`__ version).
`PyPy <http://pypy.org/>`__ is also known to work.


==============
Example usages
==============

QUERY
===

.. code-block:: python

    >>>from kylin_client.kylin_client import KylinClient as kyclient
    >>>client = kyclient(host='127.0.0.1:7070', user='ADMIN', password='KYLIN')
    >>>client.query('select * from kylin_test', project='kylin_test', limit=500)


