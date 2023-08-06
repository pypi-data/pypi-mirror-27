Mock for the redis-py client library
====================================

| Supports writing tests for code using the
  `redis-py <https://github.com/andymccurdy/redis-py>`__ library
| without requiring a `redis-server <http://redis.io>`__ install.

|Build Status|

Installation
------------

Use pip:

::

    pip install mockredispy

Usage
-----

| Both ``mockredis.mock_redis_client`` and
  ``mockredis.mock_strict_redis_client`` can be
| used to patch instances of the *redis client*.

For example, using the
`mock <http://www.voidspace.org.uk/python/mock/>`__ library:

::

    @patch('redis.Redis', mock_redis_client)

Or:

::

    @patch('redis.StrictRedis', mock_strict_redis_client)

Testing
-------

| Many unit tests exist to verify correctness of mock functionality. In
  addition, most
| unit tests support testing against an actual redis-server instance to
  verify the tests
| against ground truth. See ``mockredis.tests.fixtures`` for more
  details and disclaimers.

Supported python versions
-------------------------

-  Python 2.7
-  Python 3.2
-  Python 3.3
-  Python 3.4
-  PyPy
-  PyPy3

Attribution
-----------

This code is shamelessly derived from work by `John
DeRosa <http://seeknuance.com/2012/02/18/replacing-redis-with-a-python-mock/>`__.

.. |Build Status| image:: https://travis-ci.org/locationlabs/mockredis.png
   :target: https://travis-ci.org/locationlabs/mockredis
