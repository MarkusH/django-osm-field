from django.core.urlresolvers import reverse
from django.db import models

from osm_field.fields import OSMField


class ExampleModel(models.Model):
    location = OSMField()
    another = OSMField()

    def __str__(self):
        return str(self.get_location_info())

    def get_absolute_url(self):
        return reverse('detail', kwargs={'pk': self.pk})
