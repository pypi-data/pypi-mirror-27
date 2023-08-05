Python geoLink Formatter
========================

|license| |build status| |coverage report| |python version| |format|
|status|

This is a small library, meant to be used in combination with OEREBlex. It is capable of parsing a received
geoLink response (XML) and converting it to multiple formats, such as HTML, which can be styled for
presentation.

For detailed information, please refer to the online documentation:

https://gf-bl.gitlab.io/python-geolink-formatter/

.. |license| image:: https://img.shields.io/pypi/l/geolink_formatter.svg
   :target: https://pypi.python.org/pypi/geolink_formatter
.. |build status| image:: https://gitlab.com/gf-bl/python-geolink-formatter/badges/master/build.svg
   :target: https://gitlab.com/gf-bl/python-geolink-formatter/commits/master
.. |coverage report| image:: https://gitlab.com/gf-bl/python-geolink-formatter/badges/master/coverage.svg
   :target: https://gitlab.com/gf-bl/python-geolink-formatter/commits/master
.. |python version| image:: https://img.shields.io/pypi/pyversions/geolink_formatter.svg
   :target: https://pypi.python.org/pypi/geolink_formatter
.. |format| image:: https://img.shields.io/pypi/format/geolink_formatter.svg
   :target: https://pypi.python.org/pypi/geolink_formatter
.. |status| image:: https://img.shields.io/pypi/status/geolink_formatter.svg
   :target: https://pypi.python.org/pypi/geolink_formatter


Changelog
---------


1.3.0
*****

Supported geoLink schema versions: v1.0.0, v1.1.0 (default)

- Add support for multiple geoLink schema versions


1.2.0
*****

Supported geoLink schema versions: 20171108 (v1.1.0)

- Use new geoLink schema


1.1.2
*****

Supported geoLink schema version: 20170214 (v1.0.0)

- All attributes are optional, as defined in the schema


1.1.1
*****

Supported geoLink schema version: 20170214 (v1.0.0)

- Allow documents with empty file list


1.1.0
*****

Supported geoLink schema version: 20170214 (v1.0.0)

- Add support for Python 3


1.0.0
*****

Supported geoLink schema version: 20170214 (v1.0.0)

- Initial version


