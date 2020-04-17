=====
Usage
=====

.. py:module:: osm_field

Model Layer
===========

You need to add three model fields to your model:

1. :class:`~fields.OSMField`
2. :class:`~fields.LatitudeField`
3. :class:`~fields.LongitudeField`

**django-osm-field** expects them to have a certain name schema: The
:class:`~fields.OSMField` defines the base name, the
:class:`~fields.LatitudeField` and :class:`~fields.LongitudeField` have the
same name appended with ``_lat`` and ``_lon`` respectively. See the following
example to get an idea:

.. code-block:: python

    from django.db import models

    from osm_field.fields import LatitudeField, LongitudeField, OSMField


    class MyModel(models.Model):
        location = OSMField()
        location_lat = LatitudeField()
        location_lon = LongitudeField()

It is possible, though, to overwrite the default naming for latitude and
longitude fields by giving their names as arguments to the
:class:`~fields.OSMField`:

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
            fields = ('location', 'location_lat', 'location_lon', )
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


.. _usage-template-layer:

Template Layer
==============

**django-osm-field** shipps with a minimized `jQuery`_ version. To access it in a template use the ``static`` templatetag:

.. code-block:: django

    <script type="text/javascript" src="{% static "js/vendor/jquery-2.1.0.min.js" %}"></script>

You can of course load `jQuery`_ from a CDN as well:

.. code-block:: django

    <script type="text/javascript" src="//code.jquery.com/jquery-2.1.0.min.js"></script>

To get the front-end to work, you also need to include some CSS and JavaScript files. You can do this by simply using ``{{ form.media }}`` or by adding those lines explicitly:

.. code-block:: django

    <link href="{% static "css/vendor/leaflet.css" %}" type="text/css" media="screen" rel="stylesheet" />
    <link href="{% static "css/osm_field.css" %}" type="text/css" media="screen" rel="stylesheet" />
    <script type="text/javascript" src="{% static "js/vendor/leaflet.js" %}"></script>
    <script type="text/javascript" src="{% static "js/osm_field.js" %}"></script>


In the end your template should look similar to this:

.. code-block:: django

    {% load static %}<!DOCTYPE HTML>
    <html>
      <head>
        <title></title>
        <link rel="stylesheet" href="{% static "css/example.css" %}">
        <!-- Either serve jQuery yourself -->
        <script type="text/javascript" src="{% static "js/vendor/jquery-2.1.0.min.js" %}"></script>
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

.. _jQuery: http://jquery.com/download/
