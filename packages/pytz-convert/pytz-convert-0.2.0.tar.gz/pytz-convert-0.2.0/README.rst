.. -*- mode: rst -*-

pytz-convert
------------

Python extension for package `pytz <https://pypi.python.org/pypi/pytz>`_.


Badges
------

.. start-badges

.. list-table::
    :stub-columns: 1

    * - info
      - |license| |hits| |contributors|
    * - tests
      - |travis| |coveralls|
    * - package
      - |version| |supported-versions| |requires|

.. |docs| image:: https://readthedocs.org/projects/pytz-convert/badge/?style=flat
    :alt: Documentation Status
    :target: https://readthedocs.org/projects/pytz-convert

.. |hits| image:: http://hits.dwyl.io/TuneLab/pytz-convert.svg
    :alt: Hit Count
    :target: http://hits.dwyl.io/TuneLab/pytz-convert

.. |contributors| image:: https://img.shields.io/github/contributors/TuneLab/pytz-convert.svg
    :alt: Contributors
    :target: https://github.com/TuneLab/pytz-convert/graphs/contributors

.. |license| image:: https://img.shields.io/badge/License-MIT-yellow.svg
    :alt: License Status
    :target: https://opensource.org/licenses/MIT

.. |travis| image:: https://travis-ci.org/TuneLab/pytz-convert.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/TuneLab/pytz-convert

.. |coveralls| image:: https://coveralls.io/repos/TuneLab/pytz-convert/badge.svg?branch=master&service=github
    :alt: Code Coverage Status
    :target: https://coveralls.io/r/TuneLab/pytz-convert

.. |requires| image:: https://requires.io/github/TuneLab/pytz-convert/requirements.svg?branch=master
    :alt: Requirements Status
    :target: https://requires.io/github/TuneLab/pytz-convert/requirements/?branch=master

.. |version| image:: https://img.shields.io/pypi/v/pytz-convert.svg?style=flat
    :alt: PyPI Package latest release
    :target: https://pypi.python.org/pypi/pytz-convert

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/pytz-convert.svg?style=flat
    :alt: Supported versions
    :target: https://pypi.python.org/pypi/pytz-convert

.. end-badges


Install
-------

.. code-block:: bash

    pip install pytz-convert


Architecture
------------

``pytz-convert`` is an extension of the `pytz <https://pypi.python.org/pypi/pytz>`_ providing functions for converting timezone names, abbreviations, and offsets.


Functions
---------

- ``convert_bing_ads_tz``: Convert **Bing timezone name** to **Standard timezone name**.
- ``convert_tz_abbrev_to_tz_hours()``: Convert **timezone abbreviation** to **timezone hours**.
- ``convert_tz_abbrev_to_tz_offset()``: Convert **timezone abbreviation** to **timezone offset**.
- ``convert_tz_abbrev_to_tz_seconds()``: Convert **timezone abbreviation** to **timezone seconds**.
- ``convert_tz_hours_to_tz_offset()``: Convert **timezone hours** into **timezone offset**.
- ``convert_tz_name_to_date_tz_abbrev()``: Convert **timezone name + date** to **timezone abbreviation**.
- ``convert_tz_name_to_date_tz_offset()``: Convert **timezone name + date** to **timezone offset**.
- ``convert_tz_name_to_now_tz_abbrev()``: Convert **timezone name + current date** to current **timezone abbreviation**.
- ``convert_tz_name_to_now_tz_offset()``: Convert **timezone name + current date** to current **timezone offset**.
- ``convert_tz_offset_and_date_to_tz_name()``: Convert **timezone offset + date** to **timezone name**.
- ``convert_tz_offset_to_now_tz_abbrev()``: Convert **timezone offset + current date** to current **timezone abbreviation**.
- ``convert_tz_offset_to_tz_hours()``: Convert **timezone offset** to **hours**.
- ``convert_tz_offset_to_tz_minutes()``: Convert **timezone offset** to **minutes**.
- ``convert_tz_offset_to_tz_seconds()``: Convert **timezone offset** to **seconds**.
- ``parse_gmt_offset_timezone()``: Parse GMT string into **timezone name** and **timezone offset**.
- ``validate_tz_abbrev()``: Validate **timezone abbreviation**.
- ``validate_tz_name()``: Validate **timezone name**.

Requirements
------------

``pytz-convert`` module is built upon Python 3 and has dependencies upon
several Python modules available within `Python Package Index PyPI <https://pypi.python.org/pypi>`_.

.. code-block:: bash

    make install-requirements

or


.. code-block:: bash

    python3 -m pip uninstall --yes --no-input -r requirements.txt
    python3 -m pip install --upgrade -r requirements.txt


Dependencies
^^^^^^^^^^^^

- `pytz <https://pypi.python.org/pypi/pytz>`_
- `python-dateutil <https://pypi.python.org/pypi/python-dateutil>`_
- `wheel <https://pypi.python.org/pypi/wheel>`_
