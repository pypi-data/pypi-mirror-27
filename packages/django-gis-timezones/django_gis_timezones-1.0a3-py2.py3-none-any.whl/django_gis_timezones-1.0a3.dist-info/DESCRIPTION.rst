====================
Django Gis Timezones
====================

Simple model to save timezones using geo-spatial data.

Quick start
-----------

**1** Install using pip::

    $ pip install django-gis-timezones

**2** Add "gum" to your INSTALLED_APPS settings like this::

    INSTALLED_APPS += ('gis_timezones',)

**3** Download and create models::

    $ ./manage.py import_timezones





History
-------

1.0a3 (2017-12-04)
+++++++++++++++++

* Support for Django 2.0

1.0a2 (2017-3-09)
+++++++++++++++++

* Fixed order in Point.

1.0a1 (2017-2-20)
+++++++++++++++++

* First release on PyPI.


