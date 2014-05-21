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

    from osm_field.fields import OSMField


    class MyModel(models.Model):
        location = OSMField()

Apart from the field ``location`` there will also be a field ``location_lat``
and a field ``location_lon``.


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

    {{ form.media }}
    <form action="" method="post">
        {% csrf_token %}
        {{ form.as_p }}
        <input type="submit" value="Save" />
    </form>
