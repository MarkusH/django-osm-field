=====
Usage
=====


Model Layer
===========

You only need to add a single model field to your model. django-osm-field will
automatically add two additional fields ``<name>_lat`` and ``<name>_lon`` to
the model to store the latitude and longitude:

.. code-block:: python

    from django.core.urlresolvers import reverse
    from django.db import models

    from osm_field.fields import LatitudeField, LongitudeField, OSMField


    class MyModel(models.Model):
        location = OSMField()
        location_lat = LatitudeField()
        location_lon = LongitudeField()

Apart from the field ``location`` you will also need to add a field
``location_lat`` and a field ``location_lon``. If you want the latitude and
longitude fields to have different names, you can specify them explicitly on
the ``OSMField``:

.. code-block:: python

    class MyModel(models.Model):
        location = OSMField(lat_field='latitude', lon_field='longitude')
        latitude = LatitudeField()
        longitude = LongitudeField()


Form Layer
==========

.. code-block:: python

    from django import forms

    from .models import MyModel


    class MyModelForm(forms.ModelForm):

        class Meta:
            fields = ['location', 'location_lat', 'location_lon']
            model = MyModel


View Layer
==========

.. code-block:: python

    from django.views.generic import CreateView

    from .forms import MyModelForm
    from .models import MyModel


    class MyCreateView(CreateView):
        form_class = MyModelForm
        model = MyModel


Template Layer
==============

.. code-block:: django

    {% load static from staticfiles %}<!DOCTYPE HTML>
    <html>
      <head>
        <title></title>
        <link rel="stylesheet" href="{% static "css/example.css" %}">
        <!-- Either serve jQuery yourself -->
        <link rel="stylesheet" href="{% static "js/vendor/jquery-2.1.0.min.js" %}">
        <!-- or from a CDN -->
        <script type="text/javascript" src="//code.jquery.com/jquery-2.1.0.min.js"></script>
      </head>
      <body>
        {{ form.media }}
        <form action="" method="post">
          {% csrf_token %}
          {{ form.as_p }}
          <input type="submit" value="Save" />
        </form>
      </body>
    </html> 
