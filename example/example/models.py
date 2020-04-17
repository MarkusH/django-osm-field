from django.db import models
from django.urls import reverse

from osm_field.fields import LatitudeField, LongitudeField, OSMField


class ExampleModel(models.Model):
    location = OSMField()
    location_lat = LatitudeField()
    location_lon = LongitudeField()
    another = OSMField(lat_field="some_lat_field", lon_field="other_lon_field")
    some_lat_field = LatitudeField()
    other_lon_field = LongitudeField()

    def __str__(self):
        return str(self.get_location_info())

    def get_absolute_url(self):
        return reverse("detail", kwargs={"pk": self.pk})
