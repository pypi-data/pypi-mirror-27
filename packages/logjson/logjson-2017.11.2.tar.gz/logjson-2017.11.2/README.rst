.. image:: https://img.shields.io/badge/stdlib--only-yes-green.svg
    :target: https://img.shields.io/badge/stdlib--only-yes-green.svg

.. image:: https://travis-ci.org/cjrh/logjson.svg?branch=master
    :target: https://travis-ci.org/cjrh/logjson

.. image:: https://coveralls.io/repos/github/cjrh/logjson/badge.svg?branch=master
    :target: https://coveralls.io/github/cjrh/logjson?branch=master

.. image:: https://img.shields.io/pypi/pyversions/logjson.svg
    :target: https://pypi.python.org/pypi/logjson

.. image:: https://img.shields.io/github/tag/cjrh/logjson.svg
    :target: https://img.shields.io/github/tag/cjrh/logjson.svg

.. image:: https://img.shields.io/badge/install-pip%20install%20logjson-ff69b4.svg
    :target: https://img.shields.io/badge/install-pip%20install%20logjson-ff69b4.svg

.. image:: https://img.shields.io/pypi/v/logjson.svg
    :target: https://img.shields.io/pypi/v/logjson.svg

.. image:: https://img.shields.io/badge/calver-YYYY.MM.MINOR-22bfda.svg
    :target: http://calver.org/


logjson
======================

**Goal**: easily generate structured JSON logging.
`logstash <https://www.elastic.co/products/logstash>`_ mode is optional.

.. code-block:: python

    import logging
    import logjson
    logger = logging.getLogger('blah')
    logger.addHandler(logjson.JSONHandler())
    logger.info('hi %s %s!', 'you', 'there')

Output:

.. code-block:: json

    {
      "name": "blah",
      "msg": "hi %s %s!",
      "args": [
        "you",
        "there"
      ],
      "levelname": "INFO",
      "levelno": 20,
      "pathname": "<snip>",
      "filename": "test_main.py",
      "module": "test_main",
      "exc_text": null,
      "stack_info": null,
      "lineno": 17,
      "funcName": "test_main",
      "created": 1511750128.6285746,
      "msecs": 628.5746097564697,
      "relativeCreated": 23.08201789855957,
      "thread": 139929130264384,
      "threadName": "MainThread",
      "processName": "MainProcess",
      "process": 18460,
      "message": "hi you there!",
      "created_iso": "2017-11-27T02:35:28.628575+00:00"
    }

Logstash mode is a param away:

.. code-block:: python

    logger = logging.getLogger('ls')
    logger.addHandler(logjson.JSONHandler(logstash_mode=True))
    logger.info('logstash test')

Output:

.. code-block:: json

    {
      "@message": "logstash test",
      "@source_host": "localhost.localdomain",
      "@timestamp": "2017-11-27T02:35:28.631275+00:00",
      "@fields": {
        "name": "ls",
        "msg": "logstash test",
        "args": [],
        "levelname": "INFO",
        "levelno": 20,
        "pathname": "<snip>",
        "filename": "test_main.py",
        "module": "test_main",
        "exc_text": null,
        "stack_info": null,
        "lineno": 42,
        "funcName": "test_logstash",
        "created": 1511750128.631275,
        "msecs": 631.274938583374,
        "relativeCreated": 25.782346725463867,
        "thread": 139929130264384,
        "threadName": "MainThread",
        "processName": "MainProcess",
        "process": 18460
      }
    }
