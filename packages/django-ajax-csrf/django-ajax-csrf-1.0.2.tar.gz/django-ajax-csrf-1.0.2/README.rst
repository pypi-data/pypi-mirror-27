django-ajax-csrf
================

.. image:: https://img.shields.io/pypi/v/django-ajax-csrf.svg
   :target: https://pypi.python.org/pypi/django-ajax-csrf
.. image:: https://img.shields.io/pypi/pyversions/django-ajax-csrf.svg
   :target: https://pypi.python.org/pypi/django-ajax-csrf
.. image:: https://img.shields.io/pypi/format/django-ajax-csrf.svg
   :target: https://pypi.python.org/pypi/django-ajax-csrf
.. image:: https://img.shields.io/pypi/l/django-ajax-csrf.svg
   :target: https://pypi.python.org/pypi/django-ajax-csrf

* Requires jQuery javascript library

Installation
------------

.. code:: bash

    $ pip install django-ajax-csrf

.. code:: python

    INSTALLED_APPS += (
        'django_ajax',
    )

Usage::

    {% load csrf_tags %}
    {% include_ajax_csrf_token %}

Authour
-------

nnsnodnb

LICENSE
-------

Copyright (c) 2017 Yuya Oka Released under the MIT license (see `LICENSE <LICENSE>`__)
