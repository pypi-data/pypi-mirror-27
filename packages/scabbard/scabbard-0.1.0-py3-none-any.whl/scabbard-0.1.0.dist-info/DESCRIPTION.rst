.. image:: https://img.shields.io/badge/pypi--blue.svg
    :target: https://pypi.python.org/pypi/bravado/
    :alt: PyPi version

.. image:: https://img.shields.io/badge/python-3.6-blue.svg
    :target: https://???/scabbard/
    :alt: Supported Python versions

Scabbard
==========

About
-----

Scabbard is a Pythonic client for the Sabre Dev Studio REST APIs.  With Scabbard, it
is not necessary to create extensive low-level boilerplate code before you can use each API call.
You can begin to make real REST calls to the Sabre Dev Studio APIs with only 3 lines of code (including the import).

A scabbard is a sheath for holding a sword, such as a sabre :)

https://en.wikipedia.org/wiki/Scabbard

Sabre Dev Studio REST API documentation:

https://developer.sabre.com/docs/read/rest_apis/

https://developer.sabre.com/io-docs

Scabbard docs:
https://bundgus.github.io/scabbard/

GitHub Home:
https://github.com/bundgus/scabbard


Example Usage
-------------

A file called api_connect_parameters.json must exist in the directory
in which python is run, with your Sabre Dev Studio clientID and clientSecret credentials.

You can register for a free Sabre Dev Studio account at the following URL:
https://developer.sabre.com/apps/mykeys


.. code-block:: javascript

    {
      "clientId": "zzzzzzzzzzzzzzzz",
      "clientSecret": "xxxxxxxx",
      "environment": "https://api.test.sabre.com",
      "group": "DEVCENTER",
      "domain": "EXT",
      "formatVersion": "V1"
    }


.. code-block:: Python

    from scabbard import get_client

    client = get_client()
    countries = client.Air_Utility.V1ListsSupportedCountriesGet(pointofsalecountry='NZ').result()

    print('PointOfSale')
    print(countries.PointOfSale)

    print('OriginCountries')
    for c in countries.OriginCountries:
        print(c.CountryCode, c.CountryName)

    print('DestinationCountries')
    for c in countries.DestinationCountries:
        print(c.CountryCode, c.CountryName)

    print('Links')
    for l in countries.Links:
        print(l.rel)
        print(l.href)


Installation
------------

.. code-block:: bash

    $ pip install scabbard

License
-------

Copyright (c) 2018, Mark Bundgus. All rights reserved.

Scabbard is licensed with a `BSD 3-Clause
License <http://opensource.org/licenses/BSD-3-Clause>`__.


