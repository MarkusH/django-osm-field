================
Django OSM Field
================

.. image:: https://img.shields.io/pypi/v/django-osm-field.svg
   :target: https://pypi.python.org/pypi/django-osm-field

.. image:: https://img.shields.io/pypi/l/django-osm-field.svg
   :target: https://pypi.python.org/pypi/django-osm-field

.. image:: https://img.shields.io/pypi/dm/django-osm-field.svg
   :target: https://pypi.python.org/pypi/django-osm-field

.. image:: https://img.shields.io/travis/MarkusH/django-osm-field/master.svg
   :target: https://travis-ci.org/MarkusH/django-osm-field

.. image:: https://img.shields.io/codecov/c/github/MarkusH/django-osm-field/master.svg
   :target: https://codecov.io/github/MarkusH/django-osm-field


Django OpenStreetMap Field

* Free software: MIT license
* Documentation: http://django-osm-field.rtfd.org.

Releasing
=========

* Ensure everything is merged into ``develop``
* Ensure the currently active branch is ``develop``
* Run ``tox`` and ensure all tests pass
* Ensure changelog is up to date
* Change to branch ``master``
* Merge branch ``develop``
* Run ``bumpversion major|minor|patch``
* Push changes and tags to Github
* Build Python packages with ``python setup.py sdist bdist_wheel``
* Upload package with ``twine upload -s dist/[.whl-FILE-TO-UPLOAD] dist/[.tar.gz-FILE-TO-UPLOAD]``.
