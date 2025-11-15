============
Installation
============

Install **django-osm-field** into your virtual environment or you site-packages using pip:

.. code:: console

    $ pip install django-osm-field

To make **django-osm-field** available in your Django project, you first have to add it to the INSTALLED_APPS in your settings.py. If you are unsure where to put it, just append it:

.. code:: python

    INSTALLED_APPS = [
        # Your other Django apps.
        "osm_field",
    ]
