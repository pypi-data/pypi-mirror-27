=======================
Django Request Position
=======================

Django app to add a "position" field to the request, using GeoIP or GPS data given in the request headers. Some
references about this:

* `A Uniform Resource Identifier for Geographic Locations ('geo' URI) <http://tools.ietf.org/rfc/rfc5870>`_.
* `HTTP Geolocation draft-thomson-geopriv-http-geolocation-00 <http://tools.ietf.org/html/draft-thomson-geopriv-http-geolocation-00>`_.


Quick start
-----------

**1** Install using pip::

    pip install django-belt

**2** Add "request_position" to your INSTALLED_APPS settings like this::

    INSTALLED_APPS += ('request_position',)


**3** Add the middleware::

    MIDDLEWARE += (
        'request_position.middleware.RequestPositionMiddleware',
    )


Settings
--------

* ``REQUEST_POSITION_REMOTE_ADDR_ATTR`` (default: "REMOTE_ADDR")
* ``REQUEST_POSITION_DEFAULT_IP`` (default: "127.0.0.1")
* ``REQUEST_POSITION_DEFAULT_POSITION`` (default: None)
* ``REQUEST_POSITION_DEFAULT_COUNTRY_CODE`` (default: None)
* ``REQUEST_POSITION_COOKIE_NAME`` (default: "_request_position")
* ``REQUEST_POSITION_GEO_HEADER`` (default: "HTTP_GEOLOCATION")
* ``REQUEST_POSITION_OVERRIDE_LATITUDE_PARAM`` (default "lat")
* ``REQUEST_POSITION_OVERRIDE_LONGITUDE_PARAM`` (default "lon")
* ``REQUEST_POSITION_OVERRIDE_COUNTRY_CODE_PARAM`` (default "cc")
* ``REQUEST_POSITION_USE_GIS_POINT`` (default False)




History
-------

1.0a9 (2017-12-04)
+++++++++++++++++

* Fixed error wile providing a IP that does not exists.

1.0a7 (2017-12-04)
+++++++++++++++++

* Added ``geoip2`` requirement.

1.0a6 (2017-12-04)
+++++++++++++++++

* Support for Django 2.0.

1.0a5 (2017-2-28)
+++++++++++++++++

* Fixed settings variables prefix.
* Fixed problem with default REQUEST_POSITION_DEFAULT_COUNTRY_CODE value.
* Added settings variables to README.

1.0a4 (2017-2-28)
+++++++++++++++++

* Fixed problem with missing REMOTE_ADDR_ATTR setting variable.

1.0a3 (2017-2-28)
+++++++++++++++++

* Fixed problem with missing header.


1.0a2 (2017-2-28)
+++++++++++++++++

* Fixed Django 1.10 compatibility with new middleware.

1.0a1 (2017-2-21)
+++++++++++++++++

* First release on PyPI.


