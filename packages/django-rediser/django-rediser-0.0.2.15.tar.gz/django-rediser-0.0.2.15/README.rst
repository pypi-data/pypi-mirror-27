Django-Rediser
==============

|build| |codacy| |pypi| |license|

*Index:* - `Introduction <#Chapter_1>`__ - `Installation <#Chapter_2>`__
- `Usage <#Chapter_3>`__ - `Examples <#Chapter_4>`__

Introduction
------------

Django-Rediser (Django Redis Helper) is a simple yet convenient wrapper
for redis package. It lets you use Redis DB without worrying about
connections and json encoding/decoding.

There's 2 classes right now:

-  RedisStorage: main wrapper class, that ensures you have a connection
   to Redis server when you send commands to it.
-  RedisJSON: RedisStorage descendant, implementing json
   encoding/decoding.

Installation
------------

To install Django-Rediser, simply:

::

      pip install django-rediser

Usage
-----

We'll add usage information soon.

Examples
--------

We'll add some examples soon.

.. |build| image:: https://travis-ci.org/lexycore/django-rediser.svg?branch=master
   :target: https://travis-ci.org/lexycore/django-rediser
.. |codacy| image:: https://api.codacy.com/project/badge/Grade/a39bba3f74ea4e1bae63e010d2ba812a
   :target: https://www.codacy.com/app/lexycore/django-rediser/dashboard
.. |pypi| image:: https://img.shields.io/pypi/v/django-rediser.svg
   :target: https://pypi.python.org/pypi/django-rediser
.. |license| image:: https://img.shields.io/pypi/l/django-rediser.svg
   :target: https://github.com/lexycore/django-rediser/blob/master/LICENSE
